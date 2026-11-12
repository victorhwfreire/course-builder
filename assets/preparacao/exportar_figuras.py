"""Exporta as figuras SVG de uma aula para PNG, em resolução dupla, para inserir no Gamma.

Uso, na pasta da turma, depois de construir_aula.py: python -B preparacao/exportar_figuras.py m3_a1
Requer Playwright com o Chromium instalado (python -m playwright install chromium).
"""
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parent.parent


def main(ident):
    modulo, aula = re.fullmatch(r"m(\d)_a(\d)", ident).groups()
    pasta = RAIZ / f"M{modulo}" / f"aula-{aula}" / "figuras"
    svgs = sorted(pasta.glob("slide-*.svg"))
    if not svgs:
        print(f"Nenhuma figura em {pasta}; rode antes construir_aula.py {ident}.")
        return 1
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        for svg in svgs:
            w, h = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg.read_text(encoding="utf-8")).groups())
            pagina = navegador.new_page(viewport={"width": int(w), "height": int(h)}, device_scale_factor=2)
            pagina.goto(svg.as_uri())
            pagina.screenshot(path=str(svg.with_suffix(".png")))
            pagina.close()
        navegador.close()
    print(f"{len(svgs)} figuras exportadas para PNG em {pasta.relative_to(RAIZ)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "m3_a1"))
