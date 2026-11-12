"""Gera o estudo dirigido de uma aula em HTML e PDF (A4).

Uso, na pasta da turma: python -B preparacao/construir_estudo.py m3_a1 [--sem-pdf]
Conteúdo: o dicionário ESTUDO da fonte preparacao/aulas/<id>.py; figuras: os fluxogramas dos slides citados.
O PDF sai com Playwright (Chromium) em M<m>/aula-<n>/estudo-dirigido.pdf.
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
from estilo_cesar import FONTES, TOKENS, inline  # noqa: E402
from turma import CASO, FERRAMENTA, ORG  # noqa: E402

CSS = TOKENS + """
@page{size:A4;margin:16mm 15mm 18mm}
*{box-sizing:border-box}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{margin:0;background:var(--papel);color:var(--texto);font-family:var(--f-texto);font-size:10.6pt;line-height:1.55}
main{max-width:180mm;margin:0 auto;padding-block:8mm;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
h1,h2,h3,h4{color:var(--tinta);line-height:1.18;margin:0;text-wrap:balance}
h1{font-size:25pt;font-weight:800;letter-spacing:-.02em}
h2{font-size:16.5pt;font-weight:800;letter-spacing:-.01em}
h3{font-size:12pt;font-weight:700}
p{margin:0}
code{font-family:var(--f-codigo);font-size:.88em;background:var(--superficie-2);border:1px solid var(--linha);border-radius:4px;padding:0 .3em;color:var(--tinta)}
.sobre{font-size:8pt;letter-spacing:.09em;text-transform:uppercase;color:var(--marca-tx);font-weight:700}
.capa{display:flex;flex-direction:column;gap:10pt;padding-bottom:12pt;border-bottom:3px solid var(--marca);margin-bottom:14pt}
.lide{font-size:12pt;color:var(--tinta-2)}
.meta{display:flex;flex-wrap:wrap;gap:6pt}
.meta span{background:var(--superficie-2);border:1px solid var(--linha);border-radius:999px;padding:2pt 9pt;font-size:9pt;color:var(--tinta-2)}
.bloco{display:flex;flex-direction:column;gap:8pt;margin:0 0 16pt}
.quadro{border:1px solid var(--linha);border-radius:var(--raio);padding:10pt 12pt;background:var(--superficie-2);display:flex;flex-direction:column;gap:6pt}
.quadro.marca{background:var(--marca-suave);border-color:#FFD2B8}
.quadro.certo{background:var(--certo-suave);border-color:#BFE3CD}
.quadro.aviso{background:var(--aviso-suave);border-color:#F3D9A4}
.rot{font-size:7.6pt;letter-spacing:.09em;text-transform:uppercase;font-weight:700;color:var(--tinta-3)}
.quadro.marca .rot{color:var(--marca-forte)}.quadro.certo .rot{color:var(--certo)}.quadro.aviso .rot{color:var(--aviso)}
ul,ol{margin:0;padding-left:15pt;display:flex;flex-direction:column;gap:3pt}
.conceito{break-before:page;display:flex;flex-direction:column;gap:9pt}
.conceito .num{font-family:var(--f-codigo);font-size:9pt;color:var(--marca-tx);font-weight:700}
.definicao{font-size:11.6pt;font-weight:600;color:var(--tinta);border-left:4px solid var(--marca);padding:2pt 0 2pt 10pt}
figure{margin:2pt 0;break-inside:avoid}
figure svg{width:100%;height:auto;display:block;max-height:70mm}
figcaption{font-size:8.4pt;color:var(--tinta-3);margin-top:3pt}
.quadro,.definicao,pre,.pedido{break-inside:avoid}
.lado{display:grid;grid-template-columns:1fr 1fr;gap:8pt;break-inside:avoid}
.lado>*{min-width:0}
table{border-collapse:collapse;width:100%;font-size:9.4pt}
th,td{text-align:left;vertical-align:top;padding:4pt 6pt;border-bottom:1px solid var(--linha)}
th{font-size:8pt;text-transform:uppercase;letter-spacing:.06em;color:var(--tinta-3)}
td:first-child{font-weight:700;color:var(--tinta);width:32%}
.pratica{break-before:page;display:flex;flex-direction:column;gap:9pt}
.cab-pratica{display:flex;justify-content:space-between;gap:10pt;align-items:baseline;border-bottom:2px solid var(--marca);padding-bottom:4pt}
.cab-pratica .tempo{font-family:var(--f-codigo);font-size:9pt;color:var(--tinta-3);white-space:nowrap}
ol.passos{list-style:none;padding:0;counter-reset:p;gap:8pt}
ol.passos>li{counter-increment:p;display:grid;grid-template-columns:20pt 1fr;gap:6pt;break-inside:avoid}
ol.passos>li::before{content:counter(p);display:flex;align-items:center;justify-content:center;width:18pt;height:18pt;border-radius:50%;background:var(--marca);color:#fff;font-weight:700;font-size:9pt}
ol.passos>li>div{display:flex;flex-direction:column;gap:5pt;min-width:0}
pre{margin:0;font-family:var(--f-codigo);font-size:8.6pt;line-height:1.45;background:#1E1C1A;color:#F4F2EF;border-radius:8px;padding:7pt 9pt;white-space:pre-wrap;overflow-wrap:anywhere}
.pedido{border:1px dashed var(--linha-forte);border-radius:8px;padding:7pt 9pt;background:var(--papel);font-size:9.4pt}
.pedido small{display:block;font-size:7.4pt;letter-spacing:.09em;text-transform:uppercase;font-weight:700;color:var(--tinta-3);margin-bottom:3pt}
.checklist{list-style:none;padding:0}
.checklist li{display:grid;grid-template-columns:14pt 1fr;gap:5pt}
.checklist li::before{content:"";width:9pt;height:9pt;border:1.5px solid var(--linha-forte);border-radius:2pt;margin-top:3pt}
.secao{break-before:page;display:flex;flex-direction:column;gap:10pt}
.resp p{break-inside:avoid}
a{color:var(--marca-tx)}
"""


def lista(itens, classe=""):
    c = f' class="{classe}"' if classe else ""
    return f"<ul{c}>" + "".join(f"<li><span>{inline(x)}</span></li>" for x in itens) + "</ul>"


def figura(slides, n, legenda=None):
    s = slides[n - 1]
    fluxo = s.get("fluxo")
    if not fluxo or "forma" not in fluxo:
        return ""
    svg, _ = figuras.desenhar(fluxo, f"e{n}")
    return f'<figure>{svg}<figcaption>{escape(legenda or fluxo["descricao"])}</figcaption></figure>'


def passo_html(p):
    partes = [f"<p>{inline(p['t'])}</p>"]
    if p.get("cmd"):
        partes.append(f"<pre>{escape(p['cmd'])}</pre>")
    if p.get("prompt"):
        partes.append(f'<div class="pedido"><small>Texto para o {escape(FERRAMENTA)}</small>{inline(p["prompt"])}</div>')
    if p.get("obs"):
        partes.append(f'<p class="rot">{inline(p["obs"])}</p>')
    return "<li><div>" + "".join(partes) + "</div></li>"


def montar(meta, slides, e):
    mapa = next(n for n, s in enumerate(slides, 1) if s["bloco"] == "Mapa da aula")
    h = [f"""<section class="capa">
<p class="sobre">Estudo dirigido · {escape(meta['aula'])} · {escape(meta['modulo'])}</p>
<h1>{escape(meta['titulo'])}</h1>
<p class="lide">{inline(e['objetivo'])}</p>
<div class="meta"><span>Aula de {escape(meta['data'])}</span><span>Tempo sugerido: {escape(e['tempo'])}</span><span>{escape(meta['curso'])}</span></div>
</section>
<section class="bloco"><h2>Como usar este estudo</h2>
<p>Primeiro leia os conceitos na ordem: cada um sai do anterior, como na aula. Depois faça as práticas, que repetem no seu computador o que o professor demonstrou, com o {escape(FERRAMENTA)} e o caso {escape(CASO)}. No fim, confira a autoavaliação e as respostas das perguntas.</p>
<div class="quadro"><span class="rot">Antes de começar</span>{lista(e['antes'], 'checklist')}</div>
</section>
<section class="bloco"><h2>O mapa da aula</h2>
<p>Pergunta da aula: <b>{escape(meta['pergunta'])}</b></p>
{figura(slides, mapa)}
</section>"""]
    for i, c in enumerate(e["conceitos"], 1):
        p1, r1 = c["pergunta"]
        h.append(f"""<section class="conceito">
<p class="num">Conceito {i} de {len(e['conceitos'])}</p>
<h2>{escape(c['titulo'])}</h2>
<p class="definicao">{inline(c['definicao'])}</p>
{''.join(f'<p>{inline(t)}</p>' for t in c['texto'])}
{figura(slides, c['fig']) if c.get('fig') else ''}
<div class="lado"><div class="quadro marca"><span class="rot">No caso {escape(CASO)}</span><p>{inline(c['exemplo'])}</p></div>
<div class="quadro aviso"><span class="rot">Confusão frequente</span><p>{inline(c['erro'])}</p></div></div>
<div class="quadro"><span class="rot">Para conferir · resposta no fim</span><p>{inline(p1)}</p></div>
</section>""")
    glos = "".join(f"<tr><td>{inline(t)}</td><td>{inline(d)}</td></tr>" for t, d in e["glossario"])
    h.append(f'<section class="secao"><h2>Glossário da aula</h2><table><thead><tr><th>Termo</th><th>O que é</th></tr></thead><tbody>{glos}</tbody></table></section>')
    for p in e["praticas"]:
        h.append(f"""<section class="pratica">
<div class="cab-pratica"><h2>{escape(p['titulo'])}</h2><span class="tempo">{escape(p['tempo'])}</span></div>
<p><b>Objetivo.</b> {inline(p['objetivo'])}</p>
<ol class="passos">{''.join(passo_html(x) for x in p['passos'])}</ol>
<div class="quadro"><span class="rot">O que observar</span>{lista(p['observe'])}</div>
<div class="quadro certo"><span class="rot">Está pronto quando</span><p>{inline(p['pronto'])}</p></div>
{f'<div class="quadro marca"><span class="rot">Para ir além</span><p>{inline(p["extra"])}</p></div>' if p.get('extra') else ''}
</section>""")
    resp = "".join(f"<p><b>{i}. {inline(c['pergunta'][0])}</b><br>{inline(c['pergunta'][1])}</p>" for i, c in enumerate(e["conceitos"], 1))
    leit = "".join(f'<li>{inline(t)}. <a href="{escape(u)}">{escape(u)}</a> — {inline(n)}.</li>' for t, u, n in e["leituras"])
    h.append(f"""<section class="secao"><h2>Autoavaliação</h2>
<p>Marque o que você já consegue fazer sem consultar o material. O que ficar em branco indica o conceito para reler.</p>
{lista(e['autoavaliacao'], 'checklist')}
<h2>Respostas das perguntas</h2><div class="resp bloco">{resp}</div>
<h2>Para ler depois</h2><ul>{leit}</ul>
</section>""")
    titulo = f"Estudo dirigido · {meta['aula']}"
    return ('<!doctype html>\n<html lang="pt-BR"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            f"<title>{escape(titulo)}</title>{FONTES}<style>{CSS}</style></head><body><main>"
            + "\n".join(h) + "</main></body></html>\n")


def para_pdf(html_path, pdf_path, meta):
    from playwright.sync_api import sync_playwright
    rodape = (f'<div style="width:100%;font-family:Arial,sans-serif;font-size:8px;color:#5C5955;padding:0 15mm;'
              f'display:flex;justify-content:space-between"><span>{escape(meta["aula"])} · Estudo dirigido · {escape(ORG)}</span>'
              '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page()
        pag.goto(html_path.as_uri(), wait_until="networkidle")
        pag.evaluate("document.fonts.ready")
        pag.pdf(path=str(pdf_path), format="A4", print_background=True, display_header_footer=True,
                header_template="<div></div>", footer_template=rodape,
                margin={"top": "16mm", "bottom": "18mm", "left": "15mm", "right": "15mm"})
        nav.close()


def main(ident, gerar_pdf=True):
    fonte = importlib.import_module(ident)
    meta, slides = fonte.META, fonte.SLIDES
    destino = RAIZ / meta["pasta"]
    html_path = destino / "estudo-dirigido.html"
    html_path.write_text(montar(meta, slides, fonte.ESTUDO), encoding="utf-8", newline="\n")
    print(f"Gerado {html_path.relative_to(RAIZ)}")
    if gerar_pdf:
        pdf = destino / "estudo-dirigido.pdf"
        para_pdf(html_path, pdf, meta)
        print(f"Gerado {pdf.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "m3_a1", "--sem-pdf" not in sys.argv))
