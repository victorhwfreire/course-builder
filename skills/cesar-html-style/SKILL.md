---
name: cesar-html-style
description: Shared CESAR dark-theme CSS and standalone HTML5 template for lesson artifacts. Use when generating any HTML artifact (plano de aula, roteiro, portal) that must match the CESAR visual identity and print to PDF cleanly.
---

# cesar-html-style

You generate HTML artifacts for a course module (planos de aula, roteiros do instrutor, portal do instrutor). Every artifact shares one visual identity: the CESAR dark theme defined in `assets/estilo.css` (this skill's bundled stylesheet). Your job is to link that stylesheet, emit a self-contained HTML5 document, parameterize the accent color from the module spec, and keep the result well-formed and printable.

## 1. Link the shared stylesheet

The stylesheet lives next to this SKILL.md at `assets/estilo.css`. Copy it into the artifact bundle (the agent that invokes you knows the output directory) and link it with a **relative path** from each HTML file:

- Artifact at the bundle root (e.g. `portal.html`): `<link rel="stylesheet" href="estilo.css">`
- Artifact one level deep (e.g. `aula-1/roteiro.html`): `<link rel="stylesheet" href="../estilo.css">`

Never absolute paths, never `file://`, never a `<style>` inline copy of the whole stylesheet. One copy of `estilo.css` per bundle, linked relatively.

## 2. Self-contained HTML5 document skeleton

Every artifact is a complete HTML5 doc — no server, no build step, opens by double-click. Use this shape:

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ titulo do artifact }} — {{ modulo }} · IA para Devs ({{ org }} {{ ano }})</title>
  <link rel="stylesheet" href="{{ path relativo a estilo.css }}">
  <style>:root{--accent:{{ cor_acento }};--accent-soft:{{ cor_acento_soft }}}}</style>
</head>
<body>
  <main>
    <header class="hero">
      <div class="kicker">{{ contexto · modulo · artifact · org · ano }}</div>
      <h1>{{ titulo }}</h1>
      <p class="sub">{{ subtitulo curto }}</p>
      <div class="meta">
        <span class="pill"><b>{{ dado em destaque }}</b> · {{ detalhe }}</span>
        <!-- mais pills conforme necessario -->
      </div>
    </header>

    <!-- corpo do artifact: secoes .secao, .roteiro-slide, .bloco, .tablewrap, etc. -->

    <footer>{{ rodape padrao do modulo }}</footer>
  </main>
</body>
</html>
```

`lang="pt-BR"` always. `<meta charset="UTF-8">` and viewport always present. The `<style>` block in `<head>` is the **only** inline CSS — and it carries just the accent override (next section).

## 3. Parameterize the accent color from the spec

`estilo.css` ships with `--accent:#e2231a` (the CESAR red) as default. The module spec provides `spec.branding.cor_acento` (e.g. `"#e2231a"`). Override it per-document via a tiny `:root` block in `<head>`:

```html
<style>:root{--accent:#e2231a;--accent-soft:#ff5a4d}</style>
```

Rules:
- Read `spec.branding.cor_acento` and use that exact hex. Default to `#e2231a` if the field is absent.
- Derive `--accent-soft` as a perceptually lighter version of the same hue (for `#e2231a` use `#ff5a4d`). If you cannot derive it, reuse the accent hex for both.
- Do **not** edit `estilo.css` to hardcode a module's accent — the stylesheet stays generic; the override lives in each document's `<head>`.
- All other tokens (`--bg`, `--panel`, `--ink`, `--accent-2`, etc.) stay as shipped. Do not recolor the theme beyond the accent.

## 4. Keep HTML well-formed and printable

- Always close tags; never emit raw `<br>` inside `<p>` where a block element fits better.
- Use the stylesheet's component classes rather than inventing inline styles: `.hero`, `.secao`, `.roteiro-slide`, `.bloco`/`.bloco-time`/`.bloco-body`, `.tablewrap`, `.diga`, `.nota-inst`, `.passo`, `.pill`, `.tag`/`.t-auto`/`.t-hitl`/`.t-inst`/`.t-aluno`, `.check`, `.portal-grid`/`.aula-card`/`.reslink`.
- Escape `&`, `<`, `>` in body text (`&amp;`, `&lt;`, `&gt;`).
- The stylesheet is print/PDF-friendly (`@media print` flips to a light theme and avoids breaking blocks across pages). Do not add `print-color-adjust` hacks or `@page` rules — the existing print rules are enough.
- Validate mentally before returning: single `<main>`, single `</body></html>`, every `<div>` closed, every `<table>` inside `.tablewrap`.

## 5. Self-check before returning the artifact

- [ ] `estilo.css` is linked via a **relative** path correct for the file's depth.
- [ ] `<html lang="pt-BR">`, `<meta charset="UTF-8">`, viewport meta all present.
- [ ] A `:root` accent override in `<head>` uses `spec.branding.cor_acento` (or `#e2231a` default).
- [ ] No inline CSS beyond that `:root` override.
- [ ] Document opens standalone in a browser (no server, no external JS) and prints to PDF without layout breaks.

## 6. Mode `estudo-dirigido` uses the light CESAR theme instead

In mode `estudo-dirigido` no agent writes HTML by hand and this stylesheet is not used. The generators in `preparacao/` carry the light CESAR theme in `preparacao/estilo_cesar.py` (DM Sans, orange `#FF6002`, white paper), inlined into every page so each one opens by double click and can be published as an Artifact. That theme was approved by the course owner: do not switch it to dark, nor change palette or font, without asking.