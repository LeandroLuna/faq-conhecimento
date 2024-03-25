#Acesso

Para ter acesso às unidades I e II da FIAP, e a alguns dos seus ambientes - como sala do servidor, por exemplo -,
os usuários devem passar antes por uma catraca. Para isso, devem encostar (em caso de aproximação) ou passar
(em caso de leitor de código de barras) o cartão de acesso fornecido pelo Help Center, RH ou recepção (no caso
dos visitantes).

Para que um usuário tenha permissão para passar por determinada catraca, é realizada uma verificação, seguindo o
seguinte fluxo:

<div style="height: 390px; overflow-x:scroll;">
    <img src="/processos/catracas/acesso.svg" style="max-width: initial;" alt="Processo de acesso às catracas">
</div>

A API que a catraca consome consulta diretamente de uma tabela chamada **CEPesquisa**.

Essa tabela foi criada para atender à necessidade do tempo de resposta para o usuário ser muito rápido, validando quase
que instantaneamente se ele possui acesso ou não. Nela, estão centralizadas todas as informações como usuário, cartão,
local e horários (apenas de cartões ativos).

Ela é regerada através da procedure **ProcessamentoCEPesquisa**, chamada através de um CRON do Jenkins a cada 10 minutos
ou manualmente, por um botão disponibilizado no sistema.

##Acesso por liberação manual

Existem casos em que pessoas que não possuem cartões de acesso queiram acessar a FIAP, como alunos que perderam/esqueceram
a carteirinha ou ainda não pagaram por ela. Por isso, os funcionários da recepção tem a possibilidade de realizarem a liberação
da catraca manualmente, através do sistema.

Atualmente, apenas as catracas "Catraca 1 - Unidade I" e "Catraca 10 - Unidade II" da entrada principal podem ter seu
acesso liberado dessa forma.

<div style="height: 460px; overflow-x:scroll;">
    <img src="/processos/catracas/liberacao-manual.svg" style="max-width: initial;" alt="Processo de acesso às catracas via liberação manual">
</div>

#TODO

- Explicar mais minunciosamente a relação entre perfil > local > catracas > liberação;

!!! warning "Atenção"
    Página em construção
