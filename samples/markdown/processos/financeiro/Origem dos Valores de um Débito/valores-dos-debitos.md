# Origem dos Valores de um Débito

<div style="height: 750px; overflow-x:scroll;">
    <img src="../valores-dos-debitos.svg" style="max-width: initial;">
</div>

## Ofertas

As ofertas consistem nos **planos de pagamento** que são disponibilizados para 
cada **turma**.

## FNTabelaValor

Na **FNTabelaValor** são armazenados as seguintes informações para cada oferta:

- **Ano**: Ano que a turma se inicia;
- **TabPreco**: Turma a qual se refere;
- **Plano**: Número conforme [Planos de Pagamento](http://conhecimento.fiap.com.br/processos/financeiro/Planos%20de%20Pagamento%20e%20suas%20Alterações/planos-pagamento/);
- **Valor da Matrícula**;
- **Valor da Renovação de Matrícula**;

Ao gerar um débito de **Matrícula** ou **Renovação**, seus valores são 
preenchidos utilizando as informações da **FNTabelaValor** como "molde".

## FNTabelaValorVencimento

Cada oferta da **FNTabelaValor** está vinculada a uma lista de registros da 
**FNTabelaValorVencimento** e cada registro é tido como "molde" para gerar um 
débito de **Mensalidade**.

A **FNTabelaValorVencimento** armazena as seguintes informações:

- **Mês** e **Ano**: Mês/Ano que o débito será cobrado;
- **Número da parcela**: Ordem dos registros;
- **Data de Desconto**: Data limite do período de **pontualidade**, normalmente 
próxima ao **dia 5 de cada mês**;
- **Valor Desconto**: Valor que será cobrado dentro do período de 
**pontualidade** (até a **Data de Desconto**);
- **Data de Vencimento**: Data limite de pagamento sem acréscimo de juros e 
multa, normalmente próxima ao **dia 15 de cada mês**;
- **Valor Cheio**: Valor que será cobrado caso o aluno perca o período de 
pontualidade, mas ainda esteja dentro do limite da **Data de Vencimento**;
- **Multa** e **Juros**: Porcentagens (**de 0 a 1**) a serem acrescidas no 
**Valor Cheio** caso o aluno não pague até a **Data de Vencimento**. Após a 
**Data de Vencimento**, o valor final é atualizado diariamente;

## Baixando uma Matrícula ou Renovação

A baixa de um débito pode ser feita de várias formas:

- Pagamento 
([Boleto](http://conhecimento.fiap.com.br/tabelas/financeiro/Boleto/) 
ou Cartão);
- [Abono](http://conhecimento.fiap.com.br/processos/financeiro/Aplica%C3%A7%C3%A3o%20de%20Abono%20em%20D%C3%A9bitos/aplicacao-de-abono/);
- [Bolsa resultante = 100%](http://conhecimento.fiap.com.br/processos/financeiro/Aplica%C3%A7%C3%A3o%20de%20Bolsas%20em%20D%C3%A9bitos/aplicacao-de-bolsa/);
- [Dedução completa](http://conhecimento.fiap.com.br/processos/financeiro/Altera%C3%A7%C3%A3o%20de%20Valor%20de%20D%C3%A9bito%20%28Dedu%C3%A7%C3%A3o%20e%20Acr%C3%A9scimo%29/alteracao-de-valor-de-debito-deducao-e-acrescimo/#deducao-de-valor);


Quando uma **Matrícula** ou **Renovação** é baixada, a trigger da FNDebitos 
**trFNDebitos** identifica esta alteração e, dentre outros procedimentos, 
executa uma procedure para gerar as mensalidade. De acordo com a 
**Unidade de Negócio** do aluno (**FIAP School**, **Graduação**, **MBA**, 
**Pós Tech**) 
e o **tipo de débito** (**Matrícula**, **Renovação de Matrícula** ou 
**Matricula-Integral**), é definido qual procedure deve ser executada:

- **spGeraMensalidadeMatriculaCopi**: para Matrículas de FIAP School;
- **spGeraMensalidadeMatriculaFiap**: para Matrículas de Graduação;
- **spGeraMensalidadeMatriculaIntegralCopi**: para Matrículas de Período 
Integral (FIAP School);
- **spGeraDebitoMensalidadesPos**: para Matrículas de MBA;
- **spGeraDebitoMensalidadesPosTech**: para Matrículas de Pós Tech;
- **spGeraMensalidadeRematriculaCopi**: para Renovações de FIAP School;
- **spGeraMensalidadeRematriculaFIAP**: para Renovações de Graduação;

Estas procedures são responsáveis por recuperar o **CodigoTabelaValor** do 
débito baixado e **gerar as mensalidades** de acordo com as informações das 
tabelas **FNTabelaValor** e **FNTabelaValorVencimento** que estão vinculadas ao 
**CodigoTabelaValor** recuperado.

As **Mensalidades** geradas na **FNDebitos** terão estes campos preenchidos de 
acordo com as **tabelas de valor**:

- **CodigoTabelaValor** = **FNTabelaValor.Codigo**;
- **CodigoTabelaValorVencimento** = **FNTabelaValorVencimento.Codigo**;
- **Ano** = **FNTabelaValorVencimento.Ano**;
- **Mes** = **FNTabelaValorVencimento.Mes**;
- **TabPreco** = **FNTabelaValor.TabPreco**;
- **Plano** = **FNTabelaValor.Plano**;
- **ValorCheioNominal** = **FNTabelaValorVencimento.ValorCheio**;
- **ValorDescontoNominal** = **FNTabelaValorVencimento.ValorDesconto**;
- **DataVencimentoPadrao** = **FNTabelaValorVencimento.DataVencimento**;
- **DataDescontoPadrao** = **FNTabelaValorVencimento.DataDesconto**;
- **TaxaJuros** = **FNTabelaValorVencimento.JurosDia**;
- **TaxaMulta** = **FNTabelaValorVencimento.Multa**;

## Datas dos Débitos

As **5 colunas** principais de **datas nos débitos**:

- **DataVencimentoPadrao**: recebe o informado na coluna **DataVencimento** da 
**FNTabelaValorVencimento**;
- **DataDescontoPadrao**: recebe o valor informado na coluna **DataDesconto** da 
**FNTabelaValorVencimento**;
- **DataVencimentoDebito**: por padrão, recebe o mesmo valor da coluna 
**DataVencimentoPadrao**. Mas caso ocorra uma alteração de data via sistema, 
recebe a **nova data**;
- **DataDescontoDebito**: por padrão, recebe o mesmo valor da coluna 
**DataDescontoPadrao**. Mas caso ocorra uma alteração de data via sistema, 
recebe a **nova data**;
- **DataVencimento**: recebe o valor da coluna **DataVencimentoDebito** ou 
**DataDescontoDebito**, de acordo com a **data atual**;
    - **Até a DataDescontoDebito**: DataVencimento recebe o valor da 
    **DataDescontoDebito**.
    - **Após a DataDescontoDebito**: DataVencimento recebe o valor da 
    **DataVencimentoDebito**.


## Valores dos Débitos

As **5 colunas** principais de **valores nos débitos**:

- **ValorCheioNominal**: recebe o valor informado na coluna **ValorCheio** da 
**FNTabelaValorVencimento**;
- **ValorDescontoNominal**: recebe o valor informado na coluna **ValorDesconto**
da **FNTabelaValorVencimento**;
- **ValorCheioDebito**: valor da coluna **ValorCheioNominal** com 
[**Bolsa**](http://conhecimento.fiap.com.br/processos/financeiro/Aplica%C3%A7%C3%A3o%20de%20Bolsas%20em%20D%C3%A9bitos/aplicacao-de-bolsa/), 
[**Dedução** e **Acréscimo**](http://conhecimento.fiap.com.br/processos/financeiro/Altera%C3%A7%C3%A3o%20de%20Valor%20de%20D%C3%A9bito%20%28Dedu%C3%A7%C3%A3o%20e%20Acr%C3%A9scimo%29/alteracao-de-valor-de-debito-deducao-e-acrescimo) aplicados;
- **ValorDescontoDebito**: valor da coluna **ValorDescontoNominal** com 
[**Bolsa**](http://conhecimento.fiap.com.br/processos/financeiro/Aplica%C3%A7%C3%A3o%20de%20Bolsas%20em%20D%C3%A9bitos/aplicacao-de-bolsa/), 
[**Dedução** e **Acréscimo**](http://conhecimento.fiap.com.br/processos/financeiro/Altera%C3%A7%C3%A3o%20de%20Valor%20de%20D%C3%A9bito%20%28Dedu%C3%A7%C3%A3o%20e%20Acr%C3%A9scimo%29/alteracao-de-valor-de-debito-deducao-e-acrescimo) aplicados;
- **ValorDebito**: recebe o valor da coluna **ValorCheioDebito** ou 
**ValorDescontoDebito**, de acordo com a **data atual**;
    - **Até a DataDescontoDebito**: ValorDebito recebe o **ValorDescontoDebito**.
    - **Após a DataDescontoDebito, até a DataVencimentoDebito**: ValorDebito 
    recebe o **ValorCheioDebito**.
    - **Após a DataVencimentoDebito**: ValorDebito recebe o **ValorCheioDebito** 
    acrescido de **Multa** e **Juros**, calculados diariamente.

## Valores sendo atribuídos na prática

```sql
-- Valor de Desconto ou Pontualidade: R$ 800,00
DECLARE @ValorDescontoNominal AS MONEY = 800; 
-- Valor Cheio: R$ 1.000,00
DECLARE @ValorCheioNominal AS MONEY = 1000; 

-- Data de Desconto ou Pontualidade: 05/09/2023
DECLARE @DataDescontoDebito AS DATE = '2023-09-05'; 
-- Data de Vencimento: 15/09/2023
DECLARE @DataVencimentoDebito AS DATE = '2023-09-15'; 

-- Taxa de Juros: 0,033%
DECLARE @TaxaJuros AS FLOAT = 0.00033; 
-- Taxa de Multa: 2%
DECLARE @TaxaMulta AS FLOAT = 0.02; 

/*
Alterar valores abaixo e executar o script para auxiliar no entendimento
Datas de exemplo:
- '2023-09-04': Antes da pontualidade
- '2023-09-11': Entre a pontualidade e o vencimento
- '2023-09-18': Depois do vencimento
*/

DECLARE @DataAtual AS DATE = '2023-09-04'; -- OBS: Originalmente, utiliza o valor de GETDATE()
DECLARE @Bolsa AS MONEY = 10; -- Aceita valores de 0 até 100 (%) e não admite nulos
DECLARE @ValorDeducao AS MONEY = 300; -- Admite nulos
DECLARE @ValorAcrescimo AS MONEY = 100; -- Admite nulos

-- Normalizando datas, para utilizar próximo dia útil caso a data informada não seja um dia útil
SET @DataDescontoDebito = BaseEducacional.dbo.fnRetornaDiaUtilFinanceiro(@DataDescontoDebito);
SET @DataVencimentoDebito = BaseEducacional.dbo.fnRetornaDiaUtilFinanceiro(@DataVencimentoDebito);
SET @DataAtual = BaseEducacional.dbo.fnRetornaDiaUtilFinanceiro(@DataAtual);

-- Valores com Bolsa, Dedução e Acréscimo aplicados
DECLARE @ValorDescontoDebito AS MONEY = ROUND(@ValorDescontoNominal * (1 - @Bolsa/100) - ISNULL(@ValorDeducao, 0) + ISNULL(@ValorAcrescimo, 0), 2);
DECLARE @ValorCheioDebito AS MONEY = ROUND(@ValorCheioNominal * (1 - @Bolsa/100) - ISNULL(@ValorDeducao, 0) + ISNULL(@ValorAcrescimo, 0), 2);

-- Valor final do débito e da data de vencimento, de acordo com a data atual
DECLARE @ValorDebito AS MONEY;
DECLARE @DataVencimento AS DATE;

DECLARE @ValorJuros AS MONEY = NULL;
DECLARE @ValorMulta AS MONEY = NULL;
DECLARE @QtDiasAtrasado AS INT = 0;

-- Até a data de pontualidade
IF @DataAtual <= @DataDescontoDebito
BEGIN
	SET @ValorDebito = @ValorDescontoDebito;
	SET @DataVencimento = @DataDescontoDebito;
END
-- Após a data de pontualidade, até a data de vencimento
ELSE IF @DataAtual > @DataDescontoDebito AND @DataAtual <= @DataVencimentoDebito
BEGIN
	SET @ValorDebito = @ValorCheioDebito;
	SET @DataVencimento = @DataVencimentoDebito;
END
-- Após a data de vencimento
ELSE
BEGIN
	SET @QtDiasAtrasado = DATEDIFF(DAY, @DataVencimentoDebito, @DataAtual);
	SET @ValorJuros = ROUND(@ValorCheioDebito * ISNULL(@TaxaJuros, 0.00033) * @QtDiasAtrasado, 2);
	SET @ValorMulta = ROUND(@ValorCheioDebito * ISNULL(@TaxaMulta, 0.02), 2);
	SET @ValorDebito = @ValorCheioDebito + ISNULL(@ValorJuros, 0) + ISNULL(@ValorMulta, 0);
	SET @DataVencimento = @DataVencimentoDebito;
END


PRINT CONCAT('ValorDescontoNominal = ', FORMAT(@ValorDescontoNominal, 'C2', 'pt-br'));
PRINT CONCAT('ValorCheioNominal = ', FORMAT(@ValorCheioNominal, 'C2', 'pt-br'));
PRINT CONCAT('ValorDescontoDebito = ', FORMAT(@ValorDescontoDebito, 'C2', 'pt-br'));
PRINT CONCAT('ValorCheioDebito = ', FORMAT(@ValorCheioDebito, 'C2', 'pt-br'));
PRINT CONCAT('ValorDebito = ', FORMAT(@ValorDebito, 'C2', 'pt-br'));
PRINT ''
PRINT CONCAT('DataAtual = ', FORMAT(@DataAtual, 'dd/MM/yyyy'));
PRINT CONCAT('DataDescontoDebito = ', FORMAT(@DataDescontoDebito, 'dd/MM/yyyy'));
PRINT CONCAT('DataVencimentoDebito = ', FORMAT(@DataVencimentoDebito, 'dd/MM/yyyy'));
PRINT CONCAT('DataVencimento = ', FORMAT(@DataVencimento, 'dd/MM/yyyy'));
PRINT ''
PRINT CONCAT('Bolsa = ', FORMAT(@Bolsa/100, 'P'));
PRINT CONCAT('ValorDeducao = ', FORMAT(@ValorDeducao, 'C2', 'pt-br'));
PRINT CONCAT('ValorAcrescimo = ', FORMAT(@ValorAcrescimo, 'C2', 'pt-br'));
PRINT ''
PRINT CONCAT('TaxaJuros = ', FORMAT(@TaxaJuros, 'P3'));
PRINT CONCAT('TaxaMulta = ', FORMAT(@TaxaMulta, 'P3'));
PRINT CONCAT('ValorJuros = ', FORMAT(ISNULL(@ValorJuros, 0), 'C2', 'pt-br'));
PRINT CONCAT('ValorMulta = ', FORMAT(ISNULL(@ValorMulta, 0), 'C2', 'pt-br'));
PRINT CONCAT('QtDiasAtrasado = ', @QtDiasAtrasado);
```


