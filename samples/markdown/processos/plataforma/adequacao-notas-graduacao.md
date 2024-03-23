# Adequação de notas para graduação

Quando um aluno é transferido de uma turma presencial para on-line, as notas devem ser lançadas proporcionalmente para a nova turma.
Esse processo é necessário para que o aluno não seja prejudicado na turma on-line e que, caso tenha a média necessária, não perca um
possível benefício relacionado à Alura.

<div style="height: 410px; overflow-x:scroll;">
    <img src="../adequacao-notas-graduacao.svg" style="max-width: initial;">
</div>
<sup> Mapeado por <a href="https://teams.microsoft.com/l/chat/0/?users=vanessa.marques@fiap.com.br"> Vanessa Marques </a> </sup>

## Links

**Link para o job no Jenkins:**<br />
[FIAPON_CRON_NOTAS_ADEQUACAO_GRADUACAO_PRESENCIAL_PARA_ONLINE](http://jenkins.fiap.com.br/job/FIAPON/job/CRON/job/NOTAS/job/FIAPON_CRON_NOTAS_ADEQUACAO_GRADUACAO_PRESENCIAL_PARA_ONLINE/)
<br />(Mapear no hosts **192.168.60.68 jenkins.fiap.com.br** e acessar via VPN)

**Rota para retornar alunos:**<br />
https://apis.fiap.com.br/api-generica/v1/LancamentoNotasTransferenciaGraduacaoPresencialOnLine

## Comandos

Utilize a query abaixo para comparar a nota atribuída ao usuário com a porcentagem de cada coluna.

```sql
SET @porcentagemAD  = 0;
SET @porcentagemEP1 = 0;
SET @user_id        = 0;
SET @turma          = 'sigla_da_turma';
SET @ano            = 0;
SET @semestre       = 0;

SELECT
    fiapead_course_modules.id AS 'cmid',
    fiapead_grade_items.itemname AS 'Atividade',
    IFNULL(fiapead_fiap_assign_config.value, 'AD') AS 'Tipo',
    ROUND(fiapead_grade_items.grademax, 2) AS 'Nota Máxima',
    CASE WHEN fiapead_fiap_assign_config.value = 'global-solution-1' THEN @porcentagemEP1 ELSE @porcentagemAD END AS 'Porcentagem',
    ROUND(( CASE WHEN fiapead_fiap_assign_config.value = 'global-solution-1' THEN @porcentagemEP1 ELSE @porcentagemAD END / 100 * fiapead_grade_items.grademax ), 2) AS 'Nota Esperada',
    ROUND(fiapead_grade_grades.finalgrade, 2) AS 'Nota Atribuída'
FROM fiapead_course_categories_resume
INNER JOIN fiapead_course
    ON fiapead_course_categories_resume.categorieid = fiapead_course.category
INNER JOIN fiapead_course_modules
    ON fiapead_course.id = fiapead_course_modules.course
    AND fiapead_course_modules.module = 1
INNER JOIN fiapead_grade_items
    ON fiapead_course_modules.instance = fiapead_grade_items.iteminstance
    AND fiapead_grade_items.itemmodule = 'assign'
INNER JOIN fiapead_moodle_relacao2004_assign
    ON fiapead_grade_items.iteminstance = fiapead_moodle_relacao2004_assign.assignid
LEFT JOIN fiapead_fiap_assign_config
    ON fiapead_moodle_relacao2004_assign.assignid = fiapead_fiap_assign_config.assignid
    AND fiapead_fiap_assign_config.configname = 'type'
LEFT JOIN fiapead_grade_grades
    ON fiapead_grade_items.id = fiapead_grade_grades.itemid
    AND fiapead_grade_grades.userid = @user_id
WHERE fiapead_course_categories_resume.nivel3 = CONCAT(@ano, '/', @semestre)
    AND fiapead_course_categories_resume.nivel5 = @turma
    AND fiapead_course.fullname REGEXP 'Fase [1-4]'
    AND (
        fiapead_fiap_assign_config.id IS NULL
        OR fiapead_fiap_assign_config.value IN ('challenge', 'global-solution-1')
    )
GROUP BY
    fiapead_course_modules.id,
    fiapead_grade_items.itemname,
    fiapead_fiap_assign_config.value,
    fiapead_grade_items.grademax,
    fiapead_grade_grades.finalgrade
    
UNION

SELECT
    fiapead_course_modules.id AS 'cmid',
    fiapead_grade_items.itemname AS 'Atividade',
    IFNULL(fiapead_fiap_quiz_config.configname, 'AD') AS 'Tipo',
    ROUND(fiapead_grade_items.grademax, 2) AS 'Nota Máxima',
    @porcentagemAD AS 'Porcentagem',
    ROUND(( @porcentagemAD / 100 * fiapead_grade_items.grademax ), 2) AS 'Nota Esperada',
    ROUND(fiapead_grade_grades.finalgrade, 2) AS 'Nota Atribuída'
FROM fiapead_course_categories_resume
INNER JOIN fiapead_course
    ON fiapead_course_categories_resume.categorieid = fiapead_course.category
INNER JOIN fiapead_course_modules
    ON fiapead_course.id = fiapead_course_modules.course
    AND fiapead_course_modules.module = 17
INNER JOIN fiapead_grade_items
    ON fiapead_course_modules.instance = fiapead_grade_items.iteminstance
    AND fiapead_grade_items.itemmodule = 'quiz'
INNER JOIN fiapead_moodle_relacao2004_quiz
    ON fiapead_grade_items.iteminstance = fiapead_moodle_relacao2004_quiz.quizid
LEFT JOIN fiapead_fiap_quiz_config
    ON fiapead_moodle_relacao2004_quiz.quizid = fiapead_moodle_relacao2004_quiz.quizid
LEFT JOIN fiapead_grade_grades
    ON fiapead_grade_items.id = fiapead_grade_grades.itemid
    AND fiapead_grade_grades.userid = @user_id
WHERE fiapead_course_categories_resume.nivel3 = CONCAT(@ano, '/', @semestre)
    AND fiapead_course_categories_resume.nivel5 = @turma
    AND fiapead_course.fullname REGEXP 'Fase [1-4]'
    AND (
        fiapead_fiap_quiz_config.id IS NULL
        OR fiapead_fiap_quiz_config.configname = 'fast_test'
    )
GROUP BY
    fiapead_course_modules.id,
    fiapead_grade_items.itemname,
    fiapead_fiap_quiz_config.configname,
    fiapead_grade_items.grademax,
    fiapead_grade_grades.finalgrade
```
