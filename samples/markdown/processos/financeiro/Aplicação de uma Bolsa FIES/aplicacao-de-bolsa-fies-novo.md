# Aplicação de uma Bolsa FIES (Modelo Novo)

<div style="height: 700px; overflow-x:scroll;">
    <img src="../aplicacao-de-bolsa-fies.svg" style="max-width: initial;">
</div>

## Nota

Esta documentação é um complemento dos procedimentos de 
[**Aplicação de Bolsa**](http://conhecimento.fiap.com.br/processos/financeiro/Aplicação%20de%20Bolsas%20em%20Débitos/aplicacao-de-bolsa/) e 
[**Aplicação de Bolsa FIES**](http://conhecimento.fiap.com.br/processos/financeiro/Aplicação%20de%20uma%20Bolsa%20FIES/aplicacao-de-bolsa-fies/).

---------------------------------------------
## FIES Novo

Para cada uma das mensalidades que recebem a bolsa **FIES** do modelo **novo**, 
as **porcentagens** de todas as bolsas vinculadas são **escalonadas**, de forma 
que, **cada** uma das **bolsa** é aplicada ao débito **separadamente**, uma por 
vez, **independentemente do grupo** que as bolsas pertencem 
(**Bolsas prioritárias** ou **demais bolsas**).

Assim como o **FIES antigo**, são gerados 6 débitos do tipo **Repasse Fies**, 
cada um deles referente a uma **Mensalidade**. Os **valores** destes débitos de 
**Repasse Fies** são equivalentes ao **valor descontado** pela bolsa FIES 
concedido ao débito.

Também são gerados **até 6** débitos de **Agente Financiador**, cada um deles 
referente a uma **Mensalidade**. Estes débitos de **Agente Financiador** 
são gerados a partir do **Mês/Ano** informado no ato do cadastro da bolsa FIES, 
até o final do semestre, e apenas se a emissão for solicitada 
(**Gerar Agente Financiador**). Os **valores** dos débitos de 
**Agente Financiador** são equivalentes ao **valor nominal de pontualidade** do 
débito com a **bolsa escalonada resultante** aplicada.

As **Mensalidades** que possuem um **Agente Financiador** correspondente (de 
mesmo mês e ano) ficam com **100% de bolsa** enquanto que as 
**demais Mensalidades** (anteriores ao "Mês/Ano" informado) recebem a 
**porcentagem escalonada resultante** na coluna **Bolsa**. 

Acompanhe o raciocínio no **Exemplo**.

### Exemplo:
```
Semestre de aplicação do FIES: 2° semestre (do mês 08/2023 ao mês 01/2024);

Bolsas do aluno neste semestre:
- 10% de "Convênio";
- 40% de "Fim Periodo";
- 60% de "FIES" (nova bolsa);

Mês/Ano de início do Agente Financiador: 10/2023;

Gerar Agente Financiador: Sim;

-------------------------------- Mensalidades ---------------------------------
BolsaResultante = 1 - Produto(1-Bolsa/100.0)
BolsaResultante = 1 - ((1-BolsaConvenio/100.0) * (1-BolsaFimPeriodo/100.0) * (1-BolsaFies/100.0))
BolsaResultante = 1 - ((1-10/100.0) * (1-40/100.0) * (1-60/100.0))
BolsaResultante = 0.784
BolsaResultante = 78.4%

--> Mensalidades 08/2023 e 09/2023 receberão 78.4% na coluna "Bolsa";

- ValorCheioNominal = R$ 2.540,00;
- ValorDescontoNominal = R$ 2.005,00;
- Bolsa = 78.4%;
- ValorCheioDebito = 2540 * (1 - 78.4 / 100.0) = R$ 548,64;
- ValorDescontoDebito = 2005 * (1 - 78.4 / 100.0) = R$ 433,08;

--> Mensalidades de 10/2023 até 01/2024 receberão 100% na coluna "Bolsa";

- ValorCheioNominal = R$ 2.540,00;
- ValorDescontoNominal = R$ 2.005,00;
- Bolsa = 100%;
- ValorCheioDebito = 2540 * (1 - 100 / 100.0) = R$ 0,00;
- ValorDescontoDebito = 2005 * (1 - 100 / 100.0) = R$ 0,00;

OBS: Lembrar de considerar os valores de Dedução e Acréscimo, caso existam.

-------------------------------- Repasse Fies ---------------------------------
Os 6 débitos de "Repasse Fies" receberão 60% do valor nominal de pontualidade 
da "Mensalidade" correspondente já com a porcentagem escalonada das outras 
bolsas exceto FIES (Prouni e Demais Bolsas), tanto nos valores-cheios quanto nos 
valores-desconto.

BolsaComDemaisBolsasEProuni = 1 - Produto(1-Bolsa/100.0)
BolsaComDemaisBolsasEProuni = 1 - ((1-BolsaConvenio/100.0) * (1-BolsaFimPeriodo/100.0))
BolsaComDemaisBolsasEProuni = 1 - ((1-10/100.0) * (1-40/100.0))
BolsaComDemaisBolsasEProuni = 0.46
BolsaComDemaisBolsasEProuni = 46%

- ValorDescontoNominal_MensalidadeComDemaisBolsasEProuni = 2005 * (1 - 46 / 100.0) = R$ 1.082,70;

- ValorCheioNominal = 1082.70 * (60 / 100.0) = R$ 649,62;
- ValorDescontoNominal = 1082.70 * (60 / 100.0) = R$ 649,62;
- Bolsa = 0%;
- ValorCheioDebito = 1082.70 * (60 / 100.0) = R$ 649,62;
- ValorDescontoDebito = 1082.70 * (60 / 100.0) = R$ 649,62;

----------------------------- Agente Financiador ------------------------------
Os débitos de "Agente Financiador" (a partir do mês/ano informado) receberão 
21.6% (100% - 78.4%) do valor nominal de pontualidade da "Mensalidade" 
correspondente, tanto nos valores-cheios quanto nos valores-desconto.

- ValorDescontoNominal_Mensalidade = R$ 2.005,00;

- ValorCheioNominal = 2005 * (21.6 / 100.0) = R$ 433,08;
- ValorDescontoNominal = 2005 * (21.6 / 100.0) = R$ 433,08;
- Bolsa = 0%;
- ValorCheioDebito = 2005 * (21.6 / 100.0) = R$ 433,08;
- ValorDescontoDebito = 2005 * (21.6 / 100.0) = R$ 433,08;
-------------------------------------------------------------------------------

Desta forma, ao somar os valores desconto de pontualidade do "Repasse Fies", do 
"Agente Financiador" e da "Mensalidade" de um mesmo mês/ano, o valor obtido é o 
valor nominal de pontualidade da "Mensalidade" com a porcentagem escalonada das 
outras bolsas exceto FIES (Prouni e Demais Bolsas):

--> 08/2023 e 09/2023
- ValorDescontoDebito_Mensalidade = R$ 433,08;
- ValorDescontoDebito_RepasseFies = R$ 649,62;
- ValorDescontoDebito_AgenteFinanciador = (NÃO EXISTE)

--> de 10/2023 até 01/2024
- ValorDescontoDebito_Mensalidade = R$ 0,00;
- ValorDescontoDebito_RepasseFies = R$ 649,62;
- ValorDescontoDebito_AgenteFinanciador = R$ 433,08;

- ValorDescontoNominal_MensalidadeComDemaisBolsasEProuni = R$ 1.082,70; // R$ 433,08 + R$ 649,62
```

Ao aplicar uma bolsa **FIES** no modelo **novo** é inserido um registro na 
**FNBolsa**, informando a **porcentagem** de bolsa e o **período** no qual a 
bolsa se aplica, dentre outros campos.

O sistema também insere **6 registros** na **FNBolsaDebitos**, uma para cada 
vínculo entre a **nova bolsa** e um débito de **Mensalidade**.

Na **FNBolsaAplicada** são inseridos **até 18 registros**:

- 6 registros vinculando cada **Mensalidade** ao tipo de bolsa **FIES**, 
informando a **porcentagem de bolsa concedida**;
- 6 registros vinculando cada **Mensalidade** ao tipo de bolsa **Repasse Fies**,
informando a **porcentagem de bolsa complementar**;
- Até 6 registros vinculando cada **Mensalidade** ao tipo de bolsa 
**Agente Financiador** (a partir do mês/ano de início do agente financiador), 
informando também a **porcentagem de bolsa concedida**;

São inseridos **6 registros** na **FNControleRepasseFies**, relacionando o débito 
de **Repasse Fies** e sua **Mensalidade** correspondente (de mesmo mês e ano).

E na **FNControleAgenteFinanciador** são inseridos **até 6 registros**, 
relacionando o débito de **Agente Financiador** e sua **Mensalidade** 
correspondente (de mesmo mês e ano).

## Entendendo a Aplicação da Bolsa FIES

Para **facilitar o entendimento** da aplicação de uma **Bolsa FIES**, é possível 
utilizar o próprio sistema 
[**Manutenção de Bolsa**](https://gitlab.fiap.com.br/dotnet/Intranet.Bolsa)
com os RMs retornados na query abaixo.

??? example "RMs para testar Bolsa FIES via Intranet.Bolsa"
	```sql
	DECLARE @DataAtual AS DATE = GETDATE();
	DECLARE @AnoConsiderar AS INT;
	DECLARE @SemestreConsiderar AS INT;

	DECLARE @TabAlunosSemFies AS TABLE
	(
		RM INT
	);

	DECLARE @TabAlunosBolsas AS TABLE
	(
		RM INT,
		CodigoDemaisBolsas INT,
		CodigoProuni INT
	);

	SET @AnoConsiderar = LEFT(FORMAT(DATEADD(MONTH, -1, @DataAtual), 'yyyyMM'), 4);
	SET @SemestreConsiderar = 1 + (FLOOR(RIGHT(FORMAT(DATEADD(MONTH, -1, @DataAtual), 'yyyyMM'), 2) - 1) / 6);

	-- Busca todos os alunos que não possuem FIES no Semestre/Ano que está sendo considerado
	INSERT INTO @TabAlunosSemFies
		(RM)
	SELECT
		FNDebitos.RM
	FROM
		BaseEducacional..FNDebitos WITH (NOLOCK)
		LEFT JOIN BaseEducacional..FNBolsa AS FNBolsaFies WITH (NOLOCK)
			ON FNBolsaFies.RM = FNDebitos.RM
			AND FNBolsaFies.Ano = @AnoConsiderar
			AND FNBolsaFies.Semestre = @SemestreConsiderar
			AND FNBolsaFies.CodigoTipoBolsa = 9 /* FIES */
			AND FNBolsaFies.Ativo = 1
	WHERE
		(FNDebitos.RM BETWEEN 50000 AND 89999 
			OR FNDebitos.RM BETWEEN 92000 AND 99998
			OR FNDebitos.RM BETWEEN 550000 AND 599999)
		AND FNDebitos.Tipo = 'Mensalidade'
		AND FNDebitos.Ano = @AnoConsiderar
		AND 
		(
			(@SemestreConsiderar = 1
			AND FNDebitos.Mes IN (2, 3, 4, 5, 6, 7))
			OR
			(@SemestreConsiderar = 2
			AND FNDebitos.Mes IN (8, 9, 10, 11, 12, 13))
		)
		AND FNDebitos.Con = 'A'
		AND FNDebitos.MesAnoEvd IS NULL
		AND FNDebitos.DataOutLan IS NULL
		AND FNDebitos.Visivel = 1
		AND FNDebitos.Excluido = 0
		AND FNDebitos.ValorPago IS NULL
		AND FNDebitos.Abonado = 0
		AND FNDebitos.ValorDebito > 0
		AND FNDebitos.Bolsa < 100
		AND FNDebitos.DebitoEmAcordo = 0
		AND FNDebitos.Plano = 1
		AND FNBolsaFies.Codigo IS NULL
	GROUP BY
		FNDebitos.RM
	HAVING
		COUNT(*) = 6
	ORDER BY
		FNDebitos.RM;

	SELECT 
		DISTINCT 
			TabAlunosSemFies.RM,
			CASE WHEN FNBolsa_DemaisBolsas.Codigo IS NULL THEN 0 ELSE 1 END AS 'TemDemaisBolsas',
			FNBolsa_DemaisBolsas.Codigo AS 'CodigoDemaisBolsas',
			CASE WHEN FNBolsa_Prouni.Codigo IS NULL THEN 0 ELSE 1 END AS 'TemProuni',
			FNBolsa_Prouni.Codigo AS 'CodigoProuni'
	FROM 
		@TabAlunosSemFies AS TabAlunosSemFies
		LEFT JOIN BaseEducacional..FNBolsa AS FNBolsa_DemaisBolsas WITH (NOLOCK)
			ON TabAlunosSemFies.RM = FNBolsa_DemaisBolsas.RM
			AND FNBolsa_DemaisBolsas.Ano = @AnoConsiderar
			AND 
			(
				(
					@SemestreConsiderar = 1
					AND 
					(
						@AnoConsiderar * 100 + 02 BETWEEN FNBolsa_DemaisBolsas.AnoInicio * 100 + FNBolsa_DemaisBolsas.MesInicio AND FNBolsa_DemaisBolsas.AnoTermino * 100 + FNBolsa_DemaisBolsas.MesTermino
						OR @AnoConsiderar * 100 + 03 BETWEEN FNBolsa_DemaisBolsas.AnoInicio * 100 + FNBolsa_DemaisBolsas.MesInicio AND FNBolsa_DemaisBolsas.AnoTermino * 100 + FNBolsa_DemaisBolsas.MesTermino
						OR @AnoConsiderar * 100 + 04 BETWEEN FNBolsa_DemaisBolsas.AnoInicio * 100 + FNBolsa_DemaisBolsas.MesInicio AND FNBolsa_DemaisBolsas.AnoTermino * 100 + FNBolsa_DemaisBolsas.MesTermino
						OR @AnoConsiderar * 100 + 05 BETWEEN FNBolsa_DemaisBolsas.AnoInicio * 100 + FNBolsa_DemaisBolsas.MesInicio AND FNBolsa_DemaisBolsas.AnoTermino * 100 + FNBolsa_DemaisBolsas.MesTermino
						OR @AnoConsiderar * 100 + 06 BETWEEN FNBolsa_DemaisBolsas.AnoInicio * 100 + FNBolsa_DemaisBolsas.MesInicio AND FNBolsa_DemaisBolsas.AnoTermino * 100 + FNBolsa_DemaisBolsas.MesTermino
						OR @AnoConsiderar * 100 + 07 BETWEEN FNBolsa_DemaisBolsas.AnoInicio * 100 + FNBolsa_DemaisBolsas.MesInicio AND FNBolsa_DemaisBolsas.AnoTermino * 100 + FNBolsa_DemaisBolsas.MesTermino
					)
				)
				OR
				(
					@SemestreConsiderar = 2
					AND 
					(
						@AnoConsiderar * 100 + 08 BETWEEN FNBolsa_DemaisBolsas.AnoInicio * 100 + FNBolsa_DemaisBolsas.MesInicio AND FNBolsa_DemaisBolsas.AnoTermino * 100 + FNBolsa_DemaisBolsas.MesTermino
						OR @AnoConsiderar * 100 + 09 BETWEEN FNBolsa_DemaisBolsas.AnoInicio * 100 + FNBolsa_DemaisBolsas.MesInicio AND FNBolsa_DemaisBolsas.AnoTermino * 100 + FNBolsa_DemaisBolsas.MesTermino
						OR @AnoConsiderar * 100 + 10 BETWEEN FNBolsa_DemaisBolsas.AnoInicio * 100 + FNBolsa_DemaisBolsas.MesInicio AND FNBolsa_DemaisBolsas.AnoTermino * 100 + FNBolsa_DemaisBolsas.MesTermino
						OR @AnoConsiderar * 100 + 11 BETWEEN FNBolsa_DemaisBolsas.AnoInicio * 100 + FNBolsa_DemaisBolsas.MesInicio AND FNBolsa_DemaisBolsas.AnoTermino * 100 + FNBolsa_DemaisBolsas.MesTermino
						OR @AnoConsiderar * 100 + 12 BETWEEN FNBolsa_DemaisBolsas.AnoInicio * 100 + FNBolsa_DemaisBolsas.MesInicio AND FNBolsa_DemaisBolsas.AnoTermino * 100 + FNBolsa_DemaisBolsas.MesTermino
						OR @AnoConsiderar * 100 + 13 BETWEEN FNBolsa_DemaisBolsas.AnoInicio * 100 + FNBolsa_DemaisBolsas.MesInicio AND FNBolsa_DemaisBolsas.AnoTermino * 100 + FNBolsa_DemaisBolsas.MesTermino
					)
				)
			)
			AND FNBolsa_DemaisBolsas.Ativo = 1
			AND FNBolsa_DemaisBolsas.CodigoTipoBolsa NOT IN 
			(
				9,  /* FIES */
				10, /* Prouni */
				62, /* Agente Financiador */
				84  /* Repasse Fies */
			)
		LEFT JOIN BaseEducacional..FNBolsa AS FNBolsa_Prouni WITH (NOLOCK)
			ON TabAlunosSemFies.RM = FNBolsa_Prouni.RM
			AND FNBolsa_Prouni.Ano = @AnoConsiderar
			AND 
			(
				(
					@SemestreConsiderar = 1
					AND 
					(
						@AnoConsiderar * 100 + 02 BETWEEN FNBolsa_Prouni.AnoInicio * 100 + FNBolsa_Prouni.MesInicio AND FNBolsa_Prouni.AnoTermino * 100 + FNBolsa_Prouni.MesTermino
						OR @AnoConsiderar * 100 + 03 BETWEEN FNBolsa_Prouni.AnoInicio * 100 + FNBolsa_Prouni.MesInicio AND FNBolsa_Prouni.AnoTermino * 100 + FNBolsa_Prouni.MesTermino
						OR @AnoConsiderar * 100 + 04 BETWEEN FNBolsa_Prouni.AnoInicio * 100 + FNBolsa_Prouni.MesInicio AND FNBolsa_Prouni.AnoTermino * 100 + FNBolsa_Prouni.MesTermino
						OR @AnoConsiderar * 100 + 05 BETWEEN FNBolsa_Prouni.AnoInicio * 100 + FNBolsa_Prouni.MesInicio AND FNBolsa_Prouni.AnoTermino * 100 + FNBolsa_Prouni.MesTermino
						OR @AnoConsiderar * 100 + 06 BETWEEN FNBolsa_Prouni.AnoInicio * 100 + FNBolsa_Prouni.MesInicio AND FNBolsa_Prouni.AnoTermino * 100 + FNBolsa_Prouni.MesTermino
						OR @AnoConsiderar * 100 + 07 BETWEEN FNBolsa_Prouni.AnoInicio * 100 + FNBolsa_Prouni.MesInicio AND FNBolsa_Prouni.AnoTermino * 100 + FNBolsa_Prouni.MesTermino
					)
				)
				OR
				(
					@SemestreConsiderar = 2
					AND 
					(
						@AnoConsiderar * 100 + 08 BETWEEN FNBolsa_Prouni.AnoInicio * 100 + FNBolsa_Prouni.MesInicio AND FNBolsa_Prouni.AnoTermino * 100 + FNBolsa_Prouni.MesTermino
						OR @AnoConsiderar * 100 + 09 BETWEEN FNBolsa_Prouni.AnoInicio * 100 + FNBolsa_Prouni.MesInicio AND FNBolsa_Prouni.AnoTermino * 100 + FNBolsa_Prouni.MesTermino
						OR @AnoConsiderar * 100 + 10 BETWEEN FNBolsa_Prouni.AnoInicio * 100 + FNBolsa_Prouni.MesInicio AND FNBolsa_Prouni.AnoTermino * 100 + FNBolsa_Prouni.MesTermino
						OR @AnoConsiderar * 100 + 11 BETWEEN FNBolsa_Prouni.AnoInicio * 100 + FNBolsa_Prouni.MesInicio AND FNBolsa_Prouni.AnoTermino * 100 + FNBolsa_Prouni.MesTermino
						OR @AnoConsiderar * 100 + 12 BETWEEN FNBolsa_Prouni.AnoInicio * 100 + FNBolsa_Prouni.MesInicio AND FNBolsa_Prouni.AnoTermino * 100 + FNBolsa_Prouni.MesTermino
						OR @AnoConsiderar * 100 + 13 BETWEEN FNBolsa_Prouni.AnoInicio * 100 + FNBolsa_Prouni.MesInicio AND FNBolsa_Prouni.AnoTermino * 100 + FNBolsa_Prouni.MesTermino
					)
				)
			)
			AND FNBolsa_Prouni.Ativo = 1
			AND FNBolsa_Prouni.CodigoTipoBolsa = 10 /* Prouni */
	ORDER BY
		CASE WHEN FNBolsa_DemaisBolsas.Codigo IS NULL THEN 0 ELSE 1 END,
		CASE WHEN FNBolsa_Prouni.Codigo IS NULL THEN 0 ELSE 1 END,
		TabAlunosSemFies.RM
	```

## Aplicando uma bolsa FIES de Modelo Novo via script

Para aplicar uma bolsa FIES de modelo novo sem utilizar o sistema 
[**Manutenção de Bolsa**](https://gitlab.fiap.com.br/dotnet/Intranet.Bolsa), 
utilize o script abaixo:

??? example "Aplicando Bolsa FIES de Modelo Novo via Script"
	```sql

	------------------------------------------------------------------------------------------------------------------------
	----- Preencha as variáveis abaixo conforme os dados da bolsa FIES -----------------------------------------------------
	------------------------------------------------------------------------------------------------------------------------
	DECLARE @NumeroTicket AS INT = 00000;
	DECLARE @RM AS INT = 84486;
	DECLARE @Ano AS INT = 2023;
	DECLARE @Semestre AS INT = 2;
	DECLARE @PorcentagemFies AS FLOAT = 73.25; 
	DECLARE @DataProcessamento AS DATE = GETDATE(); -- '2023-08-01'

	DECLARE @GerarAgenteFinanciador AS BIT = 1;
	-- Variáveis abaixo serão utilizadas apenas se @GerarAgenteFinanciador = 1
	DECLARE @MesInicioAgenteFinanciador AS INT = 10; /* de 2 até 13 */
	DECLARE @AnoInicioAgenteFinanciador AS INT = @Ano;

	------------------------------------------------------------------------------------------------------------------------
	----- Validando parâmetros de entrada ----------------------------------------------------------------------------------
	------------------------------------------------------------------------------------------------------------------------

	DECLARE @DataMinima AS DATE = '2015-01-01';
	DECLARE @DataMaxima AS DATE = CONCAT(YEAR(GETDATE())+1, '-12-31');

	IF (@RM NOT BETWEEN 50000 AND 89999 
		AND @RM NOT BETWEEN 92000 AND 99998
		AND @RM NOT BETWEEN 550000 AND 599999)
	BEGIN
		PRINT CONCAT('Erro: O RM ', @RM, ' não é de Graduação, e não pode receber uma bolsa FIES!');
	END
	ELSE IF @Ano NOT BETWEEN YEAR(@DataMinima) AND YEAR(@DataMaxima)
	BEGIN
		PRINT CONCAT('Erro: O ano deve estar entre ', YEAR(@DataMinima), ' e ', YEAR(@DataMaxima), '! (Recebido: ', @Ano, ')');
	END
	ELSE IF @Semestre NOT IN (1, 2)
	BEGIN
		PRINT CONCAT('Erro: O semestre deve receber o valor 1 ou 2! (Recebido: ', @Semestre, ')');
	END
	ELSE IF @PorcentagemFies NOT BETWEEN 0.01 AND 100
	BEGIN
		PRINT CONCAT('Erro: A porcentagem da bolsa deve estar entre 0.01% e 100%! (Recebido: ', @PorcentagemFies, ')');
	END
	ELSE IF @DataProcessamento NOT BETWEEN @DataMinima AND @DataMaxima
	BEGIN
		PRINT CONCAT('Erro: A data de processamento deve estar entre ', @DataMinima, ' e ', @DataMaxima, '! (Recebido: ', @DataProcessamento, ')');
	END
	ELSE IF EXISTS
		(
			SELECT 
				1 
			FROM 
				BaseEducacional..FNBolsa WITH (NOLOCK) 
			WHERE 
				RM = @RM 
				AND Ano = @Ano 
				AND Semestre = @Semestre 
				AND Ativo = 1 
				AND CodigoTipoBolsa = 9
		)
	BEGIN
		PRINT CONCAT('Erro: O RM ', @RM, ' já possui uma bolsa FIES no ', @Semestre, '° semestre de ', @Ano);
	END
	ELSE IF EXISTS
		(
			SELECT 
				1 
			FROM 
				BaseEducacional..FNDebitos WITH (NOLOCK) 
			WHERE 
				RM = @RM 
				AND Ano = @Ano 
				AND 
				(
					(@Semestre = 1
					AND FNDebitos.Mes IN (2, 3, 4, 5, 6, 7))
					OR
					(@Semestre = 2
					AND FNDebitos.Mes IN (8, 9, 10, 11, 12, 13))
				)
				AND Tipo = 'Mensalidade'
				AND Plano <> '1'
				AND Visivel = 1
				AND Excluido = 0
				AND Con = 'A'
				AND MesAnoEvd IS NULL
				AND DataOutLan IS NULL
		)
	BEGIN
		PRINT CONCAT('Erro: O RM ', @RM, ' não está no plano anual, portanto não pode receber uma bolsa FIES!');
	END
	ELSE IF NOT EXISTS
		(
			SELECT 
				1 
			FROM 
				BaseEducacional..FNDebitos WITH (NOLOCK) 
			WHERE 
				RM = @RM 
				AND Ano = @Ano 
				AND 
				(
					(@Semestre = 1
					AND FNDebitos.Mes IN (2, 3, 4, 5, 6, 7))
					OR
					(@Semestre = 2
					AND FNDebitos.Mes IN (8, 9, 10, 11, 12, 13))
				)
				AND Tipo = 'Mensalidade'
				AND ValorPago IS NULL
				AND Abonado = 0
				AND DebitoEmAcordo = 0
				AND ISNULL(LSer, '') <> 'P'
				AND Visivel = 1
				AND Excluido = 0
				AND Con = 'A'
				AND MesAnoEvd IS NULL
				AND DataOutLan IS NULL
		)
	BEGIN
		PRINT CONCAT('Erro: O RM ', @RM, ' não possui débitos pendentes no ', @Semestre, '° semestre de ', @Ano);
	END
	ELSE IF @GerarAgenteFinanciador = 1 
		AND 
		(
			(@Semestre = 1 AND @MesInicioAgenteFinanciador NOT BETWEEN 2 AND 7)
			OR
			(@Semestre = 2 AND @MesInicioAgenteFinanciador NOT BETWEEN 8 AND 13)
		)
	BEGIN
		PRINT CONCAT('Erro: O mês de início de Agente Financiador ', @MesInicioAgenteFinanciador, ' não está contido no ', @Semestre, '° semestre!');
	END
	ELSE IF @GerarAgenteFinanciador = 1 AND @AnoInicioAgenteFinanciador <> @Ano
	BEGIN
		PRINT CONCAT('Erro: O ano de início de Agente Financiador ', @AnoInicioAgenteFinanciador, ' deve ser o mesmo que o ano ', @Ano, '!');
	END
	ELSE
	BEGIN

		BEGIN TRY

			BEGIN TRANSACTION

			----------------------------------------------------------------------------------------------------------------
			----- Recuperando Mensalidades que receberão a bolsa FIES ------------------------------------------------------
			----------------------------------------------------------------------------------------------------------------

			DECLARE @TabDebitos AS TABLE
			(
				Codigo INT,
				Ano INT,
				Mes INT
			);

			INSERT INTO @TabDebitos
				(Codigo, 
				Ano, 
				Mes)
			SELECT
				FNDebitos.Codigo,
				FNDebitos.Ano,
				FNDebitos.Mes
			FROM
				BaseEducacional..FNDebitos WITH (NOLOCK)
				LEFT JOIN BaseEducacional..FNBolsa AS FNBolsaFies WITH (NOLOCK)
					ON FNBolsaFies.RM = FNDebitos.RM
					AND FNBolsaFies.Ano = @Ano
					AND FNBolsaFies.Semestre = @Semestre
					AND FNBolsaFies.CodigoTipoBolsa = 9 /* FIES */
					AND FNBolsaFies.Ativo = 1
			WHERE
				FNDebitos.RM = @RM
				AND FNDebitos.Tipo = 'Mensalidade'
				AND FNDebitos.Ano = @Ano
				AND 
				(
					(@Semestre = 1
					AND FNDebitos.Mes IN (2, 3, 4, 5, 6, 7))
					OR
					(@Semestre = 2
					AND FNDebitos.Mes IN (8, 9, 10, 11, 12, 13))
				)
				AND FNDebitos.Con = 'A'
				AND FNDebitos.MesAnoEvd IS NULL
				AND FNDebitos.DataOutLan IS NULL
				AND FNDebitos.Visivel = 1
				AND FNDebitos.Excluido = 0
				AND FNDebitos.ValorDebito > 0
				AND FNDebitos.Bolsa < 100
				AND FNDebitos.DebitoEmAcordo = 0
				AND FNDebitos.Plano = 1
				AND FNBolsaFies.Codigo IS NULL;

			----- Validando se existem exatamente 6 mensalidades no semestre e ano indicados
			DECLARE @QtdeMensalidadesDeUmSemestre AS INT = 6;

			IF (SELECT COUNT(*) FROM @TabDebitos) <> @QtdeMensalidadesDeUmSemestre
			BEGIN
				PRINT CONCAT('O RM ', @RM, ' não possui exatamente 6 mensalidades no ', @Semestre, '° semestre de ', @Ano);
			END
			ELSE
			BEGIN
		
				------------------------------------------------------------------------------------------------------------
				----- Preparando variáveis que serão utilizadas posteriormente ---------------------------------------------
				------------------------------------------------------------------------------------------------------------

				DECLARE @CodigoTipoBolsaFies AS INT = 9; 
				DECLARE @CodigoTipoBolsaAgenteFinanciador AS INT = 62; 
				DECLARE @CodigoTipoBolsaRepasseFies AS INT = 84; 

				-- Gerando um mesmo GUID para todos os Agente Financiador e outro para todos os Repasse Fies
				DECLARE @AgrupadorAgenteFinanciador AS VARCHAR(32) = REPLACE(NEWID(), '-', '');
				DECLARE @AgrupadorRepasseFies AS VARCHAR(32) = REPLACE(NEWID(), '-', '');

				DECLARE @Justificativa AS VARCHAR(MAX) = 
					CONCAT(
						'Aplicação via Script (Ticket ', 
						@NumeroTicket, 
						') - Cadastrado ',
						REPLACE(FORMAT(@PorcentagemFies, '00.00'), '.', ','),
						'% de bolsa ''FIES'' (Modelo novo) para o RM ', 
						@RM, 
						' no ',
						@Semestre,
						'° semestre de ',
						@Ano,
						' (Data de Processamento: ',
						FORMAT(@DataProcessamento, 'dd/MM/yyyy'),
						', ',
						CASE WHEN @GerarAgenteFinanciador = 1 THEN 
							CASE WHEN @MesInicioAgenteFinanciador = 13 THEN
								CONCAT('Mês/Ano de Início do Agente Financiador: 01/', @AnoInicioAgenteFinanciador + 1)
							ELSE
								CONCAT('Mês/Ano de Início do Agente Financiador: ', RIGHT(CONCAT('00', @MesInicioAgenteFinanciador), 2), '/', @AnoInicioAgenteFinanciador)
							END
						ELSE 
							'SEM EMISSÃO DE AGENTE FINANCIADOR'
						END,
						', gerado via Script SQL.'
					);
		
				------------------------------------------------------------------------------------------------------------
				----- Inserindo FNBolsa para o FIES ------------------------------------------------------------------------
				------------------------------------------------------------------------------------------------------------

				DECLARE @CodigoFNBolsa AS INT;

				INSERT INTO BaseEducacional..FNBolsa
					(RM,
					Porcentagem,
					Justificativa,
					CodigoTipoBolsa,
					Semestre,
					Ano,
					MesInicio,
					AnoInicio,
					MesTermino,
					AnoTermino,
					CodigoUsuarioCadastro,
					DataHoraCadastro,
					Ativo,
					CodigoPessoaAutorizou,
					NomeEmpresaParceira,
					Arquivo)
				VALUES
					(@RM,
					@PorcentagemFies,
					@Justificativa,
					@CodigoTipoBolsaFies,
					@Semestre,
					@Ano,
					CASE WHEN @Semestre = 1 THEN 2 ELSE 8 END,
					@Ano,
					CASE WHEN @Semestre = 1 THEN 7 ELSE 13 END,
					@Ano,
					1, -- Administrador
					GETDATE(),
					1,
					1, -- Administrador
					NULL,
					NULL);

				SELECT @CodigoFNBolsa = @@IDENTITY;
		
				------------------------------------------------------------------------------------------------------------
				----- Iterando cada uma das 6 Mensalidades -----------------------------------------------------------------
				------------------------------------------------------------------------------------------------------------

				DECLARE @CodigoMensalidade AS INT;
				DECLARE @AnoMensalidade AS INT;
				DECLARE @MesMensalidade AS INT;

				DECLARE 
					Ponteiro 
				CURSOR 
					READ_ONLY 
					FORWARD_ONLY 
					FAST_FORWARD 
				FOR 
				SELECT
					TabDebitos.Codigo,
					TabDebitos.Ano,
					TabDebitos.Mes
				FROM
					@TabDebitos AS TabDebitos

				OPEN Ponteiro

				FETCH NEXT FROM 
					Ponteiro 
				INTO 
					@CodigoMensalidade,
					@AnoMensalidade,
					@MesMensalidade

				WHILE @@FETCH_STATUS = 0
				BEGIN

					-- Identificando se o Mês/Ano terá Agente Financiador ou não
					DECLARE @AnoMesMensalidade AS INT = @AnoMensalidade * 100 + @MesMensalidade;
					DECLARE @AnoMesInicioAgenteFinanciador AS INT = @AnoInicioAgenteFinanciador * 100 + @MesInicioAgenteFinanciador;
				
					DECLARE @MensalidadeTeraAgenteFinanciador AS BIT =
						CASE WHEN @GerarAgenteFinanciador = 1 AND @AnoMesMensalidade >= @AnoMesInicioAgenteFinanciador THEN
							1
						ELSE
							0
						END

					-- Escalonando porcentagens de todas as bolsas da mensalidade, exceto FIES
					DECLARE @PorcentagemEscalonadaSemFies AS FLOAT = 0;

					SELECT
						@PorcentagemEscalonadaSemFies = (1 - (1 - @PorcentagemEscalonadaSemFies/100.0) * (1 - FNBolsa.Porcentagem/100.0)) * 100
					FROM
						BaseEducacional..FNBolsaDebitos WITH (NOLOCK)
						INNER JOIN BaseEducacional..FNBolsa WITH (NOLOCK)
							ON FNBolsaDebitos.CodigoBolsa = FNBolsa.Codigo
							AND FNBolsa.Ativo = 1
					WHERE
						FNBolsaDebitos.CodigoDebito = @CodigoMensalidade;
		
					--------------------------------------------------------------------------------------------------------
					----- Atualizando Porcentagem de Bolsa da Mensalidade --------------------------------------------------
					--------------------------------------------------------------------------------------------------------
					
					IF @MensalidadeTeraAgenteFinanciador = 1
					BEGIN
						-- Aplicando 100% de bolsa à Mensalidade, pois parte do valor será movido 
						-- para o débito de Agente Financiador e parte para o Repasse Fies
						UPDATE
							BaseEducacional..FNDebitos WITH (ROWLOCK)
						SET
							Bolsa = 100
						WHERE
							Codigo = @CodigoMensalidade;
					END
					ELSE
					BEGIN
						PRINT CONCAT('@PorcentagemEscalonadaSemFies ', @PorcentagemEscalonadaSemFies)
						-- Aplicando porcentagem escalonada de todas as bolsas, inclusive FIES, à Mensalidade
						UPDATE
							BaseEducacional..FNDebitos WITH (ROWLOCK)
						SET
							Bolsa = (1 - (1 - @PorcentagemEscalonadaSemFies/100.0) * (1 - @PorcentagemFies/100.0)) * 100
						WHERE
							Codigo = @CodigoMensalidade;
					END
		
					-- Atualizando a Mensalidade
					EXEC BaseEducacional..spAtualizaDebito @Codigo = @CodigoMensalidade;
		
					--------------------------------------------------------------------------------------------------------
					----- Inserir FNBolsaDebitos (Mensalidades terão vínculo com a Bolsa 'FIES') ---------------------------
					--------------------------------------------------------------------------------------------------------
			
					INSERT INTO BaseEducacional..FNBolsaDebitos
						(CodigoBolsa, CodigoDebito)
					VALUES
						(@CodigoFNBolsa, @CodigoMensalidade);
		
					--------------------------------------------------------------------------------------------------------
					----- Inserir FNBolsaAplicada (Mensalidades terão vínculo com as bolsas 'Agente Financiador', ----------
					-----'FIES' e 'Repasse Fies'). Porém, o vínculo com a bolsa 'Agente Financiador' só existirá se a ------
					----- mensalidade possuir um Agente Financiador no mesmo mês/ano. --------------------------------------
					--------------------------------------------------------------------------------------------------------

					IF @MensalidadeTeraAgenteFinanciador = 1
					BEGIN
						INSERT INTO	BaseEducacional..FNBolsaAplicada
							(CodigoTipoBolsa, CodigoDebito, Porcentagem)
						VALUES
							(@CodigoTipoBolsaFies, @CodigoMensalidade, @PorcentagemFies),
							(@CodigoTipoBolsaRepasseFies, @CodigoMensalidade, @PorcentagemFies),
							(@CodigoTipoBolsaAgenteFinanciador, @CodigoMensalidade, 100 - @PorcentagemFies);
					END
					ELSE 
					BEGIN
						INSERT INTO	BaseEducacional..FNBolsaAplicada
							(CodigoTipoBolsa, CodigoDebito, Porcentagem)
						VALUES
							(@CodigoTipoBolsaFies, @CodigoMensalidade, @PorcentagemFies),
							(@CodigoTipoBolsaRepasseFies, @CodigoMensalidade, @PorcentagemFies);
					END
		
					--------------------------------------------------------------------------------------------------------
					----- Calculando valores de Agente Financiador e Repasse Fies ------------------------------------------
					--------------------------------------------------------------------------------------------------------

					DECLARE @ValorDescontoComProuni AS MONEY;

					SELECT
						@ValorDescontoComProuni = ValorDescontoNominal * (1 - @PorcentagemEscalonadaSemFies/100.0)
					FROM
						BaseEducacional..FNDebitos
					WHERE
						Codigo = @CodigoMensalidade;

					DECLARE @ValorAgenteFinanciador AS MONEY = @ValorDescontoComProuni * (1 - @PorcentagemFies/100.0);
					DECLARE @ValorRepasseFies AS MONEY = @ValorDescontoComProuni * (@PorcentagemFies/100.0);
				
					--------------------------------------------------------------------------------------------------------
					----- Realiza procedimentos de Agente Financiador caso o mês/ano possua --------------------------------
					--------------------------------------------------------------------------------------------------------

					IF @MensalidadeTeraAgenteFinanciador = 1
					BEGIN

						-- Gera débito de Agente Financiador
						DECLARE @CodigoAgenteFinanciador AS INT;
				
						INSERT INTO BaseEducacional..FNDebitos
							(Tipo, 
							AgrupadorDebito, 
							ValorCheioNominal, 
							ValorDescontoNominal, 
							ValorCheioDebito, 
							ValorDescontoDebito, 
							ValorDebito, 
							DescricaoDebito, 
							RM, 
							Nser, 
							LSer, 
							LCur, 
							Con, 
							SPC, 
							DP, 
							Adap, 
							Bolsa, 
							Mes, 
							Ano, 
							DataVencimentoPadrao, 
							DataVencimentoDebito, 
							DataVencimento, 
							DataAtualizado, 
							QtDiasAtrasado, 
							DataHoraCadastro, 
							CodigoUsuarioCadastro, 
							Excluido, 
							Abonado, 
							DebitoEmAcordo, 
							CPFResponsavel, 
							Visivel, 
							ValidadoBaixa, 
							RecalculouMultaJuros, 
							Controle,
							AnoInicioAula)
						SELECT
							'Agente Financiador' AS 'Tipo',
							@AgrupadorAgenteFinanciador AS 'AgrupadorDebito',
							@ValorAgenteFinanciador AS 'ValorCheioNominal',
							@ValorAgenteFinanciador AS 'ValorDescontoNominal',
							@ValorAgenteFinanciador AS 'ValorCheioDebito',
							@ValorAgenteFinanciador AS 'ValorDescontoDebito',
							@ValorAgenteFinanciador AS 'ValorDebito',
							CONCAT(
								'Agente Financiador',
								': Mês: ',
								CONVERT(VARCHAR, 
									CASE WHEN FNDebitos.Mes = 13 THEN
										1 
									ELSE 
										FNDebitos.Mes 
									END),
								', Ano: ',
								CONVERT(VARCHAR, 
									CASE WHEN FNDebitos.Mes = 13 THEN 
										FNDebitos.Ano + 1 
									ELSE 
										FNDebitos.Ano 
									END)
								) AS 'DescricaoDebito',
							FNDebitos.RM,
							FNDebitos.Nser,
							FNDebitos.LSer,
							FNDebitos.LCur,
							'A' AS 'Con',
							0 AS 'SPC',
							0 AS 'DP',
							0 AS 'Adap',
							0 AS 'Bolsa',
							FNDebitos.Mes,
							FNDebitos.Ano,
							FNDebitos.DataVencimentoPadrao,
							FNDebitos.DataVencimentoDebito,
							FNDebitos.DataVencimento,
							CONVERT(DATE, GETDATE()) AS 'DataAtualizado',
							0 AS 'QtDiasAtrasado',
							GETDATE() AS 'DataHoraCadastro',
							1 AS 'CodigoUsuarioCadastro',
							0 AS 'Excluido',
							0 AS 'Abonado',
							0 AS 'DebitoEmAcordo',
							FNDebitos.CPFResponsavel,
							1 AS 'Visivel',
							0 AS 'ValidadoBaixa',
							0 AS 'RecalculouMultaJuros',
							FNDebitos.Controle,
							FNDebitos.AnoInicioAula
						FROM
							BaseEducacional..FNDebitos
						WHERE
							FNDebitos.Codigo = @CodigoMensalidade;
						SELECT @CodigoAgenteFinanciador = @@IDENTITY;
					
						-- Atualiza Agente Financiador
						EXEC BaseEducacional..spAtualizaDebito @Codigo = @CodigoAgenteFinanciador;

						-- Cadastrar FNControleAgenteFinanciador (vinculo da Mensalidade com o Agente Financiador)
						INSERT INTO BaseEducacional..FNControleAgenteFinanciador
							(CodigoFNDebito,
							CodigoFNDebitoAgenteFinanciador,
							DataHoraCadastro)
						VALUES
							(@CodigoMensalidade,
							@CodigoAgenteFinanciador,
							GETDATE());

					END

					--------------------------------------------------------------------------------------------------------
					----- Realiza procedimentos de Repasse Fies ------------------------------------------------------------
					--------------------------------------------------------------------------------------------------------

					-- Gera débito de Repasse Fies
					DECLARE @CodigoRepasseFies AS INT;
				
					INSERT INTO BaseEducacional..FNDebitos
						(Tipo, 
						AgrupadorDebito, 
						ValorCheioNominal, 
						ValorDescontoNominal, 
						ValorCheioDebito, 
						ValorDescontoDebito, 
						ValorDebito, 
						DescricaoDebito, 
						RM, 
						Nser, 
						LSer, 
						LCur, 
						Con, 
						SPC, 
						DP, 
						Adap, 
						Bolsa, 
						Mes, 
						Ano, 
						DataVencimentoPadrao, 
						DataVencimentoDebito, 
						DataVencimento, 
						DataAtualizado, 
						QtDiasAtrasado, 
						DataHoraCadastro, 
						CodigoUsuarioCadastro, 
						Excluido, 
						Abonado, 
						DebitoEmAcordo, 
						CPFResponsavel, 
						Visivel, 
						ValidadoBaixa, 
						RecalculouMultaJuros, 
						Controle,
						AnoInicioAula)
					SELECT
						'Repasse Fies' AS 'Tipo',
						@AgrupadorRepasseFies AS 'AgrupadorDebito',
						@ValorRepasseFies AS 'ValorCheioNominal',
						@ValorRepasseFies AS 'ValorDescontoNominal',
						@ValorRepasseFies AS 'ValorCheioDebito',
						@ValorRepasseFies AS 'ValorDescontoDebito',
						@ValorRepasseFies AS 'ValorDebito',
						CONCAT(
							'Repasse Fies',
							': Mês: ',
							CONVERT(VARCHAR, 
								CASE WHEN FNDebitos.Mes = 13 THEN
									1 
								ELSE 
									FNDebitos.Mes 
								END),
							', Ano: ',
							CONVERT(VARCHAR, 
								CASE WHEN FNDebitos.Mes = 13 THEN 
									FNDebitos.Ano + 1 
								ELSE 
									FNDebitos.Ano 
								END)
							) AS 'DescricaoDebito',
						FNDebitos.RM,
						FNDebitos.Nser,
						FNDebitos.LSer,
						FNDebitos.LCur,
						'A' AS 'Con',
						0 AS 'SPC',
						0 AS 'DP',
						0 AS 'Adap',
						0 AS 'Bolsa',
						FNDebitos.Mes,
						FNDebitos.Ano,
						FNDebitos.DataVencimentoPadrao,
						FNDebitos.DataVencimentoDebito,
						FNDebitos.DataVencimento,
						CONVERT(DATE, GETDATE()) AS 'DataAtualizado',
						0 AS 'QtDiasAtrasado',
						GETDATE() AS 'DataHoraCadastro',
						1 AS 'CodigoUsuarioCadastro',
						0 AS 'Excluido',
						0 AS 'Abonado',
						0 AS 'DebitoEmAcordo',
						FNDebitos.CPFResponsavel,
						1 AS 'Visivel',
						0 AS 'ValidadoBaixa',
						0 AS 'RecalculouMultaJuros',
						FNDebitos.Controle,
						FNDebitos.AnoInicioAula
					FROM
						BaseEducacional..FNDebitos
					WHERE
						FNDebitos.Codigo = @CodigoMensalidade;
					SELECT @CodigoRepasseFies = @@IDENTITY;
					
					-- Atualiza Repasse Fies
					EXEC BaseEducacional..spAtualizaDebito @Codigo = @CodigoRepasseFies;

					-- Cadastrar FNControleRepasseFies (vinculo da Mensalidade com o Repasse Fies)
					INSERT INTO BaseEducacional..FNControleRepasseFies
						(CodigoFNDebito,
						CodigoFNDebitoRepasseFies,
						DataHoraCadastro)
					VALUES
						(@CodigoMensalidade,
						@CodigoRepasseFies,
						GETDATE());

					FETCH NEXT FROM 
						Ponteiro 
					INTO 
						@CodigoMensalidade,
						@AnoMensalidade,
						@MesMensalidade

				END

				CLOSE Ponteiro
				DEALLOCATE Ponteiro

				------------------------------------------------------------------------------------------------------------
				----- Inserindo Log de cadastro da bolsa na HistoricoPessoa ------------------------------------------------
				------------------------------------------------------------------------------------------------------------

				INSERT INTO BaseEducacional..HistoricoPessoa
					(CPFCNPJ, 
					RM,
					Cabecalho,
					Observacao,
					Origem,
					CodigoUsuarioCadastro,
					DataHoraCadastro,
					Ativo)
				SELECT TOP 1
					FNDebitos.CPFResponsavel, 
					@RM,
					NULL,
					@Justificativa,
					'Bolsa',
					1,
					GETDATE(),
					1
				FROM
					@TabDebitos AS TabDebitos
					INNER JOIN BaseEducacional..FNDebitos WITH (NOLOCK)
						ON TabDebitos.Codigo = FNDebitos.Codigo;

			END

			COMMIT TRANSACTION

		END TRY
		BEGIN CATCH

			SELECT
				ERROR_LINE(),
				ERROR_NUMBER(),
				ERROR_SEVERITY(),
				ERROR_STATE(),
				ERROR_PROCEDURE(),
				ERROR_MESSAGE();

			ROLLBACK TRANSACTION

		END CATCH

	END
	```

Para identificar se a Bolsa FIES foi **cadastrada corretamente**, utilize o 
script abaixo:

??? example "Verificando se a Bolsa FIES foi cadastrada corretamente"
	```sql

	------------------------------------------------------------------------------------------------------------------------
	----- Preencha as variáveis abaixo para analisar a bolsa FIES recém cadastrada -----------------------------------------
	------------------------------------------------------------------------------------------------------------------------
	DECLARE @RM AS INT = 84486;
	DECLARE @Ano AS INT = 2023;
	DECLARE @Semestre AS INT = 2;

	-- Analisando débitos de Mensalidade, Agente Financiador e Repasse Fies
	SELECT 
		Codigo,
		RM,
		Tipo,
		Ano, 
		Mes, 
		Plano,
		Bolsa,
		ValorCheioNominal,
		ValorDescontoNominal,
		ValorCheioDebito,
		ValorDescontoDebito,
		--ValorDeducao, ValorAcrescimo,
		ValorDebito,
		ValorPago,
		Abonado,
		DataHoraCadastro
	FROM 
		BaseEducacional..FNDebitos WITH (NOLOCK)
	WHERE
		FNDebitos.RM = @RM
		AND FNDebitos.Ano = @Ano
		AND
		(
			(@Semestre = 1
			AND FNDebitos.Mes IN (2, 3, 4, 5, 6, 7))
			OR
			(@Semestre = 2
			AND FNDebitos.Mes IN (8, 9, 10, 11, 12, 13))
		)
		AND FNDebitos.Visivel = 1
		AND FNDebitos.Excluido = 0
		AND FNDebitos.Tipo IN ('Mensalidade', 'Agente Financiador', 'Repasse Fies')
	ORDER BY
		FNDebitos.Tipo,
		FNDebitos.Ano,
		FNDebitos.Mes;

	-- Analisando Bolsas
	SELECT 
		FNBolsa.RM,
		FNBolsa.Codigo,
		FNTipoBolsa.Descricao,
		--FNBolsa.CodigoTipoBolsa,
		FNBolsa.Porcentagem,
		CONCAT('De ', FNBolsa.MesInicio, '/', FNBolsa.AnoInicio, ' até ', FNBolsa.MesTermino, '/', FNBolsa.AnoTermino) AS 'Periodo',
		vUsuarioPessoa.Nome AS 'UsuarioCadastro',
		FNBolsa.DataHoraCadastro,
		FNBolsa.*
	FROM 
		BaseEducacional..FNBolsa WITH (NOLOCK)
		INNER JOIN BaseEducacional..FNTipoBolsa WITH (NOLOCK)
			ON FNBolsa.CodigoTipoBolsa = FNTipoBolsa.Codigo
		INNER JOIN BaseEducacional..vUsuarioPessoa WITH (NOLOCK)
			ON vUsuarioPessoa.Codigo = FNBolsa.CodigoUsuarioCadastro
	WHERE
		FNBolsa.RM = @RM
		AND FNBolsa.Ano = @Ano
		AND FNBolsa.Ativo = 1
	ORDER BY
		FNBolsa.DataHoraCadastro;

	-- Analisando Vinculo dos débitos com as bolsas, via FNBolsaDebitos
	SELECT 
		FNDebitos.Codigo,
		FNDebitos.RM,
		FNDebitos.Tipo,
		FNDebitos.Ano,
		FNDebitos.Mes,
		FNDebitos.Bolsa,
		FNTipoBolsa.Descricao,
		FNBolsa.Porcentagem,
		CASE WHEN FNBolsa.Codigo IS NULL THEN 
			NULL 
		ELSE 
			CONCAT('De ', FNBolsa.MesInicio, '/', FNBolsa.AnoInicio, ' até ', FNBolsa.MesTermino, '/', FNBolsa.AnoTermino) 
		END AS 'Periodo'
	FROM 
		BaseEducacional..FNDebitos WITH (NOLOCK)
		LEFT JOIN BaseEducacional..FNBolsaDebitos WITH (NOLOCK)
			ON FNBolsaDebitos.CodigoDebito = FNDebitos.Codigo
		LEFT JOIN BaseEducacional..FNBolsa WITH (NOLOCK)
			ON FNBolsaDebitos.CodigoBolsa = FNBolsa.Codigo
			AND FNBolsa.Ativo = 1
			AND FNDebitos.RM = FNBolsa.RM
		LEFT JOIN BaseEducacional..FNTipoBolsa WITH (NOLOCK)
			ON FNBolsa.CodigoTipoBolsa = FNTipoBolsa.Codigo
	WHERE
		FNDebitos.RM = @RM
		AND FNDebitos.Ano = @Ano
		AND
		(
			(@Semestre = 1
			AND FNDebitos.Mes IN (2, 3, 4, 5, 6, 7))
			OR
			(@Semestre = 2
			AND FNDebitos.Mes IN (8, 9, 10, 11, 12, 13))
		)
		AND FNDebitos.Visivel = 1
		AND FNDebitos.Excluido = 0
		AND FNDebitos.Tipo IN ('Mensalidade', 'Agente Financiador', 'Repasse Fies')
	ORDER BY
		FORMAT(FNDebitos.DataHoraCadastro, 'yyyy-MM-dd HH:mm'),
		FNDebitos.Ano,
		FNDebitos.Tipo,
		FNDebitos.Mes,
		FNTipoBolsa.Descricao;

	-- Analisando Vinculo dos débitos com as bolsas, via FNBolsaAplicada
	SELECT 
		FNDebitos.Codigo,
		FNDebitos.RM,
		FNDebitos.Tipo,
		FNDebitos.Ano,
		FNDebitos.Mes,
		FNDebitos.Bolsa,
		FNTipoBolsa.Descricao,
		FNBolsaAplicada.Porcentagem
	FROM 
		BaseEducacional..FNDebitos WITH (NOLOCK)
		LEFT JOIN BaseEducacional..FNBolsaAplicada WITH (NOLOCK)
			ON FNBolsaAplicada.CodigoDebito = FNDebitos.Codigo
		LEFT JOIN BaseEducacional..FNTipoBolsa WITH (NOLOCK)
			ON FNBolsaAplicada.CodigoTipoBolsa = FNTipoBolsa.Codigo
	WHERE
		FNDebitos.RM = @RM
		AND FNDebitos.Ano = @Ano
		AND
		(
			(@Semestre = 1
			AND FNDebitos.Mes IN (2, 3, 4, 5, 6, 7))
			OR
			(@Semestre = 2
			AND FNDebitos.Mes IN (8, 9, 10, 11, 12, 13))
		)
		AND FNDebitos.Visivel = 1
		AND FNDebitos.Excluido = 0
		AND FNDebitos.Tipo IN ('Mensalidade', 'Agente Financiador', 'Repasse Fies')
	ORDER BY
		FORMAT(FNDebitos.DataHoraCadastro, 'yyyy-MM-dd HH:mm'),
		FNDebitos.Ano,
		FNDebitos.Tipo,
		FNDebitos.Mes,
		FNTipoBolsa.Descricao;
		
	-- Analisando Vinculo das Mensalidades com os Agentes Financiadores
	SELECT
		'|' AS 'Mensalidade',
		Mensalidade.Codigo,
		Mensalidade.RM,
		Mensalidade.Tipo,
		Mensalidade.Ano, 
		Mensalidade.Mes, 
		Mensalidade.Plano,
		Mensalidade.Bolsa,
		Mensalidade.ValorCheioNominal,
		Mensalidade.ValorDescontoNominal,
		Mensalidade.ValorCheioDebito,
		Mensalidade.ValorDescontoDebito,
		--Mensalidade.ValorDeducao, Mensalidade.ValorAcrescimo,
		Mensalidade.ValorDebito,
		Mensalidade.ValorPago,
		Mensalidade.Abonado,
		Mensalidade.DataHoraCadastro,
		'|' AS 'Agente Financiador',
		AgenteFinanciador.Codigo,
		AgenteFinanciador.RM,
		AgenteFinanciador.Tipo,
		AgenteFinanciador.Ano, 
		AgenteFinanciador.Mes, 
		AgenteFinanciador.Plano,
		AgenteFinanciador.Bolsa,
		AgenteFinanciador.ValorCheioNominal,
		AgenteFinanciador.ValorDescontoNominal,
		AgenteFinanciador.ValorCheioDebito,
		AgenteFinanciador.ValorDescontoDebito,
		--AgenteFinanciador.ValorDeducao, AgenteFinanciador.ValorAcrescimo,
		AgenteFinanciador.ValorDebito,
		AgenteFinanciador.ValorPago,
		AgenteFinanciador.Abonado,
		AgenteFinanciador.DataHoraCadastro,
		'|' AS '|'
	FROM
		BaseEducacional..FNDebitos AS Mensalidade WITH (NOLOCK)
		INNER JOIN BaseEducacional..FNControleAgenteFinanciador WITH (NOLOCK)
			ON FNControleAgenteFinanciador.CodigoFNDebito = Mensalidade.Codigo
		INNER JOIN BaseEducacional..FNDebitos AS AgenteFinanciador WITH (NOLOCK)
			ON FNControleAgenteFinanciador.CodigoFNDebitoAgenteFinanciador = AgenteFinanciador.Codigo
			AND Mensalidade.RM = AgenteFinanciador.RM
			AND Mensalidade.Ano = AgenteFinanciador.Ano
			AND Mensalidade.Mes = AgenteFinanciador.Mes
			AND AgenteFinanciador.Visivel = 1
			AND AgenteFinanciador.Excluido = 0
			AND AgenteFinanciador.Tipo = 'Agente Financiador'
	WHERE
		Mensalidade.RM = @RM
		AND Mensalidade.Ano = @Ano
		AND
		(
			(@Semestre = 1
			AND Mensalidade.Mes IN (2, 3, 4, 5, 6, 7))
			OR
			(@Semestre = 2
			AND Mensalidade.Mes IN (8, 9, 10, 11, 12, 13))
		)
		AND Mensalidade.Visivel = 1
		AND Mensalidade.Excluido = 0
		AND Mensalidade.Tipo = 'Mensalidade';
		
	-- Analisando Vinculo das Mensalidades com os Repasses Fies
	SELECT
		'|' AS 'Mensalidade',
		Mensalidade.Codigo,
		Mensalidade.RM,
		Mensalidade.Tipo,
		Mensalidade.Ano, 
		Mensalidade.Mes, 
		Mensalidade.Plano,
		Mensalidade.Bolsa,
		Mensalidade.ValorCheioNominal,
		Mensalidade.ValorDescontoNominal,
		Mensalidade.ValorCheioDebito,
		Mensalidade.ValorDescontoDebito,
		--Mensalidade.ValorDeducao, Mensalidade.ValorAcrescimo,
		Mensalidade.ValorDebito,
		Mensalidade.ValorPago,
		Mensalidade.Abonado,
		Mensalidade.DataHoraCadastro,
		'|' AS 'Repasse Fies',
		RepasseFies.Codigo,
		RepasseFies.RM,
		RepasseFies.Tipo,
		RepasseFies.Ano, 
		RepasseFies.Mes, 
		RepasseFies.Plano,
		RepasseFies.Bolsa,
		RepasseFies.ValorCheioNominal,
		RepasseFies.ValorDescontoNominal,
		RepasseFies.ValorCheioDebito,
		RepasseFies.ValorDescontoDebito,
		--RepasseFies.ValorDeducao, RepasseFies.ValorAcrescimo,
		RepasseFies.ValorDebito,
		RepasseFies.ValorPago,
		RepasseFies.Abonado,
		RepasseFies.DataHoraCadastro,
		'|' AS '|'
	FROM
		BaseEducacional..FNDebitos AS Mensalidade WITH (NOLOCK)
		INNER JOIN BaseEducacional..FNControleRepasseFies WITH (NOLOCK)
			ON FNControleRepasseFies.CodigoFNDebito = Mensalidade.Codigo
		INNER JOIN BaseEducacional..FNDebitos AS RepasseFies WITH (NOLOCK)
			ON FNControleRepasseFies.CodigoFNDebitoRepasseFies = RepasseFies.Codigo
			AND Mensalidade.RM = RepasseFies.RM
			AND Mensalidade.Ano = RepasseFies.Ano
			AND Mensalidade.Mes = RepasseFies.Mes
			AND RepasseFies.Visivel = 1
			AND RepasseFies.Excluido = 0
			AND RepasseFies.Tipo = 'Repasse Fies'
	WHERE
		Mensalidade.RM = @RM
		AND Mensalidade.Ano = @Ano
		AND
		(
			(@Semestre = 1
			AND Mensalidade.Mes IN (2, 3, 4, 5, 6, 7))
			OR
			(@Semestre = 2
			AND Mensalidade.Mes IN (8, 9, 10, 11, 12, 13))
		)
		AND Mensalidade.Visivel = 1
		AND Mensalidade.Excluido = 0
		AND Mensalidade.Tipo = 'Mensalidade';

	-- Analisando log de bolsa no HistoricoPessoa
	SELECT
		*
	FROM
		BaseEducacional..HistoricoPessoa WITH (NOLOCK)
	WHERE
		RM = @RM
		AND Origem = 'Bolsa';
	```

### Observações:
```
Todas as tabelas citadas são do banco "BaseEducacional".
As informações das colunas "Bolsa" e "Porcentagem" são inseridas na escala de 0 a 100.
```
