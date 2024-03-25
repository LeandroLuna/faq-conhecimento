# Ativação do vestibular benefícios 🎁

Para notificar os estudantes sobre os benefícios de desconto do vestibular, o time do marketing solicita algumas bases de dados para mailing que podem ser geradas a partir dos modelos abaixo:

### Base 1: inscritos não pagos no PS1, PS2 e PS3-2024

```sql
use civ

SELECT * FROM 
(SELECT
		ISNULL(Vestibulando.NomeSocial, Vestibulando.Nome) AS 'Nome',
		Vestibulando.Email,
		CASE WHEN Vestibulando.TelCelular IS NOT NULL THEN CONCAT('55', Vestibulando.DDDTelCelular, RIGHT(CONCAT('999999999', Vestibulando.TelCelular), 9)) ELSE NULL END AS 'Celular',
		Boleto.DataPagamento,
		Processo.AnoProcesso,
		Processo.NumeroProcesso,
		ROW_NUMBER() OVER (PARTITION BY ProcessoVestibulando.CodVestibulando ORDER BY Processo.AnoProcesso DESC, Processo.NumeroProcesso DESC) AS 'Ordem'
	FROM
		ProcessoVestibulando
		INNER JOIN Processo ON
			ProcessoVestibulando.CodProcesso = Processo.codprocesso
		INNER JOIN Boleto ON
			ProcessoVestibulando.CodProcessoVestibulando = Boleto.CodProcessoVestibulando
		INNER JOIN Vestibulando ON
			ProcessoVestibulando.CodVestibulando = Vestibulando.CodVestibulando
	WHERE
		Processo.AnoProcesso = 2024 -- O ano pode ser alterado aqui
		AND Processo.NumeroProcesso IN (1,2,3) -- Os processos podem ser alterados aqui
		AND Vestibulando.email IS NOT NULL
		AND Vestibulando.Nome NOT LIKE '%teste%'
		AND Boleto.DataPagamento IS NULL -- Boleto não pago
		AND NOT EXISTS(SELECT * FROM ProcessoVestibulando AS ProcessoVestibulando2 WHERE ProcessoVestibulando2.CodProcesso = 61 AND ProcessoVestibulando2.CodVestibulando = ProcessoVestibulando.CodVestibulando) -- Verifica se a pessoa não está no processo atual (nesse caso, PS4 de 2024)
		AND ProcessoVestibulando.CodVestibulando NOT IN (SELECT CodVestibulando FROM Educacional..CPTVEST WHERE CodigoMatriculaRematricula IS NOT NULL)) AS Tabela -- Verifica se a pessoa não está matriculada em alguma graduação
WHERE
	Tabela.Ordem = 1
```


### Base 2: inscritos pagos no PS1 e PS2-2024

```sql

use civ
SELECT * FROM 
(SELECT
		ISNULL(Vestibulando.NomeSocial, Vestibulando.Nome) AS 'Nome',
		Vestibulando.Email,
		CASE WHEN Vestibulando.TelCelular IS NOT NULL THEN CONCAT('55', Vestibulando.DDDTelCelular, RIGHT(CONCAT('999999999', Vestibulando.TelCelular), 9)) ELSE NULL END AS 'Celular',
		Processo.AnoProcesso,
		Processo.NumeroProcesso,
		ROW_NUMBER() OVER (PARTITION BY ProcessoVestibulando.CodVestibulando ORDER BY Processo.AnoProcesso DESC, Processo.NumeroProcesso DESC) AS 'Ordem'
FROM ProcessoVestibulando
INNER JOIN Processo ON
	ProcessoVestibulando.CodProcesso = Processo.codprocesso
INNER JOIN Boleto ON
	ProcessoVestibulando.CodProcessoVestibulando = Boleto.CodProcessoVestibulando
INNER JOIN Vestibulando ON
	ProcessoVestibulando.CodVestibulando = Vestibulando.CodVestibulando
WHERE Processo.AnoProcesso = 2024
	  AND Processo.NumeroProcesso IN (1,2)
	  AND Boleto.DataPagamento IS NOT NULL -- Boleto pago
	  AND Vestibulando.Nome NOT LIKE '%teste%'
	  AND NOT EXISTS(SELECT * FROM ProcessoVestibulando AS ProcessoVestibulando2 WHERE ProcessoVestibulando2.CodProcesso = 61 AND ProcessoVestibulando2.CodVestibulando = ProcessoVestibulando.CodVestibulando)
	  AND ProcessoVestibulando.CodVestibulando NOT IN (SELECT CodVestibulando FROM Educacional..CPTVEST WHERE CodigoMatriculaRematricula IS NOT NULL)) AS Tabela
WHERE
	Tabela.Ordem = 1

```


### Base 3: Ausentes no PS3-2024

```sql

use civ

SELECT
    ISNULL(Vestibulando.NomeSocial, Vestibulando.Nome) AS 'Nome',
    Vestibulando.email,
    -- ProcessoVestibulando.Chave,
    CASE WHEN Vestibulando.TelCelular IS NOT NULL THEN CONCAT('55', Vestibulando.DDDTelCelular, RIGHT(CONCAT('999999999', Vestibulando.TelCelular), 9)) ELSE NULL END AS 'Celular'
    -- Curso.Descricao,
    -- Unidade_Curso.Unidade
FROM
    Processo
    INNER JOIN ProcessoVestibulando ON
        processo.codprocesso = ProcessoVestibulando.CodProcesso
    INNER JOIN Boleto ON
        ProcessoVestibulando.CodProcessoVestibulando = Boleto.CodProcessoVestibulando
    INNER JOIN Vestibulando ON
        ProcessoVestibulando.CodVestibulando = Vestibulando.CodVestibulando
    LEFT JOIN Opcao ON
        ProcessoVestibulando.CodProcessoVestibulando = Opcao.CodProcessoVestibulando
        AND Opcao.NumeroOpcao = 1
    LEFT JOIN Unidade_Curso ON
        Opcao.CodUnidadeCurso = Unidade_Curso.CodUnidadeCurso
    LEFT JOIN Curso ON
        Unidade_Curso.CodCurso = Curso.CodCurso
WHERE
    Processo.AnoProcesso = 2024 -- O ano pode ser alterado aqui
    AND Processo.NumeroProcesso = 3 -- Os processos podem ser alterados aqui
    AND Boleto.DataPagamento IS NOT NULL -- Boleto pago
    AND ProcessoVestibulando.CodStatus = 5 -- Não fez prova
    AND ProcessoVestibulando.CodVestibulando NOT IN (SELECT CodVestibulando FROM ProcessoVestibulando WHERE CodProcesso= 61) -- Vestibulando não pode estar no PS4 de 2024
	AND Vestibulando.Nome NOT LIKE '%teste%'
	AND ProcessoVestibulando.CodVestibulando NOT IN (SELECT CodVestibulando FROM Educacional..CPTVEST WHERE CodigoMatriculaRematricula IS NOT NULL)  -- Verifica se a pessoa não está matriculada em alguma graduação
ORDER BY
    Vestibulando.Nome
```




