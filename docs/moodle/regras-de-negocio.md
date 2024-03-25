#Regras de negócio

##Exibição de conteúdos

###De acordo com a configuração do curso
Na página de criação/edição de um curso, na seção *Formatos de exibição* é
possível selecionar quais tipos de conteúdos serão exibidos na página principal.
Caso um conteúdo não esteja selecionado, este não terá o seu ícone exibido na página
do curso.

###De acordo com a disponibilidade do conteúdo
Caso um conteúdo ainda não esteja aberto (data de abertura maior que atual) ou já
esteja fechado (data de fechamento menor que atual), ele deve ser exibido
na página do curso desabilitado.

###De acordo com término do curso

**Caso o curso seja SHIFT Presencial**
- Possui apenas conteúdos PDF, que devem sempre permanecer disponíveis.

**Caso o curso seja SHIFT NO STOP**
- Deve exibir todos os conteúdos a partir da data de inscrição do aluno + o
  tempo de duração do curso + um período de 60 dias;
- Após excedido este período, apenas os conteúdos HTML devem permanecer habilitados.

**Caso o curso seja Nano Course**
- Deve exibir todos os conteúdos até um período de dois anos após o ano em que o aluno foi registrado;
- Após isso, apenas os conteúdos HTML devem permanecer habilitados.

**Caso o curso possua uma data de fechamento**
- Deve exibir todos os conteúdos enquanto o curso está aberto + um período de
  60 dias;
- Após excedido este período, apenas os conteúdos HTML devem permanecer habilitados.

**Caso o curso não possua uma data de fechamento**
- Deve exibir todos os conteúdos.

##Regras da Plataforma
Todos os cursos cadastrados na plataforma devem possuir uma “Regra de Exibição”. Esta regra
define:

- Como o curso será exibido no menu;
- Como e por onde os alunos serão importados;
- O formato de exibição dos nano courses;
- O formato de exibição das lives;
- Quais ícones no menu e funcionalidades da plataforma o aluno terá acesso;
- Como irá ocorrer o envio de nota para o boletim em atividades do curso;
- Se os nano courses valem nota para o boletim;
- As regras de exibição dos conteúdos.

*Todas as regras ficam disponíveis no arquivo lib/fiap/regra_and_resume.php e
na tabela fiapead_fiap_regras.*