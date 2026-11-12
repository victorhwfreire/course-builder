"""Gera o guia geral dos módulos da turma para alunos, monitores e coordenação.

Uso, na pasta da turma: python -B preparacao/construir_guia_modulos.py
Conteúdo: as fontes das aulas de turma.AULAS (preparacao/aulas), as ementas de turma.EMENTAS, a tabela de links do README
e os textos de turma.GUIA_MODULOS.
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

from construir_aula import com_horarios, hm, juntar, modulos, momentos  # noqa: E402
from estilo_cesar import FONTES, TOKENS, inline  # noqa: E402
from turma import AULAS, CASO, CURSO, DOCENTE, EMENTAS, GUIA_MODULOS as G, ORG, REPO, TURMA, pdf_estudo  # noqa: E402

CSS = TOKENS + """
*{box-sizing:border-box}
[hidden]{display:none!important}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;background:var(--papel);color:var(--texto);font-family:var(--f-texto);font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased}
.wrap{max-width:1080px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
h1,h2,h3,h4{color:var(--tinta);line-height:1.15;margin:0;text-wrap:balance}
h1{font-size:clamp(2.1rem,5.4vw,3.5rem);font-weight:800;letter-spacing:-.03em;max-width:20ch}
h2{font-size:clamp(1.45rem,3vw,1.95rem);font-weight:800;letter-spacing:-.01em;max-width:34ch}
h3{font-size:1.1rem;font-weight:700}
p{margin:0}
a{color:var(--marca-tx);text-underline-offset:3px;overflow-wrap:anywhere}
code{font-family:var(--f-codigo);font-size:.86em;background:var(--superficie-2);border:1px solid var(--linha);padding:.05em .35em;border-radius:5px;color:var(--tinta);overflow-wrap:anywhere}
.sobre{font-size:.76rem;letter-spacing:.09em;text-transform:uppercase;color:var(--marca-tx);font-weight:700}
.prosa{max-width:68ch;color:var(--tinta-2)}
.topo{padding-block:52px 32px;border-bottom:1px solid var(--linha);background:linear-gradient(180deg,var(--marca-suave),var(--papel) 78%)}
.topo .wrap{display:flex;flex-direction:column;gap:18px}
.lide{font-size:1.16rem;color:var(--tinta-2);max-width:64ch}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chips span{background:var(--papel);border:1px solid var(--linha);border-radius:999px;padding:5px 12px;font-size:.88rem;color:var(--tinta-2);font-weight:600;font-variant-numeric:tabular-nums}
.chips span.destaque{background:var(--marca);border-color:var(--marca);color:#fff}
.papeis{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin-top:6px}
.papeis a{display:flex;flex-direction:column;gap:4px;text-decoration:none;border:1px solid var(--linha);background:var(--papel);border-radius:var(--raio);padding:14px 16px;min-width:0;transition:border-color .15s}
.papeis a:hover{border-color:var(--marca)}
.papeis b{color:var(--tinta);font-size:1.05rem}
.papeis b::after{content:" \\2192";color:var(--marca-tx)}
.papeis span{color:var(--tinta-3);font-size:.93rem;line-height:1.45}
nav.atalhos{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--papel);border-bottom:1px solid var(--linha)}
nav.atalhos .wrap{display:flex;gap:4px;overflow-x:auto;padding-block:6px;scrollbar-width:thin}
nav.atalhos a{flex:0 0 auto;text-decoration:none;color:var(--tinta-2);font-weight:600;font-size:.9rem;padding:6px 10px;border-radius:8px}
nav.atalhos a:hover{background:var(--marca-suave);color:var(--marca-forte)}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--papel)}
main section{padding-block:44px;border-bottom:1px solid var(--linha);scroll-margin-top:48px}
main section .wrap{display:flex;flex-direction:column;gap:18px}
main section.papel{background:var(--superficie-2)}
.fio{display:flex;flex-wrap:wrap;gap:6px;align-items:stretch}
.fio div{flex:1 1 140px;min-width:0;border:1px solid var(--linha);border-radius:10px;background:var(--papel);padding:10px 12px;display:flex;flex-direction:column;gap:2px}
.fio div b{color:var(--tinta);font-size:.95rem}
.fio div span{font-size:.84rem;color:var(--tinta-3);line-height:1.35}
.fio div small{font-size:.7rem;letter-spacing:.08em;text-transform:uppercase;font-weight:700;color:var(--marca-tx)}
/*fio-alternado*/
.modulo{display:flex;flex-direction:column;gap:12px}
.modulo>header{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 14px;border-bottom:2px solid var(--marca);padding-bottom:6px}
.modulo>header h3{font-size:1.2rem}
.modulo>header span{color:var(--tinta-3);font-size:.93rem}
.aulas{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
.aula{border:1px solid var(--linha);border-radius:var(--raio);background:var(--papel);padding:18px;display:flex;flex-direction:column;gap:12px;min-width:0}
.aula.marcada{border:2px solid var(--marca);padding:17px}
.aula .cab{display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap}
.aula .num{font-weight:800;color:var(--marca-forte);font-size:.9rem;letter-spacing:.04em}
.aula .data{font-variant-numeric:tabular-nums;color:var(--tinta-3);font-size:.9rem;font-weight:600}
.selo{background:var(--marca);color:#fff;border-radius:999px;padding:2px 10px;font-size:.75rem;font-weight:700;letter-spacing:.04em;text-transform:uppercase}
.aula h4{font-size:1.12rem;font-weight:700}
.aula .pergunta{color:var(--tinta-2);font-style:italic}
.aula .rot{font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:var(--tinta-3);font-weight:700}
.aula ol{margin:0;padding-left:1.3em;display:flex;flex-direction:column;gap:4px;font-size:.94rem}
.aula ol li::marker{color:var(--marca-tx);font-weight:700}
.aula .bloco{display:flex;flex-direction:column;gap:4px;font-size:.94rem}
.aula details{border:0;padding:0;background:transparent}
.aula summary{font-size:.94rem}
.aula details ul{margin:6px 0 0;padding-left:1.2em;font-size:.93rem;color:var(--tinta-2)}
.noite{display:flex;flex-direction:column;border:1px solid var(--linha);border-radius:var(--raio);overflow:hidden}
.faixa{display:grid;grid-template-columns:118px minmax(0,1.25fr) minmax(0,1fr);gap:16px;align-items:center;padding:12px 16px;border-bottom:1px solid var(--linha);background:var(--papel)}
.faixa:last-child{border-bottom:0}
.faixa.cab{background:var(--superficie-2);padding-block:8px}
.faixa.cab span{font-size:.74rem;letter-spacing:.07em;text-transform:uppercase;color:var(--tinta-3);font-weight:700}
.faixa .hora{font-variant-numeric:tabular-nums;font-weight:700;color:var(--tinta)}
.faixa .txt{display:flex;flex-direction:column;gap:2px;min-width:0}
.faixa .txt b{color:var(--tinta)}
.faixa .txt span{font-size:.92rem;color:var(--tinta-2);line-height:1.45}
.faixa.fixo{background:var(--marca-suave)}
.trilho{position:relative;height:14px;background:var(--superficie-3);border-radius:7px}
.trilho i{position:absolute;top:0;bottom:0;background:var(--marca);border-radius:7px}
.trilho i.pausa{background:var(--linha-forte)}
.regua{position:relative;height:18px}
.regua span{position:absolute;top:0;font-size:.74rem;font-weight:700;color:var(--tinta-3);font-variant-numeric:tabular-nums;transform:translateX(-50%)}
.regua span:first-child{transform:none}
.regua span:last-child{transform:translateX(-100%)}
.nota{font-size:.93rem;color:var(--tinta-3);max-width:72ch}
.colunas{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}
.colunas>div{min-width:0;display:flex;flex-direction:column;gap:10px}
.cartao{border:1px solid var(--linha);border-radius:var(--raio);background:var(--papel);padding:18px}
ul.marcas{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px}
ul.marcas li{display:grid;grid-template-columns:18px 1fr;gap:8px}
ul.marcas li::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--marca);margin-top:.6em}
ol.passos{margin:0;padding:0;list-style:none;counter-reset:p;display:flex;flex-direction:column;gap:12px}
ol.passos>li{counter-increment:p;display:grid;grid-template-columns:32px minmax(0,1fr);gap:12px;align-items:start}
ol.passos>li::before{content:counter(p);width:28px;height:28px;border-radius:50%;background:var(--marca);color:#fff;font-weight:800;display:grid;place-items:center;font-size:.9rem}
ol.passos>li>div{display:flex;flex-direction:column;gap:6px;min-width:0}
.cmd{display:flex;align-items:stretch;border:1px solid var(--linha);border-radius:8px;background:var(--superficie-2);overflow:hidden;max-width:100%}
.cmd pre{margin:0;padding:8px 12px;overflow-x:auto;flex:1;min-width:0;font-family:var(--f-codigo);font-size:.86rem;color:var(--tinta)}
.cmd button{flex:0 0 auto;border:0;border-left:1px solid var(--linha);background:var(--papel);color:var(--marca-tx);font:600 .82rem var(--f-texto);padding:0 12px;cursor:pointer}
.cmd button:hover{background:var(--marca-suave)}
.alerta{border:1px solid #F3D9A4;background:var(--aviso-suave);border-radius:var(--raio);padding:16px 18px;display:flex;flex-direction:column;gap:10px}
.alerta h3{color:var(--aviso)}
.rolagem{overflow-x:auto;border:1px solid var(--linha);border-radius:var(--raio);background:var(--papel)}
table{border-collapse:collapse;width:100%;font-size:.93rem}
table.larga{min-width:760px}
th,td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid var(--linha)}
th{font-size:.74rem;letter-spacing:.07em;text-transform:uppercase;color:var(--tinta-3);background:var(--superficie-2)}
tr:last-child td{border-bottom:0}
td.nowrap{white-space:nowrap;font-weight:700;color:var(--tinta);font-variant-numeric:tabular-nums}
td ul{margin:0;padding-left:1.1em}
details{border:1px solid var(--linha);border-radius:10px;padding:10px 14px;background:var(--papel)}
summary{cursor:pointer;font-weight:700;color:var(--tinta)}
.rodape{padding-block:28px 44px;color:var(--tinta-3);font-size:.9rem}
.rodape .wrap{display:flex;flex-direction:column;gap:6px}
:focus-visible{outline:3px solid var(--marca);outline-offset:2px;border-radius:4px}
@media (max-width:720px){
  body{font-size:16px}
  .faixa{grid-template-columns:1fr;gap:6px}
  .faixa.cab{display:none}
}
"""

JS = r"""
(function () {
  function hoje() { var d = new Date(); return d.getFullYear() * 10000 + (d.getMonth() + 1) * 100 + d.getDate(); }
  var h = hoje(), alvo = null;
  document.querySelectorAll(".aula[data-dia]").forEach(function (el) {
    if (!alvo && Number(el.getAttribute("data-dia")) >= h) alvo = el;
  });
  if (alvo) {
    var e_hoje = Number(alvo.getAttribute("data-dia")) === h;
    alvo.classList.add("marcada");
    var selo = alvo.querySelector(".selo");
    selo.textContent = e_hoje ? "Hoje, 19h" : "Próxima";
    selo.hidden = false;
    var chip = document.getElementById("chip-proxima");
    chip.textContent = (e_hoje ? "Hoje: " : "Próxima aula: ") + alvo.getAttribute("data-rotulo");
    chip.hidden = false;
  }
  document.querySelectorAll(".cmd button").forEach(function (b) {
    b.addEventListener("click", function () {
      var pre = b.parentNode.querySelector("pre");
      var ok = function () { b.textContent = "Copiado"; setTimeout(function () { b.textContent = "Copiar"; }, 1600); };
      var selecionar = function () {
        var r = document.createRange(); r.selectNodeContents(pre);
        var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
        b.textContent = "Selecionado";
      };
      try { navigator.clipboard.writeText(pre.textContent).then(ok, selecionar); } catch (err) { selecionar(); }
    });
  });
})();
"""


def itens(lista):
    return '<ul class="marcas">' + "".join(f"<li><span>{inline(x)}</span></li>" for x in lista) + "</ul>"


def cmd(texto):
    return f'<div class="cmd"><pre>{escape(texto)}</pre><button type="button">Copiar</button></div>'


def sem_numero(titulo):
    return re.sub(r"^Prática \d+ · ", "", titulo)


def dia_num(data):
    d, m, a = re.search(r"(\d{2})/(\d{2})/(\d{4})", data).groups()
    return int(a + m + d)


def rotulo(meta):
    mod, num = meta["aula"].split("·")[0].strip(), meta["id"][-1]
    return f"{mod} · {num}"


def primeira_frase(texto):
    texto = re.sub(r"\s*\([^)]*\)", "", texto)
    return texto.split(". ")[0].rstrip(".") + "."


def ementa():
    """Objetivo e prática de cada aula nas ementas de turma.EMENTAS."""
    saida = {}
    for caminho in EMENTAS:
        texto = (RAIZ / caminho).read_text(encoding="utf-8")
        for bloco in texto.split("## Aula ")[1:]:
            ident = "m{}_a{}".format(*bloco.split(" ")[0].split("."))
            objetivo = re.search(r"- Objetivo: (.+)", bloco).group(1).strip()
            pratica = re.search(r"- Prática: (.+)", bloco).group(1).strip()
            saida[ident] = (objetivo, pratica)
    return saida


def links():
    """Links publicados, lidos da tabela 'Páginas publicadas' do README."""
    saida = {}
    for m, n, guia, monitor in re.findall(r"^\| M(\d) · (\d) \| (https://\S+) \| (https://\S+) \|", (RAIZ / "README.md").read_text(encoding="utf-8"), re.M):
        saida[f"m{m}_a{n}"] = (guia, monitor)
    return saida


def grade(slides, meta):
    com_horarios(meta, slides)
    blocos = []
    for x in momentos(slides):
        nome = "Abertura e mapa" if x["bloco"] in ("Abertura", "Mapa da aula") else x["bloco"]
        if blocos and blocos[-1]["nome"] == nome:
            blocos[-1]["fim"], blocos[-1]["min"] = x["fim"], blocos[-1]["min"] + x["min"]
        else:
            blocos.append({"nome": nome, "ini": x["ini"], "fim": x["fim"], "min": x["min"]})
    return blocos


def estudo_no_repo(meta):
    if not REPO:
        return escape(f"{meta['pasta']}/estudo-dirigido.pdf")
    return f'<a href="{REPO}/blob/main/{pdf_estudo(meta)}">PDF no repositório</a>'


def cartoes(lista):
    return "\n".join(f'<div class="cartao"><h3>{escape(t)}</h3>{itens(x)}</div>' for t, x in lista)


def alerta(par):
    return f'<div class="alerta"><h3>{escape(par[0])}</h3>{itens(par[1])}</div>'


def montar():
    fontes = {i: importlib.import_module(i) for i in AULAS}
    em, lk = ementa(), links()
    faltam = [i for i in AULAS if i not in em or i not in lk]
    if faltam:
        sys.exit(f"Sem ementa ou link para: {', '.join(faltam)}")
    N, C, A, M, K = G["noite"], G["caso"], G["alunos"], G["monitores"], G["coordenacao"]
    grades = {i: grade(f.SLIDES, f.META) for i, f in fontes.items()}
    padrao = grades[N["padrao"]]
    excecoes = [i for i in AULAS if [(b["nome"], b["ini"], b["fim"]) for b in grades[i]] != [(b["nome"], b["ini"], b["fim"]) for b in padrao]]
    if excecoes != N["excecoes"]:
        sys.exit(f"Grade fora do previsto: as aulas {excecoes} diferem do padrão; revise a nota da seção 'Uma noite de aula'.")
    g = {i: {b["nome"]: {"ini": hm(b["ini"]), "fim": hm(b["fim"]), "min": b["min"]} for b in grades[i]} for i in AULAS}
    inicio, duracao = padrao[0]["ini"], fontes[N["padrao"]].META["duracao"]
    monitor = next(b for b in padrao if b["nome"] == "Monitor")

    metas = [fontes[i].META for i in AULAS]
    primeira, ultima = metas[0]["data"], metas[-1]["data"]
    mods = modulos(AULAS)
    alternados = [m.lower() for k, m in enumerate(mods) if k % 2]
    css = CSS.replace("/*fio-alternado*/", ",".join(f".fio div.{m}" for m in alternados) + "{background:var(--superficie-2)}" if alternados else "")

    # Percurso: um nó por aula
    fio = "".join(
        f'<div class="{i.split("_")[0] if i.split("_")[0] in alternados else ""}"><small>{escape(rotulo(fontes[i].META))}</small>'
        f'<b>{escape(fontes[i].META["titulo"].split(":")[0])}</b>'
        f'<span>{escape(fontes[i].META["pergunta"][0].upper() + fontes[i].META["pergunta"][1:])}</span></div>'
        for i in AULAS)

    # Cartões das aulas, agrupados por módulo
    por_modulo = []
    for mod in mods:
        ids = [i for i in AULAS if i.split("_")[0].upper() == mod]
        cards = []
        for i in ids:
            f = fontes[i]
            meta = f.META
            conceitos = "".join(f"<li>{inline(c['titulo'])}</li>" for c in f.ESTUDO["conceitos"])
            praticas = "".join(f"<li>{inline(sem_numero(p['titulo']))}</li>" for p in f.ESTUDO["praticas"])
            hora_monitor = hm(next(b for b in grades[i] if b["nome"] == "Monitor")["ini"])
            cards.append(f"""<article class="aula" id="aula-{i.replace('_', '-')}" data-dia="{dia_num(meta['data'])}" data-rotulo="{escape(meta['data'].split('/20')[0])} · {escape(rotulo(meta))}">
<div class="cab"><span class="num">{escape(rotulo(meta))}</span><span class="data">{escape(meta['data'])}</span><span class="selo" hidden></span></div>
<h4>{escape(meta['titulo'])}</h4>
<p class="pergunta">{escape(meta['pergunta'][0].upper() + meta['pergunta'][1:])}</p>
<div class="bloco"><span class="rot">Cinco conceitos</span><ol>{conceitos}</ol></div>
<div class="bloco"><span class="rot">Na demonstração</span><p>{inline(f.PLANO['demo_resumo'])}</p></div>
<div class="bloco"><span class="rot">Monitor, {hora_monitor}</span><p>{inline(f.MONITOR['apresentacao']['titulo'])}</p></div>
<details><summary>Estudo dirigido: três práticas</summary><ul>{praticas}</ul></details>
</article>""")
        por_modulo.append(f"""<div class="modulo"><header><h3>{escape(fontes[ids[0]].META['modulo'])}</h3><span>O {mod} {escape(G['modulos'][mod])}.</span></header>
<div class="aulas">{''.join(cards)}</div></div>""")

    # Uma noite de aula
    faixas = []
    for b in padrao:
        esq = (b["ini"] - inicio) / duracao * 100
        larg = b["min"] / duracao * 100
        fixo = b["nome"] in ("Intervalo", "Monitor")
        faixas.append(
            f'<div class="faixa{" fixo" if fixo else ""}"><span class="hora">{hm(b["ini"])}–{hm(b["fim"])}</span>'
            f'<div class="txt"><b>{escape(b["nome"])} · {b["min"]} min{" · fixo" if fixo else ""}</b><span>{escape(N["blocos"][b["nome"]])}</span></div>'
            f'<div class="trilho" aria-hidden="true"><i class="{"pausa" if b["nome"] == "Intervalo" else ""}" style="left:{esq:.2f}%;width:{larg:.2f}%"></i></div></div>')
    horas = range(-(-inicio // 60) * 60, inicio + duracao + 1, 60)
    regua = "".join(f'<span style="left:{round((h - inicio) / duracao * 100, 3):g}%">{h // 60}h</span>' for h in horas)

    # Monitores
    durante = "".join(f'<tr><td class="nowrap">{escape(momento)}</td><td>{inline(acao)}</td></tr>' for momento, acao in M["durante"])
    temas = "".join(
        f'<tr><td class="nowrap">{escape(rotulo(fontes[i].META))}<br><span style="font-weight:500;color:var(--tinta-3)">{escape(fontes[i].META["data"][:10])}</span></td>'
        f'<td>{inline(fontes[i].MONITOR["apresentacao"]["titulo"])}</td>'
        f'<td>{inline(primeira_frase(fontes[i].MONITOR["apresentacao"]["alternativa"]))}</td>'
        f'<td class="nowrap"><a href="{lk[i][1]}">Guia do monitor</a></td></tr>' for i in AULAS)

    # Coordenação
    cobertura = "".join(
        f'<tr><td class="nowrap">{escape(rotulo(fontes[i].META))}</td><td>{inline(em[i][0])}</td>'
        f'<td><b>{escape(fontes[i].META["titulo"])}.</b> {inline(fontes[i].PLANO["demo_resumo"])}</td>'
        f'<td><span style="color:var(--tinta-3)">Ementa: {inline(em[i][1])}</span><ul>'
        + "".join(f"<li>{inline(sem_numero(p['titulo']))}</li>" for p in fontes[i].ESTUDO["praticas"])
        + "</ul></td></tr>" for i in AULAS)
    materiais = "".join(
        f'<tr><td class="nowrap">{escape(rotulo(fontes[i].META))}</td><td class="nowrap">{escape(fontes[i].META["data"][:10])}</td>'
        f'<td><a href="{lk[i][0]}">Guia interativo</a></td><td><a href="{lk[i][1]}">Guia do monitor</a></td>'
        f'<td>{estudo_no_repo(fontes[i].META)}</td></tr>' for i in AULAS)

    id_caso, titulo_caso = C["slide"]
    caso = next(s for s in fontes[id_caso].SLIDES if s["titulo"].startswith(titulo_caso))
    fio_caso = "".join(f'<div><b>{escape(n[0])}</b><span>{escape(" ".join(n[1]) if isinstance(n[1], list) else n[1])}</span></div>'
                       for n in caso["fluxo"]["nos"])
    preparo = "\n".join(f"<li><div><p>{inline(texto)}</p>{cmd(comando)}</div></li>" for texto, comando in A["preparo"])
    nomes = escape(juntar(mods))

    corpo = f"""<title>Guia dos módulos {nomes}</title>
<meta name="claude:viewport-fit-sides" content="cover">
{FONTES}
<style>{css}</style>
<header class="topo"><div class="wrap">
<p class="sobre">{escape(CURSO)} · {escape(ORG)} · Turma {escape(TURMA)}</p>
<h1>Como vão funcionar os módulos {nomes}</h1>
<p class="lide">{inline(G['lide'].format(primeira=primeira[5:10], ultima=ultima[5:10]))}</p>
<div class="chips"><span>{escape(primeira[5:10])} a {escape(ultima[5:])}</span><span>{escape(G['agenda'])}</span><span>{len(AULAS)} aulas · {sum(m['duracao'] for m in metas) / 60:g} horas</span><span>Professor: {escape(DOCENTE)}</span><span class="destaque" id="chip-proxima" hidden></span></div>
<div class="papeis">
<a href="#alunos"><b>Alunos</b><span>O que acontece na aula, o que fazer depois e como preparar o computador.</span></a>
<a href="#monitores"><b>Monitores</b><span>O rodízio, o que fazer em cada momento e os temas dos {monitor['min']} minutos.</span></a>
<a href="#coordenacao"><b>Coordenação</b><span>O formato desta turma, a cobertura da ementa e o que cada aula entrega.</span></a>
</div>
</div></header>
<nav class="atalhos" aria-label="Seções"><div class="wrap">
<a href="#percurso">Percurso</a><a href="#noite">Uma noite de aula</a><a href="#caso">Caso {escape(CASO)}</a><a href="#alunos">Alunos</a><a href="#monitores">Monitores</a><a href="#coordenacao">Coordenação</a><a href="#links">Links</a>
</div></nav>
<main>
<section id="percurso"><div class="wrap">
<p class="sobre">O percurso</p>
<h2>{escape(G['percurso']['titulo'])}</h2>
<p class="prosa">{inline(G['percurso']['texto'])}</p>
<div class="fio" role="list" aria-label="{escape(G['percurso']['rotulo'])}">{fio}</div>
{''.join(por_modulo)}
</div></section>
<section id="noite"><div class="wrap">
<p class="sobre">Uma noite de aula</p>
<h2>{escape(N['titulo'])}</h2>
<p class="prosa">{inline(N['texto'].format(g=g))}</p>
<div class="noite">
<div class="faixa cab"><span>Horário</span><span>Momento</span><div class="regua">{regua}</div></div>
{''.join(faixas)}
</div>
</div></section>
<section id="caso"><div class="wrap">
<p class="sobre">O caso</p>
<h2>{escape(C['titulo'])}</h2>
<p class="prosa">{inline(C['texto'])}</p>
<div class="fio" role="list" aria-label="{escape(C['rotulo'])}">{fio_caso}</div>
<div class="colunas">
{cartoes(C['cartoes'])}
</div>
<p class="nota">{inline(C['nota'])}</p>
</div></section>
<section id="alunos" class="papel"><div class="wrap">
<p class="sobre">Para alunos</p>
<h2>{escape(A['titulo'])}</h2>
<div class="colunas">
{cartoes(A['cartoes'])}
</div>
<h3>{escape(A['preparo_titulo'])}</h3>
<ol class="passos">
{preparo}
</ol>
{alerta(A['alerta'])}
</div></section>
<section id="monitores"><div class="wrap">
<p class="sobre">Para monitores</p>
<h2>{escape(M['titulo'])}</h2>
<p class="prosa">{inline(M['texto'])}</p>
<div class="colunas">
{cartoes(M['cartoes'])}
</div>
<h3>O que você faz em cada momento da aula</h3>
<div class="rolagem"><table><thead><tr><th>Momento</th><th>Você</th></tr></thead><tbody>{durante}</tbody></table></div>
{alerta(M['alerta'])}
<h3>Os temas dos {monitor['min']} minutos</h3>
<p class="prosa">{inline(M['temas_texto'])}</p>
<div class="rolagem"><table class="larga"><thead><tr><th>Aula</th><th>Tema sugerido</th><th>Alternativa</th><th>Guia</th></tr></thead><tbody>{temas}</tbody></table></div>
</div></section>
<section id="coordenacao" class="papel"><div class="wrap">
<p class="sobre">Para a coordenação</p>
<h2>{escape(K['titulo'])}</h2>
<div class="colunas">
{cartoes(K['cartoes'])}
</div>
<h3>Cobertura da ementa, aula a aula</h3>
<div class="rolagem"><table class="larga"><thead><tr><th>Aula</th><th>Objetivo na ementa</th><th>Como a aula cobre</th><th>Prática: na ementa e no estudo dirigido</th></tr></thead><tbody>{cobertura}</tbody></table></div>
</div></section>
<section id="links"><div class="wrap">
<p class="sobre">Links</p>
<h2>Materiais publicados de cada aula</h2>
<div class="rolagem"><table class="larga"><thead><tr><th>Aula</th><th>Data</th><th>Guia interativo</th><th>Guia do monitor</th><th>Estudo dirigido</th></tr></thead><tbody>{materiais}</tbody></table></div>
<p class="prosa">{inline(G['links_texto'])}</p>
<p class="nota">Os botões ao vivo dos guias interativos rodam o Claude dentro do claude.ai e pedem permissão a quem abre.</p>
</div></section>
</main>
<footer class="rodape"><div class="wrap">
<p>{escape(metas[0]['curso'])} · Turma {escape(TURMA)} · {nomes} · Professor {escape(DOCENTE)}</p>
</div></footer>
<script>{JS}</script>
"""
    return ('<!doctype html>\n<html lang="pt-BR"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"></head><body>\n'
            '<!-- publicar:inicio -->\n' + corpo + '<!-- publicar:fim -->\n</body></html>\n')


def main():
    destino = RAIZ / "guia-modulos.html"
    destino.write_text(montar(), encoding="utf-8", newline="\n")
    print(f"Gerado {destino.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
