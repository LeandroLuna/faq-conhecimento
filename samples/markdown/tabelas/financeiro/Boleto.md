# Boletos de Carteira 109 e 112

Existem **algumas formas** dos alunos realizarem os **pagamentos** de suas
mensalidades e demais **pendências financeiras** com a FIAP. Uma delas é através
de **Boletos**.

Temos 2 tipos principais de boletos: **Carteira 112** e **Carteira 109**.

## Boletos de Carteira 112

Os boletos de **Carteira 112**, armazenados na tabela **Educacional..BMRemessa**,
são gerados pelo
[Francisco Esteves](https://teams.microsoft.com/l/chat/0/?users=festeves@fiap.com.br)
via remessa, próximo ao **dia 20** de cada mês e são referentes ao
**mês seguinte**.

Este arquivo remessa é __enviado ao Itaú__ e o __processamento__ é realizado
sempre no __dia seguinte__. Por conta disso, no período entre a
__emissão da remessa__ e o __processamento do arquivo retorno__, o registro da
tabela __Educacional..BMRemessa__ existirá, mas o campo __NossoNumero_Detalhe__
estará com o valor zerado (__00000000__).

Após o recebimento do **Arquivo de Retorno** é realizada a inclusão dele no
sistema **Controle de Arquivo de Retorno**, na **IntranetNova** (equipe do
Financeiro).

Após esta adição, o Banco de Dados __SQL Server__ executa o
__Job: Financeiro - Baixa de Pagamento__ (às 9h) que, dentre diversas outras
tarefas, atualiza o campo __NossoNumero_Detalhe__ com o
número __retornado pelo Itaú__. Assim que essa atualização é realizada, a
__Trigger: trBMRemessa__ (da  tabela __Educacional..BMRemessa__) atualiza o
campo __CodigoBMRemessa__ na tabela __Educacional..FNDebitos__.

Porém, é possível que na época de emissão de **boletos 112** o débito
ainda **não existisse**, então este débito **não terá** um boleto 112. Outra
possibilidade é que o débito sofra
**alteração de responsável, valor ou data de vencimento**, e não esteja
mais de acordo com o boleto 112 gerado anteriormente.

O sistema da
[Ficha Financeira do Aluno no Portal](https://gitlab.fiap.com.br/vuejs/Financeiro)
é capaz de exibir apenas **boletos 112**, com excessão de débitos de **Produto**,
que podem ter seus **boletos 109** também acessados.

## Boletos de Carteira 109

Já os boletos de **Carteira 109**, armazenados na tabela
**BaseEducacional..BOControle**, são emitidos pelos colaboradores na
**Ficha Financeira** da Intranet Nova. Porém, estes boletos serão emitidos
**APENAS SE** o boleto de **carteira 112** daquele débito
**não existir ou não estiver mais de acordo** com as informações atuais do
débito. Caso contrário, o **boleto 112** será retornado.

## Service.Boleto e Api.Boleto

Atualmente (em 2023) estamos desenvolvendo uma estrutura com **Api** e
**Service Windows** capaz de **atualizar boletos 112** já emitidos, e evitar a
emissão de novos **boletos 109**. Desta forma, a emissão de **boletos 109** só
se fará necessária caso o débito não possua um **boleto 112** vinculado ou não
seja possível atualizá-lo.

Para mais informações, confira a
[Documentação Completa](http://conhecimento.fiap.com.br/tabelas/financeiro/service-boleto-e-api-boleto/)
.

## Fluxo dos Boletos - Débito > Boleto > Histórico de Ocorrências

Cada um dos **débitos** que o aluno precisa pagar pode ter **um ou mais boletos**
relacionados, tanto de **carteira 109** quanto de **carteira 112**.
Cada um destes **boletos**, independente da carteira, possui uma lista de
**ocorrências** (atualização de status), como emissão, baixa, erros e outros.

## Débitos

Aqui, estamos utilizando um **RM** para buscar débitos relacionados ao
**mês do boleto** que estamos procurando. Anote o **Código do Débito** desejado
para utilizar na **query seguinte**.

```sql
-- Buscando mensalidade de Julho de 2023 do RM 95688
SELECT
	Codigo,
	RM,
	Tipo,
	Ano,
	Mes,
	--CONCAT(Nser, LCur, LSer) AS Turma,
	--Bolsa,
	ValorDebito,
	ValorPago,
	DataVencimento,
	DataPagamento,
	Abonado,
	--CodigoBMRemessa,
	--CodigoArquivoRetornoBancoRegistro,
	--ValidadoBaixa,
	--QtDiasAtrasado,
	--Con, MesAnoEvd, DataOutLan,
	--Visivel, Excluido,
	--DataHoraCadastro,
	*
FROM
	BaseEducacional..FNDebitos WITH (NOLOCK)
WHERE
	RM = 95688
	AND Mes = 7
	AND Ano = 2023
	AND Tipo = 'Mensalidade'
	AND Visivel = 1
	AND Excluido = 0
ORDER BY
	FNDebitos.Ano,
	FNDebitos.Mes

/*
Codigo   RM     Tipo         Ano   Mes  ValorDebito  ValorPago  DataVencimento  DataPagamento  Abonado  
5040195  95688  Mensalidade  2023  7    2750,00      2750,00    2023-07-05      2023-06-26     0        
*/

```

## Boletos da Carteira 112

Na query abaixo, a partir do código do débito, é possível verificar se o boleto
de __carteira 112__ foi gerado normalmente e, caso tenha sido, deve-se utilizar
o valor da coluna __NossoNumero_Detalhe__ para filtrar a query de
__histórico de ocorrências__ (atualização de status).

```sql
-- Buscando Boletos de carteira 112 vinculados ao débito em questão
SELECT
	Codigo,
	CodigoFNDebitos,
	NossoNumero_Detalhe,
	--UsoEmpresa_Detalhe,
	--Sacador_Avalista_Detalhe,
	RM,
	Mes,
	Ano,
	CodigoBMFNDebitos,
	DataEmissao_Detalhe,
	*
FROM
	Educacional..BMRemessa WITH (NOLOCK)
WHERE
	-- Filtrando pelo código do débito
	CodigoFNDebitos IN (5040195)
	-- Campo utilizado caso haja a necessidade de realizar o caminho inverso 
	-- (do histórico de ocorrências até o débito)
	--NossoNumero_Detalhe IN ('XXXXXXXX')
/*
Codigo   CodigoFNDebitos  NossoNumero_Detalhe  RM     Mes  Ano   CodigoBMFNDebitos  DataEmissao_Detalhe  
1244622  5040195          49554703             95688  7    2023  1653122            200623               
*/

```

### Cópia do Débito no Momento da Emissão do Boleto 112

Quando o **boleto 112** é gerado na tabela **Educacional..BMRemessa** é feita
uma **cópia do débito atual** para a tabela **Educacional..BMFNDebitos** para
termos a rastreabilidade de como o débito estava no momento.

```sql
-- Buscando cópia da mensalidade de Julho de 2023 do RM 95688 no momento da
-- emissão do boleto 112
SELECT
	Codigo,
	RM,
	Tipo,
	Ano,
	Mes,
	--CONCAT(Nser, LCur, LSer) AS Turma,
	--Bolsa,
	ValorDebito,
	ValorPago,
	DataVencimento,
	DataPagamento,
	Abonado,
	--CodigoBMRemessa,
	--CodigoArquivoRetornoBancoRegistro,
	--ValidadoBaixa,
	--QtDiasAtrasado,
	--Con, MesAnoEvd, DataOutLan,
	--Visivel, Excluido,
	--DataHoraCadastro,
	*
FROM
	Educacional..BMFNDebitos WITH (NOLOCK)
WHERE
	RM = 95688
	AND Mes = 7
	AND Ano = 2023
	AND Tipo = 'Mensalidade'
	AND Visivel = 1
	AND Excluido = 0
ORDER BY
	BMFNDebitos.Ano,
	BMFNDebitos.Mes

```

## Boletos da Carteira 109

Aqui serão buscados os boletos de **carteira 109**, utilizados caso o boleto 112
não exista ou esteja desatualizado em relação ao valor, data ou responsável do
débito.
Caso o boleto 109 exista, deve-se utilizar o valor da coluna **NossoNumero** para
filtrar a query de **histórico de ocorrências** (atualização de status).

```sql
-- Buscando Boletos de carteira 109 vinculados ao débito em questão
SELECT
	Codigo,
	CodigoIdentificadorSistemaOrigem,
	NossoNumero,
	--UsoEmpresa,
	--Sacado,
	DataEmissao,
	*
FROM
	BaseEducacional..BOControle WITH (NOLOCK)
WHERE
	-- Filtrando pelo código do débito
	CodigoIdentificadorSistemaOrigem IN (5040195)
	-- Campo utilizado caso haja a necessidade de realizar o caminho inverso 
	-- (do histórico de ocorrências até o débito)
	--NossoNumero IN ('XXXXXXXX')
/*
(Nenhum registro retornado)
*/

```

## Histórico de Ocorrências do Boleto (Atualizações de Status)

Na query abaixo, é possível verificar se o boleto foi emitido, pago ou
apresentou algum erro, analisando o dado da coluna **CodigoOcorrencia**.

```sql
-- Histórico de ocorrências dos boletos (tanto 109 quanto 112)
SELECT
	Codigo,
	CodigoOcorrencia,
	DataOcorrencia,
	NossoNumero,
	Erros,
	Vencimentro,
	CASE WHEN 
		CodigoOcorrencia = '06' 
	THEN 
		ValorPrincipal + TarifaCobranca 
	ELSE 
		NULL 
	END AS ValorPago,
	Carteira,
	*
FROM
	Educacional..ArquivoRetornoBancoRegistro WITH (NOLOCK)
WHERE
	NossoNumero IN ('49554703')
	-- Campo utilizado caso haja a necessidade de realizar o caminho inverso 
	-- (do histórico de ocorrências até o débito)
	--Codigo = XXXXXX
	--UsoEmpresa = 'XXXXXXXX'
ORDER BY
	ArquivoRetornoBancoRegistro.NossoNumero,
	ArquivoRetornoBancoRegistro.DataOcorrencia,
	ArquivoRetornoBancoRegistro.Codigo
/*
Codigo   CodigoOcorrencia  DataOcorrencia       NossoNumero  Erros  Vencimentro          ValorPago  Carteira  
3444200  02                2023-06-20 00:00:00  49554703            2023-07-17 00:00:00  NULL       112       
3448987  06                2023-06-26 00:00:00  49554703            2023-07-17 00:00:00  2750,00    112       
*/

```

### Principais Códigos de Ocorrência

```sh
CodigoOcorrencia   Descrição
02                 Boleto emitido
06                 Boleto liquidado (pago)
03, 15, 16, ou 17  Ocorreu um erro (analisar coluna Erros)

```

Para mais informações sobre os __códigos de ocorrência__, consultar a
[Documentação da CNAB 400](https://download.itau.com.br/bankline/layout_cobranca_400bytes_cnab_itau.pdf),
do Itaú na __Nota 17__ (página 23).

## Analisando a Ocorrência de Erros em um Boleto

Caso ocorra algum erro na emissão ou atualização de um boleto, a coluna
**Erros** será preenchida.

A coluna **Erros**, quando preenchida, armazena **1 erro a cada 2 caracteres**.

Exemplos:

- Erros = '05140000' representa a ocorrência dos erros 05 e 14;
- Erros = '11130400' representa a ocorrencia dos erros 11, 13 e 04;

Estes erros podem ser encontrados na
[Documentação da CNAB 400](https://download.itau.com.br/bankline/layout_cobranca_400bytes_cnab_itau.pdf),
do Itaú na __Nota 20__ (a partir da página 26).

## Script completo para análise de Boletos

Script que relaciona o débito desejado com ambos os tipos de boleto e suas
ocorrências, facilitando a análise como um todo.

```sql
SELECT
	'|' AS 'Débito',
	FNDebitos.Codigo,
	FNDebitos.RM,
	FNDebitos.DescricaoDebito,
	FNDebitos.ValorDebito,
	FNDebitos.ValorPago,
	FNDebitos.Abonado,
	FNDebitos.CodigoBMRemessa,
	FNDebitos.CodigoArquivoRetornoBancoRegistro,
	--FNDebitos.QtDiasAtrasado,
	--FNDebitos.Con, FNDebitos.MesAnoEvd, FNDebitos.DataOutLan,
	--FNDebitos.Visivel, FNDebitos.Excluido,
	--FNDebitos.DataHoraCadastro,
	'|' AS 'Boleto',
	Boleto.Carteira,
	Boleto.Codigo,
	Boleto.CodigoFNDebitos,
	Boleto.NossoNumero,
	--Boleto.UsoEmpresa,
	Boleto.CEP,
	Boleto.UF,
	--Boleto.Sacado,
	Boleto.RM,
	Boleto.Mes,
	Boleto.Ano,
	Boleto.DataEmissao,
	'|' AS 'Arquivo',
	Arquivo.Codigo,
	--Arquivo.Carteira,
	Arquivo.CodigoOcorrencia,
	Arquivo.DataOcorrencia,
	Arquivo.NossoNumero,
	Arquivo.Erros,
	Arquivo.Vencimentro,
	Arquivo.ValorPrincipal + Arquivo.TarifaCobranca AS ValorPago
FROM
	BaseEducacional..FNDebitos WITH (NOLOCK)
	LEFT JOIN 
	(
		SELECT
			'109' AS 'Carteira',
			Boleto_109.Codigo,
			Boleto_109.CodigoIdentificadorSistemaOrigem AS 'CodigoFNDebitos',
			Boleto_109.NossoNumero COLLATE SQL_Latin1_General_Pref_CP1_CI_AS AS 'NossoNumero',
			Boleto_109.UsoEmpresa COLLATE SQL_Latin1_General_Pref_CP1_CI_AS AS 'UsoEmpresa',
			Boleto_109.Sacado COLLATE SQL_Latin1_General_Pref_CP1_CI_AS AS 'Sacado',
			Boleto_109.CEPSacado COLLATE SQL_Latin1_General_Pref_CP1_CI_AS AS 'CEP',
			Boleto_109.UFSacado COLLATE SQL_Latin1_General_Pref_CP1_CI_AS AS 'UF',
			NULL AS 'RM',
			NULL AS 'Mes',
			NULL AS 'Ano',
			Boleto_109.DataEmissao
		FROM
			BaseEducacional..BOControle AS Boleto_109 WITH (NOLOCK)
		UNION
		SELECT
			'112' AS 'Carteira',
			Boleto_112.Codigo,
			Boleto_112.CodigoFNDebitos,
			Boleto_112.NossoNumero_Detalhe COLLATE SQL_Latin1_General_Pref_CP1_CI_AS AS 'NossoNumero',
			Boleto_112.UsoEmpresa_Detalhe COLLATE SQL_Latin1_General_Pref_CP1_CI_AS AS 'UsoEmpresa',
			Boleto_112.Sacador_Avalista_Detalhe COLLATE SQL_Latin1_General_Pref_CP1_CI_AS AS 'Sacado',
			Boleto_112.CEP_Detalhe COLLATE SQL_Latin1_General_Pref_CP1_CI_AS AS 'CEP',
			Boleto_112.Estado_Detalhe COLLATE SQL_Latin1_General_Pref_CP1_CI_AS AS 'UF',
			Boleto_112.RM,
			Boleto_112.Mes,
			Boleto_112.Ano,
			Boleto_112.DataEmissao_Detalhe AS 'DataEmissao'
		FROM
			Educacional..BMRemessa AS Boleto_112 WITH (NOLOCK)
	) AS Boleto
		ON FNDebitos.Codigo = Boleto.CodigoFNDebitos
	LEFT JOIN Educacional..ArquivoRetornoBancoRegistro AS Arquivo WITH (NOLOCK)
		ON 
		(
			(Boleto.NossoNumero = '00000000' AND Arquivo.UsoEmpresa = Boleto.UsoEmpresa COLLATE SQL_Latin1_General_Pref_CP1_CI_AS)
			OR
			(Boleto.NossoNumero <> '00000000' AND Arquivo.NossoNumero = Boleto.NossoNumero COLLATE SQL_Latin1_General_Pref_CP1_CI_AS)
		)
WHERE
	FNDebitos.RM = 95688
	AND FNDebitos.Ano * 100 + FNDebitos.Mes = 202307
	--AND FNDebitos.ValorPago IS NULL
	AND FNDebitos.Visivel = 1
	AND FNDebitos.Excluido = 0
ORDER BY
	FNDebitos.Ano,
	FNDebitos.Mes,
	Arquivo.NossoNumero,
	Arquivo.DataOcorrencia,
	Arquivo.Codigo  
/*
Débito  Codigo   RM     DescricaoDebito         ValorDebito  ValorPago  Abonado  Boleto  Carteira  Codigo   CodigoFNDebitos  NossoNumero  Arquivo  Codigo   CodigoOcorrencia  DataOcorrencia       NossoNumero  Erros  ValorPago  
|       5040195  95688  Mens. Mês 07 Ano: 2023  2750,00      2750,00    0        |       112       1244622  5040195          49554703     |        3444200  02                2023-06-20 00:00:00  49554703            NULL       
|       5040195  95688  Mens. Mês 07 Ano: 2023  2750,00      2750,00    0        |       112       1244622  5040195          49554703     |        3448987  06                2023-06-26 00:00:00  49554703            2750,00    
*/

```

## Confirmação Extra do Pagamento do Boleto

Caso, depois da análise, seja concluído que o boleto **foi pago**, é possível
solicitar que o
[Francisco Esteves](https://teams.microsoft.com/l/chat/0/?users=festeves@fiap.com.br)
realize a verificação do pagamento no **site da Braspag**, com o intuído de uma
**maior confirmação** das informações recolhidas nas consultas.

## Documentação Oficial - CNAB 400 Itaú

- [CNAB 400 Itaú](https://download.itau.com.br/bankline/layout_cobranca_400bytes_cnab_itau.pdf)

# Boletos no Portal do Aluno

!!! warning "Atenção"
    Apenas débitos alinhados com **todas estas condições** podem ser pagos:
    
    - **Não** estão no **Jurídico** e são do tipo **Acordo**;
    - Coluna **Externa** nula;
    - Coluna **ValorPago** nula;
    - Coluna **Abonado** com valor 0 (representando que não está abonado);
    - Coluna **ValorDebito** com valor superior a R$ 0,00;
