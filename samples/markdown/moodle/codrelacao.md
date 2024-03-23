#Codrelacao
O codrelacao é o código de uma "tabela resumo", onde são agrupados dados como:
disciplina, professor que ministra a disciplina, ano, turma, curso, se é 100%
on-line, se é um nano course etc.

Todos esses dados estão armazenados no SQL Server e na plataforma servem para
importar os alunos nos cursos, conceder visualização no caso de Nano Courses e
enviar notas para o boletim.

Os codrelacoes e suas informações são adicionados na plataforma por meio de um
importador que roda todos os dias às 02h e às 14h, e podem ser consultados na tabela
*fiapead_relacao_2004*.

##Importação
Nos importadores de Presencial e On-line, os alunos vêm com um array de "Relacoes".
Neste array, estão todos os codrelacoes que pertencem ao aluno.

A importação funciona por meio da relação entre codrelacao e curso na plataforma.

Essa relação entre codrelacao e curso pode ser consultada na tabela
*fiapead_moodle_relacao2004*.

###Fases e disciplinas
Os alunos serão inseridos nas fases e disciplinas que tiverem pelo menos um de seus
codrelacao relacionados com o curso.
 
**Alunos de Graduação On-line são importados somente pelo codrelacao de nivelamento.**

###Nano Courses
Os alunos irão receber visualização (Nano Courses opcionais) ou serão inscritos (Nano
Courses obrigatórios) em Nano Courses que tiverem pelo menos um de seus codrelacao
relacionados.

Alunos de Graduação Presencial (que não estejam cursando DP) possuem um codrelacao para
cada Nano Course, enquanto todas as outras modalidades possuem um codrelacao geral para
todos os Nanos.

##Envio de notas
Os cursos dentro da plataforma possuem algumas atividades que podem valer nota para os
alunos.

Para que a nota seja enviada ao boletim, nas configurações da atividade ela deve estar
relacionada com os codrelacoes que correspondem às disciplinas que o aluno irá receber
nota naquela atividade.

A relação entre atividade e codrelacao pode ser consultada em:

- fiapead_moodle_relacao2004_assign;
- fiapead_moodle_relacao2004_forum;
- fiapead_moodle_relacao2004_quiz.

##Personalizados
Na plataforma temos alguns codrelacoes negativos que chamamos de "codrelacoes
personalizados". Esses codrelacoes servem para oferecer Nano Courses para usuários que
não possuem vínculo de boletim (e consequentemente não possuem codrelacao no SQL Server)
com a FIAP.

Alguns exemplos de usuários que utilizam estes codrelacoes são funcionários e
alunos de corporates.

Estes codrelacoes são criados atráves de uma ferramenta e podem ser obrigatórios
ou não. Caso o codrelacao seja obrigatório, o usuário será inscrito nele quando for vinculado,
caso contrário, irá receber apenas a visualização.