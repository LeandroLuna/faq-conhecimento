# Comandos SQL

Esta página tem como finalidade separar consultas e comandos comuns no dia a dia do desenvolvimento
e manutenção do Moodle.

!!! warning "Cuidados importantes"
    Antes de executar em produção qualquer comando SQL desta página, o ideal é executar em
    um ambiente de testes para confirmar o resultado esperado!
    
    Para isto temos disponível em *192.168.60.11* um banco de homologação. 
    
    Acesse com seu usuário e senha para realizar os devidos testes.

## Alteração de senha

O login do moodle é realizado via plugins `manual` e `fiapldap`, 
no qual, somente o plugin manual armazena a senha na base de dados na tabela 
`fiapead_user` encriptado com o algoritmo `bcrypt`. 

Quando salvo a senha utilizando o algoritmo `MD5`, no primeiro acesso após a troca 
da senha, a hash será atualizada para formato bcrypt que é muito mais segura.  
 
```sql
UPDATE fiapead_user SET auth = 'manual', password = MD5('123456') WHERE ...
```

## Cursos em que o aluno está matriculado

Retorna todos os cursos em que o aluno está matriculado.

Colocar na condição **where** a lógica necessária para filtrar o aluno ou curso.

```sql
SELECT fiapead_course.* 
FROM fiapead_user
INNER JOIN fiapead_user_enrolments
  ON fiapead_user.id = fiapead_user_enrolments.userid
INNER JOIN fiapead_enrol
  ON fiapead_user_enrolments.enrolid = fiapead_enrol.id
INNER JOIN fiapead_course
  ON fiapead_enrol.courseid = fiapead_course.id
WHERE ...
```

## Migrar cursos de um usuário para outro

Muitas vezes acontecem casos de alunos que possuem vários cadastros (Ex: SHIFT e MBA)
e com isso é necessário migrar cursos e registros que o aluno possui em um cadastro
para o outro como forma de unificar os registros na base.

Para realizar isso, o script abaixo automatiza todo o processo. 

Basta substituir as variavéis necessárias. Geralmente nos informam qual é o usuário
de ambos os cadastros.

```sql
#
# Migra todos os cursos e itens relacionados de um usuário para outro usuário
#
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# ATENÇÃO!!!! Garantir que o usuário de destino não está inscrito em NENHUM curso
# do usuário de origem!!
#
# Caso esteja, comentar da linha 42 a 48 - O resto do script funciona normal
#
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
# @author Douglas Cabral <douglas.cabral@fiap.com.br>
#
#

#
# Username dos usuários passados por alguém
#
SET @de_username   = <username_aqui>;
SET @para_username = <username_aqui>;

#
# Variavéis para armazenar os ids dos usernames informados acima
#
SET @de_id   = 0;
SET @para_id = 0;

#
# Alimenta as variáveis de id
#
SELECT id INTO @de_id 
FROM fiapead_user
WHERE fiapead_user.username = @de_username;

SELECT id INTO @para_id
FROM fiapead_user
WHERE fiapead_user.username = @para_username;

#
# Altera a inscrição do curso
#
UPDATE fiapead_user_enrolments
SET fiapead_user_enrolments.userid = @para_id
WHERE fiapead_user_enrolments.userid = @de_id;

UPDATE fiapead_role_assignments 
SET fiapead_role_assignments.userid = @para_id
WHERE fiapead_role_assignments.userid = @de_id;


#
# Migra os assigns
#
UPDATE fiapead_assign_grades 
SET fiapead_assign_grades.userid = @para_id 
WHERE fiapead_assign_grades.userid = @de_id;

UPDATE fiapead_assign_submission
SET fiapead_assign_submission.userid = @para_id
WHERE fiapead_assign_submission.userid = @de_id;

UPDATE fiapead_assignment_submissions 
SET fiapead_assignment_submissions.userid = @para_id 
WHERE fiapead_assignment_submissions.userid = @de_id;


#
# Migra os grupos de atividades
#
UPDATE fiapead_groups_members
SET fiapead_groups_members.userid = @para_id
WHERE fiapead_groups_members.userid = @de_id;


#
# Migra o tempo nos áudios pelo usuário
#
UPDATE fiapead_conteudosaudio_user_tempo
SET fiapead_conteudosaudio_user_tempo.userid = @para_id
WHERE fiapead_conteudosaudio_user_tempo.userid = @de_id;

#
# Migra as leituras de conteúdos externos
#
UPDATE fiapead_conteudosexternos_leitura
SET fiapead_conteudosexternos_leitura.userid = @para_id
WHERE fiapead_conteudosexternos_leitura.userid = @de_id;

#
# Migra as leituras de conteúdos html
#
UPDATE fiapead_conteudoshtml_leitura_total
SET fiapead_conteudoshtml_leitura_total.user = @para_id
WHERE fiapead_conteudoshtml_leitura_total.user = @de_id;

UPDATE fiapead_conteudoshtml_user_tempo
SET fiapead_conteudoshtml_user_tempo.userid = @para_id
WHERE fiapead_conteudoshtml_user_tempo.userid = @de_id;


#
# Migra as leituras de conteúdos pdf
#
UPDATE fiapead_conteudospdf_user_tempo
SET fiapead_conteudospdf_user_tempo.userid = @para_id
WHERE fiapead_conteudospdf_user_tempo.userid = @de_id;


#
# Migra as leituras de conteúdos vídeo
#
UPDATE fiapead_conteudosvideo_user_tempo
SET fiapead_conteudosvideo_user_tempo.userid = @para_id
WHERE fiapead_conteudosvideo_user_tempo.userid = @de_id;


#
# Migra os logs de controle de visualização
#
UPDATE fiapead_fiap_controle_visualizacao
SET fiapead_fiap_controle_visualizacao.userid = @para_id
WHERE fiapead_fiap_controle_visualizacao.userid = @de_id;


#
# Migra os logs de cron
#
UPDATE fiapead_fiapcron 
SET fiapead_fiapcron.userid = @para_id
WHERE fiapead_fiapcron.userid = @de_id;


#
# Migra as pesquisas (Survey)
#
UPDATE fiapead_fiap_survey_user
SET fiapead_fiap_survey_user.userid = @para_id
WHERE fiapead_fiap_survey_user.userid = @de_id;


#
# Migra os posts do fórum
#
UPDATE fiapead_forum_discussions
SET fiapead_forum_discussions.userid = @para_id
WHERE fiapead_forum_discussions.userid = @de_id;

UPDATE fiapead_forum_discussion_subs
SET fiapead_forum_discussion_subs.userid = @para_id
WHERE fiapead_forum_discussion_subs.userid = @de_id;

UPDATE fiapead_forum_posts
SET fiapead_forum_posts.userid = @para_id
WHERE fiapead_forum_posts.userid = @de_id;

UPDATE fiapead_forum_read
SET fiapead_forum_read.userid = @para_id
WHERE fiapead_forum_read.userid = @de_id;

UPDATE fiapead_forum_subscriptions
SET fiapead_forum_subscriptions.userid = @para_id
WHERE fiapead_forum_subscriptions.userid = @de_id;

UPDATE fiapead_forum_votos
SET fiapead_forum_votos.userid = @para_id
WHERE fiapead_forum_votos.userid = @de_id;


#
# Migração de pontuação do gamification
#
UPDATE fiapead_gamification_pontuacao
SET fiapead_gamification_pontuacao.userid = @para_id
WHERE fiapead_gamification_pontuacao.userid = @de_id;


#
# Migração das notas
#
UPDATE fiapead_grade_grades
SET fiapead_grade_grades.userid = @para_id
WHERE fiapead_grade_grades.userid = @de_id;

UPDATE fiapead_grade_grades_history
SET fiapead_grade_grades_history.userid = @para_id
WHERE fiapead_grade_grades_history.userid = @de_id;


#
# Migração de informativos
#
UPDATE fiapead_informativos_cliques
SET fiapead_informativos_cliques.user = @para_id
WHERE fiapead_informativos_cliques.user = @de_id;

UPDATE fiapead_informativos_leitura
SET fiapead_informativos_leitura.user = @para_id
WHERE fiapead_informativos_leitura.user = @de_id;

UPDATE fiapead_informativos_user
SET fiapead_informativos_user.user = @para_id
WHERE fiapead_informativos_user.user = @de_id;


#
# Migração da pesquisa
#
UPDATE fiapead_pesquisas_respostas
SET fiapead_pesquisas_respostas.idusuario = @para_id
WHERE fiapead_pesquisas_respostas.idusuario = @de_id;


#
# Migração das questões
#
UPDATE fiapead_question_attempt_steps
SET fiapead_question_attempt_steps.userid = @para_id
WHERE fiapead_question_attempt_steps.userid = @de_id;


#
# Migração do quiz
#
UPDATE fiapead_quiz_attempts 
SET fiapead_quiz_attempts.userid = @para_id
WHERE fiapead_quiz_attempts.userid = @de_id;


UPDATE fiapead_quiz_grades
SET fiapead_quiz_grades.userid = @para_id
WHERE fiapead_quiz_grades.userid = @de_id;
```


## Gerar 'resume' de categorias e cursos

A tabela `fiapead_course_categories_resume` é uma tabela resumo que contém os breadcrumbs e níveis
de categorias para o Moodle de forma organizada e simples.

Ao gerenciar um curso ou categoria via admin, informações para esta tabela são geradas automaticamente via triggers, 
porém se necessário forçar a criação do 'resume' basta rodar os comandos abaixos:

```sql
SET max_sp_recursion_depth = 255;
DELETE FROM fiapead_course_categories_resume;
CALL sp_popula_fiapead_course_categories_resume(0);
```

## Inserir usuários numéricos para testes

Para testes de performance são utilizados usuários numéricos para login e navegação nos conteúdos.

**Exemplo:**
``` 
usuário: 256
senha: x 
```

Caso seja necessário criar novos usuários basta rodar o script SQL abaixo, informando o número inicial,
número final e curso no qual o usuário será inserido:

```sql
##################################################################################
# Substituir as variavéis abaixo pelas desejadas

SET @usuario_inicial = 1;
SET @usuario_final = 3000;
SET @curso_id = 525;

##################################################################################
# As variáveis abaixo serão inicializadas dinâmicamente

SET @curso_enrol_id = 0;
SET @curso_contexto_id = 0;


INSERT INTO fiapead_user 
(auth, confirmed, mnethostid, username, password, firstname, lastname, email, lang, calendartype, timezone) 
SELECT * FROM (
	SELECT 'manual', 1 AS confirmed, 1 AS mnethostid, @rownum := @rownum + 1 AS username, MD5('x'), 'teste', 'fiap', CONCAT(@rownum, '@fiap.com.br'), 'pt_br', 'gregorian', 99
	FROM (SELECT @rownum := 0) r INNER JOIN fiapead_user
	WHERE @rownum < @usuario_final) AS tbl
WHERE tbl.username >= @usuario_inicial;

SELECT fiapead_context.id INTO @curso_contexto_id
FROM fiapead_context
INNER JOIN fiapead_course
ON fiapead_context.contextlevel = 50 AND fiapead_context.instanceid = fiapead_course.id
INNER JOIN fiapead_enrol
ON fiapead_course.id = fiapead_enrol.courseid
WHERE fiapead_course.id = @curso_id;

SELECT fiapead_enrol.id INTO @curso_enrol_id
FROM fiapead_context
INNER JOIN fiapead_course
ON fiapead_context.contextlevel = 50 AND fiapead_context.instanceid = fiapead_course.id
INNER JOIN fiapead_enrol
ON fiapead_course.id = fiapead_enrol.courseid
WHERE fiapead_course.id = @curso_id;

INSERT INTO fiapead_user_enrolments (enrolid, userid, timestart, timeend, modifierid, timecreated)
SELECT @curso_enrol_id, id, UNIX_TIMESTAMP() - 1000, 0, 93, UNIX_TIMESTAMP()
FROM fiapead_user 
WHERE username BETWEEN @usuario_inicial AND @usuario_final AND firstname = 'teste' AND lastname = 'fiap';

INSERT INTO fiapead_role_assignments (roleid, contextid, userid)
SELECT 5, @curso_contexto_id, fiapead_user.id
FROM fiapead_user 
WHERE username BETWEEN @usuario_inicial AND @usuario_final AND firstname = 'teste' AND lastname = 'fiap';
```

## Apenas usuários de professores

A select abaixo seleciona apenas os usuários que são professores de algum curso dentro da plataforma.

```sql
SELECT fiapead_user.*
FROM fiapead_user
INNER JOIN fiapead_role_assignments ON fiapead_user.id = fiapead_role_assignments.userid
INNER JOIN fiapead_role ON fiapead_role_assignments.roleid = fiapead_role.id
WHERE archetype = 'editingteacher' AND suspended = 0
GROUP BY fiapead_user.email
ORDER BY username
```

## Usuários de teste, colaboradores e professores

A consulta abaixo extrai todos os usuários que são para testes na plataforma.
(teste, colaboradores e usuários de professores)

```sql
SELECT 
	 fiapead_user.id, 
    fiapead_user.deleted, 
    fiapead_user.suspended, 
    fiapead_user.username, 
    fiapead_user.firstname, 
    fiapead_user.lastname, 
    fiapead_user.email 
FROM fiapead_user 
LEFT JOIN fiapead_role_assignments
ON fiapead_user.id = fiapead_role_assignments.userid AND fiapead_role_assignments.roleid NOT IN (5, 6, 7, 8)
WHERE 
	username LIKE '%aluno%' 
    OR username LIKE '%teste%' 
    OR lastname LIKE '%teste%' 
    OR username REGEXP '^([0-9]{1,4})$' 
    OR (
		email LIKE '%@fiap.com.br'
		AND email NOT REGEXP '^rm([0-9]+)\@fiap\.com\.br$'
        AND username NOT REGEXP '^rm([0-9]{5,6})$'
        AND username NOT REGEXP '([0-9]{11})'
	)
    OR fiapead_role_assignments.id IS NOT NULL
GROUP BY fiapead_user.id;
```

## Inserir o usuário em um curso de cada regra (modalidade de curso)

Os cursos são categorizados por regras (Ex: Graduação Presencial, Graduação Online, MBA Presencial, etc...).

Para ambiente de teste, muitas vezes é necessário que um determinado usuário esteja em pelo menos um curso 
de cada regra, facilitando assim, a visualização da listagem dos conteúdos para cada modalidade de curso.

Basta alterar a variável `@userid` no SQL abaixo e executar o script inteiro:

!!! danger "Atenção"
    Os cursos no qual o usuário já esteja matriculado serão removidos!

```sql
##########################################################################################
# Alterar as variáveis abaixo para o id do usuário desejado

SET @userid = 123456789;

##########################################################################################

DELETE FROM fiapead_role_assignments WHERE userid = @userid;
DELETE FROM fiapead_user_enrolments WHERE userid = @userid;

INSERT INTO fiapead_role_assignments (roleid, contextid, userid, timemodified, modifierid) 
SELECT 5, fiapead_context.id, @userid, UNIX_TIMESTAMP(), 93 FROM fiapead_course
INNER JOIN fiapead_fiap_regras_course ON fiapead_course.id = fiapead_fiap_regras_course.courseid
INNER JOIN fiapead_enrol ON fiapead_course.id = fiapead_enrol.courseid
INNER JOIN fiapead_context ON fiapead_context.contextlevel = 50 AND fiapead_enrol.courseid = fiapead_context.instanceid
WHERE 
	fiapead_fiap_regras_course.regraid <= 8 
	AND fiapead_course.visible = 1 
    AND fiapead_course.timecreated >= UNIX_TIMESTAMP() - (60 * 60 * 24 * 365)
GROUP BY fiapead_fiap_regras_course.regraid;

INSERT INTO fiapead_user_enrolments (enrolid, userid, timestart, modifierid, timecreated)
SELECT fiapead_enrol.id, @userid, UNIX_TIMESTAMP(), 93, UNIX_TIMESTAMP() FROM fiapead_course
INNER JOIN fiapead_fiap_regras_course ON fiapead_course.id = fiapead_fiap_regras_course.courseid
INNER JOIN fiapead_enrol ON fiapead_course.id = fiapead_enrol.courseid
WHERE 
	fiapead_fiap_regras_course.regraid <= 8 
    AND fiapead_course.visible = 1 
    AND fiapead_course.timecreated >= UNIX_TIMESTAMP() - (60 * 60 * 24 * 365)
GROUP BY fiapead_fiap_regras_course.regraid;
```


## Selecionar alunos aleatórios de uma determinada regra (modalidade de curso)

A SELECT abaixo permite encontrar alunos de determinada modalidade de curso de forma aleatória.

Ideal para testes na plataforma.

```sql
##########################################################################################
# Alterar a variável abaixo para a regra desejada

SET @regraid = 1;

##########################################################################################

SELECT 
  fiapead_user.id, 
  fiapead_user.username,
  fiapead_user.firstname,
  fiapead_user.lastname,
  fiapead_user.email,
  fiapead_course.category,
  fiapead_course_categories_resume.breadcrumb,
  fiapead_fiap_regras.regra
FROM fiapead_user
INNER JOIN fiapead_user_enrolments
  ON fiapead_user.id = fiapead_user_enrolments.userid
INNER JOIN fiapead_enrol
  ON fiapead_user_enrolments.enrolid = fiapead_enrol.id
INNER JOIN fiapead_course
  ON fiapead_enrol.courseid = fiapead_course.id
INNER JOIN fiapead_fiap_regras_course
  ON fiapead_course.id = fiapead_fiap_regras_course.courseid
INNER JOIN fiapead_fiap_regras
  ON fiapead_fiap_regras_course.regraid = fiapead_fiap_regras.id
INNER JOIN fiapead_course_categories_resume
  ON fiapead_course.category = fiapead_course_categories_resume.categorieid
WHERE (username REGEXP '^([0-9]+)$' OR username REGEXP '^rm([0-9]{5,})$') 
AND email NOT LIKE '%fiap.com.br'
AND fiapead_fiap_regras_course.regraid = @regraid
ORDER BY RAND()
LIMIT 3
```

## Comparação de notas de assign (Entrega de arquivos)

Raramente pode haver atividades que foram canceladas ou possuem uma nova versão,
no qual, apenas a maior nota será considerada.

O script SQL abaixo compara as notas das duas atividades do tipo assign (Entrega de arquivos) 
e exibe a maior nota. 

Alterar as variáveis `@C1` e `@C2` para os IDs dos registros desejados da tabela `fiapead_course_module`. 

```sql
##########################################################################################
# Alterar a variável abaixo para a regra desejada
SET @C1 = 14643;
SET @C2 = 16344;

##########################################################################################

SELECT 
    users_in_course.username,
	IF (IFNULL(nota1.finalgrade, -1) > IFNULL(nota2.finalgrade, -1), nota1.assignid, nota2.assignid) AS assignid, 
    IF (IFNULL(nota1.finalgrade, -1) > IFNULL(nota2.finalgrade, -1), nota1.codrelacao, nota2.codrelacao) AS codrelacao, 
    IF (IFNULL(nota1.finalgrade, -1) > IFNULL(nota2.finalgrade, -1), nota1.finalgrade, nota2.finalgrade) AS finalgrade
FROM 
(
	SELECT fiapead_user.* 
	FROM fiapead_user
	INNER JOIN fiapead_user_enrolments
		ON fiapead_user.id = fiapead_user_enrolments.userid
	INNER JOIN fiapead_enrol
		ON fiapead_user_enrolments.enrolid = fiapead_enrol.id
	INNER JOIN fiapead_course_modules
		ON fiapead_enrol.courseid = fiapead_course_modules.course 
	WHERE 
		fiapead_course_modules.id = @C1
		AND fiapead_user.username REGEXP '^rm([0-9]{5,})'
) AS users_in_course
LEFT JOIN 
(
	SELECT 
		fiapead_user.id AS userid,
		fiapead_moodle_relacao2004_assign.assignid,
		fiapead_moodle_relacao2004_assign.codrelacao,
		fiapead_user.username,
		fiapead_grade_grades.finalgrade
	FROM fiapead_course_modules 
	INNER JOIN fiapead_grade_items
	ON fiapead_course_modules.course = fiapead_grade_items.courseid
	AND fiapead_course_modules.instance = fiapead_grade_items.iteminstance
	AND fiapead_grade_items.itemmodule = 'assign'
	INNER JOIN fiapead_grade_grades 
	ON fiapead_grade_items.id = fiapead_grade_grades.itemid
	INNER JOIN fiapead_moodle_relacao2004_assign
	ON fiapead_course_modules.instance = fiapead_moodle_relacao2004_assign.assignid
	INNER JOIN fiapead_user
	ON fiapead_grade_grades.userid = fiapead_user.id
	WHERE fiapead_course_modules.id = @C1
	AND fiapead_grade_grades.finalgrade IS NOT NULL
) AS nota1
ON users_in_course.id = nota1.userid
LEFT JOIN 
(
	SELECT 
		fiapead_user.id AS userid,
		fiapead_moodle_relacao2004_assign.assignid,
		fiapead_moodle_relacao2004_assign.codrelacao,
		fiapead_user.username,
		fiapead_grade_grades.finalgrade
	FROM fiapead_course_modules 
	INNER JOIN fiapead_grade_items
	ON fiapead_course_modules.course = fiapead_grade_items.courseid
	AND fiapead_course_modules.instance = fiapead_grade_items.iteminstance
	AND fiapead_grade_items.itemmodule = 'assign'
	INNER JOIN fiapead_grade_grades 
	ON fiapead_grade_items.id = fiapead_grade_grades.itemid
	INNER JOIN fiapead_moodle_relacao2004_assign
	ON fiapead_course_modules.instance = fiapead_moodle_relacao2004_assign.assignid
	INNER JOIN fiapead_user
	ON fiapead_grade_grades.userid = fiapead_user.id
	WHERE fiapead_course_modules.id = @C2
	AND fiapead_grade_grades.finalgrade IS NOT NULL
) AS nota2
ON users_in_course.id = nota2.userid
WHERE nota1.finalgrade IS NOT NULL OR nota2.finalgrade IS NOT NULL
```

## Comparação de notas de quiz

Raramente pode haver atividades que foram canceladas ou possuem uma nova versão,
no qual, apenas a maior nota será considerada.

O script SQL abaixo compara as notas das duas atividades do tipo quiz  
e exibe a maior nota. 

Alterar as variáveis `@nac1` e `@nac2` para os IDs dos registros desejados da tabela `fiapead_course_module`.


```sql
SET @nac1 = <id do course_module da nac1>;
SET @nac2 = <id do course_module da nac2>;

SELECT 
    REPLACE(fiapead_user.username, 'rm', '') AS username, 
    nac01.nacname,
    ROUND(IFNULL(nac01.finalgrade, 0), 2) AS 'nac1',
    ROUND(IFNULL(nac02.finalgrade, 0), 2) AS 'nac2',
    ROUND(IF(IFNULL(nac01.finalgrade, 0) > IFNULL(nac02.finalgrade, 0), IFNULL(nac01.finalgrade, 0), IFNULL(nac02.finalgrade, 0)), 2) AS 'maiornota'
FROM fiapead_user_enrolments
INNER JOIN fiapead_user ON fiapead_user_enrolments.userid = fiapead_user.id
INNER JOIN fiapead_enrol ON fiapead_user_enrolments.enrolid = fiapead_enrol.id
INNER JOIN fiapead_course_modules ON fiapead_course_modules.id = @nac1 AND fiapead_course_modules.course = fiapead_enrol.courseid
LEFT JOIN (
	SELECT fiapead_quiz_attempts.*, fiapead_grade_grades.finalgrade, fiapead_grade_grades.id AS 'gradeid', fiapead_quiz.name AS nacname
    FROM fiapead_quiz_attempts
	INNER JOIN fiapead_quiz ON fiapead_quiz_attempts.quiz = fiapead_quiz.id AND fiapead_quiz_attempts.state = 'finished'
	INNER JOIN fiapead_course_modules ON fiapead_course_modules.id = @nac1 AND fiapead_course_modules.module = 17 AND fiapead_course_modules.instance = fiapead_quiz.id
    INNER JOIN fiapead_grade_items ON fiapead_grade_items.itemtype = 'mod' AND fiapead_grade_items.itemmodule = 'quiz' AND fiapead_grade_items.iteminstance = fiapead_quiz.id
	LEFT JOIN fiapead_grade_grades ON fiapead_grade_items.id = fiapead_grade_grades.itemid AND fiapead_grade_grades.userid = fiapead_quiz_attempts.userid
) AS nac01 ON nac01.userid = fiapead_user.id
LEFT JOIN (
	SELECT fiapead_quiz_attempts.*, fiapead_grade_grades.finalgrade, fiapead_grade_grades.id AS 'gradeid', fiapead_quiz.name AS nacname 
    FROM fiapead_quiz_attempts
	INNER JOIN fiapead_quiz ON fiapead_quiz_attempts.quiz = fiapead_quiz.id AND fiapead_quiz_attempts.state = 'finished'
	INNER JOIN fiapead_course_modules ON fiapead_course_modules.id = @nac2 AND fiapead_course_modules.module = 17 AND fiapead_course_modules.instance = fiapead_quiz.id
    INNER JOIN fiapead_grade_items ON fiapead_grade_items.itemtype = 'mod' AND fiapead_grade_items.itemmodule = 'quiz' AND fiapead_grade_items.iteminstance = fiapead_quiz.id
LEFT JOIN fiapead_grade_grades ON fiapead_grade_items.id = fiapead_grade_grades.itemid AND fiapead_grade_grades.userid = fiapead_quiz_attempts.userid
) AS nac02 ON nac02.userid = fiapead_user.id
WHERE fiapead_user.username REGEXP '^rm([0-9]{5,})$' AND IFNULL(nac01.finalgrade, 0) > 0
ORDER BY fiapead_user.username;
```

## Remover revisão de quiz para Graduação Presencial no final do ano

Ao final de cada ano, as revisões de quiz são desabilitadas por questões de segurança
para evitar o vazamento das respostas para os anos posteriores.

Para automatizar o processo de desativar cada quiz, de cada curso desta modalidade (Graduação presencial),
do **ano atual**, o SQL abaixo atualiza os campos necessários da tabela `fiapead_quiz` para este fim.

```sql
UPDATE fiapead_course_modules
INNER JOIN fiapead_fiap_regras_course
    ON fiapead_course_modules.course = fiapead_fiap_regras_course.courseid
INNER JOIN fiapead_quiz
    ON fiapead_course_modules.instance = fiapead_quiz.id
SET 
    fiapead_quiz.reviewattempt = 65536,
    fiapead_quiz.reviewcorrectness = 0,
    fiapead_quiz.reviewspecificfeedback = 0,
    fiapead_quiz.reviewgeneralfeedback = 0,
    fiapead_quiz.reviewrightanswer = 0,
    fiapead_quiz.reviewoverallfeedback = 0
WHERE 
    fiapead_fiap_regras_course.regraid = 1 
    AND fiapead_course_modules.module = 17 
    AND fiapead_quiz.timeclose >= UNIX_TIMESTAMP(CONCAT(YEAR(CURDATE()), '-01-01 00:00:00'));
```

## Remover revisão de quiz por regra e categoria

Possui a mesma finalidade de *Remover revisão de quiz para Graduação Presecial no final do ano*, porém
serve para qualquer regra e especifica categorias para evitar erros.

```sql
UPDATE fiapead_course_modules
INNER JOIN fiapead_fiap_regras_course
    ON fiapead_course_modules.course = fiapead_fiap_regras_course.courseid
INNER JOIN fiapead_quiz
    ON fiapead_course_modules.instance = fiapead_quiz.id
INNER JOIN fiapead_course
  ON fiapead_course_modules.course = fiapead_course.id
SET 
    fiapead_quiz.reviewattempt = 65536,
    fiapead_quiz.reviewcorrectness = 0,
    fiapead_quiz.reviewspecificfeedback = 0,
    fiapead_quiz.reviewgeneralfeedback = 0,
    fiapead_quiz.reviewrightanswer = 0,
    fiapead_quiz.reviewoverallfeedback = 0
WHERE 
    fiapead_fiap_regras_course.regraid = @regraid
    AND fiapead_course_modules.module = 17
    AND fiapead_course.category IN ( @categorias )
```


## Atividades sem disciplinas relacionadas (relacao2004)

Atividades sem disciplinas relacionadas (tabela relacao2004), podem interferir na publicação da nota.

A SELECT abaixo lista todas as atividades que estão sem estes relacionamentos para cursos de Graduação e MBA,
tanto 20% quanto 100%.

```sql
SELECT 
    fiapead_course.id AS 'courseid',
    fiapead_course.category,
    fiapead_course.fullname,
    fiapead_course_categories_resume.breadcrumb,
    IF(fiapead_assign.id IS NOT NULL, 'assign', 'quiz') AS 'type',
    IF(fiapead_assign.id IS NOT NULL, fiapead_assign.name, fiapead_quiz.name) AS 'name',
    CONCAT('https://on.fiap.com.br/mod/', IF(fiapead_assign.id IS NOT NULL, 'assign', 'quiz'), '/view.php?id=', fiapead_course_modules.id) AS 'viewatividade',
    CONCAT('https://on.fiap.com.br/course/modedit.php?update=', fiapead_course_modules.id, '&return=0&sr=0') AS 'editatividade',
    CONCAT('https://on.fiap.com.br/troca-curso.php?id=', fiapead_course.id) AS 'trocacurso',
    CONCAT('https://on.fiap.com.br/course/view.php?id=', fiapead_course.id) AS 'viewcurso'
FROM fiapead_course
INNER JOIN fiapead_course_categories_resume
	ON fiapead_course.category = fiapead_course_categories_resume.categorieid
INNER JOIN fiapead_moodle_relacao2004
	ON fiapead_course.id = fiapead_moodle_relacao2004.course
INNER JOIN fiapead_course_modules
	ON fiapead_course.id = fiapead_course_modules.course
INNER JOIN fiapead_modules
	ON fiapead_course_modules.module = fiapead_modules.id
INNER JOIN fiapead_fiap_regras_course
	ON fiapead_course.id = fiapead_fiap_regras_course.courseid
LEFT JOIN fiapead_assign
	ON fiapead_modules.name = 'assign' AND fiapead_course_modules.instance = fiapead_assign.id
LEFT JOIN fiapead_moodle_relacao2004_assign
	ON fiapead_assign.id = fiapead_moodle_relacao2004_assign.assignid
LEFT JOIN fiapead_quiz
	ON fiapead_modules.name = 'quiz' AND fiapead_course_modules.instance = fiapead_quiz.id
LEFT JOIN fiapead_moodle_relacao2004_quiz
	ON fiapead_quiz.id = fiapead_moodle_relacao2004_quiz.id
WHERE 
    fiapead_fiap_regras_course.regraid BETWEEN 1 AND 4
    AND fiapead_assign.duedate < UNIX_TIMESTAMP()
    AND YEAR(FROM_UNIXTIME(fiapead_assign.duedate)) >= 2018
	AND fiapead_modules.name IN ('assign', 'quiz')
    AND (
        fiapead_moodle_relacao2004_assign.id IS NULL
        AND fiapead_moodle_relacao2004_quiz.id IS NULL
    )
GROUP BY 
    fiapead_course.id,
    fiapead_course.category,
    fiapead_course.fullname,
    fiapead_course_categories_resume.breadcrumb,
    IF(fiapead_assign.id IS NOT NULL, 'assign', 'quiz'),
    IF(fiapead_assign.id IS NOT NULL, fiapead_assign.name, fiapead_quiz.name)
ORDER BY fiapead_course_categories_resume.breadcrumb
```

## Reprocessar tabela de salavirtual para todos os cursos

```sql
DELETE FROM fiapead_salavirtual;

INSERT INTO fiapead_salavirtual (
   cmid,
   courseid,
   course_startdate,
   course_enddate,
   moduleid,
   module_name,
   instance,
   sequence,
   availability,
   conteudoshtmlcm,
   conteudosvideocm,
   conteudosaudiocm,
   conteudospdfcm,
   conteudoslabcm,
   conteudoslabcm_moduleid,
   conteudoslabcm_module_name,
   name,
   assign_cutoffdate,
   conteudoshtml_pacote,
   conteudoshtml_conteudospdf_id,
   conteudoshtml_tempoleitura,
   conteudoshtml_tempoportopicos,
   conteudosexternos_externalurl,
   conteudosexternos_isblank,
   conteudosexternos_islive,
   conteudosexternos_isfiaponcall,
   conteudosexternos_linkopen,
   conteudosexternos_marcador,
   lab,
   atividade,
   timeopen,
   timeclose
)
SELECT 
   course_module_id AS cmid,
   course AS courseid,             
   startdate,             
   enddate,             
   module AS moduleid,
   module_name,
   instance,
   sequence,
   availability,
   conteudoshtmlcm,
   conteudosvideocm,
   conteudosaudiocm,
   conteudospdfcm,
   conteudoslabcm,
   conteudoslabcm_moduleid,
   conteudoslabcm_module_name,
   name,
   assign_cutoffdate,
   conteudoshtml_pacote,
   conteudoshtml_conteudospdf_id,
   conteudoshtml_tempoleitura,
   conteudoshtml_tempoportopicos,
   conteudosexternos_externalurl,
   conteudosexternos_isblank,
   conteudosexternos_islive,
   conteudosexternos_isfiaponcall,
   conteudosexternos_linkopen,
   conteudosexternos_marcador,
   lab,
   IF (module_name IN ('assign', 'quiz') OR forum_assessed <> 0, 1, 0), 
   timeopen,
   timeclose
FROM (
   SELECT
      tbl.*,
      CASE
         WHEN conteudoshtml_name IS NOT NULL THEN conteudoshtml_name
         WHEN conteudospdf_name IS NOT NULL THEN conteudospdf_name
         WHEN conteudosexternos_name IS NOT NULL THEN conteudosexternos_name
         WHEN conteudosaudio_name IS NOT NULL THEN conteudosaudio_name
         WHEN conteudosvideo_name IS NOT NULL THEN conteudosvideo_name
         WHEN assign_name IS NOT NULL THEN assign_name
         WHEN quiz_name IS NOT NULL THEN quiz_name
         WHEN forum_name IS NOT NULL THEN forum_name
      END AS name,
      CASE
         WHEN conteudoshtml_lab IS NOT NULL THEN conteudoshtml_lab
         WHEN conteudospdf_lab IS NOT NULL THEN conteudospdf_lab
         ELSE 0
      END AS lab,
      CASE
         WHEN conteudoshtml_timeopen THEN conteudoshtml_timeopen
         WHEN conteudospdf_timeopen THEN conteudospdf_timeopen
         WHEN conteudosexternos_timeopen THEN conteudosexternos_timeopen
         WHEN assign_timeopen THEN assign_timeopen
         WHEN quiz_timeopen THEN quiz_timeopen
         WHEN forum_timeopen THEN forum_timeopen
         ELSE 0
      END AS timeopen,
      CASE
         WHEN conteudoshtml_timeclose THEN conteudoshtml_timeclose
         WHEN conteudospdf_timeclose THEN conteudospdf_timeclose
         WHEN conteudosexternos_timeclose THEN conteudosexternos_timeclose
         WHEN assign_timeclose THEN assign_timeclose
         WHEN quiz_timeclose THEN quiz_timeclose
         WHEN forum_timeclose THEN forum_timeclose
         ELSE 0
      END AS timeclose
   FROM (
      SELECT
          fiapead_course_modules.id AS course_module_id,
          fiapead_course_modules.course,
          fiapead_course.startdate,
          fiapead_course.enddate,
          fiapead_course_modules.module,
          fiapead_modules.name AS module_name,
          fiapead_course_modules.instance,
          fiapead_course_sections.sequence,
          fiapead_course_modules.availability,
          fiapead_fiap_conteudos_relacao.conteudoshtmlcm,
          fiapead_fiap_conteudos_relacao.conteudosvideocm,
          fiapead_fiap_conteudos_relacao.conteudosaudiocm,
          fiapead_fiap_conteudos_relacao.conteudospdfcm,
          fiapead_fiap_conteudos_relacao.conteudoslabcm,
          fiapead_fiap_conteudos_relacao.conteudoslabcm_moduleid,
          fiapead_modules_relacao.name AS conteudoslabcm_module_name,
          fiapead_conteudoshtml.pacote AS conteudoshtml_pacote,
          fiapead_conteudoshtml.name AS conteudoshtml_name,
          fiapead_conteudoshtml_pacotes.pdf AS conteudoshtml_conteudospdf_id,
          fiapead_conteudoshtml_pacotes.tempoleitura AS conteudoshtml_tempoleitura,
          fiapead_conteudoshtml_pacotes.tempoportopicos AS conteudoshtml_tempoportopicos,
          fiapead_conteudoshtml.lab AS conteudoshtml_lab,
          fiapead_conteudoshtml.timeopen AS conteudoshtml_timeopen,
          fiapead_conteudoshtml.timeclose AS conteudoshtml_timeclose,
          fiapead_conteudospdf.name AS conteudospdf_name,
          fiapead_conteudospdf.lab AS conteudospdf_lab,
          fiapead_conteudospdf.timeopen AS conteudospdf_timeopen,
          fiapead_conteudospdf.timeclose AS conteudospdf_timeclose,
          fiapead_conteudosexternos.name AS conteudosexternos_name,
          fiapead_conteudosexternos.externalurl AS conteudosexternos_externalurl,
          fiapead_conteudosexternos.isblank AS conteudosexternos_isblank,
          fiapead_conteudosexternos.islive AS conteudosexternos_islive,
          fiapead_conteudosexternos.isfiaponcall AS conteudosexternos_isfiaponcall,
          fiapead_conteudosexternos.linkopen AS conteudosexternos_linkopen,
          fiapead_conteudosexternos.marcador AS conteudosexternos_marcador,
          fiapead_conteudosexternos.timeopen AS conteudosexternos_timeopen,
          fiapead_conteudosexternos.timeclose AS conteudosexternos_timeclose,
          fiapead_conteudosaudio.name AS conteudosaudio_name,
          fiapead_conteudosvideo.name AS conteudosvideo_name,
          fiapead_assign.name AS assign_name,
          fiapead_assign.grade AS assign_grade,
          fiapead_assign.allowsubmissionsfromdate AS assign_timeopen,
          fiapead_assign.cutoffdate AS assign_cutoffdate,
          fiapead_assign.duedate AS assign_timeclose,
          fiapead_quiz.name AS quiz_name,
          fiapead_quiz.grade AS quiz_grade,
          fiapead_quiz.timeopen AS quiz_timeopen,
          fiapead_quiz.timeclose AS quiz_timeclose,
          fiapead_forum.name AS forum_name,
          fiapead_forum.assessed AS forum_assessed,
          fiapead_forum.assesstimestart AS forum_timeopen,
          fiapead_forum.assesstimefinish AS forum_timeclose
      FROM fiapead_course_modules
      INNER JOIN fiapead_modules
          ON fiapead_course_modules.module = fiapead_modules.id
      INNER JOIN fiapead_course
          ON fiapead_course_modules.course = fiapead_course.id
      INNER JOIN fiapead_course_sections
          ON fiapead_course_modules.course = fiapead_course_sections.course
      INNER JOIN fiapead_enrol
          ON fiapead_course_modules.course = fiapead_enrol.courseid	
      LEFT JOIN fiapead_fiap_conteudos_relacao
          ON fiapead_course_modules.id = fiapead_fiap_conteudos_relacao.conteudoshtmlcm
      LEFT JOIN fiapead_modules AS fiapead_modules_relacao
          ON fiapead_fiap_conteudos_relacao.conteudoslabcm_moduleid = fiapead_modules_relacao.id
      LEFT JOIN fiapead_conteudoshtml
          ON fiapead_modules.name = 'conteudoshtml' AND fiapead_course_modules.instance = fiapead_conteudoshtml.id
      LEFT JOIN fiapead_conteudoshtml_pacotes
          ON fiapead_conteudoshtml.pacote = fiapead_conteudoshtml_pacotes.id
      LEFT JOIN fiapead_conteudospdf
          ON fiapead_modules.name = 'conteudospdf' AND fiapead_course_modules.instance = fiapead_conteudospdf.id
      LEFT JOIN fiapead_conteudosexternos
          ON fiapead_modules.name = 'conteudosexternos' AND fiapead_course_modules.instance = fiapead_conteudosexternos.id
      LEFT JOIN fiapead_assign
          ON fiapead_modules.name = 'assign' AND fiapead_course_modules.instance = fiapead_assign.id	
      LEFT JOIN fiapead_quiz
          ON fiapead_modules.name = 'quiz' AND fiapead_course_modules.instance = fiapead_quiz.id
      LEFT JOIN fiapead_forum
          ON fiapead_modules.name = 'forum' AND fiapead_course_modules.instance = fiapead_forum.id
      LEFT JOIN fiapead_conteudosaudio
          ON fiapead_modules.name = 'conteudosaudio' AND fiapead_course_modules.instance = fiapead_conteudosaudio.id                 
      LEFT JOIN fiapead_conteudosvideo
          ON fiapead_modules.name = 'conteudosvideo' AND fiapead_course_modules.instance = fiapead_conteudosvideo.id
      WHERE fiapead_course_modules.deletioninprogress = 0 AND fiapead_course_modules.visible = 1
      GROUP BY fiapead_course_modules.id
   ) AS tbl
) AS t
``` 

## Quantidade de alunos que selecionaram cada Nano Course para PS

```sql
SELECT 
    fiapead_relacao_2004.disciplina,
    COUNT(fiapead_user.username) AS 'Quantidade'
FROM fiapead_fiap_user_relacao
INNER JOIN fiapead_relacao_2004
  ON fiapead_fiap_user_relacao.codrelacao = fiapead_relacao_2004.codrelacao
INNER JOIN fiapead_user
  ON fiapead_fiap_user_relacao.userid = fiapead_user.id
WHERE fiapead_fiap_user_relacao.ps = 1
GROUP BY fiapead_relacao_2004.disciplina
ORDER BY fiapead_relacao_2004.disciplina;
```

## Alunos que não selecionaram nenhum Nano Course para PS

Alunos que não selecionaram nenhum Nano Course para PS e em qual curso estão inseridos.
Informar ano dos cursos que deseja filtrar.

```sql
SET @ano = 2019;

SELECT
  vAlunoCursoResumeRegra.breadcrumb,
    vAlunoCursoResumeRegra.username,
    vAlunoCursoResumeRegra.firstname,
    vAlunoCursoResumeRegra.lastname
FROM fiapead_fiap_user_relacao
INNER JOIN vAlunoCursoResumeRegra
  ON fiapead_fiap_user_relacao.userid = vAlunoCursoResumeRegra.id
WHERE fiapead_fiap_user_relacao.userid NOT IN
  (SELECT
    fiapead_fiap_user_relacao.userid
  FROM fiapead_fiap_user_relacao
    WHERE fiapead_fiap_user_relacao.ps = 1)
    AND vAlunoCursoResumeRegra.nivel3 = @ano
GROUP BY fiapead_fiap_user_relacao.userid
ORDER BY
  vAlunoCursoResumeRegra.breadcrumb,
  vAlunoCursoResumeRegra.firstname,
    vAlunoCursoResumeRegra.lastname
```

## Atualizar o e-mail do aluno que está na plataforma no SQL Server 

Muitas vezes os alunos pedem para ter o e-mail atualizado na plataforma, o que é feito pelos gerenciadores do FIAP ON,
porém é necessário atualizar este mesmo e-mail dentro do banco do SQL Server.

Para encontrar o registro com o e-mail de alunos de Graduação:


```sql
USE Educacional;

SELECT * 
FROM PessoaEmail
WHERE PessoaEmail.Email = '<e-mail do aluno aqui>';
```

Para encontrar o registro com o e-mail de alunos de MBA:

```sql
USE webadm;

SELECT * 
FROM pos_inscricao_new
WHERE pos_inscricao_new.email = '<e-mail do aluno aqui>';
```

## Confirmação de presença em encontro FIAP ON no SQL Server

Muitas vezes são exibidos durante o ano alguns avisos com confirmação de presença para os alunos
dentro da plataforma ON para um determinado evento.

Para identificar a resposta de cada aluno, há uma chave de confirmação para o link de confirmação

Para buscar alunos ativos de uma turma de Graduação e gerar as chaves:

```sql
INSERT INTO Site_Fiap..ConfirmacaoPresencaFiapOn SELECT
    vAluno.RM,
    vPessoa.Nome,
    vPessoa.Email,
    vRelacao.Ano,
    NEWID(),
    NULL,
    'Nome do evento',
    '26 de Outubro de 2019',
    'das 8h às 12h',
    'Fiap - Aclimação',
    vRelacao.Turma,
    NULL
FROM
    vAluno
    INNER JOIN vAlunoTurma ON
        vAluno.Codigo = vAlunoTurma.CodigoAluno
    INNER JOIN vRelacao ON
        vAlunoTurma.CodigoRelacao = vRelacao.Codigo
    INNER JOIN vPessoa ON
        vAluno.CodigoPessoa = vPessoa.Codigo
WHERE
    vAluno.CodigoUnidade = 1
    AND vRelacao.CodigoUnidade = 1
    AND vRelacao.Turma = '<Nome da turma aqui - Ex: 1SIO>'
    AND vRelacao.Ano = <Ano>
    AND vAlunoTurma.CodigoTipoStatus IN (1, 23)
```

Para buscar alunos de uma turma de MBA e gerar as chaves:

```sql
INSERT INTO ConfirmacaoPresencaFiapOn (RM, Nome, Email, Ano, Chave, DataHoraConfirmacao, Titulo, Dias, Horas, Endereco, Turma, Interesse)
SELECT 
    webadm..pos_inscricao_contrato.rm,
    webadm..pos_inscricao_new.nome,
    webadm..pos_inscricao_new.email,
    2019,
    NEWID(),
    NULL,
    'Nome do evento',
    '07 de Dezembro de 2019',
    'das 09h às 17h',
    'Av. Lins de Vasconcelos, 1264 - Unidade I',
    webadm..pos_inscricao_contrato.turma,
    NULL
FROM webadm..pos_inscricao_contrato
INNER JOIN webadm..PI_InscricaoProcesso
    ON webadm..pos_inscricao_contrato.codigoInscricaoProcesso = webadm..PI_InscricaoProcesso.codigo
INNER JOIN webadm..pos_inscricao_new
    ON webadm..pos_inscricao_contrato.codigoInscricao = webadm..pos_inscricao_new.codigo
INNER JOIN webadm..pos_inscricao_turmas
    ON webadm..pos_inscricao_contrato.turma = webadm..pos_inscricao_turmas.Turma
INNER JOIN webadm..PI_Processo
    ON webadm..pos_inscricao_turmas.codigoProcesso = webadm..PI_Processo.codigo
WHERE webadm..pos_inscricao_contrato.turma IN ('<Sigla do curso 1 aqui>', '<Sigla do curso 2 aqui>')
ORDER BY webadm..pos_inscricao_contrato.turma, webadm..pos_inscricao_new.nome;
```


## Selecionar quem tem certificado de nanocourse de graduação presencial mas não tem nota (Prova foi excluída)

A SELECT abaixo pode ser alterada para outras modalidades de nanocourse, trocando apenas a regraid e o ano.

```sql
SELECT 
	fiapead_certificados_nanocourse.userid,
    fiapead_certificados_nanocourse.courseid,
    fiapead_course.fullname,
    fiapead_user.username,
    fiapead_user.firstname,
    fiapead_user.lastname,
    fiapead_user.email
FROM fiapead_certificados_nanocourse
INNER JOIN fiapead_course
	ON fiapead_certificados_nanocourse.courseid = fiapead_course.id
    AND fiapead_course.id NOT IN (
		SELECT fiapead_grade_items.courseid
        FROM fiapead_grade_items
        INNER JOIN fiapead_grade_grades
			ON fiapead_grade_items.id = fiapead_grade_grades.itemid
            AND fiapead_grade_items.itemmodule = 'quiz'
            AND fiapead_grade_grades.finalgrade IS NOT NULL
			AND fiapead_grade_grades.aggregationstatus = 'used'
		WHERE fiapead_grade_grades.userid = fiapead_certificados_nanocourse.userid
    )
INNER JOIN fiapead_course_categories_resume
	ON fiapead_course.category = fiapead_course_categories_resume.categorieid
	AND fiapead_course_categories_resume.nivel3 = '2020'
INNER JOIN fiapead_fiap_regras_course
	ON fiapead_course.id = fiapead_fiap_regras_course.courseid
    AND fiapead_fiap_regras_course.regraid = 14
INNER JOIN fiapead_user
	ON fiapead_certificados_nanocourse.userid = fiapead_user.id
LEFT JOIN fiapead_grade_items
	ON fiapead_course.id = fiapead_grade_items.courseid
    AND fiapead_grade_items.itemmodule = 'quiz'
LEFT JOIN fiapead_grade_grades
	ON fiapead_grade_items.id = fiapead_grade_grades.itemid
    AND fiapead_certificados_nanocourse.userid = fiapead_grade_grades.userid
GROUP BY fiapead_certificados_nanocourse.userid,
		fiapead_certificados_nanocourse.courseid,
		fiapead_course.fullname,
		fiapead_user.username,
		fiapead_user.firstname,
		fiapead_user.lastname,
		fiapead_user.email;
```

## Descobrir respostas dos usuários de um determinado quiz

Abaixo a consulta necessária para ver todas as respostas dadas em um quiz pelos alunos.

```sql
SELECT
	fiapead_user.username,
	fiapead_user.firstname,
	fiapead_user.lastname,
	fiapead_question.questiontext,
	fiapead_question_attempts.rightanswer,
	fiapead_question_attempts.responsesummary,
	fiapead_question_attempt_steps.*
FROM fiapead_quiz_attempts 
INNER JOIN fiapead_question_usages 
	ON fiapead_quiz_attempts.uniqueid = fiapead_question_usages.id
INNER JOIN fiapead_question_attempt_steps
    ON fiapead_quiz_attempts.userid = fiapead_question_attempt_steps.userid
INNER JOIN fiapead_question_attempts
    ON fiapead_question_attempts.id = fiapead_question_attempt_steps.questionattemptid
    AND fiapead_question_attempts.questionusageid = fiapead_quiz_attempts.uniqueid
INNER JOIN fiapead_question
    ON fiapead_question_attempts.questionid = fiapead_question.id
INNER JOIN fiapead_user 
	ON fiapead_question_attempt_steps.userid = fiapead_user.id
WHERE fiapead_quiz_attempts.quiz = < id do quiz aqui >
	AND fiapead_question_attempt_steps.sequencenumber = 2
ORDER BY 
	fiapead_user.firstname,
	fiapead_user.lastname;
```

##Remover alunos de um curso
Caso o codrelacao incorreto seja relacionado com um curso, o importador irá inserir alunos
que não deveriam ter acesso ao curso dentro dele. Para resolver este problema, o método mais
rápido é remover todos os alunos do curso e rodar o importador novamente em seguida, com os codrelacoes
corretos.

**Muito cuidado ao executar esta query, ela irá remover o acesso dos alunos ao curso.**

```sql
SET @course_id = id do curso que você deseja remover os alunos

DELETE fiapead_user_enrolments, fiapead_role_assignments
FROM fiapead_enrol
INNER JOIN fiapead_user_enrolments
	ON fiapead_enrol.id = fiapead_user_enrolments.enrolid
INNER JOIN fiapead_user
	ON fiapead_user_enrolments.userid = fiapead_user.id
INNER JOIN fiapead_context
	ON fiapead_enrol.courseid = fiapead_context.instanceid
    AND fiapead_context.contextlevel = 50
INNER JOIN fiapead_role_assignments
	ON fiapead_user_enrolments.userid = fiapead_role_assignments.userid
    AND fiapead_context.id = fiapead_role_assignments.contextid
WHERE fiapead_enrol.courseid = @course_id
	AND fiapead_user.username REGEXP '^rm'
```

##Transferir tentativa em nano entre RMs

O SQL abaixo faz a transferencia da avaliação de um nano course entre diferentes RMs.

**Por favor execute bloco a bloco, verificando se todas as váriaveis são preenchidas, e executar os selects antes dos inserts, afim de verificar se faz sentido, a quantidade de linhas ou os dados contidos!**

Foi feito entre courseid diferente, mas nada impede de ser feito para o mesmo.


```sql
-- Setar as váriaveis 
	
# Coloque aqui o RM que irá receber o quiz 
	SET @username_destino = "rmteste";
# COloque aqui onde está o quiz a ser transferido
	SET @username_fonte = "rmteste2";
# Coloque aqui o código do curso, do nano course (Destino, que irá receber a nota)
	SET @courseid_destino = 2222;
# Coloque aqui o código do curso, do nano course (Fonte, onde será usado como base pra copiar)
	SET @courseid_fonte = 2222;

	SET @userid = (select id from fiapead_user where username = @username_fonte);
	SELECT @userid;
# Setar variávies do antigo

	SET @quizid_antigo = ( 
		SELECT 
		instance FROM fiapead_course_modules 
		WHERE course = @courseid_fonte AND module = 17    
	);
	SET @course_modules_antigo = ( 
		SELECT 
		id FROM fiapead_course_modules 
		WHERE course = @courseid_fonte AND module = 17    
	);
	SELECT @quizid_antigo;
	SELECT @course_modules_antigo;
#Procurar as nota as notas antigas, deve estar certinho aqui

	select * from fiapead_quiz_grades where quiz = @quizid_antigo and userid = @userid;
	select * from fiapead_quiz_attempts where quiz = @quizid_antigo and userid = @userid;

# Setar user id do novo.

	SET @userid_novo = (select id from fiapead_user where username = @username_destino);
	SELECT @userid_novo;
# Setar variávies do novo

	SET @quizid_novo = ( 
		SELECT 
		instance FROM fiapead_course_modules 
		WHERE course = @courseid_destino AND module = 17    
	);
	SET @course_modules_novo = ( 
		SELECT 
		id FROM fiapead_course_modules 
		WHERE course = @courseid_destino AND module = 17    
	);
	SELECT @quizid_novo;
    SELECT @course_modules_novo;
# Verifica se há alguma nota ou tentativa, no quiz destino, se sim convêm apagar ou negativar	
	select * from fiapead_quiz_grades where quiz = @quizid_novo and userid = @userid_novo;
	select * from fiapead_quiz_attempts where quiz = @quizid_novo and userid = @userid_novo;

# Verificar o contextid do quiz destino
	SET @contextid = (select id from fiapead_context WHERE contextlevel = 70 and instanceid = @course_modules_novo);
    SELECT @contextid;
# Verificar o contextid da fonte 
	SET @contextid_fonte = (select id from fiapead_context WHERE contextlevel = 70 and instanceid = @course_modules_antigo);
    SELECT @contextid_fonte;
# setar o fiapead_question_usages antigo
	SET @id_question_antigo = (select uniqueid from fiapead_quiz_attempts where quiz = @quizid_antigo and userid = @userid order by timestart desc LIMIT 1);
	SELECT @id_question_antigo;
-- INSERTS

	INSERT INTO `fiapead_quiz_grades` (`quiz`, `userid`, `grade`, `timemodified`)  
		SELECT  
			@quizid_novo,
			@userid_novo,
			fiapead_quiz_grades.grade,
			fiapead_quiz_grades.timemodified        
		FROM fiapead_quiz_grades 
		WHERE quiz = @quizid_antigo AND userid = @userid
        order by timemodified desc
        LIMIT 1;

	INSERT INTO `fiapead_question_usages` (`contextid`, `component`, `preferredbehaviour`) VALUES (@contextid, 'mod_quiz', 'deferredfeedback');
	SET @id_question = (SELECT LAST_INSERT_ID());

	INSERT INTO `fiapead_quiz_attempts` (`quiz`, `userid`, `attempt`, `uniqueid`, `layout`,
	`currentpage`, `preview`, `state`, `timestart`, `timefinish`, 
	`timemodified`, `sumgrades`)
		SELECT
			@quizid_novo,
			@userid_novo,
			fiapead_quiz_attempts.attempt,
			@id_question,
			fiapead_quiz_attempts.layout,
			fiapead_quiz_attempts.currentpage,
			fiapead_quiz_attempts.preview,
			fiapead_quiz_attempts.state,
			fiapead_quiz_attempts.timestart,
			fiapead_quiz_attempts.timefinish,
			fiapead_quiz_attempts.timemodified,
			fiapead_quiz_attempts.sumgrades
		FROM  fiapead_quiz_attempts
		where quiz = @quizid_antigo and userid = @userid
        order by timestart desc LIMIT 1
        ;

	INSERT INTO fiapead_question_attempts (`questionusageid`,`slot`,`behaviour`,`questionid`,`variant`,`maxmark`,`minfraction`,`maxfraction`,`flagged`,
	`questionsummary`,`rightanswer`,`responsesummary`,`timemodified`) 
		SELECT 
			@id_question,
			slot,
			behaviour,
			questionid,
			variant,
			maxmark,
			minfraction,
			maxfraction,
			flagged,
			questionsummary,
			rightanswer,
			responsesummary,
			timemodified
		FROM fiapead_question_attempts
		WHERE fiapead_question_attempts.questionusageid = @id_question_antigo ;

	INSERT INTO `fiapead_question_attempt_steps` (`questionattemptid`, `sequencenumber`, `state`, `fraction`, `timecreated`, `userid`) 
	SELECT 
		( 
			SELECT fiapead_question_attempts2.id 
			from fiapead_question_attempts as fiapead_question_attempts2 
			where fiapead_question_attempts2.questionusageid = @id_question 
				and fiapead_question_attempts2.questionid = fiapead_question_attempts.questionid
		) as questionattemptid_novo,	
		fiapead_question_attempt_steps.sequencenumber,
		fiapead_question_attempt_steps.state,
		fiapead_question_attempt_steps.fraction,
		fiapead_question_attempt_steps.timecreated,
		@userid_novo as user_id
	FROM fiapead_question_attempt_steps
	INNER JOIN fiapead_question_attempts on fiapead_question_attempts.id = fiapead_question_attempt_steps.questionattemptid
	where fiapead_question_attempt_steps.userid = @userid and fiapead_question_attempts.questionusageid = @id_question_antigo ;

	INSERT INTO `fiapead_question_attempt_step_data` (`attemptstepid`, `name`, `value`) 
	SELECT 
		(
			SELECT fiapead_question_attempt_steps2.id
			from fiapead_question_attempt_steps as fiapead_question_attempt_steps2 
			INNER JOIN fiapead_question_attempts as fiapead_question_attempts2 on fiapead_question_attempts2.id = fiapead_question_attempt_steps2.questionattemptid
			where fiapead_question_attempt_steps2.userid = @userid_novo
			and fiapead_question_attempts2.questionid = fiapead_question_attempts.questionid			
			and fiapead_question_attempt_steps2.state = fiapead_question_attempt_steps.state	
		),        
		fiapead_question_attempt_step_data.name,
		fiapead_question_attempt_step_data.value    
	FROM fiapead_question_attempt_steps
	INNER JOIN fiapead_question_attempts on fiapead_question_attempts.id = fiapead_question_attempt_steps.questionattemptid
	INNER JOIN fiapead_question_attempt_step_data on fiapead_question_attempt_step_data.attemptstepid = fiapead_question_attempt_steps.id
	where fiapead_question_attempt_steps.userid = @userid and fiapead_question_attempts.questionusageid = @id_question_antigo;

# Verificar se foi inserido tudo certinho
	SELECT  
		*        
	FROM fiapead_quiz_grades 
	WHERE quiz = @quizid_novo AND userid = @userid_novo;

	SELECT  
		*    
	FROM fiapead_quiz_attempts 
	WHERE quiz = @quizid_novo AND userid = @userid_novo;

	SELECT 
	fiapead_question_attempts.*
	FROM fiapead_question_attempts
	WHERE fiapead_question_attempts.questionusageid = @id_question ;

	SELECT 
		fiapead_question_attempt_steps.*
	FROM fiapead_question_attempt_steps
	INNER JOIN fiapead_question_attempts on fiapead_question_attempts.id = fiapead_question_attempt_steps.questionattemptid
	where fiapead_question_attempt_steps.userid = @userid_novo and fiapead_question_attempts.questionusageid = @id_question ;

	SELECT 
		fiapead_question_attempt_step_data.*
	FROM fiapead_question_attempt_steps
	INNER JOIN fiapead_question_attempts on fiapead_question_attempts.id = fiapead_question_attempt_steps.questionattemptid
	INNER JOIN fiapead_question_attempt_step_data on fiapead_question_attempt_step_data.attemptstepid = fiapead_question_attempt_steps.id
	where fiapead_question_attempt_steps.userid = @userid_novo and fiapead_question_attempts.questionusageid = @id_question;

```

## Deixar imagem default para todos os usuários em homologação

Utilize o comando abaixo **SOMENTE NO BANCO DE HOMOLOGAÇÃO** para deixar todos os usuários com a mesma imagem padrão no perfil.

```sql
UPDATE homologacao_moodle.fiapead_files
SET fiapead_files.contenthash = '1699125bce0608e96ec9716cb10cdbf1b211cddc',
    fiapead_files.filesize = 441,
    fiapead_files.mimetype = 'image/png'
WHERE fiapead_files.component = 'user'
    AND fiapead_files.filearea = 'icon'
    AND fiapead_files.filename IN ('f1.jpg', 'f1.png');
    

UPDATE homologacao_moodle.fiapead_files
SET fiapead_files.contenthash = 'c062054d9945ff9f5fa8771f7aee192381275acf',
    fiapead_files.filesize = 445,
    fiapead_files.mimetype = 'image/png'
WHERE fiapead_files.component = 'user'
    AND fiapead_files.filearea = 'icon'
    AND fiapead_files.filename IN ('f2.jpg', 'f2.png');


UPDATE homologacao_moodle.fiapead_files
SET fiapead_files.contenthash = '5b2306e96e82b280c4b161820d7c3dedc1d51dad',
    fiapead_files.filesize = 86661,
    fiapead_files.mimetype = 'image/png'
WHERE fiapead_files.component = 'user'
    AND fiapead_files.filearea = 'icon'
    AND fiapead_files.filename IN ('f3.jpg', 'f3.png');
```
