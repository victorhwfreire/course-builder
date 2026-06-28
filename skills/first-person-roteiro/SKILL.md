---
name: first-person-roteiro
description: Voice contract for 1st-person instructor scripts (roteiros). Use when generating roteiro-instrutor HTML — enforces direct speech, .diga anchor quotes, .nota-inst bastidor notes, and bans 2nd-person imperatives directed at the audience.
---

# first-person-roteiro

You generate `roteiro-instrutor-*.html` — the script the instructor reads aloud, slide by slide, plus the live-demo walkthrough and the hands-on checkpoints. The voice is fixed: **first person, direct speech, as if the instructor is talking to the room right now**. This skill encodes the contract and a self-check you must run on your own output before returning.

## 1. Voice contract

**First person, direct speech.** Every spoken paragraph is written as the instructor saying it, in first person, addressing the room as "pessoal", "vocês", "a turma" — never as commands to the audience.

- Openers that set the tone: `"Boa noite, pessoal..."`, `"Deixa eu..."`, `"Olha..."`, `"Bom, pessoal..."`, `"Vou ser bem explícito..."`.
- Narrate what the instructor does and why: `"Vou criar o code-reviewer aqui."`, `"Deixa eu desenhar a trilha pra vocês."`, `"Agora a gente junta as peças."`
- The instructor owns the action: `"eu vou"`, `"vou mostrar"`, `"deixa eu cravar"`, `"a gente vai montar"`. The audience is the recipient, never the actor being commanded.

**PROIBIDO — 2ª pessoa imperativa dirigida à plateia.** Do not write sentences that order the audience to do something as the script's voice:
- ❌ `"Abra o terminal."`
- ❌ `"Mostre o relatório."`
- ❌ `"Explique o conceito."`
- ❌ `"Prestem atenção."` (as a command)

Imperatives are allowed only inside **enunciado do aluno** (a different artifact, written for students doing hands-on) and inside explicit stage directions / operational bastidor notes — never as the spoken roteiro voice. If the instructor needs the room to look somewhere, phrase it as first-person narration: `"Olha aqui o relatório."`, `"Repararam que..."`, `"Deixa eu mostrar o que apareceu."`.

## 2. The three block types

Each slide block uses `.roteiro-slide` with a `.cab` header (`slide-badge`, `h3`, `.tempo`). Inside, three content block types — use them exactly as the stylesheet defines them:

### `.diga` — fala-âncora (the anchor quote)
The cravable line — the phrase the instructor lands to change rhythm or close a point. Italic, blue quote. **Spoken aloud, almost literally.** One per slide, at most two.

```html
<div class="diga">"Nas próximas três horas vocês saem daqui com um time de revisão que roda sozinho no repo de vocês. Não é demo minha — é artefato de vocês, commitado."</div>
```

### `.nota-inst` — bastidor (non-spoken operational note)
Backstage only. Reminds the instructor what to open on screen, what to check, where the risk of stalling is, what to say if someone asks a specific question. **Never spoken aloud.** Prefix with `<b>Nota:</b> Bastidor: ...` or `<b>Nota de contingência:</b> Bastidor: ...`.

```html
<div class="nota-inst"><b>Nota:</b> Bastidor: mostrar o bloco de código do frontmatter com calma — eles vão digitar exatamente isto no Checkpoint 1. Se a fonte estiver pequena, aumentar agora.</div>
```

### `<b>[stage direction]</b>` — demo / hands-on passo
Inline at the start of a `.passo` body (or a slide paragraph) to mark a physical action the instructor performs on screen. **Bold, in square brackets.** The prose after the bracket is the first-person narration of what the instructor is doing and why.

```html
<div class="passo"><div class="n">1</div><div><b>[Mostro a estrutura na tela: repo na raiz, claude aberto, npm test verde]</b> Olha aqui: o repo está na raiz, com o claude aberto e o npm test verde. Tudo que eu vou criar agora são arquivos Markdown dentro de .claude/ — vocês vão poder versionar e reaproveitar.</div></div>
```

Stage directions may also nest an inline `<i>Bastidor: ...</i>` aside for a quick operational reminder inside a passo.

## 3. Structure of a roteiro

Follow the canonical shape (see the real `roteiro-instrutor-aula-1.html` for grounding):

1. `<header class="hero">` — kicker ("Roteiro do Instrutor · Módulo N · Aula X de Y"), title, sub, meta pills (data, horário, ferramenta base).
2. `.secao` "Como usar este roteiro" — two/three short paragraphs explaining the voice contract to the instructor: the prose is first-person speech; `.diga` are the cravable lines; `.nota-inst` are bastidor the instructor does NOT speak aloud.
3. `.secao` "Parte 1 — Roteiro de fala slide a slide" — one `.roteiro-slide` per slide, in order. Each slide: `.cab` (badge + h3 + tempo), spoken paragraphs, one `.diga`, optional `.nota-inst`.
4. `.secao` "Parte 2 — Demonstração guiada (live coding)" — intro paragraph + numbered `.passo` blocks with `<b>[stage direction]</b>` openers + a contingency `.nota-inst` at the end.
5. `.secao` "Parte 3 — Partes práticas (hands-on)" — intro paragraph + one `.passo` per checkpoint with `<b>[Lanço o Checkpoint N — ...]</b>` opener, each carrying `<i>Bastidor — erros comuns:</i>` and `<i>Como recolher:</i>` asides.
6. `.secao` "Encerramento" — recap + ponte para a próxima aula + frase-tese do módulo.
7. `<footer>` — rodapé padrão.

Link `estilo.css` (cesar-html-style skill) via relative path. The roteiro lives one level deep (`aula-N/roteiro-instrutor-aula-N.html`), so use `../estilo.css`.

## 4. Self-check (run on your own output before returning)

Run these checks against the HTML you produced. If any fails, fix and re-check — do not return a failing roteiro.

1. **First-person presence.** Grep the spoken paragraphs (exclude `.nota-inst` and `<b>[...]` stage directions) for first-person markers: at least one of `eu | vou | deixa eu | olha | a gente | pessoal | vocês`. A roteiro with none of these is wrong-voiced.
2. **`.diga` usage.** Confirm at least one `.diga` block in Parte 1 (most slides should have one). Zero `.diga` across the whole roteiro = fail.
3. **Imperative ban (the critical check).** Search the spoken prose (exclude `.nota-inst` blocks and text inside `<b>[...]`) for 2nd-person imperatives directed at the audience. Flag these patterns:
   - `^Abra `, `^Abre `, `^Mostre `, `^Mostrem `, `^Explique `, `^Expliquem `, `^Preste `, `^Prestem `, `^Digite `, `^Digitem `, `^Crie `, `^Criem `, `^Rode `, `^Rodem `, `^Faz `, `^Faça `, `^Vá `, `^Vão `
   - mid-sentence `, abra `, `, mostre `, `, explique ` (comma + imperative addressing the room)
   - Any of these in the spoken voice = fail. Move the action to first-person narration (`"Vou abrir..."`, `"Deixa eu mostrar..."`) or, if it is genuinely a student instruction, relocate it to the enunciado do aluno (a separate artifact).
   - Allowed exceptions: imperatives **inside `.nota-inst`** (`"mostrar o bloco"`, `"responder curto"`, `"fazer a pausa dramática"`) — these are operational notes to the instructor, not spoken to the room.
4. **`.nota-inst` is bastidor.** Every `.nota-inst` block contains the word `Bastidor:` (or `Nota de contingência:`). If absent, the note is mis-typed — fix it.
5. **Stage directions are bracketed bold.** Every `<b>[...]` opener in Partes 2 and 3 marks a physical action; verify the bracket is present and the text inside is a stage direction, not a spoken line.

A roteiro fragment like `"<p>Abra o terminal e rode /review app-exemplo/.</p>"` **must** be caught by check 3 and rewritten to, e.g., `"<p>Vou abrir o terminal aqui e rodar /review app-exemplo/ pra vocês verem o enxame trabalhando.</p>"`.