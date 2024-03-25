# Script de Busca de Triggers e Procedures

Este script SQL tem a finalidade de buscar procedures e triggers em bancos de dados SQL Server pelo nome ou pelo conteúdo.

## Como usar

1. Copie o conteúdo do script para um arquivo .sql.

2. Substitua `%SUA_BUSCA_AQUI%` pela string que deseja buscar, seja pelo nome da procedure/trigger ou por parte do seu conteúdo.

3. Execute o script em um ambiente com acesso a um servidor SQL Server e permissões adequadas para consultar os bancos de dados.

4. O script percorrerá todos os bancos de dados disponíveis no servidor e retornará os resultados contendo o nome do banco de dados, o tipo de objeto (procedure ou trigger) e a localização onde foi encontrado.

## Detalhes da Query

O script utiliza um cursor para iterar sobre todos os bancos de dados disponíveis no servidor SQL Server.

Para cada banco de dados, são executadas duas consultas dinâmicas:

Busca por procedures que contenham a string de busca fornecida no conteúdo de sua definição (sys.procedures e sys.sql_modules).
Busca por triggers que contenham a string de busca fornecida no conteúdo de sua definição, incluindo o nome da tabela associada (sys.objects e sys.sql_modules).
Os resultados das consultas são formatados para incluir informações sobre o banco de dados, o tipo de objeto (procedure ou trigger) e a localização onde foi encontrado.

O uso de UNION combina os resultados das duas consultas em uma única lista de resultados.

O cursor continua iterando até que não haja mais bancos de dados para percorrer.

Essa abordagem permite buscar procedures e triggers em todos os bancos de dados disponíveis, tanto pelo nome quanto pelo conteúdo de sua definição, fornecendo informações detalhadas sobre sua localização.

```sql
DECLARE @ValorBusca VARCHAR(MAX) = LOWER('%SUA_BUSCA_AQUI%')


DECLARE BancosCursor CURSOR FOR  
    SELECT
        [name] as 'NomeBanco'
    FROM
        sys.databases;  
DECLARE @NomeBanco VARCHAR(100)

OPEN BancosCursor;  
FETCH NEXT FROM BancosCursor INTO @NomeBanco;  
WHILE @@FETCH_STATUS = 0  
BEGIN
    EXECUTE('USE ' + @NomeBanco+';' +
        '
            SELECT
                CONCAT(''No banco: '', '''+@NomeBanco+''','' procedure: '',procedures.name) AS ''Localizacao''
            FROM
                sys.procedures WITH (NOLOCK)
                INNER JOIN sys.sql_modules WITH (NOLOCK)
                    ON procedures.object_id = sql_modules.object_id
            WHERE
                LOWER(sql_modules.definition) LIKE '''+@ValorBusca+'''
            
            UNION
            
            SELECT
                CONCAT(''No banco: '', '''+@NomeBanco+''','' trigger: '',myTrigger.name, '' na tabela: '', myTable.name) AS ''Localizacao''
            FROM
                sys.sql_modules WITH (NOLOCK)
                INNER JOIN sys.objects AS myTrigger WITH (NOLOCK)
                    ON sql_modules.object_id = myTrigger.object_id
                INNER JOIN sys.objects AS myTable WITH (NOLOCK)
                    ON myTrigger.parent_object_id = myTable.object_id
            WHERE
                LOWER(sql_modules.definition) LIKE '''+@ValorBusca+''';
        '
    )

    FETCH NEXT FROM BancosCursor INTO @NomeBanco;  
END;  
  
CLOSE BancosCursor;  
DEALLOCATE BancosCursor;
```
