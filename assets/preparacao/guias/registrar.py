"""Grava em execucoes.json as saídas dos subagentes, lidas das transcrições, e confere o pedido de cada uma.

Uso: python -B registrar.py <pasta-subagents> chave=agentId [chave=agentId ...]
A saída é o último texto do subagente, sem a linha MODELO; o pedido recebido tem de ser idêntico ao de pedidos.json.
Uma chave repetida acrescenta uma nova execução (n = 2, 3...).
"""
import json
import sys
from datetime import date
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def ler(transcricao):
    pedido, textos = None, []
    for linha in transcricao.read_text(encoding="utf-8").splitlines():
        try:
            ev = json.loads(linha)
        except json.JSONDecodeError:
            continue
        m = ev.get("message") or {}
        if ev.get("type") == "user" and pedido is None and isinstance(m.get("content"), str):
            pedido = m["content"]
        if ev.get("type") == "assistant":
            textos += [b["text"] for b in m.get("content") or [] if isinstance(b, dict) and b.get("type") == "text" and b.get("text")]
    return pedido, textos[-1] if textos else ""


def main():
    pasta = Path(sys.argv[1])
    pedidos = json.loads((AQUI / "pedidos.json").read_text(encoding="utf-8"))
    reg = json.loads((AQUI / "execucoes.json").read_text(encoding="utf-8"))
    for par in sys.argv[2:]:
        chave, agente = par.split("=")
        pedido, final = ler(pasta / f"agent-{agente}.jsonl")
        corpo, _, modelo = final.rpartition("MODELO:")
        if not corpo:
            corpo, modelo = final, "?"
        confere = (pedido or "").strip() == pedidos[chave].strip()
        lista = reg["execucoes"].setdefault(chave, [])
        lista.append({"n": len(lista) + 1, "modelo": modelo.strip(), "data": date.today().strftime("%d/%m/%Y"), "saida": corpo.strip(), "pedido_confere": confere})
        print(f"{chave} n={len(lista)} · modelo {modelo.strip()} · pedido idêntico ao registrado: {'sim' if confere else 'NÃO'}")
    (AQUI / "execucoes.json").write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
