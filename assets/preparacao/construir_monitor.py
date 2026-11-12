"""Gera o guia do monitor de uma aula: o que saber, o que fazer em cada momento e a apresentação de 20 minutos.

Uso, na pasta da turma: python -B preparacao/construir_monitor.py m3_a1
Conteúdo: o dicionário MONITOR da fonte preparacao/aulas/<id>.py; horários e momentos: os SLIDES.
O arquivo abre por duplo clique; o trecho entre publicar:inicio e publicar:fim é o corpo publicado como Artifact.
"""
import importlib
import sys
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAIZ = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "aulas"))

from construir_aula import com_horarios, hm, momentos  # noqa: E402
from estilo_cesar import FONTES, TOKENS, inline  # noqa: E402
from turma import CASO, REPO, TURMA  # noqa: E402

CSS = TOKENS + """
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--papel);color:var(--texto);font-family:var(--f-texto);font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased}
.wrap{max-width:1040px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
h1,h2,h3,h4{color:var(--tinta);line-height:1.15;margin:0;text-wrap:balance}
h1{font-size:clamp(2rem,5vw,3.2rem);font-weight:800;letter-spacing:-.025em;max-width:22ch}
h2{font-size:clamp(1.45rem,3vw,1.9rem);font-weight:800;letter-spacing:-.01em}
h3{font-size:1.08rem;font-weight:700}
p{margin:0}
a{color:var(--marca-tx);text-underline-offset:3px;overflow-wrap:anywhere}
code{font-family:var(--f-codigo);font-size:.86em;background:var(--superficie-2);border:1px solid var(--linha);padding:.05em .35em;border-radius:5px;color:var(--tinta);overflow-wrap:anywhere}
.sobre{font-size:.76rem;letter-spacing:.09em;text-transform:uppercase;color:var(--marca-tx);font-weight:700}
.topo{padding-block:48px 28px;border-bottom:1px solid var(--linha);background:linear-gradient(180deg,var(--marca-suave),var(--papel) 75%)}
.topo .wrap{display:flex;flex-direction:column;gap:16px}
.lide{font-size:1.14rem;color:var(--tinta-2);max-width:66ch}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chips span{background:var(--papel);border:1px solid var(--linha);border-radius:999px;padding:5px 12px;font-size:.88rem;color:var(--tinta-2);font-weight:600}
.chips span.destaque{background:var(--marca);border-color:var(--marca);color:#fff}
.fio{display:flex;flex-wrap:wrap;gap:6px;align-items:stretch}
.fio div{flex:1 1 140px;min-width:0;border:1px solid var(--linha);border-radius:10px;background:var(--papel);padding:10px 12px;display:flex;flex-direction:column;gap:2px}
.fio div b{color:var(--tinta);font-size:.95rem}
.fio div span{font-size:.84rem;color:var(--tinta-3);line-height:1.35}
.fio div.foco{background:var(--marca-suave);border-color:#FFC7A6}
main section{padding-block:36px;border-bottom:1px solid var(--linha)}
main section .wrap{display:flex;flex-direction:column;gap:16px}
.prosa{max-width:68ch}
.rolagem{overflow-x:auto;border:1px solid var(--linha);border-radius:var(--raio)}
table{border-collapse:collapse;width:100%;min-width:720px;font-size:.93rem}
th,td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid var(--linha)}
th{font-size:.74rem;letter-spacing:.07em;text-transform:uppercase;color:var(--tinta-3);background:var(--superficie-2)}
tr:last-child td{border-bottom:0}
td.hora{font-variant-numeric:tabular-nums;white-space:nowrap;font-weight:700;color:var(--tinta)}
th:nth-child(3){width:30%}
tr.seu td{background:var(--marca-suave)}
td .momento{display:block;font-weight:700;color:var(--tinta)}
td .slides{font-size:.8rem;color:var(--tinta-3)}
.termos{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:10px}
.termos div{border:1px solid var(--linha);border-radius:10px;padding:12px 14px;display:flex;flex-direction:column;gap:4px;min-width:0}
.termos b{color:var(--tinta)}
.termos span{font-size:.92rem;color:var(--tinta-2)}
.colunas{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}
.colunas>div{min-width:0;display:flex;flex-direction:column;gap:10px}
ul.marcas{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px}
ul.marcas li{display:grid;grid-template-columns:18px 1fr;gap:8px}
ul.marcas li>span{min-width:0;overflow-wrap:anywhere}
ul.marcas li::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--marca);margin-top:.6em}
ul.check li::before{width:13px;height:13px;border-radius:3px;background:transparent;border:2px solid var(--linha-forte);margin-top:.35em}
.alerta{border:1px solid #F3D9A4;background:var(--aviso-suave);border-radius:var(--raio);padding:16px 18px;display:flex;flex-direction:column;gap:10px}
.alerta h3{color:var(--aviso)}
details{border:1px solid var(--linha);border-radius:10px;padding:10px 14px;background:var(--papel)}
details+details{margin-top:-6px}
summary{cursor:pointer;font-weight:700;color:var(--tinta)}
details p{margin-top:8px;color:var(--tinta-2)}
.palco{border:2px solid var(--marca);border-radius:16px;padding:22px;display:flex;flex-direction:column;gap:14px;background:var(--papel)}
.palco h3{font-size:1.35rem}
.linha-tempo{display:flex;flex-direction:column;gap:0;border-left:3px solid var(--marca);margin-left:6px}
.linha-tempo div{display:grid;grid-template-columns:72px 1fr;gap:12px;padding:8px 0 8px 14px;position:relative}
.linha-tempo div::before{content:"";position:absolute;left:-8px;top:15px;width:13px;height:13px;border-radius:50%;background:var(--papel);border:3px solid var(--marca)}
.linha-tempo small{font-variant-numeric:tabular-nums;font-weight:700;color:var(--marca-forte)}
.linha-tempo p b{color:var(--tinta)}
.rodape{padding-block:28px 40px;color:var(--tinta-3);font-size:.9rem}
.rodape .wrap{display:flex;flex-direction:column;gap:8px}
:focus-visible{outline:3px solid var(--marca);outline-offset:2px;border-radius:4px}
@media (max-width:560px){body{font-size:16px}.linha-tempo div{grid-template-columns:1fr;gap:2px}}
"""


def itens(lista, classe="marcas"):
    return f'<ul class="{classe}">' + "".join(f"<li><span>{inline(x)}</span></li>" for x in lista) + "</ul>"


def montar(meta, slides, m):
    com_horarios(meta, slides)
    mom = momentos(slides)
    seu = next(x for x in mom if x["bloco"] == "Monitor")
    mapa = next(s for s in slides if s["bloco"] == "Mapa da aula")
    fio = "".join(f'<div class="{"foco" if (len(n) > 2 and n[2] == "foco") else ""}"><b>{escape(n[0])}</b>'
                  f'<span>{escape(" ".join(n[1]) if isinstance(n[1], list) else n[1])}</span></div>' for n in mapa["fluxo"]["nos"])
    linhas = []
    for x in mom:
        titulos = [s["titulo"] for s in slides[x["de"] - 1:x["ate"]]]
        faixa = f'slide {x["de"]}' if x["de"] == x["ate"] else f'slides {x["de"]}–{x["ate"]}'
        linhas.append(f'<tr class="{"seu" if x is seu else ""}"><td class="hora">{hm(x["ini"])}–{hm(x["fim"])}</td>'
                      f'<td><span class="momento">{escape(x["bloco"])}</span><span class="slides">{faixa} · {x["min"]} min</span></td>'
                      f'<td>{"<br>".join(escape(t) for t in titulos)}</td><td>{inline(m["durante"].get(x["bloco"], "Acompanhar o chat."))}</td></tr>')
    termos = "".join(f"<div><b>{inline(t)}</b><span>{inline(d)}</span></div>" for t, d in m["termos"])
    duvidas = "".join(f"<details><summary>{inline(q)}</summary><p>{inline(r)}</p></details>" for q, r in m["duvidas"])
    a = m["apresentacao"]
    roteiro = "".join(f"<div><small>{escape(t)}</small><p><b>{escape(parte)}.</b> {inline(c)}</p></div>" for t, parte, c in a["roteiro"])
    repo = f' Caso {escape(CASO)} e estudos dirigidos: <a href="{REPO}">{REPO[8:]}</a>.' if REPO else ""
    titulo_pagina = f"Monitoria {meta['aula'].split('·')[0].strip()}.{meta['id'][-1]}"
    corpo = f"""<title>{escape(titulo_pagina)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
{FONTES}
<style>{CSS}</style>
<header class="topo"><div class="wrap">
<p class="sobre">Guia do monitor · {escape(meta['aula'])} · {escape(meta['modulo'])}</p>
<h1>{escape(meta['titulo'])}</h1>
<p class="lide">{inline(m['resumo'])}</p>
<div class="chips"><span>{escape(meta['data'])} · {hm(slides[0]['ini'])}–{hm(slides[-1]['fim'])}</span><span>Professor: {escape(meta['docente'])}</span>
<span class="destaque">Apresentação do monitor: {hm(seu['ini'])}–{hm(seu['fim'])}</span></div>
</div></header>
<main>
<section><div class="wrap">
<p class="sobre">A aula em uma linha</p>
<h2>Pergunta da aula: {escape(meta['pergunta'][0].upper() + meta['pergunta'][1:])}</h2>
<p class="prosa">Os conceitos vêm em cadeia, cada um consequência do anterior. A aula é expositiva: a turma assiste e só o professor opera. Ninguém precisa falar ou abrir câmera; a prática fica no estudo dirigido.</p>
<div class="fio" role="list" aria-label="Cadeia de conceitos da aula">{fio}</div>
</div></section>
<section><div class="wrap">
<p class="sobre">Fluxo da aula</p>
<h2>O que acontece em cada momento, e o que você faz</h2>
<div class="rolagem"><table><thead><tr><th>Horário</th><th>Momento</th><th>Na tela</th><th>Você</th></tr></thead><tbody>{''.join(linhas)}</tbody></table></div>
</div></section>
<section><div class="wrap">
<p class="sobre">Vocabulário</p>
<h2>Termos que você precisa dominar</h2>
<div class="termos">{termos}</div>
</div></section>
<section><div class="wrap">
<div class="colunas">
<div><p class="sobre">Antes da aula</p><h2>Preparação</h2>{itens(m['antes'], 'marcas check')}</div>
<div><p class="sobre">Durante</p><h2>Como contribuir</h2>{itens(m['contribuir'])}</div>
</div>
<div class="alerta"><h3>Fique atento</h3>{itens(m['atencao'])}</div>
</div></section>
<section><div class="wrap">
<p class="sobre">Chat</p>
<h2>Dúvidas prováveis e respostas curtas</h2>
<div>{duvidas}</div>
</div></section>
<section><div class="wrap">
<p class="sobre">Sua apresentação · {hm(seu['ini'])}–{hm(seu['fim'])} · {seu['min']} minutos</p>
<div class="palco">
<h3>{escape(a['titulo'])}</h3>
<p class="prosa"><b>Por que este tema.</b> {inline(a['porque'])}</p>
<div class="linha-tempo">{roteiro}</div>
<div class="colunas">
<div><h3>Fontes</h3>{itens(a['fontes'])}</div>
<div><h3>Evite</h3>{itens(a['evitar'])}</div>
</div>
<p class="prosa"><b>Tema alternativo.</b> {inline(a['alternativa'])}</p>
</div>
</div></section>
<section><div class="wrap">
<p class="sobre">Depois da aula</p>
<h2>Fechando o ciclo</h2>
{itens(m['depois'])}
</div></section>
</main>
<footer class="rodape"><div class="wrap">
<p>Material da aula, na pasta {escape(meta['pasta'])} do curso: roteiro.md (fala do professor e comandos da demonstração), slides-gamma.md, estudo-dirigido.pdf e guia-interativo.html.{repo}</p>
<p>{escape(meta['curso'])} · {escape(meta['modulo'])} · Turma {escape(TURMA)} · Professor {escape(meta['docente'])}</p>
</div></footer>
"""
    return ('<!doctype html>\n<html lang="pt-BR"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"></head><body>\n'
            '<!-- publicar:inicio -->\n' + corpo + '<!-- publicar:fim -->\n</body></html>\n')


def main(ident):
    fonte = importlib.import_module(ident)
    destino = RAIZ / fonte.META["pasta"] / "guia-monitor.html"
    destino.write_text(montar(fonte.META, fonte.SLIDES, fonte.MONITOR), encoding="utf-8", newline="\n")
    print(f"Gerado {destino.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "m3_a1"))
