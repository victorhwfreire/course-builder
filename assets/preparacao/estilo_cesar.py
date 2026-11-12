"""Tokens visuais CESAR (tema único claro) e utilidades de texto, comuns ao estudo dirigido e ao guia do monitor."""
import re
from html import escape

FONTES = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
          '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
          '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;'
          '0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800;1,9..40,400&display=swap">')

TOKENS = """
:root{
  --papel:#FFFFFF; --superficie-2:#F8F7F6; --superficie-3:#F1F0EE;
  --tinta:#0C0B0A; --texto:#2A2825; --tinta-2:#403E3B; --tinta-3:#5C5955;
  --linha:#E4E2DF; --linha-forte:#A5A19C;
  --marca:#FF6002; --marca-tx:#DD3805; --marca-forte:#B32C04; --marca-suave:#FFF2EB;
  --aviso-suave:#FEF4E1; --aviso:#9A5B00; --certo:#1F7A45; --certo-suave:#E7F6EE; --erro:#B42318; --erro-suave:#FCEBEA;
  --f-texto:"DM Sans","Helvetica Neue",Arial,sans-serif;
  --f-codigo:"Cascadia Mono",Consolas,"SFMono-Regular",ui-monospace,monospace;
  --raio:12px;
  color-scheme:light;
}
"""


def inline(texto):
    """Escapa o HTML e formata `código`, **negrito** e [texto](https://endereço)."""
    s = escape(texto)
    s = re.sub(r"\[([^\]]+)\]\((https://[^)\s]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    return s
