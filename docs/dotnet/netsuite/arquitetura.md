# F. Arquitetura de monitoramento
Uma vez que este projeto se trata de manter os dados da FIAP com a plataforma da NetSuite sincronizados, mantendo integridade e consistência, como também priorizando a performance do banco de dados e a segregação de regras de negócio numa aplicação .NET, foram selecionadas ferramentas específicas para esse fim. 

Nesta documentação estão descritos detalhes de implementação do projeto, desde a arquitetura utilizada no monitoramento do banco de dados, utilizando RabbitMQ e Debezium, até a implementação dos consumers em .NET Core e MassTransit.

## Arquitetura Orientada a Eventos
O projeto em questão visa reproduzir eventos ocorridos no banco de dados da FIAP na plataforma da NetSuite em tempo real, por conta disso, optou-se por uma arquitetura orientada a eventos. Nesse contexto, a tecnologia escolhida para disparar os eventos de transação SQL foi o Debezium, enquanto o sistema de mensageria RabbitMQ foi adotado para distribuir esses eventos entre as aplicações consumidoras. Detalhes mais aprofundados sobre ambas as tecnologias serão apresentados nos tópicos seguintes.

## Monitoramento do Banco de Dados
O monitoramento do banco de dados é realizado por meio da tecnologia [Debezium](https://debezium.io/) que, a partir da funcionalidade de [Change Data Capture (CDC)](https://learn.microsoft.com/en-us/sql/relational-databases/track-changes/about-change-data-capture-sql-server?view=sql-server-ver16), consegue capturar todas as alterações ocorridas nas tabelas utilizadas para cada cenário de importação (veja a documentação [Cenários de importação]()). 

A partir das alterações capturadas pelo CDC, o Debezium possui a capacidade de publicá-las em sistemas de mensageria, como o Kafka e o RabbitMQ, possibilitando que aplicações consumidoras desenvolvidas em diferentes tecnologias possam consumir as mensagens produzidas.

### Change Data Capture
O Change Data Capture (CDC) é uma técnica de banco de dados projetada para identificar e capturar alterações (inserções, atualizações, exclusões) nos dados. Ao invés de scannear continuamente o banco de dados com queries desnecessárias, o CDC rastreia e captura especificamente apenas os dados que sofreram alterações desde a última inspeção. Essa abordagem simplifica o gerenciamento e a replicação de atualizações, retirando carga do banco de dados e melhorando a performance geral.

### Por que usar CDC com Debezium ao invés de CDC baseado em trigger?
O CDC baseado em trigger depende de triggers de banco de dados, operando a nível de SQL, com alguns SGBDs oferecendo suporte nativo para triggers em sua API SQL. A real eficácia deste método é apenas a captura de dados em tempo real. A razão para usar o Debezium ao invés do trigger é porque a sua abordagem CDC é baseada em logs de transação SQL.

O CDC baseado em triggers enfrenta desafios como manutenção complexa; comprometimento da performance do banco de dados devido à execução de lógica a nível de SQL; preocupações de escalabilidade devido à acumulação de triggers; dependência de regras sistêmicas, que podem levar a potenciais conflitos; e alto consumo de recursos em ambientes distribuídos. Em contraste, o CDC baseado em log, especialmente com o Debezium, opera eficientemente, não impacta o desempenho do banco de dados, é menos invasivo e integra-se facilmente a sistemas de mensageria como Kafka, RabbitMQ, Amazon Kinesis, etc. Isso permite o consumo dessas alterações em diferentes tecnologias e linguagens de programação, retirando carga e lógica de negócio do banco de dados.

Um ponto importante é que o Debezium também garante que as mensagens sejam produzidas na mesma ordem que as operações DML (INSERT, UPDATE e DELETE) foram realizadas, mantendo a consistência dos dados. Além disso, o Debezium, por ser um sistema distribuído, também possui vários [mecanismos de proteção](https://debezium.io/documentation/faq/#what_happens_when_an_application_stops_or_crashes) para o caso em que o seu serviço seja interrompido e também para prevenção de perda de mensagens, mantendo a integridade dos dados.

Devido aos requisitos demandados pelo projeto, essa foi a abordagem escolhida.

## Message Broker

Devido à simplicidade de utilização do [RabbitMQ](https://www.rabbitmq.com/) em comparação a outros message brokers, bem como a familiaridade da equipe com a tecnologia, este foi o sistema de mensageria escolhido para o projeto.

## Consumers

Para consumir os eventos de alteração de dados, foram desenvolvidas aplicações consumidoras (consumers) em .NET. Para isso, foi aplicado o framework [MassTransit](https://masstransit.io/), que oferece suporte a diversos padrões de mensageria, incluindo Publish/Subscribe, filas de mensagens, e outros padrões comuns em sistemas baseados em eventos. Desse modo, quando as mensagens referentes a esses eventos são publicadas nas filas, os respectivos consumers consomem essas mensagens e identificam os cenários os quais elas representam, executando o processamento correto para cada uma delas a partir de estrateǵias que foram implementadas para cada cenário (veja a documentação [Cenários de importação]()).

## Arquitetura Implementada
![Monitoring Architecture](images/arquitetura/monitoring_architecture.svg)

A Figura acima representa o modo como a arquitetura orientada a eventos foi implementada nesse projeto. Basicamente, todos os eventos de inserção, exclusão e atualização das tabelas que foram habilitadas com O CDC são capturados pelo Debezium. A partir disso, esses eventos são publicados como mensagens em `fanout exchanges` no RabbitMQ, que roteiam essas mensagens para as devidas filas. Desse modo, os consumers .NET identificam e consomem as mensagens que foram publicadas nas suas respectivas filas.

Quanto às `exchanges` criadas no RabbitMQ, existe uma para cada tabela. O nome delas foram configurados conforme a documentação do debezium: `prefixo.NomeBancoDados.dbo.NomeTabela`. O prefixo utilizado foi `netsuite`, para o ambiente FIAP, e `netsuite_modulo`, para o ambiente Módulo. Desse modo, foram utilizados os seguintes bindings:

<table>
    <tr>
        <td colspan=3><center><b>Bindings</b></center></td>
    </tr>
    <tr>
        <td><b>Exchange</b></td>
        <td><b>Fila</b></td>
        <td><b>Routing Key</b></td>
    </tr>
    <tr>
        <td>netsuite.BaseEducacional.dbo.FNDebitos</td>
        <td>netsuite_debit_monitoring_queue_fiap</td>
        <td>netsuite</td>
    </tr>
    <tr>
        <td>netsuite_modulo.BaseEducacional.dbo.FNDebitos</td>
        <td>netsuite_debit_monitoring_queue_modulo</td>
        <td>netsuite_modulo</td>
    </tr>
    <tr>
        <td>netsuite.Shift.dbo.AlunoCompra</td>
        <td>netsuite_shift_purchase_queue</td>
        <td>netsuite</td>
    </tr>
    <tr>
        <td>netsuite.Educacional.dbo.Pessoa</td>
        <td>netsuite_update_customer_queue_colegiograduacao</td>
        <td>netsuite</td>
    </tr>
    <tr>
        <td>netsuite_modulo.Educacional.dbo.Pessoa</td>
        <td>netsuite_update_customer_queue_modulo</td>
        <td>netsuite_modulo</td>
    </tr>
    <tr>
        <td>netsuite.WebAdm.dbo.pos_inscricao_new</td>
        <td>netsuite_update_customer_queue_posgraduacao</td>
        <td>netsuite</td>
    </tr>
    <tr>
        <td>netsuite.WebAdm.dbo.PI_InscricaoProcessoPessoaJuridica</td>
        <td>netsuite_update_customer_queue_posgraduacao_pj</td>
        <td>netsuite</td>
    </tr>
    <tr>
        <td>netsuite.Shift.dbo.Aluno</td>
        <td>netsuite_update_customer_queue_shift</td>
        <td>netsuite</td>
    </tr>
    <tr>
        <td>netsuite.Educacional.dbo.AlunoTurma</td>
        <td>netsuite_update_subsidiary_colegiograduacao</td>
        <td>netsuite</td>
    </tr>
    <tr>
        <td>netsuite.WebAdm.dbo.pos_inscricao_contrato</td>
        <td>netsuite_update_subsidiary_posgraduacao</td>
        <td>netsuite</td>
    </tr>
</table>

Mais detalhes sobre quais cenários foram utilizadas para as suas respectivas filas e, por consequência, quais as regras de negócio implementadas nos consumers, podem ser lidas na documentação de [Cenários de importação]().