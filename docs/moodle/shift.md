#SHIFT
Os SHIFTs são cursos de curta duração oferecidos pela FIAP. Os conteúdos desses cursos são cadastrados
e acessados através da plataforma.

##ID SHIFT
Para que um aluno consiga visualizar os cursos do SHIFT ou um professor consiga realizar chamadas, é
necessário integrar os usuários da plataforma com os usuários do SHIFT. Essa integração ocorre por meio
da inserção de um código no perfil do usuário.

Para alunos, esse código é inserido no momento da [importação](/processos/plataforma/importacao-alunos-shift/),
no campo **ID Aluno SHIFT**. Além disso, também é inserida uma **Chave SHIFT**, que serve para que o aluno
consiga realizar login através do site do SHIFT na plataforma.

Já para os professores, esse código é inserido manualmente, no momento do cadastro do usuário na plataforma,
no campo **ID Professor SHIFT** na área de **Integrações**.

##Chamada
Na plataforma, um professor pode visualizar as chamadas existentes e realizar as que estão pendentes.

As chamadas listadas são exibidas conforme o ID Professor SHIFT do usuário que está visualizando a página,
consultadas a partir de uma API.

Caso o curso seja um SHIFT Presencial, para que a chamada seja exibida para o professor, ele deve ser
o professor desse curso, caso seja uma imersão, as chamadas exibidas são apresentadas conforme as aulas
que ele irá ministrar.

Após realizar a chamada, se o SHIFT for do tipo presencial ou remoto, os certificados para os alunos
são emitidos de acordo com a presença de cada um.

URL chamadas pendentes: https://apis.fiap.com.br/shift-moodle/v1/Shift/Chamada/ListarChamadasPendentes/id_professor_shift

URL chamadas existentes: https://apis.fiap.com.br/shift-moodle/v1/Shift/Chamada/ListarChamadasExistentes/id_professor_shift

**Para consultar as rotas é necessário informar um Authorization, consultar na plataforma.**

##Processos
- [Importação](/processos/plataforma/importacao-alunos-shift/)
- [Unificar o usuário do SHIFT](/processos/plataforma/unificar-usuario-shift)