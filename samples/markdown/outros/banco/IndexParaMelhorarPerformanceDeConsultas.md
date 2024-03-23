# INDEX - Melhorando Performance de Consultas (SELECTs)

## O que são Indexes (Índices) em banco de dados

O **INDEX** é um recurso do SQL que permite definir a forma como os registros da 
tabela serão **organizados**, otimizando a consulta de determinados tipos de 
filtro.

## Como funcionam os Indexes

Os **Indexes** conseguem **aumentar a performance** de consultas em tabelas, 
pois com eles a estrutura da tabela é organizada como uma **árvore de páginas**, 
para que seja possível realizar a busca sem precisar iterar todos os registros 
da tabela.

Ao definir uma coluna como **PRIMARY KEY**, o SQL adiciona automaticamente um 
**Clustered Index** nessa tabela, atrelado a esta coluna. Assim, a estrutura da 
tabela é reorganizada e, quando buscamos filtrando por esta coluna, o 
procedimento realizado é o seguinte:

<img src="../EstruturaIndex_ClusterizadoENaoClusterizado.png" style="width: fit-content;">

- O **Nó Raiz** e os **Nós das camadas Intermediárias** direcionam a busca de 
forma similar a uma "**Busca Binária**" (**Binary Search**) ou a um 
**Índice de Livro**, até que a página correta da camada de **Nós-Folha** seja 
encontrada. Esta busca é denominada **Seek**, pois encontra os registros 
pontualmente.

- Cada **Nó-Folha** armazena as informações (colunas) de determinada porção de 
registros.

```
Obs.: Uma tabela que não possui nenhum Index é chamada de Heap ("monte"), pois não possui uma organização definida.
Desta forma, qualquer busca realizada nesta tabela é do tipo Scan, iterando todos os seus registros.
```

Existem 2 principais tipos de Índice: **Clustered Index** e 
**Non Clustered Index**. A diferença básica entre eles é a lista de informações 
que são salvas nos **Nós-Folha** da árvore de páginas;

## Clustered Index

Uma tabela pode ter no máximo um **Clustered Index** (Índice clusterizado), e 
ele armazena **todas as informações** (colunas) de cada registro nos 
**Nós-Folha**. 
Como é o caso de um **Índice de Primary Key**.

Ao realizar uma busca por uma coluna com **Índice Clusterizado**, é feita apenas 
uma busca do tipo **Seek** (encontrando o registro pontualmente) e as informações 
necessárias para serem exibidas já terão sido encontradas. 

## Exemplo de criação de um Clustered Index

O script abaixo cria um Índice clusterizado na tabela **NomeTabela**, 
organizando o registros em uma árvore de páginas, de acordo com as colunas 
**NomeColuna1** e **NomeColuna2**. Os **Nós-folha** possuem informações de todas 
as colunas da tabela.

```sql
CREATE CLUSTERED INDEX IND_NomeTabela_NomeColuna1_NomeColuna2
ON NomeTabela (NomeColuna1, NomeColuna2)
```

## Non Clustered Index

Uma tabela pode ter vários **Non Clustered Indexes** (Índices não-clusterizados). 
Eles armazenam nos **Nós-Folha** essencialmente a **Primary Key** do registro 
buscado, mas também podem conter informações de uma **lista de colunas** 
definidas no momento da criação do **Index**.

Quando é feito um filtro por uma coluna com **Índice Não Clusterizado**, é 
realizada uma busca do tipo **Seek** para encontrar as **Primary Key's** e em 
seguida, caso falte uma ou mais informações dentre as solicitadas, ainda será 
necessário buscá-las no **Índice Clusterizado** da tabela, caso exista. Caso 
contrário, será feita uma busca **Scan**, iterando todos os registros da tabela.

## Exemplo de criação de um Non Clustered Index 

O script abaixo cria um Índice não-clusterizado na tabela **NomeTabela**, 
organizando o registros em uma árvore de páginas, de acordo com as colunas 
**NomeColuna1** e **NomeColuna2**. Os **Nós-folha**, além da informação da 
**PRIMARY KEY**, armazenam também as informações das colunas **NomeColuna3**, 
**NomeColuna4** e **NomeColuna5**.

```sql
CREATE INDEX IND_NomeTabela_NomeColuna1_NomeColuna2
ON NomeTabela (NomeColuna1, NomeColuna2)
-- Trecho opcional que define as colunas extras dos Nós-Folha
INCLUDE (NomeColuna3, NomeColuna4, NomeColuna5); 
```

## Exibindo os Indexes de uma tabela

```sql
USE NomeBase;
GO

-- Exibindo detalhes da tabela, inclusive os Índices criados
sp_help NomeTabela;
-- OU
-- Selecione o nome da tabela e pressione Alt+F1 para obter o mesmo resultado
```

## Prós e Contras de utilizar Indexes

A utilização de Indexes pode **aumentar a performance** das consultas, mas para 
isso, é utilizado certo **espaço de memória** para armazenar estas estruturas. 
Além disso, podem diminuir a performance de **INSERT's**, **UPDATE's** e 
**DELETE's**, pois os Indexes precisaram ser **atualizados** quando estes 
comandos são executados.