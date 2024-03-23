## Introdução
A Prova Online é um projeto .NET / Angular.js que utiliza frameworks como SignalR para integrar em tempo real dados dos alunos com o banco de dados SQL Server

## Questões
As questões estão cadastradas no banco `site_fiap` na tabela `POQuestoes`
```sql
SELECT * FROM site_fiap..POQuestao ORDER BY Codigo DESC
```
As questões são importadas utilizando uma [ferramenta](https://gitlab.fiap.com.br/dotnet/ImportadorQuestoesMoodle.Desktop) que se conecta ao servidor do Moodle, busca as questões por categorias e importa na nossa base de dados

As alternativas das questões se encontram na tabela `POQuestaoAlternativa`, com o bit `Correta` indicando a alternativa correta. O Código da questão na base da FIAP e na base do Moodle se encontram nessa tabela.

### Consultar uma questão
Para consultar uma questão e suas alternativas, é necessário fazer um **INNER JOIN** entre as tabelas `POQuestaoAlternativa` e `POQuestao`.
```sql
SELECT 
    POQuestao.Codigo AS 'CodigoQuestao',
    POQuestao.Pergunta,
    POQuestaoAlternativa.Codigo AS 'CodigoAlternativa',
    POQuestaoAlternativa.Alternativa,
    POQuestaoAlternativa.Correta
FROM
    POQuestao
    INNER JOIN POQuestaoAlternativa ON POQuestaoAlternativa.CodigoQuestao = POQuestao.Codigo
WHERE
    POQuestao.Codigo=999999 AND
    POQuestao.Ativo=1 AND
    POQuestao.Anulada = 0
```

### Anular uma questão
Para anular uma questão, deve-se atualizar o bit `Anulada` da linha da tabela POQuestao referente a questão desejada
```sql
UPDATE site_fiap..POQuestao SET Anulada = 1 WHERE Codigo = 999999
```

!!! danger "Atenção"
    É necessário [re-calcular](/fiap/prova-online/notas/#calcular-notas-novamente) as notas dos alunos quando uma questão é anulada