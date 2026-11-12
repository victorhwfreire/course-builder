"""Copia o material dos alunos para um clone do repositório da turma; o commit e o push ficam com você.

Uso, na pasta da turma: python -B preparacao/copiar_para_repositorio.py <pasta_do_clone>
Copia material-alunos/<turma.CASO_PASTA> (sem estado/ nem caches) e o estudo-dirigido.pdf de cada aula,
com o nome de turma.pdf_estudo. Arquivo apagado aqui não é apagado no clone.
"""
import importlib
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAIZ = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "aulas"))

from turma import AULAS, CASO_PASTA, pdf_estudo  # noqa: E402


def main(clone):
    destino = Path(clone)
    if not (destino / ".git").is_dir():
        sys.exit(f"{destino} não é um clone git.")
    shutil.copytree(RAIZ / "material-alunos" / CASO_PASTA, destino / CASO_PASTA, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("estado", "__pycache__", "*.pyc", ".pytest_cache"))
    print(f"{CASO_PASTA}/")
    for ident in AULAS:
        meta = importlib.import_module(ident).META
        alvo = destino / pdf_estudo(meta)
        alvo.parent.mkdir(exist_ok=True)
        shutil.copy2(RAIZ / meta["pasta"] / "estudo-dirigido.pdf", alvo)
        print(alvo.relative_to(destino).as_posix())
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
