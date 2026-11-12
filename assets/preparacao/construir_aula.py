"""Gera o material do professor de uma aula.

Uso, na pasta da turma: python -B preparacao/construir_aula.py m3_a1
Fonte única: preparacao/aulas/<id>.py (META, SLIDES, PARTE2, PLANO).
Saídas em M<m>/aula-<n>/: slides-gamma.md, gamma-colar.md, roteiro.md, plano.md, figuras/ e figuras.html.
Sai com código 1 se a fonte violar as regras do deck (tempo total, título, nós, rótulo que não cabe).
"""

import importlib
import sys
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAIZ = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "aulas"))

import figuras  # noqa: E402
from turma import AULAS, CASO, CASO_KIT, CASO_PASTA  # noqa: E402

LIMITE_TITULO = 60
LIMITE_NOS = 6
CAMPOS = ("bloco", "min", "titulo", "lede", "fala", "ancora", "conducao")
LEGENDA = ("Caixa cinza: etapa", "Tracejada: feita pelo modelo", "Borda verde: decisão humana ou controle",
           "Azul cheia: ponto de chegada", "Losango: decisão")

INSTRUCOES_GAMMA = (
    "Mantenha o texto exatamente como está, em português; não resuma nem acrescente frases. "
    "Cada bloco separado por --- é um card. O título de cada card é uma frase curta e não deve ser reescrito. "
    "Quando o card tiver uma lista numerada de etapas, desenhe um diagrama de processo com uma caixa por etapa, "
    "na ordem, ligadas por setas. Quando tiver ramos Sim e Não, use um layout de colunas, uma por ramo. "
    "Sem imagens geradas e sem ícones decorativos. Tema claro, fonte grande, pouco texto por card, alto contraste."
)


def hm(t):
    return f"{t // 60:02d}h{t % 60:02d}"


def modulos(aulas):
    """["m3_a1", "m4_a2"] -> ["M3", "M4"], na ordem."""
    return list(dict.fromkeys(a.split("_")[0].upper() for a in aulas))


def juntar(itens):
    return itens[0] if len(itens) == 1 else ", ".join(itens[:-1]) + " e " + itens[-1]


def carregar(ident):
    fonte = importlib.import_module(ident)
    return fonte, fonte.META, fonte.SLIDES


def com_horarios(meta, slides):
    h, m = map(int, meta["inicio"].split(":"))
    t = h * 60 + m
    for s in slides:
        s["ini"], s["fim"] = t, t + s["min"]
        t += s["min"]


def validar(meta, slides):
    erros = []
    total = sum(s["min"] for s in slides)
    if total != meta["duracao"]:
        erros.append(f"tempo total {total}min, esperado {meta['duracao']}min")
    for n, s in enumerate(slides, 1):
        faltam = [c for c in CAMPOS if not s.get(c)]
        if faltam:
            erros.append(f"slide {n}: faltam {', '.join(faltam)}")
        if len(s.get("titulo", "")) > LIMITE_TITULO:
            erros.append(f"slide {n}: título com {len(s['titulo'])} caracteres (máximo {LIMITE_TITULO})")
        fluxo = s.get("fluxo")
        if not fluxo and not s.get("sem_fluxo"):
            erros.append(f"slide {n}: slide de conteúdo sem fluxograma")
        if not fluxo:
            continue
        if not fluxo.get("descricao"):
            erros.append(f"slide {n}: fluxograma sem descrição textual")
        nos = figuras.contar_nos(fluxo) if "forma" in fluxo else len(fluxo.get("nos", []))
        if nos > LIMITE_NOS:
            erros.append(f"slide {n}: {nos} nós no fluxograma (máximo {LIMITE_NOS})")
        if "forma" in fluxo:
            erros += [f"slide {n}: {a}" for a in figuras.desenhar(fluxo, f"m{n}")[1]]
    return erros


def tela_md(linhas):
    out = []
    for linha in linhas:
        if not (linha.startswith("- ") and out and out[-1].startswith("- ")):
            out.append("")
        out.append(linha)
    return out


def momentos(slides):
    out = []
    for n, s in enumerate(slides, 1):
        if out and out[-1]["bloco"] == s["bloco"]:
            out[-1].update(fim=s["fim"], ate=n)
            out[-1]["min"] += s["min"]
        else:
            out.append(dict(bloco=s["bloco"], ini=s["ini"], fim=s["fim"], de=n, ate=n, min=s["min"]))
    return out


def com_figura(slides):
    return [(n, s) for n, s in enumerate(slides, 1) if "forma" in s.get("fluxo", {})]


def cabecalho(meta, slides):
    return (f"**{meta['curso']} · {meta['modulo']}.** {meta['aula']} · {meta['data']}, {hm(slides[0]['ini'])}–"
            f"{hm(slides[-1]['fim'])} · {meta['duracao']}min · {meta['docente']}.")


def prancha(meta, slides):
    secoes = []
    for n, s in com_figura(slides):
        svg, _ = figuras.desenhar(s["fluxo"], f"m{n}")
        secoes.append(f'<section><p class="k">Slide {n} · {escape(s.get("kicker", s["bloco"]))}</p>'
                      f'<h2>{escape(s["titulo"])}</h2><p class="lede">{escape(s["lede"])}</p>'
                      f'<figure>{svg}</figure><p class="desc">{escape(s["fluxo"]["descricao"])}</p></section>')
    return (
        '<!doctype html>\n<html lang="pt-BR"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>Figuras · {escape(meta["aula"])}</title><style>'
        "body{margin:0;padding:24px 16px;background:#EEF1F6;color:#1B2333;font-family:'Segoe UI',Arial,sans-serif}"
        "main{max-width:1320px;margin:0 auto}section{background:#fff;border-radius:16px;padding:20px 24px;margin:0 0 24px}"
        "h1{font-size:24px}h2{font-size:22px;margin:4px 0}.k{color:#5B6B8C;margin:0;font-size:14px}"
        ".lede{margin:4px 0 12px}figure{margin:0}figure svg{width:100%;height:auto;display:block}"
        ".desc{color:#4A5568;font-size:14px}.leg span{display:inline-block;margin-right:18px}"
        "</style></head><body><main>"
        f'<h1>Figuras · {escape(meta["aula"])} · {escape(meta["titulo"])}</h1>'
        '<p class="leg">' + "".join(f"<span>{x}</span>" for x in LEGENDA) + "</p>"
        + "".join(secoes) + "</main></body></html>\n"
    )


def slides_gamma(meta, slides):
    figs = com_figura(slides)
    o = [f"# Slides — {meta['aula']} · {meta['titulo']}", "", cabecalho(meta, slides), "",
         "Texto de referência do deck: o que aparece em cada slide, a descrição de cada fluxograma e a nota de condução. "
         "A fala completa está no [roteiro](roteiro.md); o texto para colar no Gamma, em [gamma-colar.md](gamma-colar.md). "
         f"Os arquivos são gerados por `preparacao/construir_aula.py`; editar a fonte `preparacao/aulas/{meta['id']}.py`, "
         "nunca estes arquivos.", "",
         "## Como montar no Gamma", "",
         "1. Em gamma.app, criar com IA e escolher a opção de colar texto.",
         "2. Colar o conteúdo inteiro de `gamma-colar.md`. Cada `---` separa um card; se o Gamma oferecer a opção de separar card a card, escolher essa.",
         "3. Modo de texto: preservar. Imagens: nenhuma.",
         "4. No campo de instruções adicionais, colar:", "",
         f"   > {INSTRUCOES_GAMMA}", ""]
    passo = 5
    if figs:
        o.append(f"{passo}. Nos cards com figura, apagar a lista numerada que o Gamma montou e inserir a imagem "
                 "`figuras/slide-NN.png` do mesmo slide. As figuras estão na prancha [figuras.html](figuras.html).")
        passo += 1
    o += [f"{passo}. Conferir cada card contra a seção do slide abaixo.",
          f"{passo + 1}. Exportar PDF e PPTX.", "",
          "## Mapa de tempo", "", "| Momento | Slides | Horário | Tempo |", "|---|---|---|---:|"]
    for m in momentos(slides):
        faixa = str(m["de"]) if m["de"] == m["ate"] else f"{m['de']}–{m['ate']}"
        o.append(f"| {m['bloco']} | {faixa} | {hm(m['ini'])}–{hm(m['fim'])} | {m['min']}min |")
    o.append(f"| **Total** | **{len(slides)} slides** | **{hm(slides[0]['ini'])}–{hm(slides[-1]['fim'])}** | "
             f"**{sum(s['min'] for s in slides)}min** |")
    for n, s in enumerate(slides, 1):
        o += ["", f"## Slide {n} — {s['titulo']}", "",
              f"*{s.get('kicker', s['bloco'])} · {hm(s['ini'])}–{hm(s['fim'])} · {s['min']}min*", "",
              f"**{s['lede']}**"]
        if s.get("tela"):
            o += tela_md(s["tela"])
        if s.get("fluxo"):
            o += ["", f"**Fluxograma:** {s['fluxo']['descricao']}"]
            if "forma" in s["fluxo"]:
                o += ["", f"**Figura:** `figuras/slide-{n:02d}.svg`"]
        o += ["", f"**Condução:** {s['conducao']}"]
    return "\n".join(o) + "\n"


def gamma_colar(slides):
    cards = []
    for s in slides:
        c = [f"# {s['titulo']}"]
        if s.get("kicker"):
            c += ["", f"*{s['kicker']}*"]
        c += ["", s["lede"]]
        if s.get("fluxo"):
            c += ["", figuras.como_texto(s["fluxo"]) if "forma" in s["fluxo"] else "\n".join(s["fluxo"]["linhas"])]
        if s.get("tela"):
            c += tela_md(s["tela"])
        cards.append("\n".join(c))
    return "\n\n---\n\n".join(cards) + "\n"


def roteiro(meta, slides, parte2):
    o = [f"# Roteiro do professor — {meta['aula']} · {meta['titulo']}", "", cabecalho(meta, slides), "",
         "## Como usar este roteiro", "",
         "A fala e as âncoras estão em primeira pessoa. A aula é expositiva: só o professor opera e a turma assiste; "
         "nenhum momento depende de resposta da turma. Perguntas na fala são retóricas e o professor mesmo responde. "
         f"Bastidores orientam a condução e não são lidos em voz alta. {meta['roteiro_partes']}", "",
         " · ".join(f"[{texto}]({alvo})" for texto, alvo in meta["links_roteiro"]), "",
         "## Parte 1 — Fala slide a slide"]
    for n, s in enumerate(slides, 1):
        o += ["", f"### Slide {n} — {s['titulo']}", "",
              f"**{hm(s['ini'])}–{hm(s['fim'])} · {s['min']}min**", "",
              s["fala"], "",
              f"> **Âncora:** “{s['ancora']}”", "",
              f"> **Bastidor:** {s['conducao']}"]
    return "\n".join(o) + "\n\n" + parte2.strip() + "\n"


def plano(meta, slides, p):
    o = [f"# Plano — {meta['aula']} · {meta['titulo']}", "", cabecalho(meta, slides), "",
         f"**Formato: expositivo, no padrão de aula repaginada.** {p['formato']}", "",
         "| Momento | Slides | Horário | Duração |", "|---|---|---|---:|"]
    for m in momentos(slides):
        faixa = str(m["de"]) if m["de"] == m["ate"] else f"{m['de']}–{m['ate']}"
        o.append(f"| {m['bloco']} | {faixa} | {hm(m['ini'])}–{hm(m['fim'])} | {m['min']}min |")
    o.append(f"| **Total** | **{len(slides)} slides** | **{hm(slides[0]['ini'])}–{hm(slides[-1]['fim'])}** | "
             f"**{sum(s['min'] for s in slides)}min** |")
    o += ["", "## 1. Objetivo", "", p["objetivo"], "", "## 2. Resultados de aprendizagem", "",
          "Ao final, o participante é capaz de:", ""] + [f"- {r}" for r in p["resultados"]]
    conceitos = [(n, s) for n, s in enumerate(slides, 1) if s["bloco"] == "Conceitos"]
    ini, fim = conceitos[0][1]["ini"], conceitos[-1][1]["fim"]
    o += ["", "## 3. Exposição: conceitos em cadeia", "",
          f"**{hm(ini)}–{hm(fim)} · {fim - ini}min, slides {conceitos[0][0]}–{conceitos[-1][0]}.** Um slide por conceito: título "
          f"que afirma, definição em uma frase, fluxograma do mecanismo e no máximo uma linha de consequência. Pergunta da aula: "
          f"{meta['pergunta']}", "",
          "| Conceito | Slide | Tempo | Afirmação · forma do fluxograma | Liga-se a |", "|---|---|---:|---|---|"]
    for (n, s), liga in zip(conceitos, p["ligacoes"]):
        forma = {"decisao": "decisão", "convergencia": "convergência", "duas_faixas": "duas faixas"}.get(s["fluxo"].get("forma"), s["fluxo"].get("forma", "lista"))
        o.append(f"| {s['kicker'].split('·', 1)[1].strip()} | {n} | {s['min']}min | {s['titulo']} · {forma} | {liga} |")
    demo = [(n, s) for n, s in enumerate(slides, 1) if s["bloco"] == "Demonstração"]
    if demo:
        ini, fim = demo[0][1]["ini"], demo[-1][1]["fim"]
        o += ["", "## 4. Demonstração em dois atos", "",
              f"**{hm(ini)}–{hm(fim)} · {fim - ini}min, slides {demo[0][0]}–{demo[-1][0]}.** {p['demo_resumo']} "
              "Comandos, tempos internos e contingências na Parte 2 do [roteiro](roteiro.md).", "",
              "| Ato | Tempo | Condição | O que o professor faz | Conceitos à vista |", "|---|---:|---|---|---|"]
        o += [f"| {i} | {s['min']}min | {c} | {f} | {v} |" for i, ((_, s), (c, f, v)) in enumerate(zip(demo, p["atos"]), 1)]
    o += ["", "## 5. Monitor, discussão e fechamento", ""] + [f"- {x}" for x in p["fechamento"]]
    o += ["", "## 6. Materiais", "", "| Arquivo | Para quem | Como é produzido |", "|---|---|---|",
          "| [gamma-colar.md](gamma-colar.md), [slides-gamma.md](slides-gamma.md), [roteiro.md](roteiro.md), este plano | professor | "
          f"gerados de `preparacao/aulas/{meta['id']}.py` por `construir_aula.py` |",
          "| [figuras.html](figuras.html) e `figuras/slide-NN.svg` e `.png` | professor: fluxogramas para o Gamma | `construir_aula.py` e `exportar_figuras.py` |",
          "| [estudo-dirigido.pdf](estudo-dirigido.pdf) | alunos: conceitos detalhados e práticas passo a passo | `construir_estudo.py` |",
          "| [guia-monitor.html](guia-monitor.html) | monitores | `construir_monitor.py` |",
          "| [guia-interativo.html](guia-interativo.html) | professor e, se compartilhado, alunos | `preparacao/guias/gerar_guia.py` |",
          f"| [caso {CASO}](../../material-alunos/{CASO_PASTA}/README.md) | professor e alunos: {CASO_KIT} | escrito à mão |"]
    o += ["", "## 7. Riscos e contingências", ""] + [f"- {x}" for x in p["riscos"]]
    o += ["", f"**Vocabulário das figuras, igual em {juntar(modulos(AULAS))}:** " + "; ".join(x.lower() for x in LEGENDA) + "."]
    return "\n".join(o) + "\n"


def main(ident):
    fonte, meta, slides = carregar(ident)
    erros = validar(meta, slides)
    if erros:
        print("Fonte inválida:\n- " + "\n- ".join(erros))
        return 1
    com_horarios(meta, slides)
    destino = RAIZ / meta["pasta"]
    destino.mkdir(parents=True, exist_ok=True)
    saidas = {
        "slides-gamma.md": slides_gamma(meta, slides),
        "gamma-colar.md": gamma_colar(slides),
        "roteiro.md": roteiro(meta, slides, fonte.PARTE2),
        "plano.md": plano(meta, slides, fonte.PLANO),
    }
    figs = com_figura(slides)
    if figs:
        pasta = destino / "figuras"
        pasta.mkdir(exist_ok=True)
        for n, s in figs:
            svg, _ = figuras.desenhar(s["fluxo"], f"m{n}")
            (pasta / f"slide-{n:02d}.svg").write_text(svg + "\n", encoding="utf-8", newline="\n")
        saidas["figuras.html"] = prancha(meta, slides)
    for nome, texto in saidas.items():
        (destino / nome).write_text(texto, encoding="utf-8", newline="\n")
    print(f"{meta['aula']}: {len(slides)} slides, {hm(slides[0]['ini'])}–{hm(slides[-1]['fim'])}.")
    for m in momentos(slides):
        print(f"  {hm(m['ini'])}–{hm(m['fim'])}  {m['min']:>3}min  {m['bloco']}")
    print(f"Gerados em {meta['pasta']}: " + ", ".join(saidas) + (f" e {len(figs)} figuras" if figs else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "m3_a1"))
