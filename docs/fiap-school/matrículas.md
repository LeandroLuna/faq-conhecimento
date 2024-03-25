# Matrículas 

### Adicionar débito de período integral

O débito de período integral é adicionado automaticamente quando o responsável pela rematrícula finaliza o processo.

Quando o responsável finaliza o processo e entra em contato com o HelpCenter para alterar para integral, deve-se alterar na intranet3 e na ficha financeira.

### Reverter um cancelamento

Para cancelar um cancelamento (ou transferencia), deve se alterar as tabelas **Aluno**, **AlunoTurma** e **AlunoCancelamento** conforme script abaixo:

```sql hl_lines="1 2"
DECLARE @CodigoAluno INT = (SELECT Codigo FROM vAluno WHERE RM = YYYYY)
DECLARE @Ano INT = 2018

UPDATE Aluno SET StatusRegistro=0 WHERE Codigo = @CodigoAluno AND StatusRegistro=1 AND CodigoTipoStatus IN (17,3)
UPDATE Aluno SET StatusRegistro=1 WHERE Codigo = @CodigoAluno AND StatusRegistro=0 AND CodigoTipoStatus=1

UPDATE AlunoTurma SET StatusRegistro=1 WHERE CodigoAluno = @CodigoAluno AND CodigoRelacao IN (SELECT Codigo FROM vRelacao WHERE Ano = @Ano) AND StatusRegistro=0 AND CodigoTipoStatus=1
UPDATE AlunoTurma SET StatusRegistro=0 WHERE CodigoAluno = @CodigoAluno AND CodigoRelacao IN (SELECT Codigo FROM vRelacao WHERE Ano = @Ano) AND StatusRegistro=1 AND CodigoTipoStatus IN (17,3)

DELETE FROM AlunoCancelamentoCopi WHERE CodigoAluno = @CodigoAluno
```

### Contrato

Para exibir e imprimir contratos com a flag **Período Integral**, deve-se ajustar a tabela **MatriculaRematricula** da base **Educacional**.
```sql hl_lines="12"
UPDATE 
    Educacional..MatriculaRematricula 
SET
    PeriodoIntegral = 1 
WHERE 
    Ano = YEAR(GETDATE()) AND 
    CodigoAluno IN (SELECT 
                        Codigo
                    FROM 
                        Educacional..vAluno 
                    WHERE
                        RM = YYYYY) -- Ajustar conforme o RM do aluno
```


### Ficha Financeira

Para adicionar o débito integral, deve-se executar o script abaixo, alterando os campos conforme necessário

???+ note "ficha-financeira.sql"
    ```sql hl_lines="2"
    DECLARE @RM INT, @CPFResponsavel VARCHAR(20), @CodigoMatriculaRematricula INT, @CodigoAluno INT 
    SET @RM = 12345 -- RM do Aluno
    SET @CodigoAluno = (SELECT Codigo FROM Educacional..vAluno WHERE RM = @RM)
    SET @CodigoMatriculaRematricula = (SELECT Codigo FROM Educacional..vMatriculaRematricula WHERE CodigoAluno= (SELECT Codigo FROM Educacional..vAluno WHERE RM = @RM) and Ano=2018)
    SET @CPFResponsavel = (SELECT
                                vPessoa.CPF
                            FROM
                                Educacional..vAlunoResponsavel vAlunoResponsavel
                                INNER JOIN Educacional..vPessoa vPessoa ON vAlunoResponsavel.CodigoPessoaFinanceiro = vPessoa.Codigo
                            WHERE
                                CodigoAluno = @CodigoAluno AND 
                                UltimoResponsavel=1)

    INSERT INTO BaseEducacional..FNDebitos (Tipo, AgrupadorDebito, RM, NSer, LSer, LCur, Per, Con, SPC, DP, Adap, CodigoTabelaValor, TabPreco, Plano, Bolsa, ParcelaComplemento, Mes, Ano, ValorCheioNominal, ValorCheioDebito, DataVencimentoDebito, DataVencimento, ValorDebito, QtDiasAtrasado, DataHoraCadastro, CodigoUsuarioCadastro, Excluido, Abonado, DebitoEmAcordo, DescricaoDebito, Visivel, ValidadoBaixa, RecalculouMultaJuros, Controle, Bolsa1, Bolsa2, Bolsa3, Bolsa4, Bolsa5, ValorPago, DataPagamento, CPFResponsavel, NossoNumero) SELECT
                        'Matricula-Integral' AS 'Tipo',
                        REPLACE(NEWID(), '-', '') AS 'AgrupadorDebito',
                        vAluno.RM,
                        LEFT(vRelacao.Turma, 1) AS 'NSer',
                        RIGHT(vRelacao.Turma, 1) AS 'LSer',
                        SUBSTRING(vRelacao.Turma, 2, LEN(vRelacao.Turma)-2) AS 'LCur',
                        'I' AS 'Per',
                        'A' AS 'Con',
                        0 AS 'SPC',
                        0 AS 'DP',
                        0 AS 'Adap',
                        vUnidadeServicoPlano.CodigoTabelaValorIntegral,
                        FNTabelaValor.TabPreco,
                        FNTabelaValor.Plano,
                        0 AS 'Bolsa',
                        'P' AS 'ParcelaComplemento',
                        1 AS 'Mes',
                        vRelacao.Ano,
                        CASE WHEN CONVERT(DATE, vMatriculaRematricula.DataHoraMatriculou) <= FNTabelaValor.DataMatricula50 THEN
                            ISNULL(FNTabelaValor.ValorMatricula50, 0)
                        ELSE
                            CASE WHEN CONVERT(DATE, vMatriculaRematricula.DataHoraMatriculou) <= FNTabelaValor.DataMatricula40 THEN
                                ISNULL(FNTabelaValor.ValorMatricula40, 0)
                            ELSE
                                CASE WHEN CONVERT(DATE, vMatriculaRematricula.DataHoraMatriculou) <= FNTabelaValor.DataMatricula30 THEN
                                    ISNULL(FNTabelaValor.ValorMatricula30, 0)
                                ELSE
                                    ISNULL(FNTabelaValor.ValorMatricula, 0)
                                END
                            END
                        END AS 'ValorCheioNominal',
                        CASE WHEN CONVERT(DATE, vMatriculaRematricula.DataHoraMatriculou) <= FNTabelaValor.DataMatricula50 THEN
                            ISNULL(FNTabelaValor.ValorMatricula50, 0)
                        ELSE
                            CASE WHEN CONVERT(DATE, vMatriculaRematricula.DataHoraMatriculou) <= FNTabelaValor.DataMatricula40 THEN
                                ISNULL(FNTabelaValor.ValorMatricula40, 0)
                            ELSE
                                CASE WHEN CONVERT(DATE, vMatriculaRematricula.DataHoraMatriculou) <= FNTabelaValor.DataMatricula30 THEN
                                    ISNULL(FNTabelaValor.ValorMatricula30, 0)
                                ELSE
                                    ISNULL(FNTabelaValor.ValorMatricula, 0)
                                END
                            END
                        END AS 'ValorCheioDebito',
                        GETDATE() AS 'DataVencimentoDebito',
                        GETDATE() AS 'DataVencimento',
                        CASE WHEN CONVERT(DATE, vMatriculaRematricula.DataHoraMatriculou) <= FNTabelaValor.DataMatricula50 THEN
                            ISNULL(FNTabelaValor.ValorMatricula50, 0)
                        ELSE
                            CASE WHEN CONVERT(DATE, vMatriculaRematricula.DataHoraMatriculou) <= FNTabelaValor.DataMatricula40 THEN
                                ISNULL(FNTabelaValor.ValorMatricula40, 0)
                            ELSE
                                CASE WHEN CONVERT(DATE, vMatriculaRematricula.DataHoraMatriculou) <= FNTabelaValor.DataMatricula30 THEN
                                    ISNULL(FNTabelaValor.ValorMatricula30, 0)
                                ELSE
                                    ISNULL(FNTabelaValor.ValorMatricula, 0)
                                END
                            END
                        END AS 'ValorDebito',
                        0 AS 'QtDiasAtrasado',
                        GETDATE() AS 'DataHoraCadastro',
                        1 AS 'CodigoUsuarioCadastro',
                        0 AS 'Excluido',
                        0 AS 'Abonado',
                        0 AS 'DebitoEmAcordo',
                        'Matrícula Ano: ' + CONVERT(VARCHAR, vRelacao.Ano) AS 'DescricaoDebito',
                        1 AS 'Visivel',
                        0 AS 'ValidadoBaixa',
                        0 AS 'RecalculouMultaJuros',
                        'Novo' AS 'Controle',
                        0 AS 'Bolsa1',
                        0 AS 'Bolsa2',
                        0 AS 'Bolsa3',
                        0 AS 'Bolsa4',
                        0 AS 'Bolsa5',
                        CASE WHEN (CASE WHEN CONVERT(DATE, vMatriculaRematricula.DataHoraMatriculou) <= FNTabelaValor.DataMatricula50 THEN
                                        ISNULL(FNTabelaValor.ValorMatricula50, 0)
                                    ELSE
                                        CASE WHEN CONVERT(DATE, vMatriculaRematricula.DataHoraMatriculou) <= FNTabelaValor.DataMatricula40 THEN
                                            ISNULL(FNTabelaValor.ValorMatricula40, 0)
                                        ELSE
                                            CASE WHEN CONVERT(DATE, vMatriculaRematricula.DataHoraMatriculou) <= FNTabelaValor.DataMatricula30 THEN
                                                ISNULL(FNTabelaValor.ValorMatricula30, 0)
                                            ELSE
                                                ISNULL(FNTabelaValor.ValorMatricula, 0)
                                            END
                                        END
                                    END) = 0 THEN 0.01 ELSE NULL END AS 'ValorPago',
                        CASE WHEN (CASE WHEN CONVERT(DATE, vMatriculaRematricula.DataHoraMatriculou) <= FNTabelaValor.DataMatricula50 THEN
                                        ISNULL(FNTabelaValor.ValorMatricula50, 0)
                                    ELSE
                                        CASE WHEN CONVERT(DATE, vMatriculaRematricula.DataHoraMatriculou) <= FNTabelaValor.DataMatricula40 THEN
                                            ISNULL(FNTabelaValor.ValorMatricula40, 0)
                                        ELSE
                                            CASE WHEN CONVERT(DATE, vMatriculaRematricula.DataHoraMatriculou) <= FNTabelaValor.DataMatricula30 THEN
                                                ISNULL(FNTabelaValor.ValorMatricula30, 0)
                                            ELSE
                                                ISNULL(FNTabelaValor.ValorMatricula, 0)
                                            END
                                        END
                                    END) = 0 THEN CONVERT(DATE, vMatriculaRematricula.DataHoraMatriculou) ELSE NULL END AS 'DataPagamento',
                        @CPFResponsavel,
                        '301' + RIGHT('00000' + CONVERT(VARCHAR, vAluno.RM), 5) AS 'NossoNumero'
                    FROM
                        Educacional..vMatriculaRematricula AS vMatriculaRematricula
                        INNER JOIN Educacional..vAluno AS vAluno ON vMatriculaRematricula.CodigoAluno = vAluno.Codigo
                        INNER JOIN Educacional..vRelacao AS vRelacao ON vMatriculaRematricula.CodigoRelacaoMatriculado = vRelacao.Codigo
                        INNER JOIN Educacional..vUnidadeServicoPlano AS vUnidadeServicoPlano ON vRelacao.CodigoUnidadeServicoPlano = vUnidadeServicoPlano.Codigo
                        INNER JOIN BaseEducacional..FNTabelaValor AS FNTabelaValor ON vUnidadeServicoPlano.CodigoTabelaValorIntegral = FNTabelaValor.Codigo
                        LEFT JOIN BaseEducacional..FNDebitos AS FNDebitos ON vAluno.RM = FNDebitos.RM AND vRelacao.Ano = FNDebitos.Ano AND FNDebitos.Mes = 1 AND FNDebitos.Tipo = 'Matricula-Integral'
                    WHERE
                        vMatriculaRematricula.CodigoUnidade = 4 AND
                        vMatriculaRematricula.Codigo = @CodigoMatriculaRematricula AND
                        vMatriculaRematricula.Ano = YEAR(GETDATE()) AND
                        vMatriculaRematricula.DataHoraMatriculou IS NOT NULL AND
                        vAluno.RM NOT IN (SELECT RM FROM BaseEducacional..FNDebitos WHERE Mes = 1 AND Ano = YEAR(GETDATE()) AND WebAdm.Dbo.fnRetornaRMAjustado(RM) < 30000 AND Tipo = 'Matricula-Integral')
    ```
