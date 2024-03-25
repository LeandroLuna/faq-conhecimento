# Ex-alunos

## Ex-alunos de Graduação

A consulta abaixo retorna os ex-alunos e se se formaram ou apenas saíram da faculdade.

**OBS:** Alterar o ano no momento da execução

```sql
USE Educacional;

SELECT 
    vPessoa.Nome,
    vPessoa.Email,
    vAluno.RM,
    CASE WHEN EXISTS(SELECT * FROM site_fiap..Formandos AS Formandos WHERE Formandos.RM = vAluno.RM ) THEN 1 ELSE 0 END AS 'Formando'
FROM vPessoa
INNER JOIN vAluno
    ON vPessoa.Codigo = vAluno.CodigoPessoa
INNER JOIN vAlunoTurma
    ON vAluno.Codigo = vAlunoTurma.CodigoAluno
INNER JOIN vRelacao
    ON vAlunoTurma.CodigoRelacao = vRelacao.Codigo
INNER JOIN vCurso
    ON vRelacao.CodigoCurso = vCurso.Codigo
WHERE vAluno.CodigoUnidade = 1
    AND vRelacao.CodigoUnidade = 1
    AND vRelacao.Ano <= 2019
    AND vAlunoTurma.CodigoTipoStatus IN (1, 23)
    AND vAluno.RM NOT IN (
        SELECT             
            vAluno.RM
        FROM vPessoa
        INNER JOIN vAluno
            ON vPessoa.Codigo = vAluno.CodigoPessoa
        INNER JOIN vAlunoTurma
            ON vAluno.Codigo = vAlunoTurma.CodigoAluno
        INNER JOIN vRelacao
            ON vAlunoTurma.CodigoRelacao = vRelacao.Codigo
        INNER JOIN vCurso
            ON vRelacao.CodigoCurso = vCurso.Codigo
        WHERE vAluno.CodigoUnidade = 1
            AND vRelacao.CodigoUnidade = 1
            AND vRelacao.Ano = 2020
            AND vAlunoTurma.CodigoTipoStatus IN (1, 23)            
    )
    AND vPessoa.Email <> 'naotememail@fiap.com.br'    
GROUP BY
    vPessoa.Nome,
    vPessoa.Email,
    vAluno.Rm
ORDER BY vPessoa.Nome;
```


## Ex-alunos de MBA

A consulta abaixo retorna os ex-alunos de MBA.

**OBS:** Alterar o ano no momento da execução

```sql
USE webadm;

SELECT 
    pos_inscricao_contrato.rm,
    pos_inscricao_new.nome,
    pos_inscricao_new.email
FROM pos_inscricao_contrato
INNER JOIN PI_InscricaoProcesso
    ON pos_inscricao_contrato.codigoInscricaoProcesso = PI_InscricaoProcesso.codigo
INNER JOIN pos_inscricao_new
    ON pos_inscricao_contrato.codigoInscricao = pos_inscricao_new.codigo
INNER JOIN pos_inscricao_turmas
    ON pos_inscricao_contrato.turma = pos_inscricao_turmas.Turma
INNER JOIN PI_Processo
    ON pos_inscricao_turmas.codigoProcesso = PI_Processo.codigo
WHERE CONVERT(DATE, CASE WHEN LEN(pos_inscricao_turmas.mesAnoTermino) = 7 THEN '28/' ELSE '' END + pos_inscricao_turmas.mesAnoTermino, 103) < CONVERT(DATE, GETDATE())
    AND pos_inscricao_turmas.Liberado = 1
    AND (pos_inscricao_contrato.empresa IS NULL OR pos_inscricao_contrato.empresa = 0)
    AND pos_inscricao_new.email <> 'a@gmail.com'
ORDER BY pos_inscricao_new.nome;
```