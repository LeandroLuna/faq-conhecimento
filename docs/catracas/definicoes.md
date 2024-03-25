# Definições
Para entender melhor a organização que define se um usuário pode ou não acessar um local, tenha em mente as seguintes
definições:

##Catraca ou Ponto de acesso
São os dispositivos onde o usuário deve passar o cartão de acesso para poder acessar algum local da FIAP.

##Local
São os ambientes da FIAP que possuem catracas para serem acessados.

Exemplo: Entrada principal, aquário, sala do servidor, etc.

##Usuário
É quem deseja acessar a FIAP ou algum dos seus ambientes. Pode ser do tipo Colaborador, Graduação, Visitante, etc. Para realizar
o acesso, o usuário deve passar o cartão de acesso por uma catraca.

##Cartão de acesso
São cartões disponibilizados para usuários que podem ter acesso à FIAP durante um período. Esses cartões possuem duas chaves
de acesso, quando passado, uma delas é informada à catraca no momento da tentativa de acesso:

- Código de barras **(C)**: informado à catraca caso o cartão seja passado em um leitor de código de barras.
Para os alunos, esse código é o próprio RM.
**Obs.: Por conflito de range, existem duplicidades entre Graduação-Visitante e Colaborador-Colégio.**
- Aproximação **(A)**: código RFID do cartão, gerado aleatoriamente, que pode ser verificado no verso do cartão. Atualmente, é o mais
utilizado nas catracas, pelo fato do leitor de código de barras estar em processo de descontinuação. Diferente do código de barras,
não permite duplicidade.

##Perfil
É um papel que ajuda a identificar a quais locais um usuário pode ter acesso, em dias e horários previamente definidos.
Normalmente, está atrelado ao tipo do usuário, como também ao seu curso e turma.

Exemplo: O perfil de Colaborador pode acessar os locais permitidos em qualquer horário que desejar, enquanto o perfil de Ensino Fundamental
I só pode passar por uma catraca das 6h-8h (entrada) e das 12h10-15h (saída).

###Mapeamentos
Como visto no [processo de acesso](acesso.md), para que o aluno tenha acesso à FIAP, ele precisa possuir um perfil que possua permissão a
locais. Quando um novo usuário é inserido no sistema, é importante que ele seja incluído automaticamente num perfil que concorde
com os ambientes que ele pode entrar, para que já possa iniciar o uso do cartão.

Esses mapeamentos podem ser definidos conforme o tipo, curso, turma, ano e outros dados do usuário que são informados no momento da
importação.

Exemplo: O Perfil *Colaborador* é inserido para todos os usuários que são do tipo Colaborador, enquanto o perfil *Ensino Médio Técnico*
é inserido para todos os usuários que são do tipo Colégio e do curso Ensino Médio Técnico.

**Obs.: Nem todos os perfis existentes são adicionados automaticamente aos usuários, como, por exemplo, o perfil *Sala de segurança*,
concedido de forma manual somente a colaboradores específicos.**
