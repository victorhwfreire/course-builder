"""Gera o guia interativo canônico de uma aula.

Uso, na pasta da turma: python -B preparacao/guias/gerar_guia.py m3_a1
Conteúdo: preparacao/guias/conteudo_<id>.py; figuras: os fluxogramas dos slides da aula;
pedidos e saídas: pedidos.json e execucoes.json (execuções reais, sem edição); CSS: modelo.html;
JavaScript: motor.js, com agente_caso.js no lugar da linha /*@inclui agente_caso.js*/.
Saída: M<m>/aula-<n>/guia-interativo.html, que abre por duplo clique; o trecho entre
publicar:inicio e publicar:fim é o corpo publicado como Artifact (extrair_corpo.py).
"""
import html
import importlib
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
PREP = AQUI.parent
RAIZ = PREP.parent
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(PREP))
sys.path.insert(0, str(PREP / "aulas"))
import figuras  # noqa: E402
from agente_caso import descrever_ferramentas  # noqa: E402
from turma import CASO, CASO_PASTA, CURSO, ORG, TURMA  # noqa: E402

e = html.escape
MODELO = (AQUI / "modelo.html").read_text(encoding="utf-8")
CSS = re.search(r"<style>(.*?)</style>", MODELO, re.S).group(1) + """
.figura{overflow-x:auto;border:1px solid var(--linha);border-radius:var(--raio);background:#fff;padding:10px}
.figura svg{display:block;width:100%;min-width:640px;height:auto}
.barra-composto{height:30px;border-radius:9px;border:2px solid var(--tinta);overflow:hidden;background:var(--superficie)}
.barra-composto span{display:block;height:100%;background:var(--marca);transition:width .25s}
.controles input[type=range]{accent-color:var(--marca);width:min(260px,100%)}
.valor{font-family:var(--f-codigo);font-weight:700;color:var(--tinta)}
tr.dest td{background:var(--marca-suave);font-weight:700}
.voltas{display:flex;flex-direction:column;gap:8px}
.volta{display:grid;grid-template-columns:86px 1fr;gap:10px;align-items:start;border:1px solid var(--linha);border-radius:10px;padding:10px 12px;background:var(--superficie)}
.volta small{font:700 .74rem var(--f-codigo);color:var(--marca-forte);text-transform:uppercase;letter-spacing:.05em;padding-top:3px}
.volta code{white-space:nowrap}
@media (max-width:560px){.volta{grid-template-columns:1fr}}
.vivo-extra{display:flex;flex-direction:column;gap:10px;margin-top:18px;padding-top:16px;border-top:1px solid var(--linha)}
.vivo-tit{margin:0;font-weight:700;color:var(--tinta)}
blockquote.citacao{margin:.4em 0;padding:.4em .9em;border-left:3px solid var(--marca);background:var(--marca-suave);border-radius:0 8px 8px 0}
.volta small.ok{font:600 .78rem var(--f-codigo);color:var(--tinta-3);text-transform:none;letter-spacing:0;overflow-wrap:anywhere}
.volta small.erro{font:700 .78rem var(--f-codigo);color:var(--erro);text-transform:none;letter-spacing:0;overflow-wrap:anywhere}
.controles input[type=number]{font:inherit;width:9em;max-width:100%;padding:6px 8px;border:1px solid var(--linha-forte);border-radius:8px;background:var(--superficie);color:var(--tinta)}
"""
DADOS_CASO = RAIZ / "material-alunos" / CASO_PASTA / "dados"
MARCA_CASO = "  /*@inclui agente_caso.js*/\n"


def arquivos_do_caso():
    return {p.name: p.read_text(encoding="utf-8") for p in sorted(DADOS_CASO.iterdir()) if p.is_file()}


def motor():
    js = (AQUI / "motor.js").read_text(encoding="utf-8")
    if MARCA_CASO not in js:
        sys.exit(f"motor.js sem a linha {MARCA_CASO.strip()}")
    return js.replace(MARCA_CASO, (AQUI / "agente_caso.js").read_text(encoding="utf-8"))


MOTOR = motor()
REG = json.loads((AQUI / "execucoes.json").read_text(encoding="utf-8"))["execucoes"]
PEDIDOS = json.loads((AQUI / "pedidos.json").read_text(encoding="utf-8"))


class Contexto:
    def __init__(self, fonte):
        self.fonte, self.meta, self.slides = fonte, fonte.META, fonte.SLIDES
        self.arquivos = arquivos_do_caso()
        self.txt, self.bancadas, self.pedidos_usados = {}, {}, set()

    def reg(self, chave, n=1):
        return next(x for x in REG[chave] if x["n"] == n)

    def saida(self, chave, n=1, rotulo=None):
        item = self.reg(chave, n)
        tid = f"txt-{chave}-{n}"
        self.txt[tid] = item["saida"]
        return {"saida": tid, "rotulo": rotulo or f"Registrada · execução {n}", "detalhe": f"{item['modelo']} · {item['data']} · texto sem edição"}

    def pedido(self, chave, rotulo="Pedido enviado, texto exato"):
        self.pedidos_usados.add(chave)
        return {"pedido": chave, "rotulo": rotulo}

    def figura(self, n):
        fluxo = self.slides[n - 1]["fluxo"]
        svg, _ = figuras.desenhar(fluxo, f"g{n}")
        return f'<div class="figura">{svg}</div>'

    def bancada(self, pref, b, numero):
        selo = b.get("selo", f"Bancada {numero}")
        real = " real" if b.get("real") else ""
        cab = f'<div class="bancada-cab"><span class="selo{real}">{e(selo)}</span><h3>{b["h3"]}</h3><p>{b["p"]}</p></div>'
        cfg = {k: v for k, v in b.items() if k not in ("h3", "p", "selo", "real", "aviso", "chave_html")}
        t = b["tipo"]
        if t == "passos":
            corpo = (f'<div class="passos-nav"><div class="pontos" id="{pref}-pontos" role="group" aria-label="Passos"></div>'
                     f'<button type="button" class="btn sec" id="{pref}-voltar">Voltar</button>'
                     f'<button type="button" class="btn" id="{pref}-avancar">Próximo passo</button></div>'
                     f'<div class="passo-tit"><small id="{pref}-cont"></small><strong id="{pref}-tit"></strong></div>'
                     f'<div class="explica" id="{pref}-explica" aria-live="polite"></div><div id="{pref}-corpo"></div>')
            if b.get("vivo"):
                self.pedidos_usados.add(b["vivo"])
                corpo += (f'<details class="revelar" data-ao-vivo hidden><summary>Ver o pedido que o botão envia</summary><div>'
                          f'<div class="pedido"><small>Pedido enviado, texto exato</small>{e(PEDIDOS[b["vivo"]])}</div></div></details>'
                          f'<div class="controles" data-ao-vivo hidden><button type="button" class="btn vivo" id="{pref}-rodar">{e(b.get("vivo_rotulo", "Rodar agora"))}</button>'
                          f'<span class="aviso-vivo" id="{pref}-aviso"></span></div>'
                          f'<div class="saida" data-ao-vivo hidden><div class="saida-cab"><b>Ao vivo</b><span>o mesmo pedido, rodado agora</span></div>'
                          f'<div class="saida-corpo" id="{pref}-vivo"><p class="pensando">Clique no botão para uma nova execução.</p></div></div>')
            if b.get("agente"):
                ag = b["agente"]
                self.pedidos_usados.add(ag["chave"])
                ferramentas_txt = descrever_ferramentas(ag)
                corpo += (f'<div class="vivo-extra" data-ao-vivo hidden><p class="vivo-tit">{e(ag["titulo"])}</p>'
                          f'<details class="revelar"><summary>Ver o pedido e as ferramentas que o botão oferece</summary><div>'
                          f'<div class="pedido"><small>Pedido enviado, texto exato</small>{e(PEDIDOS[ag["chave"]])}</div>'
                          f'<p>Ferramentas da página: {ferramentas_txt}</p></div></details>'
                          f'<div class="controles"><button type="button" class="btn vivo" id="{pref}-agente">{e(ag["rotulo"])}</button>'
                          f'<span class="aviso-vivo" id="{pref}-agaviso"></span></div>'
                          f'<div class="voltas" id="{pref}-agvoltas" aria-live="polite"></div>'
                          f'<div class="saida"><div class="saida-cab"><b>Ao vivo</b><span>o agente, rodado agora</span></div>'
                          f'<div class="saida-corpo" id="{pref}-agvivo"><p class="pensando">Clique no botão para uma nova execução.</p></div></div></div>')
        elif t == "quiz":
            corpo = (f'<div class="nota" style="max-width:none"><b>A chave</b><span>{b["chave_html"]}</span></div>' if b.get("chave_html") else "")
            corpo += f'<div class="quiz" id="{pref}-quiz"></div>'
        elif t == "composto":
            corpo = (f'<div class="controles"><label class="campo" for="{pref}-acerto">Acerto em cada passo: <span class="valor" id="{pref}-va"></span>'
                     f'<input type="range" id="{pref}-acerto" min="80" max="99" step="1" value="95"></label>'
                     f'<label class="campo" for="{pref}-passos">Passos em sequência: <span class="valor" id="{pref}-vp"></span>'
                     f'<input type="range" id="{pref}-passos" min="1" max="30" step="1" value="10"></label></div>'
                     f'<div class="barra-composto" id="{pref}-barra" role="img" aria-label="Acerto da execução inteira"></div>'
                     f'<div class="explica" id="{pref}-explica" aria-live="polite"></div><div id="{pref}-tab"></div>')
        elif t == "custo":
            padrao = {"chamadas": 3, "entrada": 60000, "cache": 90, "saida": 1000, "pin": 5, "pcache": 0.5, "pout": 25, "sucesso": 80}
            padrao.update(b.get("valores", {}))
            rotulos = [("chamadas", "Chamadas ao modelo por tarefa", 1), ("entrada", "Tokens de entrada por chamada", 1000),
                       ("cache", "% da entrada lida do cache", 5), ("saida", "Tokens de saída por chamada", 100),
                       ("pin", "US$ por milhão, entrada", 0.25), ("pcache", "US$ por milhão, cache lido", 0.05),
                       ("pout", "US$ por milhão, saída", 0.5), ("sucesso", "% de tarefas resolvidas", 5)]
            corpo = '<div class="controles">' + "".join(
                f'<label class="campo" for="{pref}-{k}">{e(r)}<input type="number" id="{pref}-{k}" value="{padrao[k]}" min="0" step="{p}"></label>'
                for k, r, p in rotulos) + "</div>"
            corpo += f'<div class="explica" id="{pref}-explica" aria-live="polite"></div><div id="{pref}-res"></div>'
        else:
            raise ValueError(f"bancada de tipo desconhecido: {t}")
        if b.get("aviso"):
            corpo += f'<p class="aviso-vivo">{b["aviso"]}</p>'
        self.bancadas[pref] = cfg
        return f'<div class="bancada" id="{pref}">{cab}<div class="bancada-corpo">{corpo}</div></div>'


def secao_conceito(ctx, i, c, total):
    return f'''<section class="secao" id="c{i}"><div class="wrap">
<div class="secao-cab"><p class="sobrelinha"><i>{i}</i> Conceito {i} de {total} · {e(c["tema"])}</p><h2>{e(c["h2"])}</h2></div>
<div class="definicao"><span class="rot">Definição</span><p>{c["definicao"]}</p></div>
<div class="prosa">{"".join(f"<p>{p}</p>" for p in c["prosa"])}</div>
<figure class="figura-wrap" aria-label="{e(ctx.slides[c["slide"] - 1]["fluxo"]["descricao"])}">{ctx.figura(c["slide"])}</figure>
{ctx.bancada(f"b-c{i}", c["bancada"], i)}
<div class="nota regra"><b>Na prática</b><span>{c["pratica"]}</span></div>
<details class="revelar"><summary>Pergunta para pensar: {c["pergunta"][0]}</summary><div><p>{c["pergunta"][1]}</p></div></details>
</div></section>'''


def montar(ident):
    fonte = importlib.import_module(ident)
    ctx = Contexto(fonte)
    G = importlib.import_module(f"conteudo_{ident}").construir(ctx)
    meta = ctx.meta
    n = len(G["conceitos"])
    nav = ('<li><a href="#partida">Ponto de partida</a></li>'
           + "".join(f'<li><a href="#c{i}">{i} {e(c["nav"])}</a></li>' for i, c in enumerate(G["conceitos"], 1))
           + '<li><a href="#demo">Demonstração</a></li><li><a href="#discussao">Discussão</a></li>'
             '<li><a href="#cartao">Cartão</a></li><li><a href="#fechamento">Fechamento</a></li>')
    fio = "".join(f'<a href="#c{i}"><span class="n">{i}</span><strong>{e(c["nav"])}</strong><span class="d">{e(c["fio"])}</span></a>'
                  for i, c in enumerate(G["conceitos"], 1))
    fio += f'<a href="#fechamento"><span class="n">?</span><strong>A pergunta</strong><span class="d">{e(G["pergunta"])}</span></a>'
    conceitos = "".join(secao_conceito(ctx, i, c, n) for i, c in enumerate(G["conceitos"], 1))
    atos = "".join(ctx.bancada(f"b-ato{k}", ato, k) for k, ato in enumerate(G["demo"]["atos"], 1))
    d = G["discussao"]
    ideias = "<br>".join(f"<b>{i}.</b> {x}" for i, x in enumerate(G["cartao"]["ideias"], 1))
    mapa = "".join(f"<div><small>{i} · {e(c['nav'])}</small><strong>{x[0]}</strong><p>{x[1]}</p></div>"
                   for i, (c, x) in enumerate(zip(G["conceitos"], G["fechamento"]["mapa"]), 1))
    mapa += f'<div><small>Resposta</small><strong>{G["fechamento"]["resposta"][0]}</strong><p>{G["fechamento"]["resposta"][1]}</p></div>'
    corpo = f"""<title>{e(G['title'])}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800;1,9..40,400&display=swap">
<style>{CSS}</style>
<header class="trilha"><div class="wrap"><a class="marca" href="#topo">{e(meta['aula'].split('·')[0].strip())} · Aula {meta['id'][-1]}</a><nav aria-label="Seções da aula"><ol>{nav}</ol></nav></div></header>
<main>
<section class="abertura" id="topo"><div class="wrap">
<p class="sobrelinha">{e(meta['aula'])} · {e(meta['modulo'])} · {e(CURSO)} · {e(ORG)} · {e(meta['data'])}</p>
<h1>{G['h1']}</h1>
<p class="lide">{G['lide']}</p>
<nav class="fio" aria-label="O fio da aula">{fio}</nav>
<div class="como"><div><i>1</i><span><b>Leia a ideia</b>Cada seção abre com uma definição curta e um exemplo do caso {e(CASO)}.</span></div><div><i>2</i><span><b>Mexa na bancada</b>As bancadas são simuladores e passo a passos: mude uma opção ou avance um passo e veja o efeito.</span></div><div><i>3</i><span><b>Confira o real</b>Respostas marcadas como <b>registradas</b> vieram de execuções reais, sem edição. O botão <b>Rodar agora</b> chama o Claude ao vivo.</span></div></div>
<p class="carimbo"><span><b>Execuções registradas:</b> {G['carimbo']}</span><span><b>Caso:</b> {e(CASO)}, fictício</span></p>
</div></section>
<section class="secao" id="partida"><div class="wrap">
<div class="secao-cab"><p class="sobrelinha">Ponto de partida</p><h2>{G['partida']['h2']}</h2></div>
<div class="ambiente">{"".join(f"<div><b>{t}</b>{x}</div>" for t, x in G['partida']['ambiente'])}</div>
<div class="historia">{G['partida']['historia']}</div>
<div class="nota projeto"><b>A pergunta desta aula</b><span>{e(G['pergunta'])} Guarde a sua resposta de agora. No fim, a gente compara.</span></div>
</div></section>
{conceitos}
<section class="secao" id="demo"><div class="wrap">
<div class="secao-cab"><p class="sobrelinha">Demonstração · a mesma tarefa em dois atos</p><h2>{G['demo']['h2']}</h2></div>
<div class="prosa">{"".join(f"<p>{p}</p>" for p in G['demo']['prosa'])}</div>
{atos}
<p class="aviso-vivo" data-sem-ao-vivo>Os botões ao vivo aparecem quando esta página está aberta no Claude e você permite que ela use o Claude. As execuções registradas funcionam em qualquer lugar.</p>
</div></section>
<section class="secao" id="discussao"><div class="wrap">
<div class="secao-cab"><p class="sobrelinha">Discussão</p><h2>{d['h2']}</h2></div>
<div class="argumentos"><div><b>Argumento A</b>{d['a']}</div><div><b>Argumento B</b>{d['b']}</div><div class="q">{e(G['pergunta'])}</div></div>
{"".join(f'<details class="revelar"><summary>{q}</summary><div><p>{r}</p></div></details>' for q, r in d['revelar'])}
</div></section>
<section class="secao" id="cartao"><div class="wrap">
<div class="secao-cab"><p class="sobrelinha">Cartão de consulta</p><h2>O que levar para o trabalho amanhã</h2></div>
<div class="cartoes"><div><h4>As ideias</h4><p>{ideias}</p></div><div><h4>{G['cartao']['chave'][0]}</h4><p>{G['cartao']['chave'][1]}</p></div>
<div><h4>{G['cartao']['checklist'][0]}</h4><ul class="checklist">{"".join(f"<li>{x}</li>" for x in G['cartao']['checklist'][1])}</ul></div></div>
</div></section>
<section class="secao" id="fechamento"><div class="wrap">
<div class="secao-cab"><p class="sobrelinha">Fechamento</p><h2>{G['fechamento']['h2']}</h2></div>
<div class="mapa-final">{mapa}</div>
<div class="nota projeto"><b>{G['fechamento'].get('proximo_rotulo', 'Antes da próxima aula')}</b><span>{G['fechamento']['proximo']}</span></div>
</div></section>
</main>
<footer class="rodape"><div class="wrap">
<p><b>Sobre as execuções.</b> {G['rodape']}</p>
<p><b>Fontes citadas</b></p><ul>{"".join(f"<li>{x}</li>" for x in G['fontes'])}</ul>
<p>{e(CURSO)} · {e(ORG)} · {e(meta['modulo'])} · {e(meta['aula'])} · Turma {e(TURMA)} · {e(meta['docente'])}</p>
</div></footer>
"""
    dados = {"bancadas": ctx.bancadas, "pedidos": {k: PEDIDOS[k] for k in sorted(ctx.pedidos_usados)}}
    dados_json = json.dumps(dados, ensure_ascii=False).replace("</", "<\\/")
    corpo += "".join(f'<script type="text/plain" id="{tid}">{t.replace("</", "<\\/")}</script>\n' for tid, t in ctx.txt.items())
    corpo += f'<script type="application/json" id="dados-guia">{dados_json}</script>\n<script>\n{MOTOR}</script>\n'
    pagina = ('<!doctype html>\n<html lang="pt-BR"><head><meta charset="utf-8">'
              '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"></head><body>\n'
              "<!-- publicar:inicio -->\n" + corpo + "<!-- publicar:fim -->\n</body></html>\n")
    destino = RAIZ / meta["pasta"] / "guia-interativo.html"
    destino.write_text(pagina, encoding="utf-8", newline="\n")
    print(f"{destino.relative_to(RAIZ)} · {len(pagina)} caracteres · bancadas: {len(ctx.bancadas)} · saídas: {len(ctx.txt)} · pedidos: {len(ctx.pedidos_usados)}")


if __name__ == "__main__":
    montar(sys.argv[1] if len(sys.argv) > 1 else "m3_a1")
