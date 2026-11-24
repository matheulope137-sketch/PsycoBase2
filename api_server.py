"""
PsicoBase - API do Professor Digital de Psicologia
Servidor REST para apoio pedagógico e estudantil em Psicologia.
Zero dependências externas: roda diretamente com a biblioteca padrão do Python (Python 3.8+).

Endpoints:
  GET  /api/status               - Status da API, estatísticas e tópicos disponíveis
  POST /api/professor/chat       - Conversa didática com o professor virtual
  POST /api/professor/explicar   - Decomposição didática de conceitos psicológicos
  POST /api/professor/caso-clinico - Geração e tutoria de estudos de caso hipotéticos
  POST /api/professor/simulado   - Geração de questões de simulado para treino
  POST /api/professor/avaliar    - Avaliação pedagógica de explicações/resumos de estudantes
  GET  /api/docs                 - Painel interativo de documentação e testes
"""

import json
import os
import re
import sys
import time
import unicodedata
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

PORT = int(os.environ.get("PORT", 8000))
START_TIME = time.time()

def normalizar(t):
    if not t:
        return ""
    t = unicodedata.normalize("NFD", str(t))
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return t.lower().strip()

# ==================== DIRETRIZES ÉTICAS E DE SEGURANÇA ====================
CRISE_TERMOS = [
    'suicid', 'me matar', 'quero morrer', 'nao quero viver',
    'acabar com a minha vida', 'automutil', 'me cortar', 'me machucar', 'autolesao'
]

DIAG_TERMOS = [
    'tenho depressao', 'tenho ansiedade', 'tenho transtorno',
    'eu tenho tdah', 'sera que eu tenho', 'diagnostica',
    'diagnostico para mim', 'meu diagnostico', 'interprete meu teste',
    'meu laudo', 'meu filho tem', 'minha filha tem', 'qual remedio', 'quantos mg', 'dose de'
]

RESPOSTA_CRISE = {
    "status": "crise",
    "resposta": (
        "Sinto muito que você esteja passando por um momento tão difícil. "
        "Como sou um Professor Digital voltado para o estudo acadêmico, não posso oferecer atendimento psicológico de urgência. "
        "Por favor, procure acolhimento humano agora mesmo:\n\n"
        "• CVV (Centro de Valorização da Vida): Ligue 188 (ligação gratuita, 24 horas) ou acesse cvv.org.br.\n"
        "• Em situações de risco imediato: Ligue 192 (SAMU) ou vá à UPA / pronto-socorro mais próximo.\n"
        "Você não está sozinho(a), busque apoio especializado imediatamente."
    ),
    "fontes": ["Centro de Valorização da Vida (CVV - 188)", "SAMU 192"],
    "pergunta_reflexao": None
}

RESPOSTA_DIAGNOSTICO = {
    "status": "recusado_orientacao_etica",
    "resposta": (
        "De acordo com os princípios éticos da Psicologia e o Código de Ética Profissional do Psicólogo (CFP), "
        "avaliações diagnósticas, interpretação de laudos e prescrições terapêuticas exigem formação profissional, "
        "processo estruturado de acolhimento e registro ativo no Conselho Regional de Psicologia (CRP).\n\n"
        "Como Professor Digital, meu papel é exclusivamente educativo. Posso explicar o conceito teórico, a história "
        "do construto ou os critérios gerais segundo os manuais (CID-11 / DSM-5) para fins de estudo acadêmico. "
        "Gostaria que analisássemos o conceito teórico por trás desse tema?"
    ),
    "fontes": ["Código de Ética Profissional do Psicólogo (Resolução CFP nº 010/2005)"],
    "pergunta_reflexao": "Como a Psicologia científica diferencia uma avaliação clínica contextualizada de um mero rótulo diagnóstico?"
}

# ==================== BASE DE CONHECIMENTO PEDAGÓGICA ====================
CONCEITOS_BASE = {
    "reforco negativo": {
        "conceito": "Reforço Negativo",
        "area": "Análise do Comportamento / Behaviorismo",
        "definicao_simples": "Remoção ou alívio de um estímulo desagradável (aversivo) após um comportamento, aumentando a chance de o comportamento se repetir.",
        "definicao_academica": "Aumento na probabilidade de uma resposta devido à remoção, atenuação ou adiamento contingente de um estímulo aversivo (comportamentos de fuga ou esquiva).",
        "analogia": "Colocar o cinto de segurança no carro para cessar o apito sonoro irritante: o comportamento de afivelar é reforçado pelo alívio do barulho.",
        "exemplo_pratico": "Tomar um remédio para aliviar uma dor de cabeça: como a dor cedeu (remoção do aversivo), a probabilidade de tomar o remédio em futuras dores aumenta.",
        "erro_comum": "O erro mais clássico em provas: achar que reforço negativo é punição! Reforço SEMPRE aumenta a frequência; punição diminui.",
        "autores_chave": ["B. F. Skinner"],
        "dica_prova": "Fórmula de ouro: Reforço = aumenta comportamento. Negativo = subtrai estímulo (alívio). Portanto, reforço negativo fortalece o comportamento pelo alívio."
    },
    "reforco positivo": {
        "conceito": "Reforço Positivo",
        "area": "Análise do Comportamento / Behaviorismo",
        "definicao_simples": "Apresentação de um estímulo agradável ou recompensador após um comportamento que aumenta a probabilidade desse comportamento voltar a ocorrer no futuro.",
        "definicao_academica": "Operação na qual a ocorrência de uma resposta é contingente à apresentação de um estímulo reforçador, resultando no aumento da frequência ou taxa futura de emissão da referida classe de respostas.",
        "analogia": "Regar uma planta logo após ela brotar uma folha: o cuidado faz com que ela continue crescendo com mais força.",
        "exemplo_pratico": "Um estudante resolve uma questão difícil de estatística e recebe um elogio detalhado do professor, sentindo-se motivado a continuar resolvendo os exercícios.",
        "erro_comum": "Confundir reforço positivo com recompensa moral ou achar que positivo significa 'bom'. Positivo refere-se à adição de um estímulo ao ambiente.",
        "autores_chave": ["B. F. Skinner", "Edward Thorndike"],
        "dica_prova": "Lembre-se sempre: 'Positivo' = somar/apresentar estímulo; 'Reforço' = aumentar probabilidade de resposta."
    },
    "inconsciente": {
        "conceito": "Inconsciente (Psicanálise)",
        "area": "Psicanálise",
        "definicao_simples": "A parte da mente que guarda pensamentos, desejos, memórias e pulsões que não estão acessíveis à nossa consciência direta, mas influenciam sentimentos e atitudes.",
        "definicao_academica": "Instância psíquica constituída por conteúdos recalcados aos quais foi recusado o acesso ao sistema pré-consciente/consciente pelas forças da censura, operando segundo o processo primário e o princípio do prazer.",
        "analogia": "A parte submersa de um iceberg: a ponta visível na superfície é a consciência, enquanto a imensa massa de gelo oculta sob as águas comanda a navegação.",
        "exemplo_pratico": "Um ato falho (lapsus linguae) ou um sonho em que um desejo reprimido aparece de forma disfarçada por meio de condensação e deslocamento.",
        "erro_comum": "Tratar o inconsciente como se fosse um 'depósito de lixo' ou algo místico. Para Freud, é um sistema ativo e dinâmico com leis próprias de funcionamento.",
        "autores_chave": ["Sigmund Freud", "Jacques Lacan", "Carl Gustav Jung"],
        "dica_prova": "Na 1ª Tópica freudiana: Inconsciente, Pré-Consciente, Consciente. Na 2ª Tópica: Id, Ego, Superego."
    },
    "esquema cognitivo": {
        "conceito": "Esquemas e Crenças Centrais (TCC)",
        "area": "Terapia Cognitivo-Comportamental",
        "definicao_simples": "Padrões mentais ou 'lentes' internas construídas ao longo da vida através dos quais interpretamos nós mesmos, os outros e o futuro.",
        "definicao_academica": "Estruturas cognitivas estáveis e duradouras de armazenamento e processamento da informação que orientam a percepção, categorização e atribuição de significado aos eventos.",
        "analogia": "Usar óculos com lentes coloridas: se a lente for azul, o mundo inteiro parecerá azul, mesmo que a realidade tenha todas as cores.",
        "exemplo_pratico": "Um estudante com a crença central de desvalia ('sou incapaz') tira nota 8 em uma prova e pensa: 'o professor foi bonzinho, eu dei sorte', filtrando qualquer evidência de competência.",
        "erro_comum": "Achar que pensamentos automáticos e esquemas são a mesma coisa. Pensamentos automáticos são superficiais e rápidos; esquemas são as estruturas profundas que os geram.",
        "autores_chave": ["Aaron Beck", "Judith Beck"],
        "dica_prova": "A Tríade Cognitiva de Beck envolve visões sobre: 1) Si mesmo; 2) O mundo/outros; 3) O futuro."
    },
    "metodologia cientifica": {
        "conceito": "Método Científico e Hipóteses em Psicologia",
        "area": "Metodologia de Pesquisa",
        "definicao_simples": "Processo sistemático e empírico de formular perguntas testáveis, coletar dados com instrumentos válidos e analisar se as evidências sustentam ou refutam a ideia inicial.",
        "definicao_academica": "Conjunto de procedimentos epistemológicos e empíricos balizados por falseabilidade, reprodutibilidade, controle de variáveis intervenientes e operacionalização de construtos teóricos.",
        "analogia": "Um detetive rigoroso que não aceita boatos: ele isola a cena, coleta impressões digitais padronizadas e confronta os fatos antes de acusar qualquer suspeito.",
        "exemplo_pratico": "Em vez de afirmar vagamente 'flashcards ajudam', o pesquisador define uma hipótese nula e alternativa, seleciona um grupo controle e grupo experimental, e compara o ganho de retenção após 14 dias.",
        "erro_comum": "Confundir correlação com causalidade ('variáveis que andam juntas nem sempre são causa e efeito uma da outra').",
        "autores_chave": ["Karl Popper", "Wilhelm Wundt"],
        "dica_prova": "A validade interna avalia se o efeito decorreu da variável independente; a validade externa avalia se os achados podem ser generalizados."
    },
    "etica profissional": {
        "conceito": "Ética e Responsabilidade Profissional no Brasil",
        "area": "Ética e Legislação (CFP)",
        "definicao_simples": "Conjunto de deveres, limites e princípios que guiam a atuação da(o) psicóloga(o) para proteger os direitos humanos, o sigilo e o bem-estar dos indivíduos atendidos.",
        "definicao_academica": "Normatização deontológica regida pelo Conselho Federal de Psicologia (Resolução CFP nº 010/2005) e Conselhos Regionais (CRPs), fundamentada na Declaração Universal dos Direitos Humanos e na dignidade da pessoa.",
        "analogia": "O corrimão firme em uma escada alta: ele garante segurança e limites claros para que tanto o profissional quanto o paciente transitem sem quedas.",
        "exemplo_pratico": "A manutenção rigorosa do sigilo profissional, a recusa a práticas que promovam discriminação ou violência e a não utilização de métodos sem fundamentação científica reconhecida.",
        "erro_comum": "Achar que o sigilo profissional é absoluto em qualquer hipótese (há exceções estritas previstas em lei e no Código para proteção da vida com quebra de sigilo no estritamente necessário).",
        "autores_chave": ["Conselho Federal de Psicologia (CFP)", "Conselho Regional de Psicologia (CRP)"],
        "dica_prova": "Artigo 1º e 2º do Código de Ética do CFP são os mais cobrados em concursos e provas de conselho."
    }
}

CASOS_CLINICOS = [
    {
        "id": "caso-1",
        "titulo": "O Caso de Lucas: Ansiedade Acadêmica e Esquiva",
        "area": "Psicologia Clínica / TCC e Comportamental",
        "contexto": "Lucas, 20 anos, estudante do 2º período, procurou o Serviço de Apoio ao Estudante relatando taquicardia, sudorese e pensamentos catastróficos antes de seminários orais.",
        "vinheta": (
            "Lucas relata: 'Toda vez que tenho que apresentar um trabalho, sinto meu peito apertar e tenho certeza de que vou travar e passar vergonha na frente de todo mundo'. "
            "Na última semana, faltou à aula no dia da apresentação e enviou um atestado médico para justificar. "
            "Ele relata que no momento em que decidiu não ir à aula, sentiu um 'alívio imediato', mas no dia seguinte foi invadido por profunda culpa e desânimo."
        ),
        "questoes_norteadoras": [
            "1. Como o alívio imediato sentido por Lucas atua como 'reforço negativo' para o comportamento de faltar à apresentação?",
            "2. Qual distorção cognitiva (ex.: catastrofização, leitura mental) pode ser identificada em sua fala?",
            "3. De acordo com o modelo comportamental, o que a esquiva prolongada faz com a ansiedade a longo prazo?"
        ],
        "orientacao_etica": "Lembre-se: este estudo é estritamente pedagógico. Em um contexto real de estágio, o acolhimento deve priorizar a escuta ativa, sem rótulos pejorativos."
    },
    {
        "id": "caso-2",
        "titulo": "O Dilema na Escola Municipal: Quebra de Sigilo e Proteção",
        "area": "Psicologia Escolar e Ética Profissional",
        "contexto": "Juliana, psicóloga escolar recém-formada em uma escola de ensino fundamental, atende uma aluna de 14 anos.",
        "vinheta": (
            "Durante a escuta de acolhimento espontânea, a aluna relata em confidência que sofre agressões físicas e negligência grave em sua residência por parte do responsável. "
            "A aluna implora aos prantos: 'Por favor, não conte para ninguém, nem para o diretor nem para meus pais, se não vai ser pior para mim!'. "
            "A diretora da escola exige saber detalhadamente o que a aluna conversou durante o atendimento na sala da psicologia."
        ),
        "questoes_norteadoras": [
            "1. À luz do Código de Ética Profissional do Psicólogo (Art. 9º e 10º) e do Estatuto da Criança e do Adolescente (ECA), como Juliana deve proceder em relação à denúncia de maus-tratos?",
            "2. Juliana deve entregar o relatório integral confidencial para a diretora da escola ou repassar apenas as informações estritamente necessárias para a proteção da jovem?",
            "3. Como comunicar a decisão à adolescente de maneira ética, empática e acolhedora?"
        ],
        "orientacao_etica": "O sigilo profissional cede lugar à proteção indeclinável da vida e integridade física de crianças e adolescentes, atuando em rede com o Conselho Tutelar."
    }
]

SIMULADOS_PADRAO = [
    {
        "id": "q1",
        "tema": "Behaviorismo",
        "enunciado": "Um motorista que afivela o cinto de segurança para eliminar o aviso sonoro intermitente do painel está sob contingência de:",
        "alternativas": [
            {"letra": "A", "texto": "Reforço Positivo, pois ganhou segurança."},
            {"letra": "B", "texto": "Punição Positiva, pois o som é aversivo."},
            {"letra": "C", "texto": "Reforço Negativo, pois o comportamento remove o estímulo aversivo."},
            {"letra": "D", "texto": "Extinção operante, pois o alarme para de funcionar."}
        ],
        "correta": "C",
        "explicacao": "O comportamento (afivelar o cinto) é fortalecido pela remoção contingente do som irritante (estímulo aversivo). Esse é o conceito clássico de reforço negativo (fuga/esquiva)."
    },
    {
        "id": "q2",
        "tema": "Metodologia",
        "enunciado": "Em um estudo sobre estresse e memória, pesquisadores mediram os níveis de cortisol salivar antes de uma prova. Nesse contexto, o cortisol é considerado:",
        "alternativas": [
            {"letra": "A", "texto": "Um construto teórico não observável."},
            {"letra": "B", "texto": "Uma definição operacional e indicador biológico do construto estresse."},
            {"letra": "C", "texto": "Uma variável de confusão incontrolável."},
            {"letra": "D", "texto": "Uma hipótese nula descartada a priori."}
        ],
        "correta": "B",
        "explicacao": "O estresse psicológico é o construto teórico; o nível de cortisol salivar mensurado é a sua definição operacional objetiva."
    },
    {
        "id": "q3",
        "tema": "Ética Profissional",
        "enunciado": "De acordo com o Código de Ética Profissional do Psicólogo brasileiro, o atendimento e divulgação de serviços NÃO deve:",
        "alternativas": [
            {"letra": "A", "texto": "Informar a qualificação profissional e o número de CRP."},
            {"letra": "B", "texto": "Promover garantias infundadas de cura ou resultados rápidos milagrosos."},
            {"letra": "C", "texto": "Fundamentar-se em métodos cientificamente validados."},
            {"letra": "D", "texto": "Esclarecer sobre honorários e enquadre antes do início do processo."}
        ],
        "correta": "B",
        "explicacao": "É expressamente vedado ao psicólogo garantir ou induzir a convicção de certeza de resultados, conforme prevê o Código de Ética (Artigo 20)."
    }
]

# ==================== MOTOR DE PROCESSAMENTO DO PROFESSOR ====================
def encontrar_conceito(texto):
    """Encontra o conceito mais relevante por prioridade de correspondência."""
    t_norm = normalizar(texto)
    chaves_ordenadas = sorted(CONCEITOS_BASE.keys(), key=lambda k: len(k), reverse=True)
    for chave in chaves_ordenadas:
        if chave in t_norm:
            return CONCEITOS_BASE[chave]
    for chave in chaves_ordenadas:
        palavras = [w for w in chave.split() if len(w) > 4 and w not in ('reforco', 'positivo', 'negativo')]
        if palavras and any(p in t_norm for p in palavras):
            return CONCEITOS_BASE[chave]
    return None

def gerar_resposta_chat(pergunta, contexto_aula=None, historico=None):
    """Gera uma resposta didática e acolhedora estruturada pelo Professor Digital."""
    p_norm = normalizar(pergunta)
    
    # 1. Checagem de crise
    if any(normalizar(term) in p_norm for term in CRISE_TERMOS):
        return RESPOSTA_CRISE
        
    # 2. Checagem de solicitação de diagnóstico pessoal
    if any(normalizar(term) in p_norm for term in DIAG_TERMOS):
        return RESPOSTA_DIAGNOSTICO
        
    # 3. Busca de conceito na base interna
    item = encontrar_conceito(pergunta)
    if item:
        return {
            "status": "respondido",
            "resposta": (
                f"Olá! Que excelente pergunta sobre **{item['conceito']}**.\n\n"
                f"**Em poucas palavras:** {item['definicao_simples']}\n\n"
                f"**Aprofundando academicamente:** {item['definicao_academica']}\n\n"
                f"💡 **Analogia para fixar:** {item['analogia']}\n\n"
                f"📌 **Aplicação prática:** {item['exemplo_pratico']}\n\n"
                f"⚠️ **Cuidado em provas:** {item['erro_comum']}"
            ),
            "autores": item["autores_chave"],
            "fontes": [f"Unidade de {item['area']}", "PsicoBase - Caderno Acadêmico"],
            "pergunta_reflexao": f"Você consegue identificar uma situação do seu cotidiano de estudos em que {item['conceito'].lower()} se manifesta?"
        }
            
    # 4. Resposta pedagógica heurística contextualizada
    resposta_padrao = (
        f"Excelente questão de estudo! Na formação em Psicologia, analisar essa temática exige integrarmos "
        f"três pilares fundamentais: o **rigor conceitual**, o **contexto histórico das abordagens** e a **ética profissional**.\n\n"
        f"Quando analisamos \"*{pergunta[:90].strip()}*\", é recomendável refletir se estamos observando o fenômeno "
        f"sob uma perspectiva descritiva (comportamento manifesto) ou interpretativa (processos intrapsíquicos ou socioculturais).\n\n"
        f"Para avançar nos seus estudos, sugiro consultar as aulas correspondentes na aba **Aprender** e revisar os termos na **Biblioteca**."
    )
    
    return {
        "status": "respondido",
        "resposta": resposta_padrao,
        "fontes": ["Plataforma PsicoBase", "Diretrizes Curriculares Nacionais de Psicologia (DCNs)"],
        "pergunta_reflexao": "Qual abordagem teórica da Psicologia você considera mais adequada para investigar esse problema e por quê?"
    }

def avaliar_explicacao_estudante(tema, explicacao):
    """Avalia pedagogicamente um resumo ou explicação enviada pelo estudante."""
    exp_norm = normalizar(explicacao)
    
    # Segurança
    if any(normalizar(term) in exp_norm for term in CRISE_TERMOS):
        return RESPOSTA_CRISE
    if any(normalizar(term) in exp_norm for term in DIAG_TERMOS):
        return RESPOSTA_DIAGNOSTICO
        
    tamanho = len(explicacao.strip())
    if tamanho < 25:
        return {
            "status": "avaliado",
            "nivel": "insuficiente",
            "acertos": ["Tentativa inicial de síntese."],
            "faltou": ["Desenvolvimento da ideia central", "Exemplos ou contextualização teórica"],
            "pontos_atencao": ["Sua resposta está muito curta para avaliarmos a compreensão conceitual."],
            "sugestao_estudo": "Procure formular sua explicação em pelo menos dois ou três períodos completos, incluindo a definição e um exemplo."
        }
        
    acertos = []
    faltou = []
    
    palavras_chave_psico = ["comportamento", "processo", "mente", "estimulo", "reforco", "inconsciente", "sujeito", "ambiente", "cognicao", "social", "etica", "metodo"]
    chaves_encontradas = [w for w in palavras_chave_psico if w in exp_norm]
    
    if chaves_encontradas:
        acertos.append(f"Boa apropriação do vocabulário técnico da área ({', '.join(chaves_encontradas[:4])}).")
    else:
        faltou.append("Inserir termos conceituais mais precisos da literatura psicológica.")
        
    if "exemplo" in exp_norm or "como quando" in exp_norm or "por exemplo" in exp_norm:
        acertos.append("Excelente iniciativa de ilustrar o conceito com um caso prático.")
    else:
        faltou.append("Adicionar uma analogia ou exemplo prático para consolidar a fixação.")
        
    nivel = "completo" if len(chaves_encontradas) >= 3 and tamanho > 120 else ("parcial" if tamanho >= 50 else "insuficiente")
    
    return {
        "status": "avaliado",
        "nivel": nivel,
        "acertos": acertos or ["Ideia inicial compreensível e bem direcionada."],
        "faltou": faltou or ["Aprofundar a relação com os autores fundamentais."],
        "pontos_atencao": ["Lembre-se sempre de distinguir o senso comum da terminologia científica."],
        "sugestao_estudo": "Compare sua resposta com a síntese do módulo correspondente em PsicoBase e crie um flashcard com os pontos que faltaram!"
    }

# ==================== HANDLER HTTP REST ====================
class ProfessorAPIHandler(BaseHTTPRequestHandler):
    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-API-Key, X-Gemini-Key, X-OpenAI-Key")

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_cors_headers()
        self.end_headers()

    def responder_json(self, status_code, dados):
        corpo = json.dumps(dados, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(corpo)

    def responder_html(self, status_code, html_str):
        corpo = html_str.encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(corpo)

    def ler_body_json(self):
        try:
            comp = int(self.headers.get("Content-Length", 0))
            if comp <= 0:
                return {}
            raw = self.rfile.read(comp).decode("utf-8")
            return json.loads(raw)
        except Exception:
            return {}

    def do_GET(self):
        rota = self.path.split("?")[0].rstrip("/")
        
        if rota in ("", "/api", "/api/docs", "/docs"):
            self.responder_html(200, HTML_DOCS)
            return
            
        if rota == "/api/status":
            self.responder_json(200, {
                "sistema": "PsicoBase - Professor Digital API",
                "versao": "1.2.0",
                "status": "online",
                "uptime_segundos": round(time.time() - START_TIME, 1),
                "disciplinas_cobertas": [
                    "Introdução à Psicologia",
                    "História da Psicologia",
                    "Análise do Comportamento (Behaviorismo)",
                    "Psicanálise e Psicodinâmica",
                    "Terapias Cognitivo-Comportamentais",
                    "Neurociências e Processos Básicos",
                    "Psicologia do Desenvolvimento",
                    "Psicologia Social e Comunitária",
                    "Personalidade e Diferenças Individuais",
                    "Metodologia Científica e Psicometria",
                    "Ética Profissional e Legislação do CFP",
                    "Psicopatologia e Saúde Mental"
                ],
                "endpoints": [
                    {"metodo": "POST", "caminho": "/api/professor/chat", "descricao": "Conversa pedagógica com o professor virtual"},
                    {"metodo": "POST", "caminho": "/api/professor/explicar", "descricao": "Decomposição didática de conceitos"},
                    {"metodo": "POST", "caminho": "/api/professor/caso-clinico", "descricao": "Estudos de caso hipotéticos orientados"},
                    {"metodo": "POST", "caminho": "/api/professor/simulado", "descricao": "Geração de questões de simulado"},
                    {"metodo": "POST", "caminho": "/api/professor/avaliar", "descricao": "Avaliação pedagógica de explicações de alunos"}
                ]
            })
            return
            
        if rota == "/api/professor/casos":
            self.responder_json(200, {"casos": CASOS_CLINICOS})
            return
            
        if rota == "/api/professor/simulado":
            self.responder_json(200, {"questoes": SIMULADOS_PADRAO})
            return

        self.responder_json(404, {"erro": "Rota não encontrada", "docs": "/api/docs"})

    def do_POST(self):
        rota = self.path.split("?")[0].rstrip("/")
        dados = self.ler_body_json()
        
        if rota == "/api/professor/chat":
            pergunta = dados.get("pergunta") or dados.get("mensagem") or ""
            if not pergunta.strip():
                self.responder_json(400, {"erro": "O campo 'pergunta' é obrigatório."})
                return
            resultado = gerar_resposta_chat(pergunta, dados.get("aula_id"))
            self.responder_json(200, resultado)
            return

        if rota == "/api/professor/explicar":
            termo = normalizar(dados.get("conceito") or dados.get("termo") or "")
            if not termo:
                self.responder_json(400, {"erro": "O campo 'conceito' é obrigatório."})
                return
            item = encontrar_conceito(termo)
            if item:
                self.responder_json(200, {"status": "encontrado", **item})
            else:
                self.responder_json(200, {
                    "status": "generico",
                    "conceito": termo.capitalize(),
                    "area": "Psicologia Geral",
                    "definicao_simples": f"Conceito estudado na literatura psicológica contemporânea.",
                    "definicao_academica": f"Construto teórico associado ao estudo do comportamento e dos processos mentais.",
                    "analogia": "Considere como as engrenagens de um relógio: cada peça contribui para o funcionamento do todo perceptivo.",
                    "exemplo_pratico": f"Identificado na observação empírica de sujeitos em situações cotidianas.",
                    "erro_comum": "Utilizar a intuição do senso comum sem a verificação científica adequada.",
                    "autores_chave": ["Consulte as referências em PsicoBase"],
                    "dica_prova": "Verifique a definição operacional adotada pela banca da sua prova."
                })
            return

        if rota == "/api/professor/caso-clinico":
            caso_id = dados.get("caso_id")
            caso = next((c for c in CASOS_CLINICOS if c["id"] == caso_id), None) if caso_id else CASOS_CLINICOS[0]
            self.responder_json(200, {"status": "sucesso", "caso": caso})
            return

        if rota == "/api/professor/simulado":
            tema = dados.get("tema", "").lower()
            qtd = min(int(dados.get("quantidade", 3)), 10)
            questoes = [q for q in SIMULADOS_PADRAO if not tema or tema in q["tema"].lower()] or SIMULADOS_PADRAO
            self.responder_json(200, {"status": "sucesso", "quantidade": len(questoes[:qtd]), "questoes": questoes[:qtd]})
            return

        if rota == "/api/professor/avaliar":
            tema = dados.get("tema") or dados.get("aula_titulo") or "Geral"
            explicacao = dados.get("explicacao_estudante") or dados.get("resposta") or ""
            if not explicacao.strip():
                self.responder_json(400, {"erro": "O campo 'explicacao_estudante' é obrigatório."})
                return
            avaliacao = avaliar_explicacao_estudante(tema, explicacao)
            self.responder_json(200, avaliacao)
            return

        self.responder_json(404, {"erro": "Endpoint não encontrado", "docs": "/api/docs"})

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

# ==================== PAINEL DE DOCUMENTAÇÃO INTERATIVO (HTML) ====================
HTML_DOCS = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PsicoBase · API do Professor Digital de Psicologia</title>
<style>
:root{
  --primaria:#4A1525; --secundaria:#816A9B; --fundo:#FBF9F7; --card:#FFFFFF; --texto:#25252B; --borda:#E2D9D2; --destaque:#9D71E8;
  --verde:#2E7D32; --azul:#1565C0;
}
*{box-sizing:border-box}
body{font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;margin:0;background:var(--fundo);color:var(--texto);line-height:1.6}
header{background:var(--primaria);color:#fff;padding:2rem 1.5rem;box-shadow:0 4px 12px rgba(0,0,0,0.1)}
.container{max-width:960px;margin:0 auto;padding:1.5rem}
.badge{display:inline-block;padding:3px 10px;border-radius:99px;font-size:0.78rem;font-weight:600;margin-right:6px}
.badge.get{background:#E3F2FD;color:var(--azul)}
.badge.post{background:#E8F5E9;color:var(--verde)}
.card{background:var(--card);border:1px solid var(--borda);border-radius:14px;padding:1.5rem;margin-bottom:1.5rem;box-shadow:0 2px 6px rgba(0,0,0,0.03)}
h1{margin:0 0 0.5rem;font-size:1.8rem}
h2{color:var(--primaria);margin-top:0;font-size:1.3rem;border-bottom:2px solid var(--borda);padding-bottom:0.5rem}
pre{background:#1E1E24;color:#E6EDF3;padding:1rem;border-radius:10px;overflow-x:auto;font-size:0.88rem}
input,textarea,button{width:100%;font:inherit;padding:10px 14px;border-radius:8px;border:1px solid var(--borda);margin-top:6px;margin-bottom:12px}
button{background:var(--primaria);color:#fff;border:0;cursor:pointer;font-weight:600;transition:opacity 0.2s}
button:hover{opacity:0.9}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem}
@media(max-width:768px){.grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<header>
  <div class="container">
    <div style="font-size:2rem;margin-bottom:0.4rem">ψ PsicoBase</div>
    <h1>API do Professor Digital de Psicologia</h1>
    <p style="margin:0;opacity:0.9">Serviço de inteligência pedagógica para apoio estudantil, tira-dúvidas socrático, estudos de caso e avaliação formativa.</p>
  </div>
</header>

<main class="container">
  <div class="card">
    <h2>Visão Geral da API</h2>
    <p>Esta API foi projetada para atuar como um <strong>tutor acadêmico 24/7</strong> para estudantes de graduação e entusiastas de Psicologia. Ela respeita estritamente o <em>Código de Ética do Psicólogo (CFP)</em>, recusando diagnósticos pessoais ou condutas médicas e redirecionando prontamente situações de crise ao CVV (188).</p>
    <p><strong>URL Base:</strong> <code>http://localhost:8000/api</code> | <strong>CORS:</strong> Habilitado para qualquer origem (<code>*</code>).</p>
  </div>

  <div class="grid">
    <!-- Testador Chat -->
    <div class="card">
      <h2><span class="badge post">POST</span> /api/professor/chat</h2>
      <p class="muted">Tira-dúvidas conceitual com explicação pedagógica e pergunta socrática.</p>
      <label>Sua pergunta ou dúvida:
        <textarea id="chat-pergunta" rows="3" placeholder="Ex.: O que é reforço negativo e como difere de punição?"></textarea>
      </label>
      <button onclick="testarChat()">Enviar Pergunta</button>
      <div id="chat-resp" style="display:none">
        <strong>Resposta da API:</strong>
        <pre><code id="chat-json"></code></pre>
      </div>
    </div>

    <!-- Testador Explicar -->
    <div class="card">
      <h2><span class="badge post">POST</span> /api/professor/explicar</h2>
      <p class="muted">Decomposição didática (definição, analogia, exemplo e dicas de prova).</p>
      <label>Conceito:
        <input id="exp-termo" value="reforço negativo" placeholder="Ex.: inconsciente, reforço negativo, esquema cognitivo">
      </label>
      <button onclick="testarExplicar()">Explicar Conceito</button>
      <div id="exp-resp" style="display:none">
        <strong>Resposta da API:</strong>
        <pre><code id="exp-json"></code></pre>
      </div>
    </div>

    <!-- Testador Caso Clínico -->
    <div class="card">
      <h2><span class="badge post">POST</span> /api/professor/caso-clinico</h2>
      <p class="muted">Obtém uma vinheta de caso clínico hipotético e questões norteadoras.</p>
      <button onclick="testarCaso()">Carregar Estudo de Caso</button>
      <div id="caso-resp" style="display:none">
        <strong>Caso Clínico:</strong>
        <pre><code id="caso-json"></code></pre>
      </div>
    </div>

    <!-- Testador Avaliar -->
    <div class="card">
      <h2><span class="badge post">POST</span> /api/professor/avaliar</h2>
      <p class="muted">Avaliação formativa do resumo ou explicação escrita pelo aluno.</p>
      <label>Explicação do estudante:
        <textarea id="aval-texto" rows="3" placeholder="Ex.: Reforço negativo é quando retiramos algo chato para a pessoa continuar fazendo a ação..."></textarea>
      </label>
      <button onclick="testarAvaliar()">Avaliar Explicação</button>
      <div id="aval-resp" style="display:none">
        <strong>Feedback Pedagógico:</strong>
        <pre><code id="aval-json"></code></pre>
      </div>
    </div>
  </div>
</main>

<script>
async function postAPI(endpoint, body) {
  const r = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  return await r.json();
}

async function testarChat() {
  const p = document.getElementById('chat-pergunta').value.trim();
  if(!p) return alert('Digite uma pergunta.');
  const d = await postAPI('/api/professor/chat', { pergunta: p });
  document.getElementById('chat-resp').style.display = 'block';
  document.getElementById('chat-json').textContent = JSON.stringify(d, null, 2);
}

async function testarExplicar() {
  const c = document.getElementById('exp-termo').value.trim();
  const d = await postAPI('/api/professor/explicar', { conceito: c });
  document.getElementById('exp-resp').style.display = 'block';
  document.getElementById('exp-json').textContent = JSON.stringify(d, null, 2);
}

async function testarCaso() {
  const d = await postAPI('/api/professor/caso-clinico', {});
  document.getElementById('caso-resp').style.display = 'block';
  document.getElementById('caso-json').textContent = JSON.stringify(d, null, 2);
}

async function testarAvaliar() {
  const t = document.getElementById('aval-texto').value.trim();
  if(!t) return alert('Digite sua explicação.');
  const d = await postAPI('/api/professor/avaliar', { explicacao_estudante: t });
  document.getElementById('aval-resp').style.display = 'block';
  document.getElementById('aval-json').textContent = JSON.stringify(d, null, 2);
}
</script>
</body>
</html>
"""

def main():
    server = ThreadedHTTPServer(("0.0.0.0", PORT), ProfessorAPIHandler)
    print(f"==================================================")
    print(f"🎓 PsicoBase - API do Professor Digital de Psicologia")
    print(f"🚀 Servidor rodando em: http://localhost:{PORT}")
    print(f"📖 Documentação interativa: http://localhost:{PORT}/api/docs")
    print(f"==================================================")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nFinalizando servidor...")
        server.server_close()

if __name__ == "__main__":
    main()
