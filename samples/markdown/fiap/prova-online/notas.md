# Notas

As notas são calculadas automaticamente enquanto o aluno realiza a prova, e são processadas e publicadas pelo Helpdesk quando o departamento do EAD liberar.

## Cálcular notas novamente

Caso uma questão seja anulada, é necessário o re-cálculo da mesma, que pode ser feito utilizando o script abaixo, adequando-o ao código da questão que foi anulada.

???+ note "recalcular-notas.sql"
    ```sql
    USE site_fiap
    GO
    DECLARE @CodigoQuestao INT
    DECLARE Ponteiro CURSOR FOR SELECT Codigo FROM POQuestao WHERE POQuestao.Anulada = 1
    OPEN Ponteiro
    FETCH NEXT FROM Ponteiro INTO @CodigoQuestao
    WHILE @@FETCH_STATUS = 0
    BEGIN

        UPDATE
            POProvaAluno
        SET
            POProvaAluno.Nota = Tabela.NotaProva,
            POProvaAluno.Publicado = 0
        FROM
            (SELECT
                Tabela.Codigo,
                ROUND(SUM(CASE WHEN Tabela.Anulada = 1 THEN
                    CASE WHEN Tabela.PrimeiraAlternativa = 1 THEN
                        Tabela.NotaPorPergunta
                    ELSE
                        0
                    END
                ELSE
                    CASE WHEN Tabela.Selecionada = 1 AND Tabela.Correta = 1 THEN
                        Tabela.NotaPorCorreta
                    ELSE
                        0
                    END
                END), 1) AS 'NotaProva'
            FROM
                (SELECT
                    CONVERT(FLOAT, Tabela.QtdMaximoPonto) / Tabela.QtPerguntas AS 'NotaPorPergunta',
                    (CONVERT(FLOAT, Tabela.QtdMaximoPonto) / Tabela.QtPerguntas) / Tabela.QTCorretas AS 'NotaPorCorreta',
                    *
                FROM
                    (SELECT
                        SUM(Tabela.QTPerguntas) OVER (PARTITION BY Tabela.Codigo ORDER BY Tabela.Codigo) AS 'QTPerguntas',
                        Tabela.QTPerguntas AS 'PrimeiraAlternativa',
                        SUM(CONVERT(INT, Tabela.Correta)) OVER (PARTITION BY Tabela.Codigo, Tabela.CodigoQuestao ORDER BY Tabela.CodigoQuestao) AS 'QTCorretas',
                        Tabela.Codigo,
                        Tabela.CodigoQuestao,
                        Tabela.QtdMaximoPonto,
                        Tabela.Anulada,
                        Tabela.Selecionada,
                        Tabela.Correta
                    FROM
                        (SELECT
                            CASE WHEN ROW_NUMBER() OVER (PARTITION BY POProvaAluno.Codigo, POProvaAlunoQuestao.CodigoQuestao ORDER BY POProvaAlunoQuestao.CodigoQuestao) = 1 THEN 1 ELSE 0 END AS 'QTPerguntas',
                            POProvaAluno.Codigo,
                            POProvaAlunoQuestao.CodigoQuestao,
                            POProva.QtdMaximoPonto,
                            POQuestao.Anulada,
                            POProvaAlunoAlternativa.Selecionada,
                            POQuestaoAlternativa.Correta
                        FROM
                            POProvaAluno
                            INNER JOIN POProva ON POProvaAluno.CodigoProva = POProva.Codigo
                            INNER JOIN POProvaAlunoQuestao ON POProvaAluno.Codigo = POProvaAlunoQuestao.CodigoProvaAluno
                            INNER JOIN POQuestao ON POProvaAlunoQuestao.CodigoQuestao = POQuestao.Codigo
                            INNER JOIN POProvaAlunoAlternativa ON POProvaAlunoQuestao.Codigo = POProvaAlunoAlternativa.CodigoProvaAlunoQuestao
                            INNER JOIN POQuestaoAlternativa ON POProvaAlunoAlternativa.CodigoProvaQuestaoAlternativa = POQuestaoAlternativa.Codigo
                        WHERE
                            POProvaAluno.Codigo IN (SELECT POProvaAlunoQuestao.COdigoProvaAluno FROM POProvaAlunoQuestao WHERE POProvaAlunoQuestao.CodigoQuestao = @CodigoQuestao)) AS Tabela) AS Tabela) AS Tabela
            GROUP BY
                Tabela.Codigo) AS Tabela
        WHERE
            POProvaAluno.Codigo = Tabela.Codigo
        
        FETCH NEXT FROM Ponteiro INTO @CodigoQuestao
    END
    CLOSE Ponteiro
    DEALLOCATE Ponteiro
    ```