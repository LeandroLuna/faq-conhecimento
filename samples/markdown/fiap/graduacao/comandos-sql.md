# Comandos SQL

Esta página é referente aos comandos SQL comuns para as coisas da Graduação

## Informações de um aluno (Pode ser adaptado para pegar uma turma inteira)

Query para buscar info de alunos ativos de graduação.

```sql
SELECT
    vPessoa.Nome,
    vPessoa.Email,
    vAluno.RM,
    vRelacao.Ano,
    vRelacao.Turma,
    vCurso.Descricao,
    vRelacao.EAD,
    vTipoStatus.Descricao AS 'Status'
FROM Educacional..vPessoa AS vPessoa
INNER JOIN Educacional..vAluno AS vAluno
    ON vPessoa.Codigo = vAluno.CodigoPessoa
INNER JOIN Educacional..vAlunoTurma AS vAlunoTurma
    ON vAluno.Codigo = vAlunoTurma.CodigoAluno
INNER JOIN Educacional..vRelacao AS vRelacao
    ON vAlunoTurma.CodigoRelacao = vRelacao.Codigo
INNER JOIN Educacional..vCurso AS vCurso
    ON vRelacao.CodigoCurso = vCurso.Codigo
INNER JOIN Educacional..vTipoStatus AS vTipoStatus
    ON vAlunoTurma.CodigoTipoStatus = vTipoStatus.Codigo
WHERE vAluno.CodigoUnidade = 1
    AND vRelacao.CodigoUnidade = 1
    AND vAluno.RM = {rm}
    AND vAlunoTurma.CodigoTipoStatus IN (1, 23)
```


**Palavras-chave:**  graduação, query, sql, informações de alunos, informação de aluno, consulta, busca de alunos
