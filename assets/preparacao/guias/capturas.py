"""Fotografa a abertura e cada bancada do guia em 1280 px e 390 px, para conferir o layout com Read.

Uso:
    python -B capturas.py <guia.html> <pasta_saida> [--passos] [--larguras 1280,390] [--escuro]

Relata erros de JavaScript da página, a largura de rolagem (deve ser igual à da janela) e
controles ao vivo visíveis, que fora do claude.ai deveriam estar ocultos.
Com --passos, clica em cada ponto dos passo a passo (.pontos button) e fotografa cada passo.
Com --escuro, emula o tema escuro do sistema (prefers-color-scheme: dark) e prefixa os arquivos com "escuro-".
Requer: pip install playwright && python -m playwright install chromium
"""
import argparse
import pathlib

from playwright.sync_api import sync_playwright


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("guia")
    ap.add_argument("saida")
    ap.add_argument("--passos", action="store_true")
    ap.add_argument("--larguras", default="1280,390")
    ap.add_argument("--escuro", action="store_true")
    a = ap.parse_args()
    tema = "dark" if a.escuro else "light"
    pref = "escuro-" if a.escuro else ""

    url = pathlib.Path(a.guia).resolve().as_uri()
    out = pathlib.Path(a.saida)
    out.mkdir(parents=True, exist_ok=True)
    larguras = [int(x) for x in a.larguras.split(",")]
    problemas = 0

    with sync_playwright() as p:
        nav = p.chromium.launch()
        for largura in larguras:
            pg = nav.new_page(viewport={"width": largura, "height": 900}, color_scheme=tema)
            erros = []
            pg.on("pageerror", lambda e: erros.append(str(e)))
            pg.goto(url, wait_until="domcontentloaded")
            pg.wait_for_timeout(1500)
            rolagem = pg.evaluate("document.documentElement.scrollWidth")
            vivos = pg.evaluate(
                "[...document.querySelectorAll('[data-ao-vivo]')].filter(e => e.offsetParent !== null).length"
            )
            print(f"{tema} {largura}px: erros JS={erros or 'nenhum'} · largura de rolagem={rolagem} · controles ao vivo visíveis={vivos}")
            problemas += bool(erros) + (rolagem > largura) + bool(vivos)

            alvos = ["#topo"] + [f"#{i}" for i in pg.eval_on_selector_all(".bancada[id]", "els => els.map(e => e.id)")]
            for alvo in alvos:
                el = pg.locator(alvo)
                if not el.count():
                    continue
                el.screenshot(path=str(out / f"{pref}{largura}-{alvo[1:]}.png"))
                if a.passos and alvo != "#topo":
                    botoes = pg.locator(f"{alvo} .pontos button")
                    for i in range(botoes.count()):
                        botoes.nth(i).click()
                        pg.wait_for_timeout(150)
                        el.screenshot(path=str(out / f"{pref}{largura}-{alvo[1:]}-p{i + 1}.png"))
            pg.close()
        nav.close()

    print(f"Capturas em {out}. {'Sem problemas detectados.' if not problemas else f'{problemas} problema(s) acima.'}")


if __name__ == "__main__":
    main()
