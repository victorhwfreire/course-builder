#!/usr/bin/env python3
"""Cria a pasta preparacao/ de uma turma com os geradores de assets/preparacao e um turma.py lido do spec.

Uso: python scaffold_preparacao.py <module.spec.yaml> <pasta_saida>
Copia assets/preparacao/ para <pasta_saida>/preparacao/ sem sobrescrever arquivo que já exista (avisa quais pulou),
cria aulas/, professor/ e guias/ e escreve turma.py. Campo ausente no spec fica com o marcador <...> do modelo.
Requer pyyaml.
"""
import json
import re
import shutil
import sys
import unicodedata
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent / "assets" / "preparacao"
IGNORAR = {"__pycache__", ".pytest_cache"}


def slug(texto):
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def id_aula(aula):
    """{"modulo": "M3", "numero": 1} -> "m3_a1"."""
    return f"m{re.sub('[^0-9]', '', str(aula['modulo']))}_a{aula['numero']}"


def campos(spec):
    curso, turma, caso = spec.get("curso") or {}, spec.get("turma") or {}, spec.get("caso") or {}
    nome_caso = caso.get("nome", "")
    aulas = [id_aula(a) for a in spec.get("aulas") or [] if a.get("modulo") and a.get("numero")]
    return {
        "TURMA": turma.get("codigo", ""),
        "CURSO": curso.get("nome", ""),
        "ORG": (spec.get("branding") or {}).get("org", ""),
        "DOCENTE": turma.get("docente", ""),
        "FERRAMENTA": (spec.get("ferramenta_base") or {}).get("nome", "Claude Code"),
        "CASO": nome_caso,
        "CASO_PASTA": caso.get("pasta") or (f"caso-{slug(nome_caso)}" if nome_caso else ""),
        "REPO": turma.get("repositorio", ""),
        "EMENTAS": spec.get("ementas") or ["ementa.md"],
        "AULAS": aulas,
    }


def turma_py(valores):
    texto = (KIT / "turma.py").read_text(encoding="utf-8")
    for nome, valor in valores.items():
        if valor:
            linha = f"{nome} = {json.dumps(valor, ensure_ascii=False)}"
            texto, n = re.subn(rf"^{nome} = .*$", lambda _: linha, texto, count=1, flags=re.M)
            if not n:
                sys.exit(f"O modelo {KIT / 'turma.py'} não tem a linha {nome} = ...")
    return texto


def main(caminho_spec, saida):
    spec_path = Path(caminho_spec)
    if not spec_path.is_file():
        sys.exit(f"Spec não encontrado: {spec_path}")
    try:
        import yaml
    except ImportError:
        sys.exit("Falta o pyyaml: pip install pyyaml")
    try:
        spec = yaml.safe_load(spec_path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as erro:
        sys.exit(f"Spec com YAML inválido ({spec_path}): {erro}")
    if not isinstance(spec, dict):
        sys.exit(f"Spec sem um mapa YAML na raiz: {spec_path}")

    destino = Path(saida) / "preparacao"
    copiados, pulados = [], []
    for origem in sorted(KIT.rglob("*")):
        rel = origem.relative_to(KIT)
        if origem.is_dir() or rel.as_posix() == "turma.py" or IGNORAR & set(rel.parts) or origem.suffix == ".pyc":
            continue
        alvo = destino / rel
        if alvo.exists():
            pulados.append(rel.as_posix())
            continue
        alvo.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origem, alvo)
        copiados.append(rel.as_posix())
    for pasta in ("aulas", "professor", "guias"):
        (destino / pasta).mkdir(parents=True, exist_ok=True)

    valores = campos(spec)
    turma = destino / "turma.py"
    if turma.exists():
        pulados.append("turma.py")
    else:
        turma.write_text(turma_py(valores), encoding="utf-8", newline="\n")

    print(f"{len(copiados)} arquivos copiados para {destino}")
    if pulados:
        print(f"Pulados, já existiam ({len(pulados)}): " + ", ".join(pulados))
    if "turma.py" not in pulados:
        vazios = [n for n, v in valores.items() if not v]
        print("turma.py escrito do spec" + (f"; sem valor no spec, ficaram como no modelo: {', '.join(vazios)}" if vazios else "")
              + ". Preencha GUIA_MODULOS e os demais <...> à mão.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1], sys.argv[2]))
