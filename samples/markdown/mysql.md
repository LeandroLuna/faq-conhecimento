# MySQL

Esta página tem como objetivo documentar configurações e processos que são realizados
frequentemente nas instalações do MySQL.

## Clonar uma base de dados

Para clonar uma base de dados basta utilizar o comando abaixo no terminal.

```shell
mysqldump nome_da_database_1 \
--host=endereco_do_host_1 \
--port=3306 \
--user=usuario \ 
--password=senha \
--single-transaction \
--compress \
--no-create-db \
--skip-add-locks \
--skip-comments | mysql \
--host=endereco_do_host_2 \
--port=3306 \
--user=usuario \ 
--password=senha nome_da_database_2
```

## Remover agrupamento por todos itens selecionados

Normalmente quando queremos utilizar **group by**, devemos agrupar por todos os campos
que estamos usando no **SELECT**. Quando queremos agrupar apenas por alguns campos
usando, basta rodar o comando abaixo no banco.

```sql
SET SESSION sql_mode = 'STRICT_ALL_TABLES'
```

## Encontrar duplicatas

Para encontrar duplicatas em seu banco de dados, basta rodar o seguinte comando:

```sql
SELECT 
	todas_as_colunas_da_sua_tabela
    COUNT(*) as duplicatas
FROM sua_tabela
WHERE condicoes
GROUP BY
	todas_as_colunas_da_sua_tabela
HAVING duplicatas > 1
```

## Remover duplicatas

Para remover as duplicatas do seu banco de dados, faça um ***INNER JOIN*** com a própria tabela
em que elas se encontram, dando apelidos para as duas.

No ***WHERE***, compare todas as colunas da sua tabela que sejam relevantes para dizer
que aquele registro é uma duplicata.

**A Primeira condição do WHERE deve comparar o ID como exemplificado abaixo, para que
sejam deletadas apenas as duplicatas, e não todos os registros**.

```sql
DELETE apelido_tabela_1
FROM tabela apelido_tabela_1
INNER JOIN tabela apelido_tabela_2
WHERE apelido_tabela_1.id > apelido_tabela_2.id
    AND apelido_tabela_1.campo1 = apelido_tablea_2.campo1
    AND apelido_tabela_1.campo2 = apelido_tablea_2.campo2
```