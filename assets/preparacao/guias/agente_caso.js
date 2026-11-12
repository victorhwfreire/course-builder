  /* ferramentas da página para o agente ao vivo */
  function ferramentasArquivos(arquivos, registrar) {
    return [
      { name: "listar_arquivos", description: "Lista os nomes dos arquivos de dados do Balcão. Não recebe argumentos.",
        execute: function () { registrar("<code>listar_arquivos</code>"); return Object.keys(arquivos); } },
      { name: "ler_arquivo", description: "Devolve o conteúdo de um arquivo de dados do Balcão pelo nome, por exemplo cobrancas.json.",
        inputSchema: { type: "object", properties: { nome: { type: "string", description: "nome do arquivo, como listar_arquivos devolve" } }, required: ["nome"] },
        execute: function (inp) {
          var nome = String(inp && inp.nome || "");
          registrar("<code>ler_arquivo</code> " + esc(nome));
          if (!Object.prototype.hasOwnProperty.call(arquivos, nome)) throw new Error("Arquivo não encontrado: " + nome + ". Use listar_arquivos para ver os nomes.");
          return arquivos[nome];
        } }
    ];
  }

  /* as ferramentas do servidor do Balcão, com os mesmos contratos e mensagens do servidor_balcao.py; estorno simulado */
  function ferramentasBalcao(ag, registrar) {
    var clientes = JSON.parse(ag.arquivos["clientes.json"]).clientes, cobrancas = JSON.parse(ag.arquivos["cobrancas.json"]).cobrancas;
    function brl(v) { return "R$ " + Number(v).toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 }); }
    function chamada(nome, inp, fn) {
      var args = esc(JSON.stringify(inp || {}));
      try {
        var r = fn(inp || {});
        registrar("<code>" + nome + "</code> " + args + '<br><small class="ok">volta: ' + esc(String(typeof r === "string" ? r : JSON.stringify(r)).slice(0, 160)) + "</small>");
        return r;
      } catch (e) {
        registrar("<code>" + nome + "</code> " + args + '<br><small class="erro">' + esc(e.message) + "</small>");
        throw e;
      }
    }
    if (ag.modo === "fraco") {
      return [{ name: "get_data", description: "Consulta dados.",
        inputSchema: { type: "object", properties: { cliente: { type: "string" }, periodo: { type: "string" } }, required: ["cliente", "periodo"] },
        execute: function (inp) { return chamada("get_data", inp, function (a) {
          var c = String(a.cliente || ""), p = String(a.periodo || "");
          if (!/^CLI-\d{3}$/.test(c) || !/^\d{4}-\d{2}$/.test(p)) throw new Error("invalid input");
          return cobrancas.filter(function (x) { return x.cliente_id === c && x.data.indexOf(p) === 0; });
        }); } }];
    }
    return [
      { name: "buscar_cliente", description: "Encontra o id de um cliente do Balcão a partir do nome do comércio. Use quando o ticket traz só o nome.",
        inputSchema: { type: "object", properties: { nome: { type: "string", description: "Nome do comércio como o cliente escreveu, ex.: 'Estúdio Pilates Vida'. Aceita parte do nome." } }, required: ["nome"] },
        execute: function (inp) { return chamada("buscar_cliente", inp, function (a) {
          var nome = String(a.nome || "").trim().toLowerCase();
          var achados = clientes.filter(function (c) { return nome && c.nome.toLowerCase().indexOf(nome) >= 0; });
          if (!achados.length) throw new Error("Nenhum cliente com nome parecido com '" + a.nome + "'. Confira a grafia ou use um trecho menor do nome.");
          if (achados.length > 1) throw new Error("'" + a.nome + "' bate com " + achados.length + " clientes. Use um trecho que identifique um só.");
          var c = achados[0];
          return { cliente_id: c.id, nome: c.nome, plano: c.plano, mensalidade: c.mensalidade };
        }); } },
      { name: "consultar_cobrancas", description: "Lista os lançamentos que o Balcão cobrou de um cliente num mês: mensalidades e tarifas, com id, data, tipo, valor e status. Use para conferir cobrança duplicada ou tarifa contestada.",
        inputSchema: { type: "object", properties: {
          cliente_id: { type: "string", description: "Id do cliente no formato CLI-123, ex.: 'CLI-102'. Se você só tem o nome, chame buscar_cliente antes." },
          mes: { type: "string", description: "Mês no formato AAAA-MM, ex.: '2026-10' para outubro de 2026." } }, required: ["cliente_id", "mes"] },
        execute: function (inp) { return chamada("consultar_cobrancas", inp, function (a) {
          var c = String(a.cliente_id || ""), m = String(a.mes || "");
          if (!/^CLI-\d{3}$/.test(c)) throw new Error("cliente_id deve ter o formato CLI-123. Recebido: '" + c + "'. Se você tem o nome do comércio, chame buscar_cliente para obter o id.");
          if (!/^\d{4}-\d{2}$/.test(m)) throw new Error("mes deve ter o formato AAAA-MM, por exemplo '2026-10'. Recebido: '" + m + "'. Reenvie com o formato correto.");
          if (!clientes.some(function (x) { return x.id === c; })) throw new Error("Não existe cliente " + c + ". Confira o id com buscar_cliente.");
          var itens = cobrancas.filter(function (x) { return x.cliente_id === c && x.data.indexOf(m) === 0; });
          return { cliente_id: c, mes: m, cobrancas: itens, total: Math.round(itens.reduce(function (s, x) { return s + x.valor; }, 0) * 100) / 100 };
        }); } },
      { name: "registrar_nota", description: "Registra uma nota no ticket. Mutante e não idempotente: cada chamada cria uma nota nova.",
        inputSchema: { type: "object", properties: { ticket_id: { type: "string", description: "Id do ticket, ex.: 'TCK-002'." }, texto: { type: "string", description: "O que foi verificado e decidido, em uma ou duas frases." } }, required: ["ticket_id", "texto"] },
        execute: function (inp) { return chamada("registrar_nota", inp, function (a) {
          return "Nota registrada no " + a.ticket_id + ". Cada chamada cria uma nota nova: não repita se esta deu certo.";
        }); } },
      { name: "emitir_estorno", description: "Emite o estorno de um lançamento. Destrutiva: dinheiro que sai não volta. Nesta demonstração o estorno é simulado.",
        inputSchema: { type: "object", properties: {
          cobranca_id: { type: "string", description: "Id do lançamento a estornar, ex.: 'COB-5003'. Obtenha com consultar_cobrancas." },
          valor: { type: "number", description: "Valor do estorno em reais, ex.: 189.90." },
          motivo: { type: "string", description: "Motivo em uma frase, ex.: 'mensalidade cobrada em duplicidade'." } }, required: ["cobranca_id", "valor", "motivo"] },
        execute: function (inp) { return chamada("emitir_estorno", inp, function (a) {
          var cob = cobrancas.filter(function (x) { return x.id === a.cobranca_id; })[0], valor = Number(a.valor);
          if (ag.guarda) {
            if (!cob) throw new Error("Negado pela política: lançamento " + a.cobranca_id + " não existe. Consulte as cobranças do cliente antes.");
            if (Math.abs(valor - cob.valor) > 0.005) throw new Error("Negado pela política: o estorno é do valor do lançamento (" + brl(cob.valor) + "), não " + brl(valor) + ".");
            if (valor > 200) throw new Error("Negado pela política: estorno acima de R$ 200,00 exige aprovação do financeiro. Registre uma nota e encaminhe.");
          }
          if (!cob) throw new Error("Não existe o lançamento " + a.cobranca_id + ". Use consultar_cobrancas para ver os ids do cliente.");
          if (!(valor > 0)) throw new Error("valor deve ser maior que zero. Recebido: " + a.valor + ".");
          return "Estorno SIMULADO de " + brl(valor) + " no lançamento " + a.cobranca_id + " (" + cob.cliente_id + "). Nenhum dinheiro foi movimentado.";
        }); } }
    ];
  }

  /* agente ao vivo: o modelo recebe ferramentas da própria página e decide o que chamar */
  function ligarAgente(pref, ag) {
    var b = $(pref + "-agente");
    if (!b) return;
    b.addEventListener("click", function () {
      var log = $(pref + "-agvoltas"), alvo = $(pref + "-agvivo"), aviso = $(pref + "-agaviso"), n = 0;
      function registrar(txt) {
        n++;
        log.insertAdjacentHTML("beforeend", '<div class="volta"><small>Chamada ' + n + "</small><span>" + txt + "</span></div>");
      }
      var ferramentas = ag.modo && ag.modo !== "arquivos" ? ferramentasBalcao(ag, registrar) : ferramentasArquivos(ag.arquivos, registrar);
      log.innerHTML = "";
      aviso.textContent = "";
      b.disabled = true;
      alvo.innerHTML = '<p class="pensando">Pensando… com ferramentas, a resposta costuma levar de 30 a 90 segundos.</p>';
      Promise.resolve(SAMPLE.limits ? SAMPLE.limits().catch(function () { return null; }) : null)
        .then(function (lim) {
          if (!lim || !lim.tools) throw { code: "tools_unavailable" };
          return SAMPLE(DADOS.pedidos[ag.chave], { tools: ferramentas, onText: function (u) { alvo.innerHTML = md(u.text); } });
        })
        .then(function () { aviso.textContent = "Resposta ao vivo, gerada agora, com " + n + " chamada(s) de ferramenta."; })
        .catch(function (e) {
          if (e && e.text) alvo.innerHTML = md(e.text); else alvo.innerHTML = "";
          if (e && e.code === "tools_unavailable") aviso.textContent = "Esta visualização não deixa a página oferecer ferramentas ao Claude. As execuções registradas acima continuam valendo.";
          else if (!(e && e.code === "cancelled")) aviso.textContent = mensagemErro(e && e.code);
          if (e && (e.code === "not_granted" || e.code === "sampling_disabled")) mostrarAoVivo(false);
        })
        .then(function () { b.disabled = false; });
    });
  }
