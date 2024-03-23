# Transaction

## O que são Transactions (Transações) em banco de dados

Transações são uma forma de executar comandos no SQL com a **possibilidade de revertê-los**, caso necessário.

Normalmente, utilizamos uma transação para **evitar a perda de dados** em caso de comandos digitados de forma errônea.

Podemos utilizar também como uma forma de **executar comandos aos poucos**, e caso esteja tudo certo, efetivar as alterações no final.

## Como utilizar transações

Para iniciar uma transação, execute a seguinte linha juntamente ao comando desejado:

```sql
BEGIN TRANSACTION
```

Uma vez iniciada a transação, todas os **comandos feitos nesta mesma aba estarão dentro da transação**, e serão reversíveis.

Caso o resultado da alteração seja o esperado, rode a seguinte linha para efetivá-la:

```sql
COMMIT TRANSACTION
```

Caso contrário, se algo de errado tiver ocorrido (mesmo que não tenha lançado explicitamente um erro), execute a seguinte linha para cancelar as alterações feitas na transação:

```sql
ROLLBACK TRANSACTION
```

## Implementando uma transação com finalização automática no SQL Server

```sql
BEGIN TRANSACTION
DELETE FROM banco..tabela WHERE campo = 'XXXX';
IF @@ERROR = 0 COMMIT ELSE ROLLBACK;
```

## Implementando uma transação com finalização automática no MySQL

```sql
START TRANSACTION;
DELETE FROM banco..tabela WHERE campo = 'XXXX';
COMMIT; # ou use ROLLBACK;
```

## Atenção ao utilizar transações

Ao iniciar uma transação, as **tabelas** onde as alterações estão sendo realizadas ficam **bloqueadas**.
Desta forma, quando uma transação está em execução, outros usuários (ou até mesmo você, caso esteja usando outra aba do SQL) não conseguirão efetuar consultas imediatas nesta tabela.
Uma consulta comum feita a uma tabela que está em transação ficará pendente (carregando) até que a transação seja finalizada (efetivada ou cancelada).

Para efetuar uma **consulta imediata** a uma tabela, independentemente se ela está bloqueada por uma transação ou não, basta adicionar o comando **WITH (NOLOCK)** à consulta, desta forma:

```sql
-- Insira o comando após o nome da tabela
SELECT
    *
FROM
    Banco..Tabela WITH (NOLOCK)
WHERE
    Codigo = 10
    
-- Ou, caso esteja usando um Alias, insira o comando após o alias da tabela
SELECT
    *
FROM
    Banco..Tabela AS Tb WITH (NOLOCK)
WHERE
    Codigo = 10
```

**OBS:** Nessa consulta, os dados que serão retornados **já terão sofrido as alterações** que estão em transação (mesmo que a transação não seja efetivada posteriormente).

## Buscando transações pendentes (em execução) no SQL Server

```sql
SELECT
	trans.session_id AS [SESSION ID],
	ESes.host_name AS [HOST NAME],
	login_name AS [LOGIN NAME],
	trans.transaction_id AS [TRANSACTION ID],
	tas.name AS [TRANSACTION NAME],
	tas.transaction_begin_time AS [TRANSACTION BEGIN TIME],
	tds.database_id AS [DATABASE ID],
	DBs.name AS [DATABASE NAME]
FROM 
	sys.dm_tran_active_transactions AS tas
	INNER JOIN sys.dm_tran_session_transactions AS trans
		ON trans.transaction_id = tas.transaction_id
	LEFT OUTER JOIN sys.dm_tran_database_transactions AS tds
		ON tas.transaction_id = tds.transaction_id
	LEFT OUTER JOIN sys.databases AS DBs
		ON tds.database_id = DBs.database_id
	LEFT OUTER JOIN sys.dm_exec_sessions AS ESes
		ON trans.session_id = ESes.session_id

WHERE 
	ESes.session_id IS NOT NULL
```