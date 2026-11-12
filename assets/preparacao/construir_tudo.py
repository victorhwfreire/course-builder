"""Regenera o material das aulas de turma.AULAS: deck, roteiro, plano, figuras (SVG e PNG), guia do monitor e estudo dirigido.

Uso, na pasta da turma: python -B preparacao/construir_tudo.py [m3_a1 m3_a2 ...]
Os guias interativos têm gerador próprio: preparacao/guias/gerar_guia.py.
"""
import subprocess
import sys
from pathlib import Path

PREP = Path(__file__).resolve().parent
sys.path.insert(0, str(PREP))

from turma import AULAS as TODAS  # noqa: E402

AULAS = sys.argv[1:] or TODAS
PASSOS = ["construir_aula.py", "exportar_figuras.py", "construir_monitor.py", "construir_estudo.py"]

falhas = []
for aula in AULAS:
    for passo in PASSOS:
        r = subprocess.run([sys.executable, "-B", str(PREP / passo), aula], capture_output=True, text=True, encoding="utf-8")
        ultima = (r.stdout.strip().splitlines() or [""])[-1]
        print(f"{aula} · {passo}: {'ok' if r.returncode == 0 else 'FALHOU'} · {ultima[:110]}", flush=True)
        if r.returncode:
            falhas.append(f"{aula} {passo}: {(r.stderr or r.stdout)[-400:]}")
print("\n".join(falhas) if falhas else "Tudo regenerado.")
sys.exit(1 if falhas else 0)
