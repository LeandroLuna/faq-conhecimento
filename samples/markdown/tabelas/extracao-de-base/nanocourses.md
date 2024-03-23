#Nano Courses

## Alunos que ainda não completaram 20 créditos em nanocourses no ano letivo

OBS: Lembrar de trocar o ano na SELECT abaixo.

```sql
SELECT
	LancamentoNotasFiap.RM,
	LancamentoNotasFiap.Turma,
	vPessoa.Nome,
	RIGHT('11' + RTRIM(LTRIM(REPLACE(REPLACE(REPLACE(vPessoa.Celular, '(', ''), ')', ''), ' ', ''))), 11)
FROM
	Educacional..LancamentoNotasFiap AS LancamentoNotasFiap WITH (NOLOCK)
	INNER JOIN Site_Fiap..Relacao_2004 AS Relacao_2004 WITH (NOLOCK) ON
		LancamentoNotasFiap.CodRelacao = Relacao_2004.Codigo
	INNER JOIN Educacional..vAluno AS vAluno ON
		LancamentoNotasFiap.RM = vAluno.RM
	INNER JOIN Educacional..vPessoa AS vPessoa ON
		vAluno.CodigoPessoa = vPessoa.Codigo
WHERE
	LancamentoNotasFiap.Ano = 2020
	AND Relacao_2004.AgrupadorNanoCourse = 1
	AND Relacao_2004.Ativo = 1
	AND LancamentoNotasFiap.Cond = 'A'
	AND LancamentoNotasFiap.dispensado = 0
	AND (
			LancamentoNotasFiap.DP = 0
			OR (
					LancamentoNotasFiap.DP = 1
					AND LancamentoNotasFiap.cursandoDp = 1
				)
		)
	AND LancamentoNotasFiap.M1 IS NULL
	AND vPessoa.Celular IS NOT NULL
	AND LEN(RIGHT('11' + RTRIM(LTRIM(REPLACE(REPLACE(REPLACE(vPessoa.Celular, '(', ''), ')', ''), ' ', ''))), 11)) = 11
	AND ISNUMERIC(RIGHT('11' + RTRIM(LTRIM(REPLACE(REPLACE(REPLACE(vPessoa.Celular, '(', ''), ')', ''), ' ', ''))), 11)) = 1
```