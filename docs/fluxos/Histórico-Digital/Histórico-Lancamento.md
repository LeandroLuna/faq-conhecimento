# Processo de Atualização de Registros do Histórico Escolar

Esta documentação descreve o procedimento de atualização de registros no histórico escolar, onde as tabelas `HistoricoLancamento`, `HistoricoLancamentoB`, e `HistoricoLancamentoF` desempenham um papel fundamental. Além disso, é apresentada a tabela `LancHistoricoTempProcessadoAnteriormente`, que armazena dados previamente processados na tabela `HistoricoLancamento`. Neste contexto, é aplicada uma rotina que analisa as mudanças feitas nos registros previamente processados, tais como turma e nota. 

Essas tabelas e o processo de atualização associado são empregados nos sistemas de registro acadêmico da FIAP, incluindo a plataforma Intranet3 (seção Alunos > Histórico Escolar) e o sistema de histórico escolar digital integrado à nova intranet. Todas essas tabelas estão presentes no banco de dados `site_fiap`.

## **Contexto**

A atualização de registros no histórico escolar ocorre diariamente para garantir a precisão e a integridade das notas registradas. Esse processo envolve a transferência de dados entre as tabelas `HistoricoLancamento`, `HistoricoLancamentoB` e `HistoricoLancamentoF`. Além disso, a tabela `LancHistoricoTempProcessadoAnteriormente` é utilizada para armazenar registros previamente processados da tabela `HistoricoLancamento`.

## **Detalhes do Processo**

### **Tabela: HistoricoLancamento**

A tabela `HistoricoLancamento` atua como a fonte primária de dados para a atualização dos registros. Ela contém os lançamentos de notas que requerem ajustes e refinamentos ao longo do tempo.

### **Tabela: HistoricoLancamentoB**

A tabela `HistoricoLancamentoB` é utilizada como um ambiente de trabalho intermediário. Quando um novo histórico é iniciado, os dados da tabela `HistoricoLancamento` são replicados para essa tabela, permitindo aos usuários fazer edições sem afetar os dados originais.

### **Ajustes e Edições**

Os usuários têm a capacidade de realizar ajustes e edições nos registros presentes na tabela `HistoricoLancamentoB`. Isso possibilita corrigir erros, inserir informações adicionais ou efetuar outras alterações necessárias.

### **Finalização do Histórico**

Quando os ajustes e edições são concluídos e o histórico está pronto para ser finalizado, o conteúdo da tabela `HistoricoLancamentoB` é copiado para a tabela `HistoricoLancamentoF`.

### **Tabela: HistoricoLancamentoF**

A tabela `HistoricoLancamentoF` abriga os registros de histórico de lançamentos que passaram por ajustes, revisões e foram finalizados pelos usuários. Esses registros são considerados a versão definitiva e precisa do histórico de lançamentos.

### **Tabela: LancHistoricoTempProcessadoAnteriormente**

A tabela `LancHistoricoTempProcessadoAnteriormente` armazena dados que foram processados previamente na tabela `HistoricoLancamento`. Uma rotina é aplicada para analisar as mudanças feitas nos registros processados anteriormente, incluindo turma, nota, entre outros.

## **Reprocessamento de Dados de Grade do Histórico**

Em determinadas situações, é possível realizar o reprocessamento dos dados de grade do histórico do aluno seguindo os passos descritos abaixo:

#### Passo 1: Exclusão dos Registros de Histórico

Primeiramente, é necessário executar o script SQL a seguir para excluir os registros referentes ao histórico do aluno desejado. Esses registros serão posteriormente resgatados e ajustados no próximo passo.

```sql
-- Substitua o valor '12345' pelo RM do aluno desejado
DECLARE @rm INT = 12345;

DELETE FROM HistoricoLancamento WHERE RM = @rm;
DELETE FROM HistoricoLancamentoB WHERE RM = @rm;
DELETE FROM HistoricoLancamentoF WHERE RM = @rm;
DELETE FROM HistoricoDados WHERE RM = @rm;
DELETE FROM HistoricoDadosB WHERE RM = @rm;
DELETE FROM LancHistoricoTempProcessadoAnteriormente WHERE RM = @rm;
```

#### Passo 2: Execução do Job de Atualização do Histórico

A seguir, é necessário executar o job chamado `Atualiza Histórico`. Esse job irá reprocessar os registros de grade do histórico, restaurando e ajustando esses dados.

**Observação**: A execução de um job está restrita a usuários autorizados e deve ser realizada apenas no ambiente de produção. Para mais detalhes sobre como executar um job no SQL Server, consulte a documentação [O que é um Job SQL Server](http://conhecimento.fiap.com.br/tabelas/buscando-jobs-em-producao/buscando-jobs-em-producao/).

## **Conclusão**

O procedimento de atualização de registros no histórico escolar envolve a transferência controlada de dados entre as tabelas `HistoricoLancamento`, `HistoricoLancamentoB`, `HistoricoLancamentoF` e `LancHistoricoTempProcessadoAnteriormente`. Isso permite aos usuários realizar edições e ajustes nos registros de maneira segura, garantindo a manutenção de um histórico preciso das notas. Ao seguir esse processo, é possível assegurar a integridade e a precisão das informações no histórico escolar ao longo do tempo.