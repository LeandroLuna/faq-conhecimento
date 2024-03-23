# Comandos SQL

Esta página é referente aos comandos SQL comuns para as coisas da Pós Graduação.

## Informações de um aluno (Pode ser adaptado para pegar uma turma inteira)

Query para buscar info de alunos ativos de pós graduação.

```sql
SELECT 
    pos_inscricao_contrato.rm,
    pos_inscricao_new.nome,
    pos_inscricao_new.email,
    pos_inscricao_new.cidade,
    pos_inscricao_new.estado,
    pos_inscricao_contrato.turma,
    pos_inscricao_turmas.nomeCurso,
    pos_inscricao_turmas.EAD
FROM webadm..pos_inscricao_contrato AS pos_inscricao_contrato
INNER JOIN webadm..PI_InscricaoProcesso AS PI_InscricaoProcesso
    ON pos_inscricao_contrato.codigoInscricaoProcesso = PI_InscricaoProcesso.codigo
INNER JOIN webadm..pos_inscricao_new AS pos_inscricao_new
    ON pos_inscricao_contrato.codigoInscricao = pos_inscricao_new.codigo
INNER JOIN webadm..pos_inscricao_turmas AS pos_inscricao_turmas
    ON pos_inscricao_contrato.turma = pos_inscricao_turmas.Turma
INNER JOIN webadm..PI_Processo AS PI_Processo
    ON pos_inscricao_turmas.codigoProcesso = PI_Processo.codigo
WHERE pos_inscricao_contrato.rm = <Colocar o rm aqui>
ORDER BY pos_inscricao_contrato.turma, pos_inscricao_new.nome
```

**Palavras-chaves:** pós, mba, query, sql, informações de alunos, informação de aluno, consulta, pos_inscricao_contrato, pos_inscricao_new, pos_inscricao_turmas, busca de alunos

## Alteração de presença de aluno na Pós (Presencialmente ou On-line):

Caso o professor erre o tipo de chamada, para alterar o tipo da presença do aluno usar:

```sql
UPDATE site_fiap.dbo.ChamadaPosAluno
    SET TipoPresenca=N'O' -- Pode ser O ou P 
    WHERE CodigoChamada = <código da chamada aqui>
    AND ChamadaPosAluno.TipoPresenca IS NOT NULL;
```

## Colocar como aprovado o aluno que concluiu o PowerSkill:

```sql
/*Lista de Power Skills

(Inovação)
'Disruptive Innovation & Mindset'

(Empreendedorismo)
'Entrepreneurial Behavior & Growth Hacking', 'Power Skills Weekend: Entrepreneurial Behavior & Growth Hacking'

(Negócios)
'Exponential Business Development'

(Tecnologia)
'Leading Technology Transformation'
*/
USE Site_Fiap
GO
UPDATE
	PSTrilhaInscricao
SET
	Aprovado = 1
WHERE
	Codigo IN (SELECT 
					MAX(PSTrilhaInscricao.Codigo)
				FROM 
					PSTrilhaInscricao
					INNER JOIN PSTrilha ON
						PSTrilhaInscricao.CodigoPSTrilha = PSTrilha.Codigo
				WHERE
					PSTrilha.Titulo IN (/*Copiar aqui a linha (inteira com as aspas e virgulas) com o nome do(s) power(s) skill(s)*/)
					AND PSTrilhaInscricao.RM IN (/*Colocar aqui a lista de RM separada por virgula*/)
				GROUP BY
					PSTrilhaInscricao.RM)
	AND Aprovado = 0
```


## Informações da chamada de um aluno

```sql
SELECT 
    ChamadaPosAluno.RM,
    CASE ChamadaPosAluno.Presente 
        WHEN 0 THEN 'NÃO'
        ELSE 'SIM'
    END AS Presente,
    ChamadaPos.DataFinalizado,
    vRelacao_2004.disciplina,
    vRelacao_2004.professor,
    vRelacao_2004.nomeModulo,
    ChamadaPos.Horario
FROM ChamadaPosAluno
INNER JOIN ChamadaPos
    ON ChamadaPosAluno.CodigoChamada = ChamadaPos.Codigo
INNER JOIN vRelacao_2004
    ON ChamadaPos.CodigoRelacao = vRelacao_2004.codigoRelacao
WHERE ChamadaPosAluno.RM = <rm do aluno aqui>
    AND ChamadaPos.Finalizado = 1
    AND ChamadaPosAluno.Situacao = 'A'
ORDER BY ChamadaPos.DataFinalizado;
```
