# 🧠 PsicoBase

> **Plataforma web interativa de estudos e API de apoio pedagógico para estudantes e entusiastas de Psicologia.**

---

## 🌟 Sobre o Projeto

O **PsicoBase** foi desenvolvido para apoiar calouros, graduandos e estudantes autodidatas de Psicologia em sua jornada acadêmica. O projeto combina um currículo estruturado de **12 eixos temáticos com 47 aulas aprofundadas**, sistema de **repetição espaçada (SRS)** com flashcards interativos 3D, temporizador **Pomodoro** integrado, síntese de voz para leitura das aulas, caderno de anotações e um **Professor Digital de Psicologia** (com API REST própria e suporte a múltiplos provedores).

---

## ✨ Principais Funcionalidades

### 🖥️ Interface e Experiência do Estudante (`index.html`)
- **Design Moderno e Acolhedor:** Visual limpo e responsivo (mobile-first e sidebar para desktop) com temas **Claro** e **Escuro**.
- **12 Módulos da Graduação:** 47 aulas cobrindo Epistemologia, História, Behaviorismo, Psicanálise, TCC, Neurociências, Processos Básicos, Desenvolvimento, Social, Personalidade, Metodologia e Ética (CFP).
- **⏱️ Temporizador Pomodoro Integrado:** Ciclos de 25 minutos de estudo com som e contabilização automática dos minutos na sua meta diária.
- **🔥 Rastreador de Sequência (Streak):** Monitoramento diário de consistência de estudos.
- **🔊 Leitor de Voz (Text-to-Speech):** Permite ouvir as aulas pelo navegador em português (`pt-BR`).
- **📝 Caderno de Anotações por Aula:** Salve observações pessoais e resumos diretamente no navegador com salvamento automático.
- **🧠 Flashcards com Repetição Espaçada (SRS):** Cartões 3D com rotação suave e atalhos de teclado (`Espaço` para virar, `1` Difícil, `2` Bom, `3` Fácil).
- **🔍 Busca Rápida Global (`Ctrl + K`):** Localize qualquer aula, autor ou conceito do glossário em tempo real.
- **📦 Backup e Privacidade:** Seus dados e progresso ficam guardados de forma segura e privada no navegador, com exportação e importação de backups em JSON.

---

### 🎓 API do Professor Digital de Psicologia (`api_server.py`)
Serviço REST desenvolvido em **Python nativo (sem dependências externas)** que atua como tutor socrático 24/7.

- **Conformidade Ética:** Respeita as diretrizes do **Código de Ética Profissional do Psicólogo (CFP)**, recusando diagnósticos pessoais e fornecendo acolhimento e redirecionamento imediato para o **CVV (188)** em situações de crise.
- **Painel Interativo de Testes:** Documentação e console Swagger em `http://localhost:8000/api/docs`.
- **Modos de Operação:**
  1. **Motor Local/Offline Integrado:** Funciona instantaneamente sem necessidade de chaves de API pagas.
  2. **Conexão com LLMs:** Suporta integração opcional com Google Gemini, OpenAI ou Anthropic Claude.

#### Endpoints Disponíveis:
| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/api/status` | Verifica a integridade, estatísticas e tópicos da API |
| `POST` | `/api/professor/chat` | Tira-dúvidas socrático conceitual e metodológico |
| `POST` | `/api/professor/explicar` | Decomposição pedagógica de conceitos (definição, analogia e exemplo) |
| `POST` | `/api/professor/caso-clinico` | Geração de vinhetas de casos hipotéticos para treino clínico e ético |
| `POST` | `/api/professor/simulado` | Questões de múltipla escolha com justificativa |
| `POST` | `/api/professor/avaliar` | Feedback formativo de explicações e resumos redigidos pelo estudante |

---

## 🚀 Como Executar o Projeto

### 1. Utilizando a Interface Web
Basta abrir o arquivo `index.html` em qualquer navegador moderno (Chrome, Edge, Firefox, Safari). Não requer instalação de pacotes ou servidores para uso básico.

### 2. Executando a API do Professor Digital
Com o Python 3.8+ instalado na sua máquina:

```bash
# Iniciar o servidor da API
python api_server.py
```

O servidor estará disponível em:
- **API Base:** `http://localhost:8000/api`
- **Painel de Testes & Documentação:** `http://localhost:8000/api/docs`

### 3. Rodando os Testes Automatizados da API
```bash
python test_api.py
```

---

## 📂 Estrutura de Arquivos

```
PsycoBase/
├── index.html           # Aplicação web moderna completa (SPA)
├── PsicoBase.html       # Cópia compatível da aplicação web
├── api_server.py        # Servidor REST do Professor Digital (Python nativo)
├── test_api.py          # Suíte de testes automatizados da API
├── build_index.py       # Script de montagem e sincronização da aplicação
├── README.md            # Documentação completa do projeto
└── .gitignore           # Arquivos ignorados pelo controle de versão
```

---

## 📜 Licença e Ética
Este projeto possui caráter estritamente educativo e formativo para estudantes de graduação e entusiastas de Psicologia. Não substitui psicoterapia, consulta clínica ou supervisão presencial qualificada.
