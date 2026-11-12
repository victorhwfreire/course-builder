"""Extrai do HTML canônico o trecho publicável (entre os marcadores) para publicar como Artifact.

Uso:
    python -B extrair_corpo.py <canonico.html> <saida.html> [--comparar <publicado.html>]

Com --comparar, diz se o trecho extraído é idêntico ao arquivo publicado (saída 0) ou não (saída 1).
"""
import argparse
import pathlib
import re
import sys

INICIO = "<!-- publicar:inicio -->"
FIM = "<!-- publicar:fim -->"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("canonico")
    ap.add_argument("saida")
    ap.add_argument("--comparar")
    a = ap.parse_args()

    fonte = pathlib.Path(a.canonico).read_text(encoding="utf-8")
    m = re.search(re.escape(INICIO) + r"\r?\n(.*)" + re.escape(FIM), fonte, re.S)
    if not m:
        sys.exit(f"Marcadores {INICIO} e {FIM} não encontrados em {a.canonico}")
    corpo = m.group(1)
    if not corpo.lstrip().startswith("<title>"):
        print("Aviso: o trecho publicável não começa com <title>.", file=sys.stderr)

    saida = pathlib.Path(a.saida)
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text(corpo, encoding="utf-8", newline="")
    print(f"{len(corpo)} caracteres em {saida}")

    if a.comparar:
        publicado = pathlib.Path(a.comparar).read_text(encoding="utf-8")
        if publicado == corpo:
            print("IGUAIS: o publicado corresponde ao canônico.")
        else:
            print("DIFERENTES: publique de novo a partir do canônico.")
            sys.exit(1)


if __name__ == "__main__":
    main()
