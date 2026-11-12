"""Descrição, no guia, das ferramentas que agente_caso.js entrega ao agente ao vivo; reescreva junto com ele para um caso novo."""
from html import escape as e


def descrever_ferramentas(ag):
    modo = ag.get("modo", "arquivos")
    if modo == "fraco":
        return "<code>get_data</code>, a ferramenta do contrato fraco, com descrição “Consulta dados.” e erro “invalid input”."
    if modo == "forte":
        return ("<code>buscar_cliente</code>, <code>consultar_cobrancas</code>, <code>registrar_nota</code> e "
                "<code>emitir_estorno</code> (simulado), com o contrato forte do servidor do caso"
                + (", e o estorno passa pela regra do guarda.py." if ag.get("guarda") else "; sem regra de guarda."))
    return ("<code>listar_arquivos</code> e <code>ler_arquivo</code>, que devolvem os arquivos "
            + e(", ".join(ag["arquivos"])) + " do caso.")
