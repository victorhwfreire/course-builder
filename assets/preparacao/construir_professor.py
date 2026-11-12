"""Gera o guia do professor de uma aula: a fala slide a slide e o passo a passo da demonstração.

Uso, na pasta da turma: python -B preparacao/construir_professor.py m3_a1
Conteúdo: preparacao/professor/fala_<id>.py. Títulos, horários, âncoras, figuras e condução: preparacao/aulas/<id>.py.
O arquivo abre por duplo clique; o trecho entre publicar:inicio e publicar:fim é o corpo publicado como Artifact.
"""
import importlib
import re
import sys
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAIZ = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "aulas"))
sys.path.insert(0, str(HERE / "professor"))

import figuras  # noqa: E402
from construir_aula import com_horarios, hm, momentos  # noqa: E402
from estilo_cesar import FONTES, TOKENS, inline  # noqa: E402
from turma import CASO, REPO, TURMA  # noqa: E402

CSS = TOKENS + """
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:64px}
body{margin:0;background:var(--papel);color:var(--texto);font-family:var(--f-texto);font-size:17px;line-height:1.65;-webkit-font-smoothing:antialiased}
.wrap{max-width:980px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
h1,h2,h3{color:var(--tinta);line-height:1.15;margin:0;text-wrap:balance}
h1{font-size:clamp(2rem,5vw,3.1rem);font-weight:800;letter-spacing:-.025em;max-width:22ch}
h2{font-size:clamp(1.35rem,3vw,1.8rem);font-weight:800;letter-spacing:-.01em}
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
nav.indice{position:sticky;top:0;z-index:5;background:rgba(255,255,255,.96);border-bottom:1px solid var(--linha)}
nav.indice .wrap{display:flex;gap:6px;overflow-x:auto;padding-block:10px;scrollbar-width:thin}
nav.indice a{flex:0 0 auto;text-decoration:none;font-size:.86rem;font-weight:600;color:var(--tinta-2);border:1px solid var(--linha);border-radius:999px;padding:4px 11px;background:var(--papel)}
nav.indice a.parte2{background:var(--marca-suave);border-color:#FFC7A6;color:var(--marca-forte)}
main>section{padding-block:36px;border-bottom:1px solid var(--linha)}
main>section>.wrap{display:flex;flex-direction:column;gap:16px}
.prosa{max-width:70ch;display:flex;flex-direction:column;gap:12px}
.rolagem{overflow-x:auto;border:1px solid var(--linha);border-radius:var(--raio)}
table{border-collapse:collapse;width:100%;min-width:560px;font-size:.93rem}
th,td{text-align:left;vertical-align:top;padding:9px 12px;border-bottom:1px solid var(--linha)}
th{font-size:.74rem;letter-spacing:.07em;text-transform:uppercase;color:var(--tinta-3);background:var(--superficie-2)}
tr:last-child td{border-bottom:0}
td.num{font-variant-numeric:tabular-nums;white-space:nowrap}
.caixa{border:1px solid #FFC7A6;background:var(--marca-suave);border-radius:var(--raio);padding:14px 16px;display:flex;flex-direction:column;gap:6px}
.caixa .t{font-size:.76rem;letter-spacing:.08em;text-transform:uppercase;font-weight:700;color:var(--marca-forte)}
.parte1{padding-top:30px}
.slide{padding-block:34px;border-bottom:1px solid var(--linha)}
.slide>.wrap{display:flex;flex-direction:column;gap:14px}
.slide-topo{display:flex;flex-direction:column;gap:8px}
.rotulo{font-size:.76rem;letter-spacing:.09em;text-transform:uppercase;color:var(--marca-tx);font-weight:700}
.tempo{align-self:flex-start;font-variant-numeric:tabular-nums;font-weight:700;font-size:.88rem;color:var(--tinta);background:var(--superficie-3);border-radius:999px;padding:3px 11px}
.ancora{border-left:4px solid var(--marca);padding:6px 0 6px 14px;font-weight:600;color:var(--tinta);font-size:1.04rem}
.tela{border:1px solid var(--linha);border-radius:var(--raio);background:var(--superficie-2);padding:14px;display:flex;flex-direction:column;gap:10px}
.tela .etq{font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;font-weight:700;color:var(--tinta-3)}
.tela .lede-slide{color:var(--tinta-2);font-size:.95rem}
.tela .figura{background:#fff;border-radius:10px}
.tela .figura svg{display:block;width:100%;height:auto}
.tela ul{margin:0;padding-left:18px;color:var(--tinta-2);font-size:.92rem}
.rf{font-weight:800;color:var(--tinta);font-size:1.02rem}
.fala{display:flex;flex-direction:column;gap:12px;max-width:72ch}
.cena{color:var(--tinta-3);font-style:italic}
.bastidor{border:1px dashed var(--linha-forte);border-radius:var(--raio);padding:12px 14px;background:var(--papel);font-size:.93rem;color:var(--tinta-2);display:flex;flex-direction:column;gap:6px;max-width:72ch}
.bastidor .t{font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;font-weight:700;color:var(--tinta-3)}
.ir{font-weight:700}
.parte2{background:linear-gradient(180deg,var(--marca-suave),var(--papel) 240px)}
.cartoes{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px}
.cartao{border:1px solid var(--linha);border-radius:var(--raio);background:var(--papel);padding:14px 16px;display:flex;flex-direction:column;gap:8px;min-width:0}
.cartao.largo{grid-column:1/-1}
.cmd{display:flex;flex-direction:column;background:#16120F;border-radius:10px;min-width:0}
.cmd pre{margin:0;padding:2px 14px 12px;overflow-x:auto;color:#F6EFE9;font-family:var(--f-codigo);font-size:.84rem;line-height:1.55}
.cmd code{background:none;border:0;padding:0;color:inherit;font-size:1em;overflow-wrap:normal}
.cmd button{order:-1;align-self:flex-end;margin:8px 8px 0;font:600 .78rem var(--f-texto);color:#16120F;background:#fff;border:0;border-radius:6px;padding:5px 9px;cursor:pointer}
.cmd button.ok{background:var(--certo-suave);color:var(--certo)}
.ato{display:flex;flex-direction:column;gap:14px;margin-top:10px}
.ato-cab{display:flex;flex-wrap:wrap;align-items:baseline;gap:8px 14px}
.passos{display:flex;flex-direction:column;gap:0;border-left:3px solid var(--marca);margin-left:6px}
.passo{position:relative;padding:4px 0 22px 20px;display:flex;flex-direction:column;gap:9px;min-width:0}
.passo::before{content:"";position:absolute;left:-9px;top:9px;width:15px;height:15px;border-radius:50%;background:var(--papel);border:3px solid var(--marca)}
.passo .quando{font-variant-numeric:tabular-nums;font-weight:700;color:var(--marca-forte);font-size:.9rem}
.campo{display:grid;grid-template-columns:86px 1fr;gap:10px;align-items:start}
.campo>b{font-size:.74rem;letter-spacing:.07em;text-transform:uppercase;color:var(--tinta-3);padding-top:.25em}
.campo>div{min-width:0}
.campo.dizer>div{background:var(--marca-suave);border-radius:8px;padding:8px 12px;color:var(--tinta);font-weight:600}
.campo.senao>div{background:var(--aviso-suave);border:1px solid #F3D9A4;border-radius:8px;padding:8px 12px;color:var(--tinta-2)}
.refs ul{margin:0;padding-left:18px;display:flex;flex-direction:column;gap:8px;max-width:76ch}
.nota{color:var(--tinta-3);font-size:.92rem;max-width:76ch}
.rodape{padding-block:28px 40px;color:var(--tinta-3);font-size:.9rem}
.rodape .wrap{display:flex;flex-direction:column;gap:8px}
:focus-visible{outline:3px solid var(--marca);outline-offset:2px;border-radius:4px}
@media (max-width:560px){body{font-size:16px}.campo{grid-template-columns:1fr;gap:4px}}
@media print{nav.indice,.cmd button{display:none}.slide{break-inside:avoid-page}}
"""

JS = """
document.querySelectorAll('.cmd button').forEach(function (b) {
  b.addEventListener('click', function () {
    var texto = b.parentNode.querySelector('pre').innerText;
    function feito() { b.textContent = 'Copiado'; b.classList.add('ok'); setTimeout(function () { b.textContent = 'Copiar'; b.classList.remove('ok'); }, 1600); }
    function reserva() {
      var t = document.createElement('textarea'); t.value = texto; t.setAttribute('readonly', ''); t.style.position = 'fixed'; t.style.opacity = '0';
      document.body.appendChild(t); t.select();
      try { document.execCommand('copy'); feito(); } catch (e) { b.textContent = 'Selecione e copie'; }
      document.body.removeChild(t);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(texto).then(feito, reserva); } else { reserva(); }
  });
});
"""


def fmt(texto):
    """inline() mais *itálico* e [ação] em cinza, fora de <code>: `[Console]::...` continua código."""
    partes = re.split(r"(<code>.*?</code>)", inline(texto))
    for i in range(0, len(partes), 2):
        s = re.sub(r"(?<![*\w])\*([^*\n]+)\*(?!\*)", r"<i>\1</i>", partes[i])
        partes[i] = re.sub(r"\[([^\]<>]+)\]", r'<span class="cena">[\1]</span>', s)
    return "".join(partes)


def bloco_cmd(cmds):
    if not cmds:
        return ""
    return f'<div class="cmd"><pre><code>{escape(chr(10).join(cmds))}</code></pre><button type="button">Copiar</button></div>'


def conferir(aula, fala, slides):
    erros = []
    for n in range(1, len(slides) + 1):
        f = fala.FALAS.get(n)
        if not f:
            erros.append(f"slide {n} sem fala")
        elif not 3 <= len(f["fala"]) <= 5:
            erros.append(f"slide {n}: {len(f['fala'])} parágrafos (esperado 3 a 5)")
    for ato in fala.ATOS:
        soma, previsto = sum(p["min"] for p in ato["passos"]), slides[ato["slide"] - 1]["min"]
        if soma != previsto:
            erros.append(f"{ato['titulo']}: passos somam {soma} min, slide tem {previsto}")
    parte2 = " ".join(aula.PARTE2.split())
    todos = [c for g in (fala.PREPARO, fala.CONTINGENCIA) for item in g for c in item["cmds"]]
    todos += [c for ato in fala.ATOS for p in ato["passos"] for c in p.get("cmds", [])]
    for c in todos:
        if " ".join(c.split()) not in parte2:
            erros.append(f"comando fora da PARTE2: {c}")
    return erros


def tela_do_slide(n, s):
    partes = [f'<p class="lede-slide">{fmt(s["lede"])}</p>']
    if "forma" in s.get("fluxo", {}):
        svg, _ = figuras.desenhar(s["fluxo"], f"pf{n:02d}")
        partes.append(f'<div class="figura">{svg}</div>')
    if s.get("tela"):
        partes.append("<ul>" + "".join(f"<li>{fmt(t.lstrip('- '))}</li>" for t in s["tela"]) + "</ul>")
    return f'<div class="tela"><span class="etq">Na tela</span>{"".join(partes)}</div>'


def secao_slide(n, s, f, atos_por_slide):
    rotulo = s.get("kicker") or s["bloco"]
    bastidor = fmt(s["conducao"]) + (f"<br>{fmt(f['bastidor'])}" if f.get("bastidor") else "")
    ir = ""
    if n in atos_por_slide:
        ir = f'<p class="ir"><a href="#ato-{n}">Passo a passo e comandos deste ato, na Parte 2</a></p>'
    return f"""<section class="slide" id="s{n}"><div class="wrap">
<div class="slide-topo"><span class="rotulo">{escape(rotulo)}</span>
<h2>Slide {n} - {escape(s['titulo'])}</h2>
<span class="tempo">{hm(s['ini'])} · {s['min']} min</span></div>
<div class="ancora">Âncora: “{escape(s['ancora'])}”</div>
{tela_do_slide(n, s)}
<p class="rf">Roteiro de Fala:</p>
<div class="fala">{''.join(f'<p>{fmt(p)}</p>' for p in f['fala'])}</div>
{ir}
<div class="bastidor"><span class="t">Bastidor</span><p>{bastidor}</p></div>
</div></section>"""


def campo(classe, rotulo, conteudo):
    return f'<div class="campo {classe}"><b>{rotulo}</b><div>{conteudo}</div></div>' if conteudo else ""


def secao_ato(ato, slides):
    s = slides[ato["slide"] - 1]
    t = s["ini"]
    itens = []
    for i, p in enumerate(ato["passos"], 1):
        corpo = (campo("", "Fazer", fmt(p["fazer"]) if p.get("fazer") else "")
                 + campo("", "Comando", bloco_cmd(p.get("cmds", [])))
                 + campo("", "Na tela", fmt(p["tela"]) if p.get("tela") else "")
                 + campo("dizer", "Dizer", fmt(p["dizer"]))
                 + campo("senao", "Se falhar", fmt(p["senao"]) if p.get("senao") else ""))
        itens.append(f'<div class="passo"><span class="quando">{hm(t)} · {p["min"]} min · passo {i}</span>'
                     f'<h3>{escape(p["titulo"])}</h3>{corpo}</div>')
        t += p["min"]
    return (f'<div class="ato" id="ato-{ato["slide"]}"><div class="ato-cab"><h2>{escape(ato["titulo"])}</h2>'
            f'<span class="tempo">{hm(s["ini"])}–{hm(s["fim"])} · slide {ato["slide"]}</span></div>'
            f'<div class="passos">{"".join(itens)}</div></div>')


def cartoes(lista, largo=False):
    return "".join(f'<div class="cartao{" largo" if largo or item["cmds"] else ""}"><h3>{escape(item["titulo"])}</h3>'
                   f'<p>{fmt(item["texto"])}</p>{bloco_cmd(item["cmds"])}</div>' for item in lista)


def faixa(x):
    return str(x["de"]) if x["de"] == x["ate"] else f'{x["de"]}–{x["ate"]}'


def montar(aula, fala):
    meta, slides = aula.META, aula.SLIDES
    com_horarios(meta, slides)
    mom = momentos(slides)
    atos_por_slide = {a["slide"] for a in fala.ATOS}
    indice = "".join(f'<a href="#s{x["de"]}">{escape(x["bloco"])}</a>' for x in mom)
    tabela = "".join(
        f'<tr><td>{escape(x["bloco"])}</td><td>{faixa(x)}</td>'
        f'<td class="num">{hm(x["ini"])}–{hm(x["fim"])}</td><td class="num">{x["min"]} min</td></tr>' for x in mom)
    corpo_slides = "".join(secao_slide(n, s, fala.FALAS[n], atos_por_slide) for n, s in enumerate(slides, 1))
    atos = "".join(secao_ato(a, slides) for a in fala.ATOS)
    numero = f"{meta['aula'].split('·')[0].strip()}.{meta['id'][-1]}"
    repo = f' Caso {escape(CASO)} e estudos dirigidos: <a href="{REPO}">{REPO[8:]}</a>.' if REPO else ""
    corpo = f"""<title>Professor {escape(numero)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
{FONTES}
<style>{CSS}</style>
<header class="topo"><div class="wrap">
<p class="sobre">Guia do professor · {escape(meta['aula'])} · {escape(meta['modulo'])}</p>
<h1>{escape(meta['titulo'])}</h1>
<p class="lide">Pergunta da aula: {escape(meta['pergunta'][0].upper() + meta['pergunta'][1:])} Roteiro de fala completo dos {len(slides)} slides e o passo a passo da demonstração.</p>
<div class="chips"><span>{escape(meta['data'])} · {hm(slides[0]['ini'])}–{hm(slides[-1]['fim'])}</span><span>{escape(meta['docente'])}</span>
<span>{escape(meta['curso'])} · Turma {escape(TURMA)}</span><span class="destaque">Demonstração: {hm(slides[min(atos_por_slide) - 1]['ini'])}–{hm(slides[max(atos_por_slide) - 1]['fim'])}</span></div>
</div></header>
<nav class="indice" aria-label="Momentos da aula"><div class="wrap"><a href="#uso">Como usar</a>{indice}<a class="parte2" href="#parte2">Parte 2</a><a href="#refs">Referências</a></div></nav>
<main>
<section id="uso"><div class="wrap">
<p class="sobre">Antes de tudo</p>
<h2>Como usar este roteiro</h2>
<div class="prosa">{''.join(f'<p>{fmt(p)}</p>' for p in fala.USO)}</div>
<div class="rolagem"><table><thead><tr><th>Momento</th><th>Slides</th><th>Horário</th><th>Duração</th></tr></thead><tbody>{tabela}</tbody></table></div>
<div class="caixa"><span class="t">O caso de hoje: {escape(CASO)}</span><p>{fmt(fala.CASO)}</p></div>
</div></section>
<div class="wrap parte1"><p class="sobre">Parte 1 · Fala slide a slide</p></div>
{corpo_slides}
<section id="parte2" class="parte2"><div class="wrap">
<p class="sobre">Parte 2 · Demonstração passo a passo</p>
<h2>Antes da aula</h2>
<p class="prosa">Os comandos rodam no PowerShell, na ordem. Cada bloco tem um botão para copiar tudo.</p>
<div class="cartoes">{cartoes(fala.PREPARO)}</div>
{atos}
<h2 style="margin-top:12px">Contingência</h2>
<div class="cartoes">{cartoes(fala.CONTINGENCIA)}</div>
</div></section>
<section id="refs" class="refs"><div class="wrap">
<p class="sobre">Fontes</p>
<h2>Referências usadas na fala</h2>
<ul>{''.join(f'<li>{fmt(r)}</li>' for r in fala.REFS)}</ul>
<p class="nota">{fmt(fala.NOTA)}</p>
</div></section>
</main>
<footer class="rodape"><div class="wrap">
<p>Gerado de <code>preparacao/aulas/{meta['id']}.py</code> e <code>preparacao/professor/fala_{meta['id']}.py</code>.{repo}</p>
<p>{escape(meta['curso'])} · {escape(meta['modulo'])} · Turma {escape(TURMA)} · Professor {escape(meta['docente'])}</p>
</div></footer>
<script>{JS}</script>
"""
    return ('<!doctype html>\n<html lang="pt-BR"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"></head><body>\n'
            '<!-- publicar:inicio -->\n' + corpo + '<!-- publicar:fim -->\n</body></html>\n')


def main(ident):
    aula = importlib.import_module(ident)
    fala = importlib.import_module(f"fala_{ident}")
    erros = conferir(aula, fala, aula.SLIDES)
    if erros:
        print("\n".join(erros))
        return 1
    destino = RAIZ / aula.META["pasta"] / "guia-professor.html"
    destino.write_text(montar(aula, fala), encoding="utf-8", newline="\n")
    print(f"Gerado {destino.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "m3_a1"))
