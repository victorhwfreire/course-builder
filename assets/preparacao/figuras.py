"""Desenha os fluxogramas dos slides em SVG, no vocabulário de formas da disciplina.

Caixa cinza = etapa; tracejada = produzida por IA; borda verde = julgamento humano;
azul cheia = ponto de chegada; losango = decisão.
Um nó é (título, apoio, tipo); apoio é texto ou lista de linhas; tipo é passo, ia, humano ou foco.
"""

from html import escape

FONTE = "'Segoe UI', Arial, sans-serif"
# Classes com prefixo fx-: o <style> de um SVG embutido vale para a página inteira e colidiria com o CSS dela.
ESTILO = (
    ".fx-fundo{fill:#FFFFFF}"
    ".fx-passo{fill:#F3F5F9;stroke:#5B6B8C;stroke-width:2}"
    ".fx-ia{fill:#FFFFFF;stroke:#7A5CC8;stroke-width:2.5;stroke-dasharray:9 6}"
    ".fx-humano{fill:#FFFFFF;stroke:#1E8A5A;stroke-width:3.5}"
    ".fx-foco{fill:#1F4FD8;stroke:#1F4FD8;stroke-width:2}"
    ".fx-decisao{fill:#FFF6DB;stroke:#B8860B;stroke-width:2.5}"
    ".fx-faixa{fill:#EEF1F6}"
    f".fx-t{{fill:#1B2333;font-family:{FONTE}}}"
    ".fx-claro{fill:#FFFFFF}"
    ".fx-seta{stroke:#5B6B8C;stroke-width:2.5;fill:none}"
    ".fx-ponta{fill:#5B6B8C}"
    f".fx-rot{{fill:#3F4A5A;font-family:{FONTE};font-style:italic;text-transform:none;letter-spacing:0}}"
)
T1, T2 = 20, 16
# Largura média de um caractere em fração da fonte: estimativa conservadora para Segoe UI e Arial.
LARGURA = {T1: 0.56, T2: 0.50}
FOLGA = 24


def _linhas(apoio):
    if not apoio:
        return []
    return [apoio] if isinstance(apoio, str) else list(apoio)


def _cabe(texto, largura, tamanho):
    return len(texto) <= int((largura - FOLGA) / (tamanho * LARGURA[tamanho]))


class Figura:
    def __init__(self, uid):
        self.uid, self.partes, self.avisos = uid, [], []

    def _texto(self, cx, cy, linhas):
        alturas = [tam * 1.28 for _, tam, _ in linhas]
        y = cy - sum(alturas) / 2
        for (texto, tam, classe), alt in zip(linhas, alturas):
            peso = ' font-weight="700"' if tam == T1 else ""
            classes = " ".join("fx-" + c for c in classe.split())
            self.partes.append(f'<text class="{classes}" x="{cx:.0f}" y="{y + alt / 2:.1f}" font-size="{tam}"{peso} '
                               f'text-anchor="middle" dominant-baseline="central">{escape(texto)}</text>')
            y += alt

    def no(self, x, y, w, h, no):
        titulo, apoio, tipo = (no + ("passo",))[:3] if len(no) == 2 else no
        classe_t = "t claro" if tipo == "foco" else "t"
        self.partes.append(f'<rect class="fx-{tipo}" x="{x}" y="{y}" width="{w}" height="{h}" rx="14"/>')
        linhas = [(titulo, T1, classe_t)] + [(l, T2, classe_t) for l in _linhas(apoio)]
        for texto, tam, _ in linhas:
            if not _cabe(texto, w, tam):
                self.avisos.append(f"“{texto}” não cabe numa caixa de {w}px")
        self._texto(x + w / 2, y + h / 2, linhas)

    def losango(self, cx, cy, w, h, linhas):
        pts = f"{cx},{cy - h / 2} {cx + w / 2},{cy} {cx},{cy + h / 2} {cx - w / 2},{cy}"
        self.partes.append(f'<polygon class="fx-decisao" points="{pts}"/>')
        for texto in linhas:
            if not _cabe(texto, w * 0.62, T2):
                self.avisos.append(f"“{texto}” não cabe no losango")
        self._texto(cx, cy, [(t, T2, "t") for t in linhas])

    def seta(self, pontos, rotulo=None, em=None):
        d = " ".join(f"{x:.0f},{y:.0f}" for x, y in pontos)
        self.partes.append(f'<polyline class="fx-seta" points="{d}" marker-end="url(#{self.uid})"/>')
        if rotulo:
            self.partes.append(f'<text class="fx-rot" x="{em[0]:.0f}" y="{em[1]:.0f}" font-size="{T2}" '
                               f'text-anchor="middle" dominant-baseline="central">{escape(rotulo)}</text>')

    def faixa(self, x, y, w, h, texto):
        if not _cabe(texto, w, T2):
            self.avisos.append(f"faixa “{texto}” não cabe")
        self.partes.append(f'<rect class="fx-faixa" x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>')
        self._texto(x + w / 2, y + h / 2, [(texto, T2, "t")])

    def rotulo(self, x, y, texto, ancora="start"):
        self.partes.append(f'<text class="fx-t" x="{x}" y="{y}" font-size="{T1}" font-weight="700" '
                           f'text-anchor="{ancora}" dominant-baseline="central">{escape(texto)}</text>')

    def svg(self, w, h, descricao):
        d = escape(descricao, quote=True)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" '
                f'height="{h:.0f}" role="img" aria-label="{d}"><title>{d}</title><style>{ESTILO}</style>'
                f'<defs><marker id="{self.uid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" '
                f'markerHeight="8" orient="auto-start-reverse"><path class="fx-ponta" d="M0,0 L10,5 L0,10 z"/></marker></defs>'
                f'<rect class="fx-fundo" x="0" y="0" width="{w:.0f}" height="{h:.0f}" rx="16"/>{"".join(self.partes)}</svg>')


def _cadeia(f, fx):
    nos = fx["nos"]
    n = len(nos)
    w = {1: 260, 2: 260, 3: 260, 4: 210, 5: 196}.get(n, 186)
    gap = 48 if n <= 5 else 40
    h, m, topo = 112, 24, 24
    xs = [m + i * (w + gap) for i in range(n)]
    for i, (x, no) in enumerate(zip(xs, nos)):
        f.no(x, topo, w, h, no)
        if i:
            f.seta([(xs[i - 1] + w + 3, topo + h / 2), (x - 3, topo + h / 2)])
    altura = topo + h + m
    if fx.get("retorno"):
        base = topo + h + 40
        c0, c1 = xs[0] + w / 2, xs[-1] + w / 2
        f.seta([(c1, topo + h + 3), (c1, base), (c0, base), (c0, topo + h + 5)], fx["retorno"], ((c0 + c1) / 2, base + 22))
        altura = base + 52
    return xs[-1] + w + m, altura


def _convergencia(f, fx):
    (a, b), saida = fx["entradas"], fx["saida"]
    wl, hl, xl, y1 = 300, 104, 24, 24
    y2 = y1 + hl + 44
    xr, wr, hr = xl + wl + 140, 300, 124
    yr = (y1 + y2 + hl) / 2 - hr / 2
    f.no(xl, y1, wl, hl, a)
    f.no(xl, y2, wl, hl, b)
    f.no(xr, yr, wr, hr, saida)
    meio = xl + wl + 70
    f.seta([(xl + wl + 3, y1 + hl / 2), (meio, y1 + hl / 2), (meio, yr + hr / 2 - 18), (xr - 3, yr + hr / 2 - 18)])
    f.seta([(xl + wl + 3, y2 + hl / 2), (meio, y2 + hl / 2), (meio, yr + hr / 2 + 18), (xr - 3, yr + hr / 2 + 18)])
    return xr + wr + 24, y2 + hl + 24


def _leque(f, fx):
    entrada, saidas = fx["entrada"], fx["saidas"]
    he, hs, gap = 110, 86, 18
    ys = [24 + i * (hs + gap) for i in range(len(saidas))]
    cy = (ys[0] + ys[-1] + hs) / 2
    xe, we = 24, 230
    xs, ws = xe + we + 150, 260
    f.no(xe, cy - he / 2, we, he, entrada)
    for y, no in zip(ys, saidas):
        f.no(xs, y, ws, hs, no)
        f.seta([(xe + we + 3, cy), (xs - 3, y + hs / 2)])
    largura = xs + ws + 24
    yf = ys[-1] + hs + 24
    f.faixa(24, yf, largura - 48, 56, fx["faixa"])
    return largura, yf + 56 + 24


def _decisao(f, fx):
    wb, hb, gap = 196, 100, 40
    y_sim, y_nao = 24, 24 + hb + 100
    cy = (y_sim + y_nao + hb) / 2
    wd, hd = 250, 170
    x = 24
    if fx.get("inicio"):
        f.no(x, cy - hb / 2, 180, hb, fx["inicio"])
        x += 180 + 56
        f.seta([(x - 53, cy), (x - 3, cy)])
    cx = x + wd / 2
    f.losango(cx, cy, wd, hd, fx["pergunta"])
    x0 = cx + wd / 2 + 70
    for ramo, y, rotulo, ponta in (("sim", y_sim, "Sim", cy - hd / 2), ("nao", y_nao, "Não", cy + hd / 2)):
        meio_y = y + hb / 2
        f.seta([(cx, ponta), (cx, meio_y), (x0 - 3, meio_y)], rotulo, ((cx + x0) / 2, meio_y - 16))
        for i, no in enumerate(fx[ramo]):
            xi = x0 + i * (wb + gap)
            f.no(xi, y, wb, hb, no)
            if i:
                f.seta([(xi - gap + 3, meio_y), (xi - 3, meio_y)])
    maior = max(len(fx["sim"]), len(fx["nao"]))
    return x0 + maior * (wb + gap) - gap + 24, y_nao + hb + 24


def _duas_faixas(f, fx):
    colunas, (r1, r2) = fx["colunas"], fx["rotulos"]
    wb, hb, gap, wl = 214, 96, 28, 150
    y1, y2 = 24, 24 + hb + 64
    f.rotulo(24, y1 + hb / 2, r1)
    f.rotulo(24, y2 + hb / 2, r2)
    for i, (cima, baixo) in enumerate(colunas):
        x = 24 + wl + i * (wb + gap)
        f.no(x, y1, wb, hb, cima)
        f.no(x, y2, wb, hb, baixo)
        f.seta([(x + wb / 2, y1 + hb + 3), (x + wb / 2, y2 - 3)])
    return 24 + wl + len(colunas) * (wb + gap) - gap + 24, y2 + hb + 24


FORMAS = {"cadeia": _cadeia, "convergencia": _convergencia, "leque": _leque,
          "decisao": _decisao, "duas_faixas": _duas_faixas}


def desenhar(fluxo, uid):
    """Devolve (svg, avisos); avisos lista os rótulos que não cabem."""
    f = Figura(uid)
    w, h = FORMAS[fluxo["forma"]](f, fluxo)
    return f.svg(w, h, fluxo["descricao"]), f.avisos


def contar_nos(fluxo):
    forma = fluxo["forma"]
    if forma == "cadeia":
        return len(fluxo["nos"])
    if forma == "convergencia":
        return 3
    if forma == "leque":
        return 1 + len(fluxo["saidas"])
    if forma == "decisao":
        return 1 + bool(fluxo.get("inicio")) + max(len(fluxo["sim"]), len(fluxo["nao"]))
    return len(fluxo["colunas"])


def _no_md(no):
    apoio = " ".join(_linhas(no[1]))
    return f"**{no[0]}**" + (f" — {apoio}" if apoio else "")


def como_texto(fluxo):
    """Versão em texto do fluxograma, para o Gamma e para leitores de tela."""
    forma = fluxo["forma"]
    if forma == "cadeia":
        linhas = [f"{i}. {_no_md(no)}" for i, no in enumerate(fluxo["nos"], 1)]
        return "\n".join(linhas + ([f"\n↻ {fluxo['retorno']}"] if fluxo.get("retorno") else []))
    if forma == "convergencia":
        a, b = fluxo["entradas"]
        return f"{_no_md(a)}\n\n{_no_md(b)}\n\n→ {_no_md(fluxo['saida'])}"
    if forma == "leque":
        saidas = " · ".join(f"**{no[0]}**" for no in fluxo["saidas"])
        return f"{_no_md(fluxo['entrada'])} → {saidas}\n\n{fluxo['faixa']}"
    if forma == "decisao":
        cab = (_no_md(fluxo["inicio"]) + " → ") if fluxo.get("inicio") else ""
        sim = " → ".join(_no_md(no) for no in fluxo["sim"])
        nao = " → ".join(_no_md(no) for no in fluxo["nao"])
        return f"{cab}**{' '.join(fluxo['pergunta'])}**\n- **Sim** → {sim}\n- **Não** → {nao}"
    r1, r2 = fluxo["rotulos"]
    cima = " · ".join(_no_md(c) for c, _ in fluxo["colunas"])
    baixo = " · ".join(_no_md(b) for _, b in fluxo["colunas"])
    return f"**{r1}:** {cima}\n\n**{r2}:** {baixo}"
