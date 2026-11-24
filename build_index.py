# -*- coding: utf-8 -*-
"""
Builder para o index.html da PsicoBase
Integra todo o conteúdo pedagógico original de 47 aulas + glossários
com a nova direção de arte: Editorial Humanista Contemporâneo,
Ergonomia Cognitiva, Tipografia Lora + Plus Jakarta Sans, Modo Foco Zen,
Pomodoro com respiração e estética de fichamento de pesquisa.
"""

import os
import re

source_path = r"c:\Users\MatheusRochaLopes\Downloads\PsicoBase (1).html"
if not os.path.exists(source_path):
    source_path = r"c:\Users\MatheusRochaLopes\Desktop\PsycoBase\PsicoBase.html"

with open(source_path, "r", encoding="utf-8") as f:
    orig = f.read()

# Extrair bloco de dados curriculares (constantes de conteúdo)
start_data = orig.find("const CHAVE=")
end_sort = orig.find('GLOSSARIO.sort((a,b)=>a.termo.localeCompare(b.termo,"pt-BR"));')
if end_sort != -1:
    end_data = end_sort + len('GLOSSARIO.sort((a,b)=>a.termo.localeCompare(b.termo,"pt-BR"));')
else:
    m = re.search(r"/\* =+ ESTADO.*?=+\s*\*/", orig)
    end_data = m.start() if m else -1

if start_data == -1 or end_data == -1:
    raise ValueError("Erro ao delimitar dados curriculares!")

dados_curriculares = orig[start_data:end_data].strip()

novo_html = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#4A1525">
<meta name="description" content="PsicoBase - O espaço onde a mente humana é estudada com profundidade, método e acolhimento.">
<title>PsicoBase · Onde a Mente Humana é Estudada com Rigor e Acolhimento</title>

<!-- Tipografia: Lora (Editorial Clássico) + Plus Jakarta Sans (Ergonomia Digital) -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">

<style>
/* ==========================================================================
   DESIGN SYSTEM PSICOBASE: EDITORIAL HUMANISTA CONTEMPORÂNEO
   ========================================================================== */
:root {
  /* Paleta Modo Claro: Estúdio de Pesquisa & Biblioteca Acolhedora */
  --bg-canvas: #F8F6F0;       /* Linho / Pergaminho suave (elimina fadiga ocular) */
  --bg-card: #FFFFFF;         /* Superfície de cartão pura */
  --bg-fichamento: #FAF8F4;   /* Tom de papel de ficha bibliográfica */
  --bg-sepia: #F3ECE1;       /* Sepia sutil para destaques */
  --fg-base: #242124;         /* Grafite quente e profundo */
  --fg-muted: #645D68;        /* Cinza grafite atenuado */
  --borda-suave: #E7E1D8;     /* Linha de encadernação clássica */
  --borda-foco: #7A5C91;

  /* Cores de Identidade & Afeto */
  --primaria: #4A1525;        /* Bordô / Vinho Clássico (rigor e história) */
  --primaria-hover: #380F1B;
  --primaria-tint: rgba(74, 21, 37, 0.07);
  --secundaria: #7A5C91;      /* Lavanda Aveludada / Ametista (psique e calmaria) */
  --secundaria-tint: rgba(122, 92, 145, 0.12);
  
  /* Cores Funcionais de Redução de Carga Mental */
  --salvia: #3A7356;          /* Verde Sálvia (foco sereno e acertos) */
  --salvia-tint: rgba(58, 115, 86, 0.12);
  --terracota: #BD6148;       /* Terracota Suave (atenção sem alarme punitivo) */
  --terracota-tint: rgba(189, 97, 72, 0.12);
  --ambar: #C28D38;           /* Ocre / Âmbar Antigo (conquistas e consistência) */
  --ambar-tint: rgba(194, 141, 56, 0.12);

  /* Sombras Táteis & Orgânicas */
  --sombra-card: 0 4px 16px rgba(50, 40, 35, 0.04), 0 1px 3px rgba(50, 40, 35, 0.03);
  --sombra-hover: 0 8px 26px rgba(50, 40, 35, 0.08), 0 2px 6px rgba(50, 40, 35, 0.04);
  --sombra-flutuante: 0 12px 36px rgba(74, 21, 37, 0.12);

  /* Tipografia & Métricas de Leitura */
  --font-serif: 'Lora', Georgia, 'Times New Roman', serif;
  --font-sans: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
  --leitura-max-ch: 70ch;
  --line-height-leitura: 1.72;
  --radius-card: 16px;
  --radius-pill: 9999px;

  /* Easing Orgânico Calm Tech (respiração) */
  --calm-ease: cubic-bezier(0.2, 0.8, 0.2, 1);
  --duracao-rapida: 0.2s;
  --duracao-padrao: 0.35s;
}

body.escuro {
  /* Paleta Modo Escuro: Sessão Noturna de Leitura & Consultório Introspectivo */
  --bg-canvas: #131217;       /* Ardósia profunda com subtom roxo/índigo */
  --bg-card: #1E1B24;         /* Superfície de leitura noturna */
  --bg-fichamento: #25222D;
  --bg-sepia: #2B2633;
  --fg-base: #F4F1F7;
  --fg-muted: #A39BAA;
  --borda-suave: #302B3A;
  --borda-foco: #C7A7EC;

  --primaria: #E29BB0;        /* Bordô rosé acolhedor */
  --primaria-hover: #F0B3C4;
  --primaria-tint: rgba(226, 155, 176, 0.15);
  --secundaria: #C7A7EC;      /* Lavanda luminosa */
  --secundaria-tint: rgba(199, 167, 236, 0.16);

  --salvia: #66D39D;          /* Menta serena */
  --salvia-tint: rgba(102, 211, 157, 0.15);
  --terracota: #FF8A73;
  --terracota-tint: rgba(255, 138, 115, 0.15);
  --ambar: #F0BF65;
  --ambar-tint: rgba(240, 191, 101, 0.15);

  --sombra-card: 0 4px 20px rgba(0, 0, 0, 0.35);
  --sombra-hover: 0 8px 30px rgba(0, 0, 0, 0.5);
  --sombra-flutuante: 0 12px 40px rgba(0, 0, 0, 0.65);
}

/* Reset Universal com Foco em Fluidez */
*, *::before, *::after { box-sizing: border-box; }
[hidden] { display: none !important; }
html { scroll-behavior: smooth; }

body {
  margin: 0; padding: 0;
  font-family: var(--font-sans);
  background-color: var(--bg-canvas);
  color: var(--fg-base);
  line-height: 1.65;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  transition: background-color var(--duracao-padrao) var(--calm-ease), color var(--duracao-padrao) var(--calm-ease);
}
body.grande { font-size: 112%; }

/* ==========================================================================
   ESTILOS DE CABEÇALHO & IDENTIDADE VISUAL (PSI)
   ========================================================================== */
.app-header {
  position: sticky; top: 0; z-index: 50;
  background: rgba(248, 246, 240, 0.9);
  backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
  border-bottom: 1px solid var(--borda-suave);
  padding: 12px 24px;
  display: flex; align-items: center; justify-content: space-between; gap: 16px;
  transition: all var(--duracao-padrao) var(--calm-ease);
}
body.escuro .app-header { background: rgba(19, 18, 23, 0.9); }

.header-brand {
  display: flex; align-items: center; gap: 12px;
  text-decoration: none; color: var(--primaria);
  font-family: var(--font-serif); font-weight: 700; font-size: 1.35rem;
  letter-spacing: -0.01em;
}

/* Marca d'água / Símbolo Psi Minimalista */
.psi-emblem {
  width: 36px; height: 36px; border-radius: 12px;
  background: var(--primaria); color: #FFF;
  display: flex; align-items: center; justify-content: center;
  font-family: var(--font-serif); font-size: 1.3rem; font-weight: 600;
  box-shadow: 0 2px 8px rgba(74, 21, 37, 0.2);
  transition: transform var(--duracao-padrao) var(--calm-ease);
}
body.escuro .psi-emblem {
  background: var(--primaria-tint); color: var(--primaria);
  border: 1px solid var(--primaria);
}
.header-brand:hover .psi-emblem { transform: rotate(-5deg) scale(1.05); }

/* Pomodoro com Respiração & Pílula de Foco */
.pomo-pill {
  display: inline-flex; align-items: center; gap: 8px;
  background: var(--bg-card); border: 1px solid var(--borda-suave);
  padding: 6px 14px; border-radius: var(--radius-pill);
  font-family: var(--font-sans); font-size: 0.88rem; font-weight: 700;
  color: var(--primaria); box-shadow: var(--sombra-card);
  transition: all var(--duracao-padrao) var(--calm-ease);
}
.pomo-breath-circle {
  width: 8px; height: 8px; border-radius: 50%;
  background: var(--salvia);
  display: inline-block;
}
.pomo-pill.ativo .pomo-breath-circle {
  animation: pulseBreath 3s infinite var(--calm-ease);
}
@keyframes pulseBreath {
  0%, 100% { transform: scale(1); opacity: 0.6; }
  50% { transform: scale(1.8); opacity: 1; box-shadow: 0 0 10px var(--salvia); }
}

.btn-icon-subtle {
  background: none; border: none; cursor: pointer; color: inherit;
  padding: 2px 6px; font-size: 0.95rem; border-radius: 6px;
  display: inline-flex; align-items: center; justify-content: center;
  transition: background-color var(--duracao-rapida);
}
.btn-icon-subtle:hover { background: var(--primaria-tint); }

.header-actions { display: flex; align-items: center; gap: 10px; }

.btn-header {
  display: inline-flex; align-items: center; gap: 6px;
  background: var(--bg-card); color: var(--fg-base);
  border: 1px solid var(--borda-suave); padding: 7px 14px;
  border-radius: var(--radius-pill); font-size: 0.86rem; font-weight: 600;
  cursor: pointer; transition: all var(--duracao-rapida) var(--calm-ease);
}
.btn-header:hover {
  border-color: var(--secundaria); background: var(--secundaria-tint);
  transform: translateY(-1px);
}

/* ==========================================================================
   NAVEGAÇÃO TÁTIL & SIDEBAR DESKTOP
   ========================================================================== */
nav.inferior {
  position: fixed; bottom: 0; left: 0; right: 0;
  background: rgba(248, 246, 240, 0.95);
  backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
  border-top: 1px solid var(--borda-suave);
  display: flex; justify-content: space-around; z-index: 40;
  padding-bottom: env(safe-area-inset-bottom);
  transition: background var(--duracao-padrao) var(--calm-ease);
}
body.escuro nav.inferior { background: rgba(19, 18, 23, 0.95); }

nav.inferior a {
  flex: 1; text-align: center; padding: 10px 4px;
  font-size: 0.74rem; font-weight: 600; text-decoration: none;
  color: var(--fg-muted); display: flex; flex-direction: column;
  align-items: center; gap: 4px; min-height: 58px; justify-content: center;
  transition: color var(--duracao-rapida), transform var(--duracao-rapida);
}
nav.inferior a svg { width: 22px; height: 22px; stroke-width: 2.1; transition: stroke var(--duracao-rapida); }
nav.inferior a[aria-current="page"] { color: var(--primaria); font-weight: 700; }
nav.inferior a[aria-current="page"] svg { stroke: var(--primaria); }

.wrap {
  max-width: 860px; margin: 0 auto;
  padding: 24px 20px 100px;
}

/* Desktop Sidebar Editorial */
@media (min-width: 960px) {
  body { padding-left: 270px; padding-bottom: 0; }
  .app-header { left: 270px; width: calc(100% - 270px); }
  nav.inferior {
    top: 0; bottom: 0; left: 0; right: auto; width: 270px;
    flex-direction: column; justify-content: flex-start; gap: 6px;
    padding: 30px 18px; border-top: 0; border-right: 1px solid var(--borda-suave);
  }
  .nav-header-desktop {
    padding: 0 10px 24px; margin-bottom: 12px;
    border-bottom: 1px solid var(--borda-suave);
    display: flex; align-items: center; gap: 12px;
  }
  nav.inferior a {
    flex: none; flex-direction: row; justify-content: flex-start; gap: 14px;
    padding: 12px 16px; border-radius: 12px; font-size: 0.95rem; min-height: 48px;
  }
  nav.inferior a[aria-current="page"] {
    background: var(--primaria-tint); color: var(--primaria);
    border-left: 4px solid var(--primaria); font-weight: 700;
  }
  .wrap { max-width: 980px; padding: 36px 44px 80px; }
}

/* ==========================================================================
   TIPOGRAFIA & CARDS COM TEXTURA DE FICHA BIBLIOGRÁFICA
   ========================================================================== */
h1, h2, h3, h4 {
  color: var(--fg-base); font-family: var(--font-serif);
  font-weight: 600; line-height: 1.3;
}
h1 {
  font-size: 2.15rem; margin: 0.4rem 0 1.2rem;
  letter-spacing: -0.025em; font-weight: 700;
}
h2 {
  font-size: 1.45rem; margin: 2rem 0 0.9rem;
  color: var(--primaria); border-bottom: 1px solid var(--borda-suave);
  padding-bottom: 6px;
}
h3 { font-size: 1.15rem; margin: 1.2rem 0 0.4rem; }

p {
  font-size: 1.05rem; line-height: var(--line-height-leitura);
  max-width: var(--leitura-max-ch);
}
.muted { color: var(--fg-muted); font-size: 0.92rem; }

/* Ficha Bibliográfica / Card Tátil */
.card {
  background: var(--bg-card);
  border: 1px solid var(--borda-suave);
  border-radius: var(--radius-card);
  padding: 24px; margin: 18px 0;
  box-shadow: var(--sombra-card);
  position: relative; overflow: hidden;
  transition: transform var(--duracao-padrao) var(--calm-ease), box-shadow var(--duracao-padrao) var(--calm-ease);
}
.card:hover {
  transform: translateY(-2px);
  box-shadow: var(--sombra-hover);
}

/* Watermark de Psi para cards nobres */
.card.destaque {
  border-left: 5px solid var(--primaria);
  background: linear-gradient(135deg, var(--bg-card) 70%, var(--bg-sepia) 100%);
}
.card.destaque::after {
  content: 'Ψ';
  position: absolute; right: -10px; bottom: -20px;
  font-family: var(--font-serif); font-size: 9rem; font-weight: 700;
  color: var(--primaria); opacity: 0.035; pointer-events: none;
  user-select: none; line-height: 1;
}

/* Botões Ergonômicos */
.btn {
  display: inline-flex; align-items: center; justify-content: center; gap: 8px;
  background: var(--primaria); color: #FFF; border: 2px solid var(--primaria);
  border-radius: 12px; padding: 11px 22px; font-family: var(--font-sans);
  font-weight: 600; font-size: 0.96rem; cursor: pointer; min-height: 46px;
  text-decoration: none; margin: 4px 6px 4px 0;
  box-shadow: 0 2px 8px rgba(74, 21, 37, 0.16);
  transition: all var(--duracao-rapida) var(--calm-ease);
}
.btn:hover {
  background: var(--primaria-hover); border-color: var(--primaria-hover);
  text-decoration: none; transform: translateY(-1.5px);
  box-shadow: 0 4px 12px rgba(74, 21, 37, 0.24);
}
.btn.sec {
  background: transparent; color: var(--primaria);
  border-color: var(--borda-suave); box-shadow: none;
}
.btn.sec:hover {
  background: var(--primaria-tint); border-color: var(--primaria);
}
.btn.sm {
  padding: 6px 14px; font-size: 0.86rem; min-height: 36px; border-radius: 8px;
}

/* Tags de Fichamento */
.tag {
  display: inline-flex; align-items: center; gap: 5px;
  background: var(--bg-sepia); color: var(--fg-base);
  padding: 4px 12px; border-radius: var(--radius-pill);
  font-size: 0.78rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.04em; border: 1px solid var(--borda-suave);
}
.tag.concluido { background: var(--salvia-tint); color: var(--salvia); border-color: transparent; }
.tag.pendente { background: var(--primaria-tint); color: var(--primaria); border-color: transparent; }

/* Barra de Progresso Suave */
.barra {
  height: 7px; background: var(--borda-suave);
  border-radius: var(--radius-pill); overflow: hidden; margin: 10px 0;
}
.barra > div {
  height: 100%; background: var(--salvia);
  transition: width 0.5s var(--calm-ease);
}

/* Grades Táteis */
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 18px; margin: 18px 0; }
.grid-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 14px; margin: 16px 0; }

.stat-box {
  background: var(--bg-card); border: 1px solid var(--borda-suave);
  border-radius: var(--radius-card); padding: 18px; text-align: center;
  box-shadow: var(--sombra-card);
}
.stat-box .num {
  font-family: var(--font-serif); font-size: 1.85rem; font-weight: 700;
  color: var(--primaria); display: block; line-height: 1.15;
}
.stat-box .rotulo {
  font-size: 0.8rem; font-weight: 700; color: var(--fg-muted);
  text-transform: uppercase; letter-spacing: 0.05em; margin-top: 4px; display: block;
}

/* ==========================================================================
   SELOS CONCEITUAIS DOS 12 EIXOS TEMÁTICOS (MÓDULOS)
   ========================================================================== */
.modulo-card {
  position: relative; border-radius: var(--radius-card);
  background: var(--bg-card); border: 1px solid var(--borda-suave);
  padding: 24px; box-shadow: var(--sombra-card);
  transition: all var(--duracao-padrao) var(--calm-ease);
  overflow: hidden;
}
.modulo-card:hover { transform: translateY(-3px); box-shadow: var(--sombra-hover); }

/* Selos conceituais táteis no topo do card */
.modulo-card::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px;
  background: var(--borda-suave);
}
.modulo-card[data-mod="1"]::before { background: linear-gradient(90deg, var(--primaria), var(--secundaria)); }
.modulo-card[data-mod="2"]::before { background: var(--ambar); } /* História */
.modulo-card[data-mod="3"]::before { background: var(--primaria); } /* Psicanálise e Abordagens */
.modulo-card[data-mod="4"]::before { background: linear-gradient(90deg, #9D71E8, #3A7356); } /* Neurociências */
.modulo-card[data-mod="5"]::before { background: var(--secundaria); } /* Processos Básicos */
.modulo-card[data-mod="6"]::before { background: #2F6F9F; } /* Behaviorismo/Aprendizagem */
.modulo-card[data-mod="7"]::before { background: var(--salvia); } /* Desenvolvimento */
.modulo-card[data-mod="8"]::before { background: #D97736; } /* Social */
.modulo-card[data-mod="9"]::before { background: #8E4A49; } /* Personalidade */
.modulo-card[data-mod="10"]::before { background: #45625D; } /* Metodologia Científica */
.modulo-card[data-mod="11"]::before { background: var(--ambar); } /* Ética CFP */
.modulo-card[data-mod="12"]::before { background: var(--terracota); } /* Psicopatologia */

/* ==========================================================================
   FLASHCARD 3D CLÁSSICO (REPETIÇÃO ESPAÇADA)
   ========================================================================== */
.flashcard-wrap { perspective: 1200px; margin: 28px 0; }
.flashcard {
  background: var(--bg-card); border: 2px solid var(--borda-suave);
  border-radius: 20px; min-height: 280px; padding: 36px 30px;
  box-shadow: var(--sombra-hover); cursor: pointer;
  display: flex; flex-direction: column; justify-content: center; align-items: center;
  text-align: center; transition: transform 0.6s var(--calm-ease);
  transform-style: preserve-3d; position: relative; user-select: none;
}
.flashcard.virado { transform: rotateY(180deg); }
.flashcard-lado { position: relative; backface-visibility: hidden; width: 100%; }
.flashcard-verso {
  position: absolute; top: 0; left: 0; right: 0; bottom: 0; padding: 36px 30px;
  backface-visibility: hidden; transform: rotateY(180deg);
  display: flex; flex-direction: column; justify-content: center; align-items: center;
  background: var(--bg-fichamento); border-radius: 18px;
}
.flashcard h2 { font-family: var(--font-serif); border: none; padding: 0; }

/* ==========================================================================
   MODO FOCO ZEN DE LEITURA (AULA SEM DISTRAÇÕES)
   ========================================================================== */
body.modo-zen {
  padding-left: 0 !important;
  background-color: #FAF8F5;
}
body.escuro.modo-zen { background-color: #111014; }

body.modo-zen .app-header,
body.modo-zen nav.inferior {
  display: none !important;
}
body.modo-zen .wrap {
  max-width: 760px; padding: 50px 24px;
}
.btn-zen-toggle {
  position: fixed; right: 24px; bottom: 24px; z-index: 90;
  box-shadow: var(--sombra-flutuante);
}

/* ==========================================================================
   O PROFESSOR DIGITAL & BANNER ÉTICO CFP / CVV 188
   ========================================================================== */
.chat-container {
  display: flex; flex-direction: column; gap: 16px;
  margin: 20px 0; max-height: 520px; overflow-y: auto; padding-right: 8px;
}
.chat-msg { display: flex; gap: 14px; max-width: 90%; }
.chat-msg.prof { align-self: flex-start; }
.chat-msg.aluno { align-self: flex-end; flex-direction: row-reverse; }

.chat-avatar {
  width: 40px; height: 40px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-family: var(--font-serif); font-size: 1.15rem; font-weight: 700; flex-shrink: 0;
}
.chat-msg.prof .chat-avatar {
  background: var(--primaria); color: #FFF;
  box-shadow: 0 2px 8px rgba(74, 21, 37, 0.25);
}
.chat-msg.aluno .chat-avatar { background: var(--secundaria); color: #FFF; }

.chat-bubble {
  padding: 16px 22px; border-radius: 20px;
  font-size: 0.98rem; line-height: 1.68;
}
.chat-msg.prof .chat-bubble {
  background: var(--bg-card); border: 1px solid var(--borda-suave);
  border-top-left-radius: 4px; box-shadow: var(--sombra-card);
}
.chat-msg.aluno .chat-bubble {
  background: var(--primaria); color: #FFFFFF;
  border-top-right-radius: 4px;
}
body.escuro .chat-msg.aluno .chat-bubble { background: var(--secundaria); color: #FFF; }

/* Banner Ético Permanente */
.banner-etico {
  background: var(--bg-sepia); border: 1px solid var(--borda-suave);
  border-radius: 12px; padding: 12px 18px; margin-top: 14px;
  font-size: 0.84rem; display: flex; align-items: center; gap: 12px;
  color: var(--fg-muted);
}
.banner-etico strong { color: var(--primaria); }

/* Inputs e Formulários */
.campo {
  width: 100%; padding: 12px 16px; border-radius: 12px;
  border: 1px solid var(--borda-suave); background: var(--bg-card); color: var(--fg-base);
  font: inherit; font-size: 0.96rem; transition: all var(--duracao-rapida) var(--calm-ease);
}
.campo:focus {
  outline: none; border-color: var(--primaria);
  box-shadow: 0 0 0 3px var(--primaria-tint);
}

.toast {
  position: fixed; top: 24px; left: 50%; transform: translateX(-50%);
  background: #242124; color: #FFFFFF; padding: 12px 24px; border-radius: 30px;
  z-index: 9999; max-width: 90%; font-size: 0.92rem; font-weight: 600;
  box-shadow: var(--sombra-flutuante); animation: fadeUp 0.3s var(--calm-ease);
}
@keyframes fadeUp {
  from { opacity: 0; transform: translate(-50%, 15px); }
  to { opacity: 1; transform: translate(-50%, 0); }
}

/* Opções de Seleção & Quizzes (.alt) */
.alt {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 13px 18px;
  margin: 10px 0;
  border-radius: 12px;
  border: 1.5px solid var(--borda-suave);
  background: var(--bg-card);
  color: var(--fg-base);
  cursor: pointer;
  transition: all var(--duracao-rapida) var(--calm-ease);
  user-select: none;
  font-size: 0.98rem;
  line-height: 1.55;
}
.alt:hover {
  border-color: var(--primaria);
  background: var(--primaria-tint);
  transform: translateY(-1px);
}
.alt input[type="radio"],
.alt input[type="checkbox"] {
  margin-top: 3px;
  accent-color: var(--primaria);
  width: 18px;
  height: 18px;
  cursor: pointer;
  flex-shrink: 0;
}
.alt:has(input:checked) {
  border-color: var(--primaria);
  background: var(--primaria-tint);
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(74, 21, 37, 0.08);
}
body.escuro .alt:has(input:checked) {
  border-color: var(--primaria);
  background: rgba(226, 155, 176, 0.15);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

/* Fieldset e Legend para Quizzes */
fieldset.card, fieldset {
  border: 1px solid var(--borda-suave);
  border-radius: var(--radius-card);
  padding: 20px 22px;
  margin: 18px 0;
  background: var(--bg-card);
  box-shadow: var(--sombra-card);
}
legend {
  font-family: var(--font-serif);
  font-weight: 700;
  font-size: 1.05rem;
  color: var(--fg-base);
  padding: 0 10px;
  line-height: 1.4;
}

/* Feedback de Resultados Formativos */
.res {
  padding: 16px 20px;
  border-radius: 12px;
  margin: 14px 0;
  border-left: 5px solid var(--borda-suave);
  background: var(--bg-card);
  box-shadow: var(--sombra-card);
  line-height: 1.6;
}
.res.ok {
  border-left-color: var(--salvia);
  background: var(--salvia-tint);
}
.res.ok strong {
  color: var(--salvia);
}
.res.erro {
  border-left-color: var(--terracota);
  background: var(--terracota-tint);
}
.res.erro strong {
  color: var(--terracota);
}

/* Utilitários Responsivos e Textarea */
textarea.campo {
  resize: vertical;
  min-height: 120px;
  line-height: 1.6;
  font-family: var(--font-sans);
}
@media (min-width: 768px) {
  .d-md-inline { display: inline !important; }
}

/* Modal de Busca Rápida */
.modal-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(19, 18, 23, 0.6); backdrop-filter: blur(8px);
  z-index: 999; display: flex; align-items: flex-start; justify-content: center; padding: 60px 16px;
}
.modal-content {
  background: var(--bg-card); border: 1px solid var(--borda-suave);
  border-radius: 20px; max-width: 660px; width: 100%; max-height: 82vh;
  display: flex; flex-direction: column; box-shadow: var(--sombra-flutuante);
}
.modal-header { padding: 18px 24px; border-bottom: 1px solid var(--borda-suave); display: flex; align-items: center; gap: 14px; }
.modal-body { padding: 20px 24px; overflow-y: auto; flex: 1; }
</style>
</head>
<body>
<div id="aviso" class="toast" role="status" aria-live="polite" hidden></div>

<!-- Top Header com Identidade Psi e Pomodoro com Respiração -->
<header class="app-header" id="header" hidden>
  <a href="#/inicio" class="header-brand">
    <div class="psi-emblem">Ψ</div>
    <span>PsicoBase</span>
  </a>
  
  <div class="header-actions">
    <!-- Streak -->
    <div class="btn-header" title="Sequência de dias dedicados ao estudo" id="streak-badge">🔥 0 dias</div>
    
    <!-- Pomodoro de Foco -->
    <div class="pomo-pill" id="pomo-box" title="Pomodoro de Estudo & Foco">
      <span class="pomo-breath-circle"></span>
      <span id="pomo-display">25:00</span>
      <button class="btn-icon-subtle" id="pomo-toggle" onclick="togglePomodoro()" title="Iniciar/Pausar">▶</button>
      <button class="btn-icon-subtle" id="pomo-reset" onclick="resetPomodoro()" title="Reiniciar">↺</button>
    </div>
    
    <!-- Busca Rápida (Ctrl+K) -->
    <button class="btn-header" onclick="abrirBuscaModal()" title="Busca Rápida de Aulas e Termos (Ctrl+K)">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
      <span style="display:none" class="d-md-inline">Buscar</span>
    </button>

    <!-- Alternador de Tema -->
    <button class="btn-header" onclick="alternarTema()" title="Alternar Modo Noturno / Leitura em Linho">
      <span id="tema-icon">🌙</span>
    </button>
  </div>
</header>

<!-- Navegação Principal com Estética Editorial -->
<nav class="inferior" id="nav" aria-label="Navegação principal" hidden>
  <div class="nav-header-desktop" style="display:none">
    <div class="header-brand">
      <div class="psi-emblem">Ψ</div>
      <span>PsicoBase</span>
    </div>
  </div>
  <a href="#/inicio" data-nav="inicio">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
    <span>Início</span>
  </a>
  <a href="#/aprender" data-nav="aprender">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>
    <span>Aprender</span>
  </a>
  <a href="#/revisar" data-nav="revisar">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
    <span>Revisar</span>
  </a>
  <a href="#/professor" data-nav="professor">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path><circle cx="9" cy="10" r="1"></circle><circle cx="15" cy="10" r="1"></circle></svg>
    <span>Professor IA</span>
  </a>
  <a href="#/biblioteca" data-nav="biblioteca">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
    <span>Biblioteca</span>
  </a>
  <a href="#/perfil" data-nav="perfil">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
    <span>Perfil</span>
  </a>
</nav>

<!-- Conteúdo Dinâmico -->
<main id="app" class="wrap" tabindex="-1"></main>

<!-- Modal de Busca Rápida -->
<div id="modal-busca" class="modal-overlay" style="display:none" onclick="if(event.target===this) fecharBuscaModal()">
  <div class="modal-content">
    <div class="modal-header">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
      <input id="input-busca-modal" class="campo" type="search" placeholder="Pesquisar em todas as 47 aulas, autores e termos..." oninput="executarBuscaModal(this.value)" autocomplete="off">
      <button class="btn sec sm" onclick="fecharBuscaModal()">✕</button>
    </div>
    <div id="modal-busca-resultados" class="modal-body">
      <p class="muted">Digite uma palavra-chave para encontrar conteúdos em toda a PsicoBase.</p>
    </div>
  </div>
</div>

<script>
(()=>{
'use strict';

/* ==================== DADOS CURRICULARES (47 AULAS E GLOSSÁRIO) ==================== */
""" + dados_curriculares + r"""

/* ==================== ESTADO E PERSISTÊNCIA ==================== */
function estadoPadrao(){
 return {
   perfil:null, aulasConcluidas:{}, tentativas:[], cartoes:{}, minPorDia:{},
   anotacoes:{}, ultimaAula:null, abertas:{}, tema:'claro', fonte:'normal',
   apiServidor:'http://localhost:8000/api', chaveIA:'', criadoEm:Date.now()
 };
}
function carregar(){
 let s=null;
 try{ s=JSON.parse(localStorage.getItem(CHAVE)); }catch(e){ s=null; }
 return Object.assign(estadoPadrao(), (s && typeof s==='object')?s:{});
}
let estado=carregar();
const app=document.getElementById('app');
const nav=document.getElementById('nav');
const header=document.getElementById('header');
let sessao=null;
let obPasso=1;
let obDados={nivel:'',objetivo:'',tempo:'',preferencias:[],apelido:''};
let filaRev=null;
let revIndice=0;
let revVerso=false;
let modoZenAtivo=false;

/* Pomodoro Timer */
let pomoTempo=25*60;
let pomoInterval=null;
let pomoAtivo=false;

function salvar(){
 try{ localStorage.setItem(CHAVE, JSON.stringify(estado)); return true; }
 catch(e){ aviso('Não foi possível salvar neste navegador. Exporte um backup pelo Perfil.'); return false; }
}

function garantirCartoes(aulaId){
 const a=AULAS[aulaId]; if(!a||!a.cartoes) return;
 a.cartoes.forEach(c=>{ if(!estado.cartoes[c.id]) estado.cartoes[c.id]={stage:0,prox:diaNum(),vezes:0,historico:[]}; });
}
function garantirTodos(){ Object.keys(AULAS).forEach(garantirCartoes); }
garantirTodos();

/* ==================== UTILITÁRIOS ==================== */
const $=(s,r=document)=>r.querySelector(s);
function esc(s){ return String(s===undefined||s===null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
function dataISO(d){ d=d||new Date(); return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0'); }
function diaNum(d){ d=d||new Date(); return Math.floor(Date.UTC(d.getFullYear(),d.getMonth(),d.getDate())/86400000); }

function aviso(msg){
 const t=$('#aviso'); t.textContent=msg; t.hidden=false;
 clearTimeout(aviso._t); aviso._t=setTimeout(()=>{ t.hidden=true; },3500);
}

function rota(){ return (location.hash||'#/inicio').replace(/^#/,''); }

function alternarTema(){
 estado.tema = estado.tema==='escuro'?'claro':'escuro';
 salvar();
 aplicarVisual();
}
window.alternarTema = alternarTema;

function alternarModoZen(){
 modoZenAtivo = !modoZenAtivo;
 document.body.classList.toggle('modo-zen', modoZenAtivo);
 aviso(modoZenAtivo ? 'Modo Leitura Zen ativado 🌿' : 'Modo Leitura Zen desativado');
}
window.alternarModoZen = alternarModoZen;

function aplicarVisual(){
 document.body.classList.toggle('escuro', estado.tema==='escuro');
 document.body.classList.toggle('grande', estado.fonte==='grande');
 const ic=$('#tema-icon'); if(ic) ic.textContent = estado.tema==='escuro'?'☀️':'🌙';
 atualizarStreak();
}

function calcularStreak(){
 const dias = Object.keys(estado.minPorDia).filter(k=>estado.minPorDia[k]>0).sort().reverse();
 if(!dias.length) return 0;
 let streak=0;
 let atual=new Date();
 let check=dataISO(atual);
 if(!dias.includes(check)){
   atual.setDate(atual.getDate()-1);
   check=dataISO(atual);
   if(!dias.includes(check)) return 0;
 }
 while(dias.includes(check)){
   streak++;
   atual.setDate(atual.getDate()-1);
   check=dataISO(atual);
 }
 return streak;
}

function atualizarStreak(){
 const el=$('#streak-badge');
 if(el){
   const s=calcularStreak();
   el.textContent='🔥 ' + s + (s===1?' dia':' dias');
 }
}

/* ==================== POMODORO ==================== */
function formatarTempoPomo(s){
 const m=Math.floor(s/60);
 const seg=s%60;
 return String(m).padStart(2,'0')+':'+String(seg).padStart(2,'0');
}
function togglePomodoro(){
 pomoAtivo=!pomoAtivo;
 const btn=$('#pomo-toggle');
 const box=$('#pomo-box');
 if(pomoAtivo){
   if(btn) btn.textContent='⏸';
   if(box) box.classList.add('ativo');
   pomoInterval=setInterval(()=>{
     if(pomoTempo>0){
       pomoTempo--;
       const disp=$('#pomo-display'); if(disp) disp.textContent=formatarTempoPomo(pomoTempo);
     }else{
       clearInterval(pomoInterval);
       pomoAtivo=false;
       if(btn) btn.textContent='▶';
       if(box) box.classList.remove('ativo');
       aviso('🎉 Parabéns! Ciclo Pomodoro concluído (+25 min de foco registrados).');
       const k=dataISO();
       estado.minPorDia[k]=(estado.minPorDia[k]||0)+25;
       salvar();
       pomoTempo=25*60;
     }
   },1000);
 }else{
   if(btn) btn.textContent='▶';
   if(box) box.classList.remove('ativo');
   clearInterval(pomoInterval);
 }
}
window.togglePomodoro = togglePomodoro;

function resetPomodoro(){
 clearInterval(pomoInterval);
 pomoAtivo=false;
 pomoTempo=25*60;
 const disp=$('#pomo-display'); if(disp) disp.textContent='25:00';
 const btn=$('#pomo-toggle'); if(btn) btn.textContent='▶';
 const box=$('#pomo-box'); if(box) box.classList.remove('ativo');
}
window.resetPomodoro = resetPomodoro;

/* ==================== TEMPO DE ESTUDO ==================== */
function iniciarSessao(id){ encerrarSessao(); sessao={id:id, inicio:Date.now()}; }
function encerrarSessao(){
 if(!sessao) return;
 const min=Math.min(Math.round((Date.now()-sessao.inicio)/60000), 120);
 if(min>0){
   const k=dataISO();
   estado.minPorDia[k]=(estado.minPorDia[k]||0)+min;
   salvar();
 }
 sessao=null;
}
window.addEventListener('pagehide', encerrarSessao);
document.addEventListener('visibilitychange', ()=>{ if(document.visibilityState==='hidden') encerrarSessao(); });

/* ==================== REVISÃO ESPAÇADA ==================== */
function revisoesPendentes(){
 garantirTodos();
 return Object.entries(estado.cartoes).filter(([id,c])=>c.prox<=diaNum()).map(([id])=>id);
}
function achaCartao(id){
 for(const a of Object.values(AULAS)){
  const c=(a.cartoes||[]).find(x=>x.id===id);
  if(c) return {id:c.id, frente:c.frente, verso:c.verso, aula:a.titulo, aulaId:a.id};
 }
 return null;
}
function responderCartao(id,nivel){
 const c=estado.cartoes[id]; if(!c) return;
 let s=c.stage;
 if(nivel==='dificil') s=0;
 else if(nivel==='bom') s=Math.max(1,s);
 else if(nivel==='facil') s=Math.min(INTERVALOS.length-1,s+1);
 c.stage=s;
 c.prox=diaNum()+INTERVALOS[s];
 c.vezes++;
 c.historico.push({d:dataISO(), n:nivel});
 salvar();
}

/* ==================== LEITOR DE VOZ (PODCAST ZEN) ==================== */
let vozFalando=false;
function falarTexto(texto){
 if(!('speechSynthesis' in window)) return aviso('Síntese de voz não suportada pelo seu navegador.');
 if(vozFalando){
   window.speechSynthesis.cancel();
   vozFalando=false;
   const btn=$('#btn-audio-aula'); if(btn) btn.innerHTML='🔊 Ouvir Aula (Podcast)';
   return;
 }
 window.speechSynthesis.cancel();
 const utt=new SpeechSynthesisUtterance(texto);
 utt.lang='pt-BR';
 utt.rate=0.95; /* Leitura cadenciada e acolhedora */
 utt.onend=()=>{
   vozFalando=false;
   const btn=$('#btn-audio-aula'); if(btn) btn.innerHTML='🔊 Ouvir Aula (Podcast)';
 };
 vozFalando=true;
 window.speechSynthesis.speak(utt);
 const btn=$('#btn-audio-aula'); if(btn) btn.innerHTML='⏹ Pausar Áudio';
}
window.falarTexto = falarTexto;

/* ==================== ANOTAÇÕES DO ESTUDANTE ==================== */
function salvarAnotacaoAula(aulaId, texto){
 estado.anotacoes=estado.anotacoes||{};
 estado.anotacoes[aulaId]=texto;
 salvar();
 const tag=$('#status-anotacao');
 if(tag){ tag.textContent='Fichamento salvo ✓'; setTimeout(()=>{ tag.textContent=''; },2000); }
}
window.salvarAnotacaoAula = salvarAnotacaoAula;

/* ==================== ESTATÍSTICAS ==================== */
function estatisticas(){
 garantirTodos();
 const total=estado.tentativas.length;
 const acertos=estado.tentativas.filter(t=>t.ok).length;
 const concl=Object.keys(estado.aulasConcluidas).filter(id=>AULAS[id]).length;
 const minutos=Object.values(estado.minPorDia).reduce((a,b)=>a+b,0);
 const pend=revisoesPendentes().length;
 const hoje=diaNum();
 const previstas=Object.values(estado.cartoes).filter(c=>c.prox>hoje && c.prox<=hoje+7).length;
 return {
   total:total, acertos:acertos, pct:total?Math.round(acertos/total*100):null,
   concl:concl, totalAulas:Object.keys(AULAS).length,
   minutos:Math.round(minutos), pend:pend, previstas:previstas
 };
}

function proximaAula(){
 const ord=Object.keys(AULAS);
 const ult=estado.ultimaAula;
 if(ult && AULAS[ult] && !estado.aulasConcluidas[ult]) return ult;
 return ord.find(id=>!estado.aulasConcluidas[id])||ord[0];
}

/* ==================== MOTOR DO PROFESSOR DIGITAL ==================== */
const CRISE_TERMOS_LISTA=['suicid','me matar','quero morrer','nao quero viver','não quero viver','acabar com a minha vida','automutil','me cortar','me machucar','autolesao'];
const DIAG_TERMOS_LISTA=['tenho depressao','tenho ansiedade','tenho transtorno','eu tenho tdah','sera que eu tenho','diagnostica','diagnostico para mim','meu diagnostico','interprete meu teste','qual remedio','quantos mg'];

const RESPOSTA_CRISE_TXT="Sinto muito que você esteja passando por um momento tão delicado. Como Professor Virtual acadêmico, não tenho autorização para oferecer atendimento psicológico ou emergencial. "
+"Por favor, busque acolhimento humano agora mesmo: Ligue 188 (CVV - Centro de Valorização da Vida, gratuito 24h) ou em caso de risco iminente, ligue 192 (SAMU).";

const RESPOSTA_DIAG_TXT="De acordo com o Código de Ética Profissional do Psicólogo (CFP), avaliações diagnósticas e prescrições terapêuticas exigem formação profissional e acolhimento presencial/remoto por psicólogo com registro ativo no CRP. "
+"Meu papel é exclusivamente didático. Posso explicar como a literatura científica aborda o tema de forma conceitual para fins de estudo acadêmico.";

async function chamarProfessorIA(mensagem, contextoAula){
 const mNorm=mensagem.toLowerCase();
 if(CRISE_TERMOS_LISTA.some(t=>mNorm.includes(t))) return {resposta:RESPOSTA_CRISE_TXT, fontes:['CVV (188)','SAMU (192)']};
 if(DIAG_TERMOS_LISTA.some(t=>mNorm.includes(t))) return {resposta:RESPOSTA_DIAG_TXT, fontes:['Código de Ética Profissional (CFP)']};

 // 1. Tentar conexão com API local (api_server.py)
 if(estado.apiServidor){
   try{
     const res=await fetch(estado.apiServidor.replace(/\/$/,'')+'/professor/chat',{
       method:'POST',headers:{'Content-Type':'application/json'},
       body:JSON.stringify({pergunta:mensagem, aula_id:contextoAula}),
       signal:AbortSignal.timeout(3500)
     });
     if(res.ok){
       const d=await res.json();
       if(d.resposta) return {resposta:d.resposta, fontes:d.fontes||['API PsicoBase']};
     }
   }catch(e){ /* Fallback automático para o motor offline */ }
 }

 // 2. Motor Heurístico/Offline embutido
 for(const [id, a] of Object.entries(AULAS)){
   if(mNorm.includes(a.titulo.toLowerCase()) || (a.objetivos||[]).some(o=>mNorm.includes(o.toLowerCase()))){
     const resumoTxt=(a.resumo||[]).join(' ');
     return {
       resposta:"Olá! Na aula **"+a.titulo+"**, investigamos exatamente essa temática.\n\n"
         +"📌 **Conceito Central:** "+(resumoTxt||a.secoes[0].p[0])+"\n\n"
         +"💡 **Reflexão Socrática:** Como você explicaria a distinção entre a definição popular desse termo e a sua formulação científica?",
       fontes:['Aula: '+a.titulo, a.disciplina]
     };
   }
 }

 return {
   resposta:"Excelente reflexão acadêmica! Para compreendermos esse aspecto na Psicologia, é crucial delimitarmos sob qual matriz epistemológica estamos trabalhando (Comportamental, Cognitiva, Psicanalítica ou Humanista).\n\n"
     +"Sugiro que você explore as aulas correspondentes na aba **Aprender** e consulte os termos fundamentais na **Biblioteca** para estruturar seu fichamento.",
   fontes:['Diretrizes Curriculares Nacionais (DCNs) de Psicologia','Plataforma PsicoBase']
 };
}

/* ==================== VIEWS (DESIGN EDITORIAL) ==================== */

/* View: Bem-Vindo */
function viewBemVindo(){
 const pct=Math.round((obPasso-1)/5*100);
 let corpo='';
 if(obPasso===1){
  corpo='<p style="font-size:1.15rem;font-family:var(--font-serif);color:var(--primaria);line-height:1.7">'
   +'O espaço onde a mente humana é estudada com profundidade, método e acolhimento.</p>'
   +'<div class="card destaque"><p>Sua formação e curiosidade científica guiadas por conteúdos estruturados em 12 eixos temáticos, fichamento de pesquisa, repetição espaçada e tutoria socrática.</p></div>'
   +'<button class="btn" onclick="proximoOnboarding(1)">Iniciar Jornada Intelectual →</button>';
 }else if(obPasso===2){
  corpo='<p>Qual é o seu nível atual de intimidade com a Psicologia?</p>'
   +'<div class="card">'+Object.entries(NIVEIS).map(([k,v])=>'<label class="alt"><input type="radio" name="ob-nivel" value="'+k+'"> <span>'+v+'</span></label>').join('')+'</div>'
   +'<button class="btn" onclick="proximoOnboarding(2)">Continuar →</button>';
 }else if(obPasso===3){
  corpo='<p>Qual é o seu objetivo de estudo primordial?</p>'
   +'<div class="card">'+Object.entries(OBJETIVOS).map(([k,v])=>'<label class="alt"><input type="radio" name="ob-obj" value="'+k+'"> <span>'+v+'</span></label>').join('')+'</div>'
   +'<button class="btn" onclick="proximoOnboarding(3)">Continuar →</button>';
 }else if(obPasso===4){
  corpo='<p>Qual tempo diário você deseja reservar para suas sessões de leitura e foco?</p>'
   +'<div class="card">'+Object.entries(TEMPOS).map(([k,v])=>'<label class="alt"><input type="radio" name="ob-tempo" value="'+k+'"> <span>'+v+'</span></label>').join('')+'</div>'
   +'<button class="btn" onclick="proximoOnboarding(4)">Continuar →</button>';
 }else if(obPasso===5){
  corpo='<p>Como prefere ser chamado(a) durante as tutorias?</p>'
   +'<div class="card"><input id="ob-nome" class="campo" placeholder="Seu nome ou apelido acadêmico" maxlength="40"></div>'
   +'<button class="btn" onclick="proximoOnboarding(5)">Entrar na PsicoBase →</button>';
 }
 return '<div class="barra"><div style="width:'+pct+'%"></div></div>'
  +'<p class="muted">Configuração de Percurso · Passo '+obPasso+' de 5</p>'
  +'<h1>Boas-vindas à PsicoBase</h1>'+corpo;
}

window.proximoOnboarding = function(etapa){
 if(etapa===1){ obPasso=2; render(); return; }
 if(etapa===2){
   const sel=$('input[name="ob-nivel"]:checked');
   if(!sel) return aviso('Escolha uma opção para continuar.');
   obDados.nivel=sel.value; obPasso=3; render(); return;
 }
 if(etapa===3){
   const sel=$('input[name="ob-obj"]:checked');
   if(!sel) return aviso('Escolha seu objetivo.');
   obDados.objetivo=sel.value; obPasso=4; render(); return;
 }
 if(etapa===4){
   const sel=$('input[name="ob-tempo"]:checked');
   if(!sel) return aviso('Escolha sua meta diária de foco.');
   obDados.tempo=sel.value; obPasso=5; render(); return;
 }
 if(etapa===5){
   const apelido=$('#ob-nome').value.trim();
   obDados.apelido=apelido;
   estado.perfil=obDados;
   salvar();
   location.hash='#/inicio';
   render();
 }
};

/* View: Início (Editorial Humanista) */
function viewInicio(){
 const p=estado.perfil||{};
 const st=estatisticas();
 const prox=proximaAula();
 const aulaObj=AULAS[prox]||AULAS['m1-a1'];
 const sauda=new Date().getHours()<12?'Bom dia':(new Date().getHours()<18?'Boa tarde':'Boa noite');
 const nome=p.apelido?', '+esc(p.apelido):'';
 
 return ''
 +'<div style="margin-bottom:28px">'
  +'<h1 style="margin-bottom:4px;font-family:var(--font-serif)">'+sauda+nome+'.</h1>'
  +'<p class="muted" style="font-size:1.1rem;font-family:var(--font-serif);font-style:italic">'
   +'"O espaço onde a mente humana é estudada com profundidade, método e acolhimento."'
  +'</p>'
 +'</div>'
 
 // Card Destaque: Continuar Estudos
 +'<div class="card destaque">'
  +'<div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px">'
   +'<div>'
    +'<span class="tag pendente">Sessão em Andamento</span>'
    +'<h2 style="margin:8px 0;border:none;padding:0">'+esc(aulaObj.titulo)+'</h2>'
    +'<p class="muted" style="margin:0">'+esc(aulaObj.disciplina)+' · Estimado: '+aulaObj.tempo+' min</p>'
   +'</div>'
   +'<a href="#/aula/'+aulaObj.id+'" class="btn">Retomar Fichamento →</a>'
  +'</div>'
 +'</div>'

 // Métricas Táteis
 +'<div class="grid-stats">'
  +'<div class="stat-box"><span class="num">'+st.concl+'/'+st.totalAulas+'</span><span class="rotulo">Aulas Lidas</span></div>'
  +'<div class="stat-box"><span class="num">'+st.pend+'</span><span class="rotulo">Revisões Hoje</span></div>'
  +'<div class="stat-box"><span class="num">'+st.minutos+'m</span><span class="rotulo">Foco Acumulado</span></div>'
  +'<div class="stat-box"><span class="num">'+(st.pct!==null?st.pct+'%':'-')+'</span><span class="rotulo">Retenção</span></div>'
 +'</div>'

 // Rotas de Acesso Rápido
 +'<h2>Acesso Rápido ao Conhecimento</h2>'
 +'<div class="grid">'
  +'<a href="#/professor" class="card" style="display:flex;align-items:center;gap:16px;color:inherit;text-decoration:none">'
   +'<div style="font-size:1.8rem;background:var(--primaria-tint);color:var(--primaria);width:54px;height:54px;border-radius:14px;display:flex;align-items:center;justify-content:center;font-family:var(--font-serif);font-weight:700">Ψ</div>'
   +'<div><strong>Professor Digital</strong><p class="muted" style="margin:2px 0">Tire dúvidas com escuta socrática e casos clínicos</p></div>'
  +'</a>'
  +'<a href="#/revisar" class="card" style="display:flex;align-items:center;gap:16px;color:inherit;text-decoration:none">'
   +'<div style="font-size:1.8rem;background:var(--salvia-tint);color:var(--salvia);width:54px;height:54px;border-radius:14px;display:flex;align-items:center;justify-content:center">📇</div>'
   +'<div><strong>Fichamento & Flashcards</strong><p class="muted" style="margin:2px 0">'+st.pend+' fichas agendadas pelo algoritmo SRS</p></div>'
  +'</a>'
  +'<a href="#/aprender" class="card" style="display:flex;align-items:center;gap:16px;color:inherit;text-decoration:none">'
   +'<div style="font-size:1.8rem;background:var(--secundaria-tint);color:var(--secundaria);width:54px;height:54px;border-radius:14px;display:flex;align-items:center;justify-content:center">📚</div>'
   +'<div><strong>12 Eixos Temáticos</strong><p class="muted" style="margin:2px 0">Trilha curricular completa com 47 aulas</p></div>'
  +'</a>'
  +'<a href="#/biblioteca" class="card" style="display:flex;align-items:center;gap:16px;color:inherit;text-decoration:none">'
   +'<div style="font-size:1.8rem;background:var(--ambar-tint);color:var(--ambar);width:54px;height:54px;border-radius:14px;display:flex;align-items:center;justify-content:center">📖</div>'
   +'<div><strong>Biblioteca & Glossário</strong><p class="muted" style="margin:2px 0">Catálogo de termos e seu caderno pessoal</p></div>'
  +'</a>'
 +'</div>';
}

/* View: Aprender (12 Eixos com Selos Conceituais) */
function viewAprender(){
 const modulosHtml=MODULOS.map(m=>{
  const aulas=Object.entries(AULAS).filter(([id,a])=>a.modulo===m.id);
  const feitas=aulas.filter(([id])=>estado.aulasConcluidas[id]).length;
  const pct=aulas.length?Math.round((feitas/aulas.length)*100):0;
  return ''
  +'<div class="modulo-card" data-mod="'+m.id+'">'
   +'<div style="display:flex;justify-content:space-between;align-items:flex-start">'
    +'<div>'
     +'<span class="tag">Eixo '+m.id+'</span>'
     +'<h2 style="margin:8px 0;border:none;padding:0"><a href="#/modulo/'+m.id+'">'+esc(m.titulo)+'</a></h2>'
     +'<p class="muted" style="margin-bottom:8px">'+esc(m.desc)+'</p>'
    +'</div>'
    +'<span class="tag '+(pct===100?'concluido':'')+'">'+pct+'%</span>'
   +'</div>'
   +'<div class="barra"><div style="width:'+pct+'%"></div></div>'
   +'<div style="display:flex;justify-content:space-between;align-items:center;margin-top:12px">'
    +'<span class="muted" style="font-size:0.86rem">'+aulas.length+' aulas · '+feitas+' concluídas</span>'
    +'<a href="#/modulo/'+m.id+'" class="btn sec sm">Abrir Eixo →</a>'
   +'</div>'
  +'</div>';
 }).join('');

 return ''
 +'<h1>Eixos Curriculares de Psicologia</h1>'
 +'<p class="muted">Os 12 módulos estruturantes da formação acadêmica: da epistemologia filosófica à prática biopsicossocial e ética profissional.</p>'
 +'<div class="grid">'+modulosHtml+'</div>';
}

/* View: Módulo */
function viewModulo(n){
 const m=MODULOS.find(x=>String(x.id)===String(n));
 if(!m) return '<h1>Eixo não encontrado</h1><p><a href="#/aprender">Voltar</a></p>';
 const aulas=Object.entries(AULAS).filter(([id,a])=>a.modulo===m.id);
 
 const lista=aulas.map(([id,a],i)=>{
  const conc=!!estado.aulasConcluidas[id];
  return ''
  +'<div class="card" style="display:flex;align-items:center;justify-content:space-between;margin:10px 0">'
   +'<div>'
    +'<strong style="font-family:var(--font-serif);font-size:1.1rem">'+(i+1)+'. <a href="#/aula/'+id+'">'+esc(a.titulo)+'</a></strong>'
    +'<p class="muted" style="margin:3px 0;font-size:0.86rem">'+esc(a.nivel)+' · tempo estimado: '+a.tempo+' min</p>'
   +'</div>'
   +(conc?'<span class="tag concluido">✓ Concluída</span>':'<a href="#/aula/'+id+'" class="btn sm sec">Fichar Aula</a>')
  +'</div>';
 }).join('');

 return ''
 +'<p class="muted"><a href="#/aprender">← Todos os Eixos</a></p>'
 +'<h1>Eixo '+m.id+': '+esc(m.titulo)+'</h1>'
 +'<p class="muted">'+esc(m.desc)+'</p>'
 +'<div style="margin:24px 0">'+lista+'</div>';
}

/* View: Aula (com Leitor Zen e Foco Ergonômico) */
function viewAula(id){
 const a=AULAS[id];
 if(!a) return '<h1>Aula não encontrada</h1><p><a href="#/aprender">Voltar</a></p>';
 iniciarSessao(id);
 estado.ultimaAula=id;
 estado.abertas=estado.abertas||{}; estado.abertas[id]=true;
 garantirCartoes(id);
 salvar();
 
 const mod=MODULOS.find(m=>m.id===a.modulo);
 const concl=!!estado.aulasConcluidas[id];
 const textoAudio = (a.secoes||[]).map(s=>s.t+'. '+(s.p||[]).join(' ')).join(' ');
 const anotacaoAtual = (estado.anotacoes&&estado.anotacoes[id])||'';

 const secoesHtml=(a.secoes||[]).map(s=>''
  +'<h2>'+esc(s.t)+'</h2>'
  +(s.p||[]).map(p=>'<p>'+esc(p)+'</p>').join('')
  +(s.pausa?'<div class="card" style="border-left:4px solid var(--secundaria);background:var(--bg-fichamento)">'
    +'<strong style="font-family:var(--font-serif);color:var(--primaria)">Pare e Reflita:</strong>'
    +'<p style="margin:6px 0">'+esc(s.pausa.p)+'</p>'
    +'<details style="margin-top:8px"><summary style="cursor:pointer;font-weight:600;color:var(--primaria)">Orientação reflexiva do professor</summary><p class="muted" style="margin-top:6px">'+esc(s.pausa.r)+'</p></details>'
   +'</div>':'')
 ).join('');

 const quizHtml=(a.questoes||[]).map((q,i)=>''
  +'<fieldset class="card" style="margin:18px 0;border:1px solid var(--borda-suave)">'
   +'<legend style="font-weight:700;font-family:var(--font-serif);padding:0 8px">'+(i+1)+'. '+esc(q.enunciado)+'</legend>'
   +(q.alts||[]).map((t,j)=>'<label class="alt"><input type="radio" name="'+q.id+'" value="'+j+'"> <span>'+LETRAS[j]+') '+esc(t)+'</span></label>').join('')
  +'</fieldset>'
 ).join('');

 return ''
 +'<div style="display:flex;justify-content:space-between;align-items:center">'
  +'<p class="muted"><a href="#/modulo/'+a.modulo+'">← '+(mod?esc(mod.titulo):'Eixo')+'</a></p>'
  +'<button class="btn-header" onclick="alternarModoZen()" title="Alternar Modo Leitura Zen">🌿 Modo Zen</button>'
 +'</div>'
 
 +'<div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;margin-top:6px">'
  +'<div>'
   +'<h1 style="margin-bottom:4px">'+esc(a.titulo)+'</h1>'
   +'<p class="muted">'+esc(a.disciplina)+' · '+esc(a.nivel)+' · Leitura estimada: '+a.tempo+' min</p>'
  +'</div>'
  +(concl?'<span class="tag concluido">✓ Aula Concluída</span>':'<button class="btn sm" onclick="marcarConcluida(\''+id+'\')">Concluir Aula</button>')
 +'</div>'
 
 // Barra de Ferramentas Ergonômica
 +'<div style="display:flex;gap:10px;flex-wrap:wrap;margin:14px 0">'
  +'<button id="btn-audio-aula" class="btn-header" onclick="falarTexto(\''+esc(textoAudio).replace(/'/g,"\\'")+'\')">🔊 Ouvir Aula (Podcast)</button>'
  +'<a href="#/professor" class="btn-header">Ψ Debater esta Aula com o Tutor</a>'
 +'</div>'

 // Caixa de Objetivos Conceituais
 +'<div class="card destaque">'
  +'<strong style="font-family:var(--font-serif);font-size:1.05rem">Objetivos de Compreensão Epistemológica:</strong>'
  +'<ul style="margin:8px 0 0;padding-left:22px">'+(a.objetivos||[]).map(o=>'<li>'+esc(o)+'</li>').join('')+'</ul>'
 +'</div>'
 
 +secoesHtml
 
 // Caderno de Fichamento
 +'<div class="card" style="background:var(--bg-fichamento);border-left:4px solid var(--ambar)">'
  +'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">'
   +'<strong style="font-family:var(--font-serif);font-size:1.1rem">📝 Caderno de Fichamento da Aula</strong>'
   +'<span id="status-anotacao" class="muted" style="font-size:0.82rem"></span>'
  +'</div>'
  +'<p class="muted" style="margin-top:0;font-size:0.9rem">Registre seus resumos analíticos, pontes entre teorias e impressões críticas. Salvo automaticamente no seu navegador.</p>'
  +'<textarea class="campo" style="min-height:120px" placeholder="Escreva seu fichamento acadêmico aqui..." oninput="salvarAnotacaoAula(\''+id+'\', this.value)">'+esc(anotacaoAtual)+'</textarea>'
 +'</div>'
 
 // Questões de Fixação
 +'<h2>Avaliação Formativa</h2>'
 +'<form id="form-quiz" onsubmit="event.preventDefault(); submeterQuiz(\''+id+'\', this)">'
  +quizHtml
  +'<button type="submit" class="btn">Submeter Respostas</button>'
 +'</form>'
 +'<div id="resultado-quiz"></div>';
}

function corrigirAula(aulaId, form){
 const a = AULAS[aulaId];
 if(!a) return { acertos: 0, total: 0, res: [] };
 let acertos = 0;
 const res = [];
 (a.questoes || []).forEach(q => {
  const v = form.querySelector('input[name="'+q.id+'"]:checked');
  const marcada = v ? Number(v.value) : -1;
  const ok = (marcada === q.correta);
  if(ok) acertos++;
  res.push({ q: q, marcada: marcada, ok: ok });
  if(!Array.isArray(estado.tentativas)) estado.tentativas = [];
  estado.tentativas.push({ d: dataISO(), aula: aulaId, q: q.id, ok: ok, marcada: marcada });
 });
 salvar();
 return { acertos: acertos, total: (a.questoes || []).length, res: res };
}
window.corrigirAula = corrigirAula;

function mostrarResultado(r){
 if(!r || !r.total) return;
 const pct = Math.round((r.acertos / r.total) * 100);
 const linhas = (r.res || []).map(x => {
  const cls = x.ok ? 'ok' : 'erro';
  const rotulo = x.ok ? '✓ Resposta Correta' : '✕ Resposta Incorreta';
  const detalhe = x.ok ? '' : '<p style="margin:6px 0;font-size:0.92rem"><strong>Sua resposta:</strong> ' + (x.marcada >= 0 ? LETRAS[x.marcada] + ') ' + esc(x.q.alts[x.marcada]) : '<em class="muted">Não respondida</em>') + '.<br><strong style="color:var(--salvia)">Resposta esperada:</strong> ' + LETRAS[x.q.correta] + ') ' + esc(x.q.alts[x.q.correta]) + '.</p>';
  return '<div class="res ' + cls + '"><p style="margin:0 0 6px 0"><strong>' + rotulo + '.</strong> ' + esc(x.q.enunciado) + '</p>' + detalhe + '<p class="muted" style="margin:6px 0 0;font-size:0.88rem;border-top:1px dashed var(--borda-suave);padding-top:6px"><em>Fundamentação epistemológica:</em> ' + esc(x.q.justificativa) + '</p></div>';
 }).join('');
 
 const dica = (r.acertos === r.total) 
   ? 'Excelente domínio conceitual! Continue para a próxima aula ou consolide o conteúdo nas fichas de repetição espaçada.' 
   : 'Recomendamos reler os tópicos reflexivos associados aos pontos assinalados e praticar os flashcards desta aula.';

 const container = document.getElementById('resultado-quiz');
 if(container){
   container.innerHTML = '<div class="card destaque" style="margin-top:20px;border-left:5px solid ' + (pct >= 70 ? 'var(--salvia)' : 'var(--terracota)') + '">'
     + '<strong style="font-family:var(--font-serif);font-size:1.2rem;color:' + (pct >= 70 ? 'var(--salvia)' : 'var(--terracota)') + '">Desempenho Formativo: ' + r.acertos + ' de ' + r.total + ' (' + pct + '%)</strong>'
     + '<p style="margin:8px 0 0">' + dica + '</p>'
     + '</div>' + linhas;
   container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
 }
}
window.mostrarResultado = mostrarResultado;

window.marcarConcluida = function(id){
 estado.aulasConcluidas[id]=true;
 salvar();
 aviso('Aula concluída com sucesso! Fichamento salvo. 🌿');
 render();
};

window.submeterQuiz = function(aulaId, form){
 const res = corrigirAula(aulaId, form);
 mostrarResultado(res);
 if(res.acertos >= Math.ceil(res.total * 0.7)){
   estado.aulasConcluidas[aulaId]=true;
   salvar();
   aviso('Aula concluída com excelente aproveitamento! 🌿');
 } else {
   aviso('Quiz submetido. Revise os pontos indicados para fixar os conceitos. 📖');
 }
};

/* View: Revisar (Fichas 3D de Repetição Espaçada) */
function viewRevisar(){
 garantirTodos();
 if(filaRev===null){ filaRev=revisoesPendentes(); revIndice=0; revVerso=false; }
 
 if(!filaRev.length){
  return '<h1>Fichamento de Repetição Espaçada</h1>'
   +'<div class="card destaque" style="text-align:center;padding:48px 24px">'
    +'<div style="font-size:3.5rem;margin-bottom:14px">🌿</div>'
    +'<h2>Mente Clara: Tudo em Dia</h2>'
    +'<p class="muted">Você revisou todas as fichas programadas pelo algoritmo de repetição para hoje.</p>'
    +'<a href="#/aprender" class="btn">Explorar Novas Aulas</a>'
   +'</div>';
 }

 const cardId=filaRev[revIndice]||filaRev[0];
 const c=achaCartao(cardId);
 if(!c) return '<h1>Erro ao ler ficha</h1>';

 return ''
 +'<h1>Repetição Espaçada (SRS)</h1>'
 +'<p class="muted">Ficha '+(revIndice+1)+' de '+filaRev.length+' pendente(s) · <span class="tag">'+esc(c.aula)+'</span></p>'
 +'<div class="flashcard-wrap" onclick="virarCard()">'
  +'<div id="flashcard-box" class="flashcard '+(revVerso?'virado':'')+'">'
   +'<div class="flashcard-lado">'
    +'<p class="muted" style="font-size:0.8rem;text-transform:uppercase;letter-spacing:0.06em">FRENTE · CLIQUE OU ESPAÇO PARA VIRAR</p>'
    +'<h2 style="margin:22px 0;font-size:1.5rem;font-family:var(--font-serif)">'+esc(c.frente)+'</h2>'
    +'<span class="btn sec sm">Ver Resposta no Verso</span>'
   +'</div>'
   +'<div class="flashcard-verso">'
    +'<p class="muted" style="font-size:0.8rem;text-transform:uppercase;letter-spacing:0.06em">VERSO · RESPOSTA CONCEITUAL</p>'
    +'<p style="font-size:1.2rem;margin:18px 0;font-family:var(--font-serif);line-height:1.7">'+esc(c.verso)+'</p>'
   +'</div>'
  +'</div>'
 +'</div>'
 
 +'<div style="display:flex;justify-content:center;gap:12px;margin-top:24px;flex-wrap:wrap">'
  +'<button class="btn sm" style="background:var(--terracota);border-color:var(--terracota)" onclick="avaliarCard(\''+c.id+'\', \'dificil\')">1. Difícil (1 dia)</button>'
  +'<button class="btn sm" style="background:var(--ambar);border-color:var(--ambar);color:#fff" onclick="avaliarCard(\''+c.id+'\', \'bom\')">2. Bom (3 dias)</button>'
  +'<button class="btn sm" style="background:var(--salvia);border-color:var(--salvia)" onclick="avaliarCard(\''+c.id+'\', \'facil\')">3. Fácil (7 dias)</button>'
 +'</div>';
}

window.virarCard = function(){
 revVerso=!revVerso;
 const b=$('#flashcard-box'); if(b) b.classList.toggle('virado', revVerso);
};

window.avaliarCard = function(id, nivel){
 responderCartao(id, nivel);
 revVerso=false;
 revIndice++;
 if(revIndice>=filaRev.length){
   filaRev=[];
 }
 render();
};

/* View: Professor Digital (Escuta Socrática & Apoio Ético) */
let historicoChat = [
 {tipo:'prof', texto:'Olá! Sou seu **Professor Digital de Psicologia**. Minha proposta pedagógica é guiá-lo(a) através do método socrático, articulando os 12 eixos temáticos e as diretrizes éticas da nossa ciência.\n\nQual conceito, autor ou dilema você gostaria de investigar hoje?'}
];

function viewProfessor(){
 const msgsHtml=historicoChat.map(m=>''
  +'<div class="chat-msg '+m.tipo+'">'
   +'<div class="chat-avatar">'+(m.tipo==='prof'?'Ψ':'👤')+'</div>'
   +'<div class="chat-bubble">'
    +m.texto.replace(/\*\*(.*?)\*\*/g,'<strong>$1</strong>').replace(/\n/g,'<br>')
   +'</div>'
  +'</div>'
 ).join('');

 return ''
 +'<h1>Professor Digital de Psicologia</h1>'
 +'<p class="muted">Tutoria e debate acadêmico baseado no currículo científico e no Código de Ética do Psicólogo (CFP).</p>'
 
 // Sugestões Epistemológicas
 +'<div style="display:flex;gap:10px;overflow-x:auto;padding-bottom:8px;margin-bottom:14px">'
  +'<button class="btn sec sm" onclick="perguntarDireto(\'O que é reforço negativo e como difere de punição?\')">💡 Reforço Negativo vs Punição</button>'
  +'<button class="btn sec sm" onclick="perguntarDireto(\'Como Freud estruturou o aparelho psíquico?\')">🧠 1ª e 2ª Tópicas de Freud</button>'
  +'<button class="btn sec sm" onclick="perguntarDireto(\'O que é o modelo biopsicossocial?\')">🌿 Modelo Biopsicossocial</button>'
  +'<button class="btn sec sm" onclick="perguntarDireto(\'Quais os limites éticos do sigilo no CFP?\')">⚖️ Ética e Sigilo (CFP)</button>'
 +'</div>'

 +'<div class="card" style="padding:20px">'
  +'<div id="chat-box" class="chat-container">'+msgsHtml+'</div>'
  +'<form id="chat-form" onsubmit="event.preventDefault(); enviarMensagemChat(this)">'
   +'<div style="display:flex;gap:12px">'
    +'<input id="chat-input" class="campo" placeholder="Pergunte sobre conceitos, autores, controvérsias ou ética..." autocomplete="off">'
    +'<button type="submit" class="btn" style="flex-shrink:0">Enviar</button>'
   +'</div>'
  +'</form>'
 +'</div>'

 // Banner Ético Permanente com CVV 188
 +'<div class="banner-etico">'
  +'<span style="font-size:1.3rem">⚖️</span>'
  +'<div>'
   +'<strong>Compromisso Ético & Cuidado:</strong> Este tutor tem finalidade exclusivamente formativa e acadêmica. Não realiza diagnósticos ou consultas clínicas. Se você ou alguém próximo estiver em sofrimento emocional intenso, ligue para o <strong>CVV (188)</strong>, serviço gratuito 24 horas, ou acesse <a href="https://cvv.org.br" target="_blank" rel="noopener">cvv.org.br</a>.'
  +'</div>'
 +'</div>';
}

window.perguntarDireto = function(texto){
 const inp=$('#chat-input');
 if(inp){ inp.value=texto; enviarMensagemChat($('#chat-form')); }
};

window.enviarMensagemChat = async function(form){
 const inp=$('#chat-input');
 const txt=inp.value.trim();
 if(!txt) return;
 inp.value='';
 
 historicoChat.push({tipo:'aluno', texto:txt});
 render();
 
 const box=$('#chat-box'); if(box) box.scrollTop=box.scrollHeight;
 
 const resp = await chamarProfessorIA(txt, estado.ultimaAula);
 historicoChat.push({tipo:'prof', texto:resp.resposta});
 render();
 
 const box2=$('#chat-box'); if(box2) box2.scrollTop=box2.scrollHeight;
};

/* View: Biblioteca & Glossário */
function viewBiblioteca(){
 const glosList = GLOSSARIO.concat(typeof GLOSSARIO_CAP!=='undefined'?GLOSSARIO_CAP:[]);

 return ''
 +'<h1>Biblioteca & Glossário</h1>'
 +'<p class="muted">Dicionário epistemológico com termos técnicos definidos sob o prisma pedagógico e acadêmico.</p>'
 
 +'<div style="margin:20px 0">'
  +'<input id="busca-biblio" class="campo" type="search" placeholder="Buscar termo conceitual no glossário..." oninput="filtrarBiblioteca(this.value)">'
 +'</div>'
 
 +'<div id="lista-biblio">'
  +glosList.slice(0, 30).map(g=>''
   +'<div class="card" style="margin:12px 0">'
    +'<div style="display:flex;justify-content:space-between;align-items:center">'
     +'<h3 style="margin:0;color:var(--primaria);font-family:var(--font-serif)">'+esc(g.termo)+'</h3>'
     +(g.aula?'<a href="#/aula/'+g.aula+'" class="tag">Aula Relacionada</a>':'')
    +'</div>'
    +'<p style="margin:8px 0"><strong>Definição Semântica:</strong> '+esc(g.simples)+'</p>'
    +(g.academico?'<p class="muted" style="margin:6px 0"><strong>Rigor Acadêmico:</strong> '+esc(g.academico)+'</p>':'')
    +(g.exemplo?'<p class="muted" style="margin:6px 0"><strong>Exemplo Clínico/Pesquisa:</strong> <em>'+esc(g.exemplo)+'</em></p>':'')
   +'</div>'
  ).join('')
 +'</div>';
}

window.filtrarBiblioteca = function(q){
 const norm = q.toLowerCase().trim();
 const glosList = GLOSSARIO.concat(typeof GLOSSARIO_CAP!=='undefined'?GLOSSARIO_CAP:[]);
 const filtrados = glosList.filter(g => g.termo.toLowerCase().includes(norm) || (g.simples||'').toLowerCase().includes(norm));
 const el=$('#lista-biblio');
 if(!el) return;
 if(!filtrados.length){ el.innerHTML='<p class="muted">Nenhum termo encontrado para "'+esc(q)+'".</p>'; return; }
 el.innerHTML = filtrados.slice(0, 30).map(g=>''
  +'<div class="card" style="margin:12px 0">'
   +'<div style="display:flex;justify-content:space-between;align-items:center">'
    +'<h3 style="margin:0;color:var(--primaria);font-family:var(--font-serif)">'+esc(g.termo)+'</h3>'
    +(g.aula?'<a href="#/aula/'+g.aula+'" class="tag">Aula Relacionada</a>':'')
   +'</div>'
   +'<p style="margin:8px 0"><strong>Definição Semântica:</strong> '+esc(g.simples)+'</p>'
   +(g.academico?'<p class="muted" style="margin:6px 0"><strong>Rigor Acadêmico:</strong> '+esc(g.academico)+'</p>':'')
  +'</div>'
 ).join('');
};

/* View: Perfil */
function viewPerfil(){
 const p=estado.perfil||{};
 return ''
 +'<h1>Perfil & Configurações</h1>'
 +'<div class="card">'
  +'<h2>Identidade Acadêmica</h2>'
  +'<label>Nome ou Apelido:<br><input id="perf-nome" class="campo" value="'+esc(p.apelido||'')+'"></label>'
  +'<div style="margin-top:16px">'
   +'<button class="btn sm" onclick="salvarPerfil()">Salvar Perfil</button>'
  +'</div>'
 +'</div>'
 
 +'<div class="card">'
  +'<h2>Conexão com a API do Professor Digital</h2>'
  +'<p class="muted">Configure a URL do servidor local (api_server.py) ou chave de IA.</p>'
  +'<label>Endpoint da API REST:<br><input id="perf-api" class="campo" value="'+esc(estado.apiServidor||'http://localhost:8000/api')+'"></label>'
  +'<div style="margin-top:16px">'
   +'<button class="btn sm" onclick="salvarConfigAPI()">Salvar Endpoint</button>'
  +'</div>'
 +'</div>'
 
 +'<div class="card">'
  +'<h2>Preservação e Portabilidade de Dados</h2>'
  +'<p class="muted">Seus dados e fichamentos residem exclusivamente na memória deste navegador.</p>'
  +'<button class="btn sec sm" onclick="exportarBackup()">📥 Baixar Backup (JSON)</button>'
  +'<button class="btn sec sm" onclick="$(\'#file-import\').click()">📤 Restaurar Backup</button>'
  +'<input type="file" id="file-import" style="display:none" onchange="importarBackup(event)" accept=".json">'
 +'</div>';
}

window.salvarPerfil = function(){
 estado.perfil=estado.perfil||{};
 estado.perfil.apelido=$('#perf-nome').value.trim();
 salvar();
 aviso('Perfil acadêmico atualizado com sucesso! 🌿');
};

window.salvarConfigAPI = function(){
 estado.apiServidor=$('#perf-api').value.trim();
 salvar();
 aviso('Configurações da API salvas!');
};

window.exportarBackup = function(){
 const blob=new Blob([JSON.stringify(estado, null, 2)], {type:'application/json'});
 const url=URL.createObjectURL(blob);
 const a=document.createElement('a'); a.href=url; a.download='psicobase-academico-'+dataISO()+'.json'; a.click();
 URL.revokeObjectURL(url);
};

window.importarBackup = function(e){
 const arq=e.target.files[0]; if(!arq) return;
 const r=new FileReader();
 r.onload=()=>{
   try{
     const d=JSON.parse(r.result);
     if(d && typeof d==='object'){
       estado=Object.assign(estadoPadrao(), d);
       salvar();
       aviso('Backup acadêmico restaurado com sucesso!');
       render();
     }
   }catch(err){ aviso('Arquivo de backup inválido.'); }
 };
 r.readAsText(arq);
};

/* ==================== BUSCA MODAL (CTRL+K) ==================== */
function abrirBuscaModal(){
 const m=$('#modal-busca'); if(m){ m.style.display='flex'; $('#input-busca-modal').focus(); }
}
window.abrirBuscaModal = abrirBuscaModal;

function fecharBuscaModal(){
 const m=$('#modal-busca'); if(m) m.style.display='none';
}
window.fecharBuscaModal = fecharBuscaModal;

window.addEventListener('keydown', e=>{
 if((e.ctrlKey||e.metaKey)&&e.key==='k'){ e.preventDefault(); abrirBuscaModal(); }
 if(e.key==='Escape') fecharBuscaModal();
});

function executarBuscaModal(q){
 const norm=q.toLowerCase().trim();
 const out=$('#modal-busca-resultados');
 if(!norm){ out.innerHTML='<p class="muted">Digite para pesquisar em aulas e no glossário.</p>'; return; }
 
 const aulasMatch = Object.entries(AULAS).filter(([id,a])=>a.titulo.toLowerCase().includes(norm));
 const termosMatch = GLOSSARIO.filter(g=>g.termo.toLowerCase().includes(norm));
 
 let h='';
 if(aulasMatch.length){
   h+='<strong style="font-family:var(--font-serif)">Aulas Encontradas:</strong><ul style="padding-left:22px;margin-top:6px">';
   aulasMatch.slice(0,5).forEach(([id,a])=>{
     h+='<li><a href="#/aula/'+id+'" onclick="fecharBuscaModal()">'+esc(a.titulo)+'</a> <span class="muted">('+esc(a.disciplina)+')</span></li>';
   });
   h+='</ul>';
 }
 if(termosMatch.length){
   h+='<strong style="font-family:var(--font-serif);margin-top:14px;display:block">Termos no Glossário:</strong><ul style="padding-left:22px;margin-top:6px">';
   termosMatch.slice(0,5).forEach(g=>{
     h+='<li><strong>'+esc(g.termo)+':</strong> '+esc(g.simples)+'</li>';
   });
   h+='</ul>';
 }
 if(!aulasMatch.length && !termosMatch.length){
   h='<p class="muted">Nenhum resultado para "'+esc(q)+'".</p>';
 }
 out.innerHTML=h;
}
window.executarBuscaModal = executarBuscaModal;

/* ==================== ROTEADOR ==================== */
function render(){
 encerrarSessao();
 const partes=rota().split('/').filter(Boolean);
 const r=partes[0]||'inicio';
 
 if(!estado.perfil && r!=='bem-vindo'){ location.hash='#/bem-vindo'; return; }
 if(estado.perfil && r==='bem-vindo'){ location.hash='#/inicio'; return; }
 if(r!=='revisar'){ filaRev=null; }
 
 let html='';
 switch(r){
  case 'bem-vindo': html=viewBemVindo(); break;
  case 'inicio': html=viewInicio(); break;
  case 'aprender': html=viewAprender(); break;
  case 'modulo': html=viewModulo(partes[1]); break;
  case 'aula': html=viewAula(partes[1]); break;
  case 'revisar': html=viewRevisar(); break;
  case 'professor': html=viewProfessor(); break;
  case 'biblioteca': html=viewBiblioteca(); break;
  case 'perfil': html=viewPerfil(); break;
  default: html='<h1>Página não encontrada</h1><p><a href="#/inicio">Voltar ao início</a></p>';
 }
 app.innerHTML=html;
 
 const showNav=estado.perfil && r!=='bem-vindo';
 nav.hidden=!showNav;
 header.hidden=!showNav;
 
 document.querySelectorAll('nav.inferior a').forEach(a=>{
  const ativo=a.dataset.nav===r || ((r==='modulo'||r==='aula')&&a.dataset.nav==='aprender');
  if(ativo) a.setAttribute('aria-current','page'); else a.removeAttribute('aria-current');
 });
 
 document.title=(r==='inicio'||!estado.perfil?'PsicoBase · Acolhimento e Rigor na Psicologia':'PsicoBase · '+r.toUpperCase());
 window.scrollTo(0, 0);
}

window.addEventListener('hashchange', render);

/* ==================== INICIALIZAÇÃO ==================== */
aplicarVisual();
render();

})();
</script>
</body>
</html>
"""

# Salva index.html no projeto
with open(r"c:\Users\MatheusRochaLopes\Desktop\PsycoBase\index.html", "w", encoding="utf-8") as f:
    f.write(novo_html)

# Salva PsicoBase.html no projeto para compatibilidade
with open(r"c:\Users\MatheusRochaLopes\Desktop\PsycoBase\PsicoBase.html", "w", encoding="utf-8") as f:
    f.write(novo_html)

# Atualiza também o arquivo em Downloads
try:
    with open(r"c:\Users\MatheusRochaLopes\Downloads\PsicoBase (2).html", "w", encoding="utf-8") as f:
        f.write(novo_html)
    print("Atualizado c:\\Users\\MatheusRochaLopes\\Downloads\\PsicoBase (2).html")
except Exception as e:
    print("Aviso ao salvar em downloads:", e)

print("Build com Design Editorial Humanista concluído com sucesso!")
print("Tamanho do index.html gerado:", len(novo_html), "caracteres")
