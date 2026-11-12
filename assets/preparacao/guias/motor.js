(function () {
  "use strict";
  var $ = function (id) { return document.getElementById(id); };
  var DADOS = JSON.parse($("dados-guia").textContent);
  var texto = function (id) { var el = $(id); return el ? el.textContent.replace(/^\s+|\s+$/g, "") : ""; };

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function inline(s) {
    s = esc(s);
    s = s.replace(/`([^`]+)`/g, "<code>$1</code>");
    s = s.replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>");
    s = s.replace(/(^|[^*])\*([^*\s][^*]*)\*/g, "$1<i>$2</i>");
    return s;
  }
  function md(src) {
    var L = src.replace(/\r/g, "").split("\n"), out = [], i = 0;
    var celulas = function (r) { return r.trim().replace(/^\||\|$/g, "").split("|").map(function (c) { return c.trim(); }); };
    while (i < L.length) {
      var l = L[i];
      if (/^\s*```/.test(l)) {
        var codigo = [];
        i++;
        while (i < L.length && !/^\s*```/.test(L[i])) { codigo.push(L[i]); i++; }
        i++;
        out.push('<pre class="cmd">' + esc(codigo.join("\n")) + "</pre>");
        continue;
      }
      if (/^\s*>/.test(l)) {
        var citacao = [];
        while (i < L.length && /^\s*>/.test(L[i])) { citacao.push(L[i].replace(/^\s*>\s?/, "")); i++; }
        out.push('<blockquote class="citacao">' + md(citacao.join("\n")) + "</blockquote>");
        continue;
      }
      if (/^\s*\|/.test(l)) {
        var rows = [];
        while (i < L.length && /^\s*\|/.test(L[i])) { rows.push(L[i]); i++; }
        var cab = celulas(rows[0]);
        var corpo = rows.slice(1).filter(function (r) { return !/^\s*\|?\s*:?-{2,}/.test(r); });
        out.push('<div class="rolagem"><table class="tabela"><thead><tr>' + cab.map(function (h) { return "<th>" + inline(h) + "</th>"; }).join("") +
          "</tr></thead><tbody>" + corpo.map(function (r) { return "<tr>" + celulas(r).map(function (c) { return "<td>" + inline(c) + "</td>"; }).join("") + "</tr>"; }).join("") + "</tbody></table></div>");
        continue;
      }
      if (/^#{1,4}\s/.test(l)) { out.push('<p class="md-h">' + inline(l.replace(/^#+\s*/, "")) + "</p>"); i++; continue; }
      if (/^\s*[-*]\s+/.test(l)) {
        var it = [];
        while (i < L.length && /^\s*[-*]\s+/.test(L[i])) { it.push(L[i].replace(/^\s*[-*]\s+/, "")); i++; }
        out.push("<ul>" + it.map(function (x) { return "<li>" + inline(x) + "</li>"; }).join("") + "</ul>");
        continue;
      }
      if (/^\s*\d+\.\s+/.test(l)) {
        var ol = [];
        while (i < L.length && /^\s*\d+\.\s+/.test(L[i])) { ol.push(L[i].replace(/^\s*\d+\.\s+/, "")); i++; }
        out.push("<ol>" + ol.map(function (x) { return "<li>" + inline(x) + "</li>"; }).join("") + "</ol>");
        continue;
      }
      if (!l.trim()) { i++; continue; }
      var par = [];
      while (i < L.length && L[i].trim() && !/^\s*(\||#{1,4}\s|[-*]\s|\d+\.\s|>|```)/.test(L[i])) { par.push(L[i]); i++; }
      out.push("<p>" + inline(par.join(" ")) + "</p>");
    }
    return out.join("");
  }
  function caixaSaida(rotulo, detalhe, conteudo) {
    return '<div class="saida"><div class="saida-cab"><b>' + esc(rotulo) + "</b><span>" + esc(detalhe) + '</span></div><div class="saida-corpo">' + conteudo + "</div></div>";
  }
  function caixaPedido(rotulo, txt) { return '<div class="pedido"><small>' + esc(rotulo) + "</small>" + esc(txt) + "</div>"; }

  /* Claude ao vivo: controles [data-ao-vivo] só aparecem quando o sample está disponível. */
  var SAMPLE = null;
  function mostrarAoVivo(sim) {
    document.querySelectorAll("[data-ao-vivo]").forEach(function (el) { el.hidden = !sim; });
    document.querySelectorAll("[data-sem-ao-vivo]").forEach(function (el) { el.hidden = sim; });
  }
  if (window.claude && typeof window.claude.use === "function") {
    window.claude.use("sample").then(function (f) { if (f) { SAMPLE = f; mostrarAoVivo(true); } }).catch(function () {});
  }
  function mensagemErro(codigo) {
    if (codigo === "not_granted" || codigo === "sampling_disabled") return "O uso do Claude não foi liberado para esta página. As execuções registradas continuam disponíveis.";
    if (codigo === "rate_limited") return "Muitas chamadas seguidas. Espere um pouco e tente de novo.";
    if (codigo === "session_expired") return "Sua sessão expirou. Entre de novo no Claude e recarregue a página.";
    if (codigo === "refused") return "O Claude não respondeu a este pedido.";
    return "A chamada não terminou. Tente de novo em alguns instantes.";
  }
  /* Resolve com o texto da resposta, ou null se a chamada falhou. */
  function rodar(entrada, alvo, aviso, botao) {
    if (!SAMPLE) return Promise.resolve(null);
    botao.disabled = true;
    aviso.textContent = "";
    alvo.innerHTML = '<p class="pensando">Pensando… a primeira parte da resposta costuma levar alguns segundos.</p>';
    return SAMPLE(entrada, { cache: false, onText: function (u) { alvo.innerHTML = md(u.text); } })
      .then(function (r) {
        aviso.textContent = r.truncated ? "Resposta ao vivo, cortada pelo limite de tamanho." : "Resposta ao vivo, gerada agora.";
        return r.text;
      })
      .catch(function (e) {
        alvo.innerHTML = e && e.text ? md(e.text) : "";
        if (!(e && e.code === "cancelled")) aviso.textContent = mensagemErro(e && e.code);
        if (e && (e.code === "not_granted" || e.code === "sampling_disabled")) mostrarAoVivo(false);
        return null;
      })
      .then(function (t) { botao.disabled = false; return t; });
  }
  function ligarVivo(pref, obterPrompt) {
    var b = $(pref + "-rodar");
    if (b) b.addEventListener("click", function () { rodar(obterPrompt(), $(pref + "-vivo"), $(pref + "-aviso"), b); });
  }
  function ligarRevisao(pref, chave1, chave2) {
    var b = $(pref + "-rodar"), aviso = $(pref + "-aviso"), final = $(pref + "-vivo2");
    if (!b) return;
    b.addEventListener("click", function () {
      var p1 = DADOS.pedidos[chave1], p2 = DADOS.pedidos[chave2];
      final.innerHTML = '<p class="pensando">A revisão começa quando o rascunho terminar.</p>';
      rodar(p1, $(pref + "-vivo"), aviso, b).then(function (rascunho) {
        if (rascunho === null) return;
        return rodar([{ role: "user", content: p1 }, { role: "assistant", content: rascunho }, { role: "user", content: p2 }], final, aviso, b);
      });
    });
  }

  /* trilha: marca a seção visível */
  var links = Array.prototype.slice.call(document.querySelectorAll(".trilha a"));
  if ("IntersectionObserver" in window) {
    var obs = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) links.forEach(function (a) { a.classList.toggle("ativo", a.getAttribute("href") === "#" + e.target.id); });
      });
    }, { rootMargin: "-40% 0px -55% 0px" });
    document.querySelectorAll("main section[id]").forEach(function (s) { obs.observe(s); });
  }

  /* conteúdo de um passo: html pronto, um pedido registrado ou uma saída registrada */
  function conteudo(c) {
    if (!c) return "";
    if (typeof c === "string") return c;
    if (c.pedido) return caixaPedido(c.rotulo || "Pedido enviado, texto exato", DADOS.pedidos[c.pedido]);
    if (c.saida) return caixaSaida(c.rotulo, c.detalhe, md(texto(c.saida)));
    if (c.lista) return c.lista.map(conteudo).join("");
    return "";
  }

  function stepper(pref, passos) {
    var atual = 0, pontos = $(pref + "-pontos"), acesos = [];
    pontos.innerHTML = passos.map(function (p, i) { return '<button type="button" data-i="' + i + '" aria-label="Passo ' + (i + 1) + '">' + (i + 1) + "</button>"; }).join("");
    function ir(i) {
      atual = Math.max(0, Math.min(passos.length - 1, i));
      var p = passos[atual];
      pontos.querySelectorAll("button").forEach(function (b, k) { b.className = k === atual ? "atual" : (k < atual ? "feito" : ""); });
      $(pref + "-cont").textContent = "Passo " + (atual + 1) + " de " + passos.length;
      $(pref + "-tit").textContent = p.t;
      $(pref + "-explica").innerHTML = p.e;
      $(pref + "-corpo").innerHTML = conteudo(p.c);
      acesos.forEach(function (n) { n.classList.remove("aceso"); });
      acesos = (p.acende || []).map(function (id) { return $(id); }).filter(Boolean);
      acesos.forEach(function (n) { n.classList.add("aceso"); });
      $(pref + "-voltar").disabled = atual === 0;
      $(pref + "-avancar").disabled = atual === passos.length - 1;
    }
    pontos.addEventListener("click", function (e) { var b = e.target.closest("button"); if (b) ir(Number(b.getAttribute("data-i"))); });
    $(pref + "-voltar").addEventListener("click", function () { ir(atual - 1); });
    $(pref + "-avancar").addEventListener("click", function () { ir(atual + 1); });
    ir(0);
  }

  function quiz(pref, cfg) {
    var box = $(pref + "-quiz");
    box.innerHTML = cfg.itens.map(function (q, i) {
      return '<div class="quiz-q" data-i="' + i + '"><span class="origem">' + q.origem + '</span><span class="enun">' + q.t + '</span><div class="opts">' +
        cfg.opcoes.map(function (o) { return '<button type="button" class="op" data-r="' + o[0] + '">' + esc(o[1]) + "</button>"; }).join("") +
        '</div><p class="fb" aria-live="polite"></p></div>';
    }).join("");
    box.addEventListener("click", function (e) {
      var b = e.target.closest(".op"); if (!b) return;
      var q = b.closest(".quiz-q"), item = cfg.itens[Number(q.getAttribute("data-i"))];
      q.querySelectorAll(".op").forEach(function (o) { o.classList.remove("certo", "errado"); });
      var certo = b.getAttribute("data-r") === item.r;
      b.classList.add(certo ? "certo" : "errado");
      if (!certo) q.querySelector('.op[data-r="' + item.r + '"]').classList.add("certo");
      q.querySelector(".fb").innerHTML = (certo ? "Isso. " : "Não exatamente. ") + item.fb;
    });
  }

  function seletor(pref, cfg) {
    var lista = $(pref + "-itens");
    lista.innerHTML = cfg.itens.map(function (it) {
      return '<label class="item-j' + (it.fixo ? " fixo" : "") + '"><input type="checkbox" id="' + pref + "-" + it.id + '" data-id="' + it.id + '"' +
        (it.padrao || it.fixo ? " checked" : "") + (it.fixo ? " disabled" : "") + '><span><b>' + esc(it.rot) + "</b>" + esc(it.desc) + "</span></label>";
    }).join("");
    function escolhidos() {
      return cfg.itens.filter(function (it) { return $(pref + "-" + it.id).checked; });
    }
    function montar() {
      var sel = escolhidos(), ids = sel.map(function (it) { return it.id; });
      var pedido = sel.map(function (it) { return it.texto; }).filter(Boolean).join(cfg.juntar || " ");
      var regra = null;
      for (var k = 0; k < cfg.regras.length; k++) {
        var r = cfg.regras[k];
        var falta = (r.se_falta || []).some(function (id) { return ids.indexOf(id) < 0; });
        var tem = (r.se_tem || []).some(function (id) { return ids.indexOf(id) >= 0; });
        if ((r.se_falta && falta) || (r.se_tem && tem)) { regra = r; break; }
      }
      $(pref + "-explica").innerHTML = regra ? regra.msg : cfg.ok;
      var montado = $(pref + "-montado");
      if (montado) montado.innerHTML = caixaPedido(cfg.rotulo_montado || "Pedido montado", pedido || "(nada selecionado)");
      var barra = $(pref + "-barra");
      if (barra) {
        var total = sel.reduce(function (s, it) { return s + (it.chars || 0); }, 0) || 1;
        barra.innerHTML = sel.filter(function (it) { return it.chars; }).map(function (it) {
          return '<span style="width:' + (100 * it.chars / total).toFixed(1) + "%;background:" + it.cor + '" title="' + esc(it.rot) + '">' + (it.chars / total > 0.12 ? esc(it.rot) : "") + "</span>";
        }).join("");
        $(pref + "-total").textContent = sel.reduce(function (s, it) { return s + (it.chars || 0); }, 0).toLocaleString("pt-BR") + " caracteres no material escolhido";
      }
      return pedido;
    }
    lista.addEventListener("change", montar);
    montar();
    if (cfg.vivo) ligarVivo(pref, function () { return (cfg.vivo_prefixo || "") + montar(); });
  }

  function calc(pref, cfg) {
    var imp = $(pref + "-imp"), urg = $(pref + "-urg"), bug = $(pref + "-bug");
    function faixa(s, comBug) { return (comBug ? s > 5 : s >= 5) ? "alta" : s >= 3 ? "media" : "baixa"; }
    function atualizar() {
      var i = Number(imp.value), u = Number(urg.value), s = i + u;
      $(pref + "-vi").textContent = i; $(pref + "-vu").textContent = u;
      var certa = faixa(s, false), errada = faixa(s, true);
      var linhas = [2, 3, 4, 5, 6].map(function (x) {
        var c = faixa(x, false), b = faixa(x, true);
        return "<tr" + (x === s ? ' class="dest"' : "") + "><td>" + x + "</td><td>" + c + "</td>" + (bug.checked ? "<td>" + b + (b !== c ? ' <span class="tag x">diverge</span>' : "") + "</td>" : "") + "</tr>";
      }).join("");
      $(pref + "-tab").innerHTML = '<div class="rolagem"><table class="tabela"><thead><tr><th>Soma</th><th>R1</th>' + (bug.checked ? "<th>Código com “maior que 5”</th>" : "") + "</tr></thead><tbody>" + linhas + "</tbody></table></div>";
      var msg = "Impacto " + i + " + urgência " + u + " = <b>soma " + s + "</b>, prioridade <b>" + certa + "</b> pela R1.";
      if (bug.checked) msg += certa === errada ? " O código com “maior que 5” também dá " + errada + " aqui: este caso não revela o defeito." : " O código com “maior que 5” dá <b>" + errada + "</b>: só a soma 5 revela o defeito. É por isso que o caso de fronteira entra no critério.";
      else if (s === 4 || s === 5) msg += " Você está na fronteira entre media e alta.";
      $(pref + "-explica").innerHTML = msg;
    }
    [imp, urg, bug].forEach(function (el) { el.addEventListener("input", atualizar); });
    atualizar();
  }

  /* erro composto: acerto por passo elevado ao número de passos */
  function composto(pref, cfg) {
    var a = $(pref + "-acerto"), n = $(pref + "-passos");
    function pct(x) { return (100 * x).toLocaleString("pt-BR", { maximumFractionDigits: 0 }) + "%"; }
    function atualizar() {
      var p = Number(a.value) / 100, k = Number(n.value), total = Math.pow(p, k);
      $(pref + "-va").textContent = a.value + "%";
      $(pref + "-vp").textContent = k;
      $(pref + "-barra").innerHTML = '<span style="width:' + (100 * total).toFixed(1) + '%"></span>';
      $(pref + "-explica").innerHTML = "Com <b>" + a.value + "%</b> de acerto em cada passo e <b>" + k + "</b> passo" + (k > 1 ? "s" : "") +
        " em sequência, a execução inteira acerta <b>" + pct(total) + "</b>. " +
        (total < 0.5 ? "Menos da metade das execuções chega ao fim sem erro." : total < 0.8 ? "Cerca de " + Math.round((1 - total) * 10) + " em cada 10 execuções erram em algum passo." : "Ainda alto, mas cada passo a mais tira um pouco.");
      var linhas = (cfg.marcos || [1, 5, 10, 20, 30]).map(function (m) {
        return "<tr" + (m === k ? ' class="dest"' : "") + "><td>" + m + "</td><td>" + pct(Math.pow(p, m)) + "</td></tr>";
      }).join("");
      $(pref + "-tab").innerHTML = '<div class="rolagem"><table class="tabela"><thead><tr><th>Passos</th><th>Acerto da execução</th></tr></thead><tbody>' + linhas + "</tbody></table></div>";
    }
    [a, n].forEach(function (el) { el.addEventListener("input", atualizar); });
    atualizar();
  }

  /*@inclui agente_caso.js*/

  /* custo: tokens e preço viram custo por chamada, por tarefa e por sucesso */
  function custo(pref, cfg) {
    var campos = ["chamadas", "entrada", "cache", "saida", "pin", "pcache", "pout", "sucesso"];
    function v(id) { return Number($(pref + "-" + id).value) || 0; }
    function usd(x) { return "US$ " + x.toLocaleString("pt-BR", { minimumFractionDigits: 4, maximumFractionDigits: 4 }); }
    function atualizar() {
      var n = v("chamadas"), ent = v("entrada"), frac = v("cache") / 100, sai = v("saida");
      var porChamada = (ent * (1 - frac) * v("pin") + ent * frac * v("pcache") + sai * v("pout")) / 1e6;
      var porTarefa = porChamada * n, taxa = v("sucesso") / 100;
      $(pref + "-res").innerHTML = '<div class="rolagem"><table class="tabela"><tbody>' +
        "<tr><td>Por chamada ao modelo</td><td><b>" + usd(porChamada) + "</b></td></tr>" +
        "<tr><td>Por tarefa (" + n + " chamada" + (n > 1 ? "s" : "") + ")</td><td><b>" + usd(porTarefa) + "</b></td></tr>" +
        '<tr class="dest"><td>Por sucesso (' + Math.round(taxa * 100) + "% das tarefas resolvidas)</td><td><b>" + (taxa > 0 ? usd(porTarefa / taxa) : "sem sucesso, custo infinito") + "</b></td></tr>" +
        "</tbody></table></div>";
      $(pref + "-explica").innerHTML = "Cada volta reenvia a janela inteira: " + n + " chamada" + (n > 1 ? "s" : "") + " de " + ent.toLocaleString("pt-BR") +
        " tokens de entrada, " + Math.round(frac * 100) + "% servidos pelo cache. Com " + Math.round(taxa * 100) + "% de sucesso, o custo de um resultado útil é " +
        (taxa > 0 ? (1 / taxa).toLocaleString("pt-BR", { maximumFractionDigits: 2 }) + " vezes o custo de uma tarefa." : "indefinido.");
    }
    campos.forEach(function (c) { var el = $(pref + "-" + c); if (el) el.addEventListener("input", atualizar); });
    atualizar();
  }

  /* copiar comandos */
  document.querySelectorAll("pre.cmd").forEach(function (pre) {
    var b = document.createElement("button");
    b.type = "button"; b.textContent = "Copiar";
    b.addEventListener("click", function () {
      var t = pre.firstChild ? pre.firstChild.textContent : pre.textContent;
      var ok = function () { b.textContent = "Copiado"; setTimeout(function () { b.textContent = "Copiar"; }, 1500); };
      try { navigator.clipboard.writeText(t).then(ok, function () { selecionar(pre); }); } catch (e) { selecionar(pre); }
    });
    pre.appendChild(b);
  });
  function selecionar(el) { var r = document.createRange(); r.selectNodeContents(el); var s = window.getSelection(); s.removeAllRanges(); s.addRange(r); }

  Object.keys(DADOS.bancadas).forEach(function (pref) {
    var cfg = DADOS.bancadas[pref];
    if (cfg.tipo === "passos") {
      stepper(pref, cfg.passos);
      if (cfg.vivo) ligarVivo(pref, function () { return DADOS.pedidos[cfg.vivo]; });
      if (cfg.agente) ligarAgente(pref, cfg.agente);
      (cfg.vivos || []).forEach(function (v, k) {
        var p = pref + "-v" + k;
        if (v.segundo) ligarRevisao(p, v.chave, v.segundo);
        else ligarVivo(p, function () { return DADOS.pedidos[v.chave]; });
      });
    } else if (cfg.tipo === "quiz") quiz(pref, cfg);
    else if (cfg.tipo === "seletor") seletor(pref, cfg);
    else if (cfg.tipo === "calc") calc(pref, cfg);
    else if (cfg.tipo === "composto") composto(pref, cfg);
    else if (cfg.tipo === "custo") custo(pref, cfg);
  });
})();
