# Extração de bases da intranet

### Base de e-mails dos responsáveis financeiros da FIAP School

Essa select retorna todos os e-mails dos responsáveis financeiros dos alunos da FIAP School.

```sql
SELECT
	vAluno.RM,
	vPessoaAluno.Nome,
	vRelacao.Ano,
	vRelacao.Turma,
	vCurso.Descricao AS 'Curso',
	vPessoaFinanceiro.Nome,
	vPessoaFinanceiro.Email
FROM
	Educacional..vAluno AS vAluno
	INNER JOIN Educacional..vAlunoTurma AS vAlunoTurma ON
		vAluno.Codigo = vAlunoTurma.CodigoAluno
	INNER JOIN Educacional..vRelacao AS vRelacao ON
		vAlunoTurma.CodigoRelacao = vRelacao.Codigo
	INNER JOIN Educacional..vCurso AS vCurso ON
		vRelacao.CodigoCurso = vCurso.Codigo
	INNER JOIN Educacional..vPessoa AS vPessoaAluno ON
		vAluno.CodigoPessoa = vPessoaAluno.Codigo
	INNER JOIN (SELECT
					vAlunoResponsavel.CodigoAluno,
					MAX(vAlunoResponsavel.AnoReferencia) AS 'AnoReferencia'
				FROM
					Educacional..vAlunoResponsavel AS vAlunoResponsavel
				GROUP BY
					vAlunoResponsavel.CodigoAluno) AS TabResp ON
		vAluno.Codigo = TabResp.CodigoAluno
	INNER JOIN Educacional..vAlunoResponsavel AS vAlunoResponsavel ON
		vAluno.Codigo = vAlunoResponsavel.CodigoAluno
		AND TabResp.AnoReferencia = vAlunoResponsavel.AnoReferencia
	INNER JOIN Educacional..vPessoa AS vPessoaFinanceiro ON
		vAlunoResponsavel.CodigoPessoaFinanceiro = vPessoaFinanceiro.Codigo
WHERE
	vAluno.CodigoUnidade = 4
	AND vRelacao.CodigoUnidade = 4
	AND vRelacao.Ano = YEAR(GETDATE())
	AND vAlunoTurma.CodigoTipoStatus IN (1, 23)
	AND vRelacao.Turma NOT LIKE '_EXT_'
	AND vPessoaFinanceiro.Email IS NOT NULL
ORDER BY
	vCurso.Descricao,
	vRelacao.Turma,
	vPessoaAluno.Nome
```

### Base de e-mails dos responsáveis financeiros da FIAP Graduação

Essa select retorna todos os e-mails dos responsáveis financeiros dos alunos da graduação.

```sql
SELECT
	vAluno.RM,
	vPessoaAluno.Nome,
	vRelacao.Ano,
	vRelacao.Turma,
	vCurso.Descricao AS 'Curso',
	vPessoaFinanceiro.Nome,
	vPessoaFinanceiro.Email
FROM
	Educacional..vAluno AS vAluno
	INNER JOIN Educacional..vAlunoTurma AS vAlunoTurma ON
		vAluno.Codigo = vAlunoTurma.CodigoAluno
	INNER JOIN Educacional..vRelacao AS vRelacao ON
		vAlunoTurma.CodigoRelacao = vRelacao.Codigo
	INNER JOIN Educacional..vCurso AS vCurso ON
		vRelacao.CodigoCurso = vCurso.Codigo
	INNER JOIN Educacional..vPessoa AS vPessoaAluno ON
		vAluno.CodigoPessoa = vPessoaAluno.Codigo
	INNER JOIN (SELECT
					vAlunoResponsavel.CodigoAluno,
					MAX(vAlunoResponsavel.AnoReferencia) AS 'AnoReferencia'
				FROM
					Educacional..vAlunoResponsavel AS vAlunoResponsavel
				GROUP BY
					vAlunoResponsavel.CodigoAluno) AS TabResp ON
		vAluno.Codigo = TabResp.CodigoAluno
	INNER JOIN Educacional..vAlunoResponsavel AS vAlunoResponsavel ON
		vAluno.Codigo = vAlunoResponsavel.CodigoAluno
		AND TabResp.AnoReferencia = vAlunoResponsavel.AnoReferencia
	INNER JOIN Educacional..vPessoa AS vPessoaFinanceiro ON
		vAlunoResponsavel.CodigoPessoaFinanceiro = vPessoaFinanceiro.Codigo
WHERE
	vAluno.CodigoUnidade = 1
	AND vRelacao.CodigoUnidade = 1
	AND vRelacao.Ano = YEAR(GETDATE())
	AND vAlunoTurma.CodigoTipoStatus IN (1, 23)
	AND vRelacao.Turma NOT LIKE '_EXT_'
	AND vPessoaFinanceiro.Email IS NOT NULL
ORDER BY
	vCurso.Descricao,
	vRelacao.Turma,
	vPessoaAluno.Nome
```

### Base de e-mails dos alunos ativos do MBA

Essa select retorna todos os e-mails dos alunos do MBA.

```sql
SELECT
	Pos_Inscricao_Contrato.RM,
	Pos_inscricao_New.Nome,
	Pos_inscricao_New.Email,
	PI_Processo.Ano,
	PI_Processo.semestre,
	Pos_Inscricao_Turmas.Turma,
	Pos_Inscricao_Turmas.nomeCurso
FROM
	webadm..Pos_Inscricao_Turmas AS Pos_Inscricao_Turmas
	INNER JOIN WebAdm..PI_Processo AS PI_Processo ON
		Pos_Inscricao_Turmas.codigoProcesso = PI_Processo.Codigo
	INNER JOIN WebAdm..Pos_Inscricao_Contrato AS Pos_Inscricao_Contrato ON
		Pos_Inscricao_Turmas.Turma = Pos_Inscricao_Contrato.Turma
	INNER JOIN WebAdm..Pos_Inscricao_New AS Pos_Inscricao_New ON
		Pos_Inscricao_Contrato.CodigoInscricao = Pos_inscricao_New.Codigo
WHERE
	Pos_Inscricao_Turmas.Liberado = 1
	AND CONVERT(DATE, GETDATE()) BETWEEN CONVERT(DATE, CASE WHEN LEN(Pos_Inscricao_Turmas.mesAnoInicio) = 7 THEN '01/' ELSE '' END + Pos_Inscricao_Turmas.mesAnoInicio, 103) AND CONVERT(DATE, CASE WHEN LEN(Pos_Inscricao_Turmas.mesAnoTermino) = 7 THEN '28/' ELSE '' END + Pos_Inscricao_Turmas.mesAnoTermino, 103)
	AND (
		Pos_Inscricao_Contrato.empresa = 0
		OR Pos_Inscricao_Contrato.empresa IS NULL
	)
ORDER BY
	Pos_Inscricao_Turmas.nomeCurso,
	PI_Processo.Ano,
	PI_Processo.semestre,
	Pos_Inscricao_Turmas.Turma,
	Pos_inscricao_New.Nome
```

### Base de e-mails dos responsáveis financeiros do Colégio Módulo

Essa select retorna todos os e-mails dos responsáveis financeiros dos alunos do Colégio Módulo.

```sql
SELECT
	vAluno.RM,
	vPessoaAluno.Nome,
	vRelacao.Ano,
	vRelacao.Turma,
	vCurso.Descricao AS 'Curso',
	vPessoaFinanceiro.Nome,
	vPessoaFinanceiro.Email
FROM
	Educacional..vAluno AS vAluno
	INNER JOIN Educacional..vAlunoTurma AS vAlunoTurma ON
		vAluno.Codigo = vAlunoTurma.CodigoAluno
	INNER JOIN Educacional..vRelacao AS vRelacao ON
		vAlunoTurma.CodigoRelacao = vRelacao.Codigo
	INNER JOIN Educacional..vCurso AS vCurso ON
		vRelacao.CodigoCurso = vCurso.Codigo
	INNER JOIN Educacional..vPessoa AS vPessoaAluno ON
		vAluno.CodigoPessoa = vPessoaAluno.Codigo
	INNER JOIN (SELECT
					vAlunoResponsavel.CodigoAluno,
					MAX(vAlunoResponsavel.AnoReferencia) AS 'AnoReferencia'
				FROM
					Educacional..vAlunoResponsavel AS vAlunoResponsavel
				GROUP BY
					vAlunoResponsavel.CodigoAluno) AS TabResp ON
		vAluno.Codigo = TabResp.CodigoAluno
	INNER JOIN Educacional..vAlunoResponsavel AS vAlunoResponsavel ON
		vAluno.Codigo = vAlunoResponsavel.CodigoAluno
		AND TabResp.AnoReferencia = vAlunoResponsavel.AnoReferencia
	INNER JOIN Educacional..vPessoa AS vPessoaFinanceiro ON
		vAlunoResponsavel.CodigoPessoaFinanceiro = vPessoaFinanceiro.Codigo
WHERE
	vAluno.CodigoUnidade = 5
	AND vRelacao.CodigoUnidade = 5
	AND vRelacao.Ano = YEAR(GETDATE())
	AND vAlunoTurma.CodigoTipoStatus IN (1, 23)
	AND vRelacao.Turma NOT LIKE '_EXT_'
	AND vPessoaFinanceiro.Email IS NOT NULL
ORDER BY
	vCurso.Descricao,
	vRelacao.Turma,
	vPessoaAluno.Nome
```