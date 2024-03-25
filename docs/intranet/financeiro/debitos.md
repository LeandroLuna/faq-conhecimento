### Recuperar log de um débito

As vezes é necessário saber o que aconteceu com um débito, alteração de valor, plano, bolsa, todas essas operacões são logadas na tabela **FNLogDebito**.
O script abaixo auxilia na tarefa recuperando informações baseadas no mês, ano e RM de um débito.

```sql hl_lines="14 15 16 17"
SELECT
	FNDebitos.Tipo,
	FNDebitos.DescricaoDebito,
	FNLogDebito.Sistema,
	FNLogDebito.Observacao,
	FNLogDebito.DataHora,
	vUsuarioPessoa.Nome
FROM
	FNDebitos 
	INNER JOIN FNBackupDebito oN FNBackupDebito.CodigoDebito = FNDebitos.Codigo
	INNER JOIN FNLogDebito ON FNLogDebito.Codigo = FNBackupDebito.CodigoLog
	INNER JOIN vUsuarioPessoa ON vUsuarioPessoa.Codigo = FNLogDebito.CodigoUsuario
WHERE
	FNDebitos.RM = 75008 AND
	FNDebitos.Mes = 3 AND
	FNDebitos.Ano = 2016 AND 
	FNDebitos.Tipo = 'Mensalidade'
ORDER BY
	FNLogDebito.DataHora

```

### Mover o primeiro débito para ser o último débito do aluno

Na pós-graduação algumas vezes aceitamos que o aluno faça a matrícula após o vencimento do primeiro débito, como o sistema gera os débitos e primeiro acaba ficando vencido, e o aluno já tem que pagar a primeira mensalidade, mas algumas vezes o financeiro abre exceção para que o primeiro débito sejá movido para o último.
Para atender essa demanta o script abaixo ajuda neste processo, basta alterar o RM e rodar o mesmo.

```sql
USE BaseEducacional
GO
DECLARE @RM INT, @CodigoPrimeiro INT, @CodigoUltimo INT, @Mes SMALLINT, @Ano INT, @DataVencimento DATE, @DataDesconto DATE
--Alterar o RM do aluno
SET @RM = 331891 
SELECT
    @CodigoPrimeiro = MAX(CASE WHEN Tabela.Primeiro = 1 THEN Tabela.Codigo ELSE NULL END),
    @CodigoUltimo = MAX(CASE WHEN Tabela.Ultimo = 1 THEN Tabela.Codigo ELSE NULL END)
FROM
    (SELECT
        ROW_NUMBER() OVER (ORDER BY FNDebitos.Ano, FNDebitos.Mes) AS 'Primeiro',
        ROW_NUMBER() OVER (ORDER BY FNDebitos.Ano DESC, FNDebitos.Mes DESC) AS 'Ultimo',
        FNDebitos.Codigo
    FROM
        FNDebitos WITH (NOLOCK)
    WHERE
        FNDebitos.RM = @RM
        AND FNDebitos.Tipo = 'Mensalidade'
        AND FNDebitos.Visivel = 1
        AND FNDebitos.Excluido = 0) AS Tabela
WHERE
    Tabela.Primeiro = 1
    OR Tabela.Ultimo = 1
IF @CodigoPrimeiro IS NOT NULL AND @CodigoUltimo IS NOT NULL
BEGIN
    IF @CodigoPrimeiro <> @CodigoUltimo
    BEGIN
        SELECT
            @Mes = FNDebitos.Mes,
            @Ano = FNDebitos.Ano
        FROM
            FNDebitos WITH (NOLOCK)
        WHERE
            FNDebitos.Codigo = @CodigoUltimo
        SET @Mes = @Mes + 1
        IF @Mes = 14
        BEGIN
            SET @Mes = 2
            SET @Ano = @Ano + 1
        END
        SET @DataDesconto = BaseEducacional.Dbo.fnRetornaDiaUtilFinanceiro(CAST(CASE WHEN @Mes = 13 THEN @Ano + 1 ELSE @Ano END AS VARCHAR) + RIGHT('00' + CAST(CASE WHEN @Mes = 13 THEN 1 ELSE @Mes END AS VARCHAR), 2) + '05')
        SET @DataVencimento = BaseEducacional.Dbo.fnRetornaDiaUtilFinanceiro(CAST(CASE WHEN @Mes = 13 THEN @Ano + 1 ELSE @Ano END AS VARCHAR) + RIGHT('00' + CAST(CASE WHEN @Mes = 13 THEN 1 ELSE @Mes END AS VARCHAR), 2) + '15')
        UPDATE
            FNDebitos
        SET
            Mes = @Mes,
            Ano = @Ano,
            DataVencimentoPadrao = @DataVencimento,
            DataDescontoPadrao = @DataDesconto,
            DataVencimentoDebito = @DataVencimento,
            DataDescontoDebito = @DataDesconto,
            DataVencimento = @DataDesconto,
            ValorMulta = 0,
            ValorJuros = 0,
            QtDiasAtrasado = 0,
            CodigoUsuarioAlteracaoDataVencimento = NULL,
            DataHoraAlteracaoDataVencimento = NULL,
            OpcaoSelecionadaAlteraDataVencimento = NULL,
            MotivoAlteracaoDataVencimento = NULL,
            DataNovoVencimento = NULL,
            DescricaoDebito = 'Mens. Mês ' + RIGHT('00' + CAST(CASE WHEN @Mes = 13 THEN 1 ELSE @Mes END AS VARCHAR), 2) + ' Ano: ' + CAST(CASE WHEN @Mes = 13 THEN @Ano + 1 ELSE @Ano END AS VARCHAR)
        WHERE
            Codigo = @CodigoPrimeiro

		EXEC spAtualizaDebito @Codigo = @CodigoPrimeiro
    END
    ELSE
    BEGIN
        PRINT 'Primeiro é o último débito são o mesmo registro!'
    END
END
ELSE
BEGIN
    PRINT 'O primeiro ou último débito não existe!'
END
```

### Filtrar débitos ativos do aluno

``` sql
SELECT
    *
FROM
    BaseEducacional..FNDebitos WITH (NOLOCK)
WHERE
    Con = 'A' AND
    MesAnoEvd IS NULL AND
    Visivel = 1 AND
    Excluido = 0 AND
    DataOutLan IS NULL AND
    DebitoEmAcordo = 0 AND
    RM = @RM
```

### Filtrar débitos passíveis de cobrança do aluno *(posso cobrar)*

``` sql
SELECT
    *
FROM
    BaseEducacional..FNDebitos WITH (NOLOCK)
WHERE
    Con = 'A' AND
    MesAnoEvd IS NULL AND
    Visivel = 1 AND
    Excluido = 0 AND
    DataOutLan IS NULL AND
    DebitoEmAcordo = 0 AND
    Bolsa < 100 AND
    ValorDebito > 0 AND
    ValorPago IS NULL AND
    Abonado = 0 AND
    RM = @RM
```

### Filtrar débitos pagos

``` sql
SELECT
    *
FROM
    BaseEducacional..FNDebitos WITH (NOLOCK)
WHERE
    CON = 'A' AND
    Visivel = 1 AND
    Excluido = 0 AND
    (Abonado = 1 OR Bolsa = 100 OR ValorPago IS NOT NULL) AND
    RM = @RM
```

### Alterar o plano de uma matrícula recém realizada na graduação

Alguns responsáveis financeiros resolvem alterar o plano selecionado logo após a realização da matrícula, o script abaixo ajuda nisso, basta informar o RM, Ano e o Plano que deve ficar e rodar.

``` sql
DECLARE @RM INT, @AnoProcesso INT, @CodigoAluno INT, @PlanoAlterar CHAR(1), @CodigoPlano INT, @CodigoTabelaValor INT, @CodigoRelacao INT, @ValorMatricula MONEY, @Plano VARCHAR(10), @TabPreco NCHAR(20), @ValorPago MONEY, @DataPagamento DATE, @Abonado INT
SET @AnoProcesso = 2020
SET @RM = 84412
SET @PlanoAlterar = 'C' --A = A Vista | B = Anual | C = Estendido | D = Estendidão
BEGIN TRANSACTION
BEGIN TRY
	IF EXISTS(SELECT * FROM Educacional..vAluno AS vAluno WHERE vAluno.RM = @RM AND vAluno.CodigoUnidade = 1)
	BEGIN
		SELECT @CodigoAluno = vAluno.Codigo FROM Educacional..vAluno AS vAluno WHERE vAluno.RM = @RM AND vAluno.CodigoUnidade = 1
		IF EXISTS(SELECT * FROM Educacional..vAlunoTurma AS vAlunoTurma INNER JOIN Educacional..vRelacao AS vRelacao ON vAlunoTurma.CodigoRelacao = vRelacao.Codigo WHERE vAlunoTurma.CodigoAluno = @CodigoAluno AND vRelacao.Ano = @AnoProcesso AND vAlunoTurma.CodigoTipoStatus IN (1, 8, 22, 23))
		BEGIN
			SELECT @CodigoRelacao = vAlunoTurma.CodigoRelacao FROM Educacional..vAlunoTurma AS vAlunoTurma INNER JOIN Educacional..vRelacao AS vRelacao ON vAlunoTurma.CodigoRelacao = vRelacao.Codigo WHERE vAlunoTurma.CodigoAluno = @CodigoAluno AND vRelacao.Ano = @AnoProcesso AND vAlunoTurma.CodigoTipoStatus IN (1, 8, 22, 23)
			IF EXISTS(SELECT * FROM Educacional..CPTVEST AS CPTVEST WHERE CPTVEST.RM = @RM AND CPTVEST.AnoProcesso = @AnoProcesso)
			BEGIN
				IF EXISTS(SELECT
								*
							FROM
								Educacional..vRelacaoUnidadeServicoPlano AS vRelacaoUnidadeServicoPlano
								INNER JOIN Educacional..vUnidadeServicoPlano AS vUnidadeServicoPlano ON
									vRelacaoUnidadeServicoPlano.CodigoUnidadeServicoPlano = vUnidadeServicoPlano.Codigo
							WHERE
								vRelacaoUnidadeServicoPlano.CodigoRelacao = @CodigoRelacao
								AND vUnidadeServicoPlano.Plano = @PlanoAlterar)
				BEGIN
					SELECT
						@CodigoPlano = vRelacaoUnidadeServicoPlano.CodigoUnidadeServicoPlano,
						@CodigoTabelaValor = vUnidadeServicoPlano.CodigoTabelaValor,
						@ValorMatricula = vUnidadeServicoPlano.ValorMatricula
					FROM
						Educacional..vRelacaoUnidadeServicoPlano AS vRelacaoUnidadeServicoPlano
						INNER JOIN Educacional..vUnidadeServicoPlano AS vUnidadeServicoPlano ON
							vRelacaoUnidadeServicoPlano.CodigoUnidadeServicoPlano = vUnidadeServicoPlano.Codigo
					WHERE
						vRelacaoUnidadeServicoPlano.CodigoRelacao = @CodigoRelacao
						AND vUnidadeServicoPlano.Plano = @PlanoAlterar

					IF EXISTS(SELECT
									*
								FROM
									BaseEducacional..FNTabelaValor AS FNTabelaValor
								WHERE
									FNTabelaValor.Codigo = @CodigoTabelaValor)
					BEGIN
						SELECT
							@TabPreco = FNTabelaValor.TabPreco,
							@Plano = FNTabelaValor.Plano
						FROM
							BaseEducacional..FNTabelaValor AS FNTabelaValor
						WHERE
							FNTabelaValor.Codigo = @CodigoTabelaValor

						IF EXISTS(SELECT * FROM BaseEducacional..FNDebitos WHERE RM = @RM AND Ano = @AnoProcesso AND Tipo = 'Matrícula')
						BEGIN
							IF NOT EXISTS(SELECT
												*
											FROM
												BaseEducacional..FNDebitos AS FNDebitos
											WHERE
												FNDebitos.RM = @RM
												AND FNDebitos.Ano = @AnoProcesso
												AND (
													FNDebitos.Bolsa > 0
													OR FNDebitos.ValorPago IS NOT NULL
													OR FNDebitos.Abonado = 1
												)
												AND FNDebitos.Tipo = 'Mensalidade')
							BEGIN
								SELECT @ValorPago = FNDebitos.ValorPago, @DataPagamento = FNDebitos.DataPagamento, @Abonado = FNDebitos.Abonado FROM BaseEducacional..FNDebitos AS FNDebitos WHERE FNDebitos.RM = @RM AND FNDebitos.Ano = @AnoProcesso AND FNDebitos.Tipo = 'Matrícula'
								UPDATE Educacional..MatriculaRematricula SET CodigoPlano = @CodigoPlano WHERE CodigoAluno = @CodigoAluno AND Ano = @AnoProcesso
								UPDATE Educacional..CPTVEST SET CodigoPlano = @CodigoPlano WHERE RM = @RM AND AnoProcesso = @AnoProcesso
								DELETE BaseEducacional..FNDebitos WHERE RM = @RM AND Ano = @AnoProcesso AND Tipo = 'Mensalidade'
								UPDATE BaseEducacional..FNDebitos SET CodigoTabelaValor = @CodigoTabelaValor, TabPreco = @TabPreco, Plano = @Plano, ValorCheioNominal = @ValorMatricula, ValorCheioDebito = @ValorMatricula, ValorDebito = @ValorMatricula WHERE FNDebitos.RM = @RM AND FNDebitos.Ano = @AnoProcesso AND FNDebitos.Tipo = 'Matrícula'
								UPDATE BaseEducacional..FNDebitos SET ValorPago = NULL, DataPagamento = NULL, Abonado = 0 WHERE FNDebitos.RM = @RM AND FNDebitos.Ano = @AnoProcesso AND FNDebitos.Tipo = 'Matrícula'
								UPDATE BaseEducacional..FNDebitos SET ValorPago = @ValorPago, DataPagamento = @DataPagamento, Abonado = @Abonado WHERE FNDebitos.RM = @RM AND FNDebitos.Ano = @AnoProcesso AND FNDebitos.Tipo = 'Matrícula'
							END
							ELSE
							BEGIN
								PRINT 'Não é possível realizar a alteração, pois o aluno tem mensalidades geradas com bolsa!'
							END
						END
						ELSE
						BEGIN
							PRINT 'Não existe o débito de matrícula para o RM informado!'
						END
					END
					ELSE
					BEGIN
						PRINT 'O plano não existe na tabela FNTabelaValor'
					END
				END
				ELSE
				BEGIN
					PRINT 'O plano informado não existe para o código relação ' + CONVERT(VARCHAR, @CodigoRelacao)
				END
			END
			ELSE
			BEGIN
				PRINT 'O aluno informado não pertence ao processo do ano ' + CONVERT(VARCHAR, @AnoProcesso)
			END
		END
		ELSE
		BEGIN
			PRINT 'Aluno não está matrículado em uma turma do ano ' + CONVERT(VARCHAR, @AnoProcesso)
		END
	END
	ELSE
	BEGIN
		PRINT 'RM informado não existe!'
	END
END TRY
BEGIN CATCH
    SELECT  
        ERROR_NUMBER() AS ErrorNumber  
        ,ERROR_SEVERITY() AS ErrorSeverity  
        ,ERROR_STATE() AS ErrorState  
        ,ERROR_PROCEDURE() AS ErrorProcedure  
        ,ERROR_LINE() AS ErrorLine  
        ,ERROR_MESSAGE() AS ErrorMessage;  

    IF @@TRANCOUNT > 0  
	BEGIN
		ROLLBACK TRANSACTION
	END
END CATCH
IF @@TRANCOUNT > 0  
BEGIN
	COMMIT TRANSACTION
END
```

!!! warning "Atenção"
    Não esquecer de alterar o RM do aluno.
