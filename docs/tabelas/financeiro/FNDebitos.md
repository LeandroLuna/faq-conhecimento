### Tipo

> Tipo do débito.

???+ note "Tipos"

    * Acordo, Acordos, Agente Financiador, Atividade Extra, CD - Mensalidade, Cheque, Confissões, Conteúdo Programático, Declaração de Escolaridade, Diferença, Diferença de Plano, Diferença Plano, Entrada, Histórico Escolar, Integral, Livro, Matrícula, Matrícula - Pós, Matricula-Integral, McDiaFeliz, Mensalidade, MI - Mensalidade, Multa, Outros, Pagamento, Passeio, Passeio-Copi, Produto, Projeto, ProvaSub-Copi, Renovação de Matrícula, Seguro Desemprego, Taxa, Teatro

### AgrupadorDebito

> Agrupar os débitos gerados em massa por aluno. (quase não usa)

### Nser & Lser & Lcur

> Número da Série / Turma / Identificação do Curso

| NSER | LCUR | LSER | PER | RESULTADO |
|---   | ---  | ---  | --- | ---       |
| 4    | SI   | A    | M   |  4SIA     |
| 6    | EXT  | M    | T   | 6EXTM     |
| 67   | NEG  |      | N   | 67NEG     |
| 1    | TGO  | C    | O   | 1TGOC     |

### SemAno

> Identificação se a turma é semestral ou anual

### Con

> Condição do débito

* A (ativo)
* E (estornado)
* X (trancado)
* D (desistente)

### MesAnoEvd

> Indica qual o mês e ano que o aluno evadiu

### Externa

> No sistema antigo indicava se estava no jurídico

Atualmente indica se o acordo está cancelado.

### SPC

> Indica se a mensalidade está no orgão de proteção ao consumidor.

Serviço de proteção ao crédito, atualmente utilzamos o SERASA.

### DP

> Indica quantas dependências (DP) o aluno irá fazer a mais no ano.

Cobra-se 15% a mais no boleto por estar fazendo dp presencial, caso semi-presencial não cobra.
A coluna também é utilizada para acrescentar 15% ao débito do aluno.

**DP de alunos 100% ON agora paga 15% por disciplina**.

### Adap

> Adaptação. (quase não usa)

### CodigoTabelaValor & CodigoTabelaValorVencimento & TabPreco

> Indica a parametrização da mensalidade daquele ano.

Sinergista com a tabela FNTabelaValorVencimento/FNTabelaValor.

Com isso consegue descobrir todos os valores/vencimentos/descontos para as mensalidades.

É atrelado inicialmente no débito do tipo 'Matricula'.

A partir dos valores, é gerado todas as mensalidades corretamente.

### TaxaMulta & TaxaJuros

> Taxa cobrada quando aluno atrasa no pagamento.

Job executa a 00:00, pega todos os débitos não pagos e vencidos, pega o valor e acresce a TAXA como multa + TAXAJuros.

Com isso chega no valor do débito atualizado.

### Plano

> Plano do aluno. Colégio é sempre 12, graduação tem 4 planos.

* 1 Anual - *12x no ano*
* 2 Extendido - *1 ano a mais do que o que deveria* ex: 4 anos vai para 5.
* 3 Extendidão - *2 anos a mais do que deveria) ex: 4 vai para 6*. (não existe mais)
* 4 A vista - *Paga as 12x em 1x*
* PÓS - *O plano é o número de parcelas* (de 1 até 24)

### Bolsa

> Porcentagem de bolsa do aluno.

Mais importante do que as tabelas de bolsa

### ParcelaComplemento
> Utilizava-se na época em que as empresas pagavam em vale.

1 parcela era dividido 2x no mês. Mas atualmente quase nenhuma empresa paga com vale.

### Mes e Ano

> Mes e ano de refêrencia.

Muito utilizado ao emitir boleto, alterar plano, antecipação, negociação.

### ValorCheioNominal

> **Valor real do curso que se origina da TabelaValor.**

### ValorDescontoNominal

> **Valor com desconto do ValorCheioNominal (pontualidade até dia 5).**

### DataVencimentoPadrao & DataDescontoPadrao

> Data de vencimento que se origina na FNTabelaValorVencimento/FNTabelaValor.

### ValorCheioDebito

> **ValorCheioNominal com bolsa, com dp, adaptação, dedução aplicado.**

### ValorDescontoDebito

> **ValorDescontoNominal com a explicação anterior aplicada.**

### ValorJuros

> (ValorCheioDebito + ValorMulta) * TaxaJuros * Qtd

(cobra-se todo dia)

### ValorMulta

> Colunas: ValorCheioDebito * TaxaMulta

(cobra-se uma vez)

### DataVencimentoDebito & DataDescontoDebito

> Serve para 'sobrescrever' a data de vencimento padrão (quando o responsável recebe após o dia da pontualidade)

### DataVencimento

> Data de vencimento 'NO HOJE'

### ValorDebito

> Valor que deverá pagar 'NO HOJE',

* **Atrasado**:

*ValorCheioDebito + ValorMulta + ValorJuros.*

* **Pontualidade**:

*até dia 5 (graduação e mba) ou 5º dia util (colégio) é a coluna ValorDescontoDebito*

* **Depois da pontualidade**:

*ValorCheioDebito*

### ValorPago

> ValorPago. **NULL = NÃO PAGOU**

### DataOutLan

> Data ultimo lançamento. Quando aluno tranca ou desiste, é inserido aqui a data.

### DataAtualizado

> (não usa mais) Antes, quando rodava o processo que atualiza o debito, dava update nesse campo pra dizer em qual dia foi atualizado mas ficava lento pois era muito registro. 

> Hoje em dia é o dia que foi cadastrado.

### QtDiasAtrasado

> Quantidade de dias atrasado, se for adiantado, exibe negativo. Mas quando chega no dia volta pra 0.

### UsoEmpresa

> Número enviamos para o banco.

### NossoNumero

> Número que o banco retorna do boleto.

*Boleto registrado carteira* **112**

*Caso carteira **109**, os dois campos nós informamos*

### NumDoc

> Identificador para débitos do sistema antigo.

### CodigoNegociacao

> Código do acordo que foi gerado para o aluno.

**Indica que esse débito foi gerado por causa do acordo ou seja, é o debito gerado na negociação para o aluno pagar. (tabela FNNegociacao(Codigo))**

### CodigoPessoaRespFinanceiro

> (não usa mais) usa-se a coluna CPFResponsavel.

### CodigoUsuarioCadastro

> Usuário da intranet que cadastrou o débito (1 = administrador / via sistema automático)

### Excluido

> Como se fosse a coluna 'Ativo', ao invés de DELETE, update = 0 nessa coluna.

### Abonado

> O aluno deve um valor, mas a empresa (FIAP) abona esse valor.

### DataHoraAbono

> Data de aplicação do abono, inserido pelo sistema de abonar.

### CpfResponsavel

> CPF da pessoa que deverá pagar o débito. É quem será cobrado pelo financeiro.

### DescricaoDebito

> Exibe informações do débito concatenada, para facilitar a exibição.

### Visivel

> Determina se o débito ficará ou não visível para o aluno / sistemas informativos.

Todo débito ativo (não excluido) é visivel. É utilizado nos tipos de débito 'Produto' que são por exemplo, passeios do colégio. Quando a pessoa cadastra o débito do passeio, não deixa visivel e caso o responsável pague, fica visivel.

**Como o passeio é opcional, não há a necessidade de exibir o débito para o aluno que não irá para o evento.**

**Normalmente quando está com valor 1 é porque está pago.**

### MotivoExclusao

> Iria utilizar em um sistema de exclusão de débito. (não existe)

### CodigoBMRemessa

> BM = BoletoMensalidade.

> Código da tabela de registro do boleto. **Educacional..BMRemessa**

### CodigoArquivoRetornoBancoRegistro

Todos os dias o financeiro entra no sistema
do banco e baixa o arquivo. (arquivo retorno/francesinha)

É um .txt que informa quais boletos foram pagos, onde, dia e valor.
Um job pega esses boletos desse arquivo, quebra em tabela e executa um update.

O sistema faz o upload do txt que o banco enviou, e roda um job,
destrincha o txt, e cadastra na Educacional..ArquivoRetornoBancoRegistro

**Colunas que compara com FNDebitos para dar update que foi pago:**

**Educacional..BMRemssa possue o código FNDebitos com isso, é possível descobrir qual o Debito pago.**

### ValidadoBaixa

> Utilizado no script que realiza baixa.

Realiza um update nos débitos que foram pagos por boleto, depois confere se foi dado baixa mesmo e se gerou diferença de mensalidade.

### MotivoAlteracaoDataVencimento

> Quando altera apenas um débito, precisa apresentar o motivo (perdeu o prazo, perdeu o boleto etc..)

Temos 2 sistemas que alteram a data de vencimento. *(1 que altera 1 debito e outro que altera vários)*

### RecalculouMultaJuros

> Script que informa se RecalculouMultaJuros. (não usa muito)

### Controle

> Em 2016 foi importado os registro antigos, então se for 'Novo' é depois dessa época.

### IDdebito

> Identificador do débito antigo. *(nós DEVS não usamos muito)*

### Bolsa 1 á 5 e Motivo 1 á 5

> Sistema Antigo, antes não usava FK nas bolsas, ou seja só podia cadastrar 5 bolsas. *(não usa-se mais)*

### CodigoBaixaAvulso

> Utilizado quando recebe diretamente na conta.

Sistema de baixa avulsa. Seleciona o debito, dia que recebeu, valor, e o motivo. Realiza um update no data pagamento, cria um FNBaixaAvulso e esse código é inserido nesta coluna.

### CodigoContaCorrente

> FK para identificar as informações da conta que irá receber o valor.

*(Para a tabela BOControle)*

### CodigoLogCriacao

> Código do Log

Em alguns sistemas que altera ou recria os débitos, existe uma tabela de log e o código é inserido nesta coluna. *(Tabela LogDebito)*

### OrgaoSPC

> Orgão que foi acionado.

Pode ser SERASA ou SPC. *(SE ou SP)*

### DataNovoVencimento

> Data do vencimento ajustada por alguém.

No sistema que altera um único débito, além de atualizar a data, adiciona aqui também.

Um job que verifica quais débitos foram alterados a data de vencimento e se o aluno ou responsável não pagar, voltará para a data original.

### OpcaoSelecionadaAlteraDataVencimento

> No sistema que altera a data de 1 débito, tem 4 opções:

* 1 - Manter o valor do débito atual até a nova data de vencimento.

* 2 - Altera o valor do debito para a pontualidade ate a nova data.

* 3 - Altera o valor do debito para o valor cheio ate a nova data.

* 4 - Calcular o juros e muta ate a nova data. e fica aqui essa opção.

### CodigoFNRecebimento

> Codigo da tabela FNRecebimento.

Quando o aluno paga aqui na própria unidade gera um recebimento ou seja pago no HELPCENTER.

### ValorAcrescimo

> Quando o aluno por exemplo, pagou mas faltou 100 reais do mês passado, então no mês seguinte é lançado a mais. e aqui vem esse valor a mais.

*(Realiza um update no valor cheio debito, valor desconto debito e valor debito)*

### ValorDeducao

> Inverso do valor acrescimo.

Exemplo: promoção, se pagar até x dia, tem 15% de desconto na sua primeira mensalidade.

### DescricaoValorDeducao

> Motivo da dedução

Exemplo: pagou rematricula até x dia.

### Estorno

> Débito que não deveria existir.

Exemplo: Gerei um débito para o aluno mas foi por engano, ele não deve pagar.

### NRPS

> Identifica a nota fiscal gerada para o aluno. *(não utilizado)*

Atualmente a informação está na tabela NFE..NFEItem

### AnoReferencia

> Ano que o débito referencia. (plano estendido)

### UnidadeParcelaEstendido

> Unidade que ele estudava no ano
