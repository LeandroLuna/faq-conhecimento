#Importação
Os alunos (com exceção de corporate e parcerias) são inscritos na plataforma
por um importador, que traz dados como rm, nome completo, curso e codrelacoes.

O aluno será inserido ou irá ganhar visualização (no caso de Nano Courses
não obrigatórios) nos cursos que estiverem atrelados a cada codrelacao
informado no array "Relacoes".
 
Essa relação entre codrelacao e curso pode ser consultada na tabela
*fiapead_moodle_relacao2004*.

##Presencial
Alunos de Graduação Presencial, MBA Presencial e MBA Híbrido possuem um importador
que roda diariamente a cada 1h.

Neste importador, também é informada a chave de integração do Portal do Aluno,
pela qual ele consegue acessar a plataforma através de "Sala de Aula Virtual".

Os alunos que são retornados pela API são consultados na tabela *ImportacaoAlunosGraduacaoMoodle_Final*
do banco *site_fiap* do SQL Server. Esta tabela é atualizada por um
job que roda diariamente às 11h, 18h e às 21h30.

URL: https://apis.fiap.com.br/shift-moodle/v1/Shift/Aluno/ListarAlunoGraduacaoMoodle

**Necessita de um authorization, consultar no importador**

##On-line
Alunos de Graduação e MBA On-line possuem um importador que roda diariamente a
cada 20 minutos.

Os alunos de Graduação On-line são importados apenas pela disciplina de
nivelamento. Além disso, alunos do 2º semestre são importados apenas a partir de Agosto,
antes disso, ou eles não irão vir no importador, ou virão com o codrelacao de nivelamento
do ano anterior.

URL: https://apis.fiap.com.br/portalmoodle/v1/Importar/DadosAlunosEADComRelacoesAgrupadas

**Necessita de um authorization, consultar no importador**

##Power Skills
Os alunos de MBA possuem a opção de escolher Power Skills para cursar, que funcionam como
pequenas extensões do curso. Eles podem realizar essa escolha pelo site da Fiap, e ela fica armazenada
no SQL Server.

Diferente das outras importações, os alunos são importados no curso em que o Power Skill escolhido
estiver relacionado, não pela disciplina, mas sim por uma [ferramenta personalizada](https://on.fiap.com.br/local/powerskill/listagem.php).

Os alunos retornados no importador são consultados a partir da procedure *sp_PSGetInscricoes* do banco
*site_fiap* do SQL Server.

O importador desses alunos roda diariamente a cada 20 minutos.

URL: https://apis.fiap.com.br/pstrilhas/v1/Inscricao

**Necessita de um authorization e de um Token, consultar no importador**

##SHIFT
Alunos de SHIFT possuem um importador que roda diariamente a cada 20 minutos.

O cron utilizado pelo Jenkins importa alunos apenas de cursos que ainda estão com a relação
aberta (coluna datafechamento em fiapead_moodle_relacaoshift).

Neste importador, são listados apenas alunos que precisam passar por alguma ação no curso
especificado (inclusão/exclusão). Caso todos os alunos já estejam atualizados, a API irá
retornar um array vazio.

Com as informações do aluno e a ação a ser realizada, também é informada a chave de integração
do site do SHIFT, pela qual ele conseguirá acessar a plataforma através de "Plataforma On-line".

URL: https://apis.fiap.com.br/shift-moodle/v1/Shift/Aluno/ConsultaAlunosNoStop/codigo_do_curso

**Necessita de um authorization, consultar no importador**

**As datas das importações podem ser consultadas em: https://on.fiap.com.br/local/importadoralunos/index.php**

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

