# Alteração de Valor de Débito (Dedução e Acréscimo)

<div style="height: 300px; overflow-x:scroll;">
    <img src="../alteracao-de-valor-de-debito-deducao-e-acrescimo.svg" style="max-width: initial;">
</div>

## Alterar Valor do Débito

Para **alterar o valor de um débito** é necessário aplicar uma **dedução** ou um 
**acréscimo** ao débito, a partir do sistema **Alterar Valor do Débito**, 
que pode ser encontrado na unidade **Help Center** 
da [Intranet Nova](https://intranet.fiap.com.br/) e 
no [Repositório do GitLab](https://gitlab.fiap.com.br/dotnet/Intranet.Negociacao) 
(**AlteraValorDebitoController**).

Além de atribuir o acréscimo ou dedução ao débito, o sistema também cadastra um 
registro na tabela **HistoricoPessoa**, informando a alteração de valor que foi 
realizada.

Conforme informado na documentação de 
[Origem dos Valores de um Débito](http://conhecimento.fiap.com.br/processos/financeiro/Origem%20dos%20Valores%20de%20um%20Débito/valores-dos-debitos/), 
para compor o valor final do débito, é feito o seguinte cálculo:

```sql
-- Valores calculados logo antes do valor final do débito:
ValorDescontoDebito = ValorDescontoNominal * (1 - Bolsa/100) - ISNULL(ValorDeducao, 0) + ISNULL(ValorAcrescimo, 0)
ValorCheioDebito = ValorCheioNominal * (1 - Bolsa/100) - ISNULL(ValorDeducao, 0) + ISNULL(ValorAcrescimo, 0)

-- Caso a data atual seja até a DataDescontoDebito (Data de pontualidade):
ValorDebito = ValorDescontoDebito

-- Caso a data atual seja após a DataDescontoDebito (Data de pontualidade) até a DataVencimentoDebito (Data de Vencimento):
ValorDebito = ValorCheioDebito

-- Caso a data atual seja após a DataVencimentoDebito (Data de Vencimento):
ValorJuros = ROUND(ValorCheioDebito * ISNULL(TaxaJuros, 0.00033) * QtDiasAtrasado, 2)
ValorMulta = ROUND(ValorCheioDebito * ISNULL(TaxaMulta, 0.02), 2)

ValorDebito = ValorCheioDebito + ISNULL(ValorJuros, 0) + ISNULL(ValorMulta, 0)

/*
OBS: 
A coluna Bolsa armazena valores de 0 a 100 e não admite nulos.
As colunas ValorDeducao e ValorAcrescimo, possuem o valor de alteração positivo.
Caso o débito não possua dedução ou acréscimo, estas colunas ficam nulas.
Caso o débito não possua valores de multa e juros, estas colunas ficam nulas.
ValorDebito é o valor final do débito.
*/
```

## Dedução de Valor

Para aplicar uma **dedução** via sistema, basta **selecionar o débito** 
desejado, marcar a opção **Deduzir**, informar o **motivo da dedução** e efetivar 
a alteração de valor.

O **limite máximo de valor** que pode ser **deduzido** é o valor que resulta em um 
**valor final zero** para o débito.

Ao aplicar uma **dedução** para um débito que **já foi deduzido**, os valores 
**não serão somados**. O valor que será **considerado** é o valor da 
**última dedução realizada**, assim como o **motivo**.

## Acréscimo de Valor

Para aplicar um **acréscimo** via sistema, **selecione o débito** 
desejado, marque a opção **Acrescer**, informe o **motivo do acréscimo** e finalize 
a alteração de valor.

Ao aplicar um **acréscimo** para um débito que **já foi acrescido**, os valores 
**não serão somados**. O valor que será **considerado** é o valor do 
**último acréscimo realizado**, assim como o **motivo**.

## Aplicando uma dedução ou um acréscimo via script:

```sql
-- Buscando o débito que será deduzido ou acrescido:
SELECT
  Codigo,
  RM,
  CPFResponsavel,
  Tipo,
  Ano,
  Mes,
  *
FROM
  BaseEducacional..FNDebitos
WHERE
  MesAnoEvd IS NULL
  AND DataOutLan IS NULL
  AND Visivel = 1
  AND Excluido = 0
  AND Abonado = 0
  AND Con = 'A'
  AND DebitoEmAcordo = 0
  AND ValorDebito > 0
  AND ValorPago IS NULL
  AND RM = @RM;

-- Caso queira aplicar uma dedução:
UPDATE
  BaseEducacional..FNDebitos
SET
  ValorDeducao = @ValorDeducao,
  DescricaoValorDeducao = @MotivoDeducao
WHERE
  Codigo = @CodigoDebito;

-- Caso queira aplicar um acréscimo:
UPDATE
  BaseEducacional..FNDebitos
SET
  ValorAcrescimo = @ValorAcrescimo,
  DescricaoValorAcrescimo = @MotivoAcrescimo
WHERE
  Codigo = @CodigoDebito;

-- Executar a procedure que atualiza o débito como um todo, tanto para acréscimo quanto para dedução:
EXEC BaseEducacional..spAtualizaDebito @Codigo = @CodigoDebito;

-- Inserindo informação de alteração de valor (acréscimo ou dedução) no histórico do aluno:
INSERT INTO BaseEducacional..HistoricoPessoa
  (CPFCNPJ, 
  RM, 
  Cabecalho, 
  Observacao, 
  Origem, 
  CodigoUsuarioCadastro, 
  DataHoraCadastro, 
  Ativo)
VALUES
  (@CPFResponsavel, 
  @RM, 
  '', 
  @MotivoAlteracaoValor, 
  'Altera Valor Debito', 
  @CodigoUsuario, 
  GETDATE(), 
  1);
```

## Ficha Financeira

Na **Ficha Financeira** do aluno 
([Projeto Intranet.Negociacao](https://gitlab.fiap.com.br/dotnet/Intranet.Negociacao), 
**ListagemDebitosController**) é possível visualizar a **alteração de valor** no 
**informativo** detalhado do **débito** em questão, além do **Histórico**.

Caso o **valor final** do débito esteja **zerado** ele não será cobrado, então o débito ficará na aba de **Pagos**.

### Observação:
```
Todas as tabelas citadas são do banco "BaseEducacional".
```