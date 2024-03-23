# SQL Server

## Caminho dos arquivos de dados do SQL Server de produção

Os arquivos de dados e logs de cada banco do SQL Server em produção (192.168.10.9) 
ficam no seguinte diretório: 

**E:/SqlServer/MSSQL12.MSSQLSERVER/MSSQL/DATA/**

## O que fazer em caso do servidor de banco de dados ficar cheio?

Quando acontece de ficar sem espaço a primeira coisa que podemos fazer é apagar o conteudo dessas pastas:

- E:\Backup\Completo
- E:\Backup\Diferencial
- E:\Backup\Log

Só isso já libera algum espaço.

Para liberar mais espaço, fazer o processo de Shrink dos logs dos bancos.
## Listar todos os jobs do SQL Server

O comando abaixo lista todos os jobs do SQL Server Agent

**Referência***: https://www.mssqltips.com/sqlservertip/2561/querying-sql-server-agent-job-information/

```sql
SELECT 
    [sJOB].[job_id] AS [JobID]
    , [sJOB].[name] AS [JobName]
    , [sDBP].[name] AS [JobOwner]
    , [sCAT].[name] AS [JobCategory]
    , [sJOB].[description] AS [JobDescription]
    , CASE [sJOB].[enabled]
        WHEN 1 THEN 'Yes'
        WHEN 0 THEN 'No'
      END AS [IsEnabled]
    , [sJOB].[date_created] AS [JobCreatedOn]
    , [sJOB].[date_modified] AS [JobLastModifiedOn]
    , [sSVR].[name] AS [OriginatingServerName]
    , [sJSTP].[step_id] AS [JobStartStepNo]
    , [sJSTP].[step_name] AS [JobStartStepName]
    , CASE
        WHEN [sSCH].[schedule_uid] IS NULL THEN 'No'
        ELSE 'Yes'
      END AS [IsScheduled]
    , [sSCH].[schedule_uid] AS [JobScheduleID]
    , [sSCH].[name] AS [JobScheduleName]
    , CASE [sJOB].[delete_level]
        WHEN 0 THEN 'Never'
        WHEN 1 THEN 'On Success'
        WHEN 2 THEN 'On Failure'
        WHEN 3 THEN 'On Completion'
      END AS [JobDeletionCriterion]
FROM
    [msdb].[dbo].[sysjobs] AS [sJOB]
    LEFT JOIN [msdb].[sys].[servers] AS [sSVR]
        ON [sJOB].[originating_server_id] = [sSVR].[server_id]
    LEFT JOIN [msdb].[dbo].[syscategories] AS [sCAT]
        ON [sJOB].[category_id] = [sCAT].[category_id]
    LEFT JOIN [msdb].[dbo].[sysjobsteps] AS [sJSTP]
        ON [sJOB].[job_id] = [sJSTP].[job_id]
        AND [sJOB].[start_step_id] = [sJSTP].[step_id]
    LEFT JOIN [msdb].[sys].[database_principals] AS [sDBP]
        ON [sJOB].[owner_sid] = [sDBP].[sid]
    LEFT JOIN [msdb].[dbo].[sysjobschedules] AS [sJOBSCH]
        ON [sJOB].[job_id] = [sJOBSCH].[job_id]
    LEFT JOIN [msdb].[dbo].[sysschedules] AS [sSCH]
        ON [sJOBSCH].[schedule_id] = [sSCH].[schedule_id]
ORDER BY [JobName]
```


## Executar um job do SQL Server Agent

**Referência***: https://docs.microsoft.com/en-us/sql/linux/sql-server-linux-run-sql-server-agent-job?view=sql-server-ver15

```sql
USE msdb ;
GO
EXEC dbo.sp_start_job N'Nome do JOB aqui!' ;
GO

```


## Buscar job que usa determinada tabela ou comando

Para saber qual JOB chama determinada tabela, view, procedure, etc, basta usar o comando abaixo:

```sql 
use msdb;

SELECT 
	[database_name],
	name,
	step_name,
	step_id,
	command
FROM 
	sysjobsteps
	INNER JOIN sysjobs ON sysjobs.job_id = sysjobsteps.job_id
WHERE 
	UPPER(sysjobsteps.command) LIKE '%Trecho a ser procurado dentro do comando executado no job%'
```


## Buscar job com última execução em determinada data e horário

A consulta abaixo retorna os jobs no qual a última execução seja maior que uma data e um horário.

**OBS 1:** A data precisa estar no formado **YYYYMMDD** e o horário no formado **HHMMSS**

**OBS 2:** Trocar a data nas seguintes linhas: "AND sysjobsteps.last_run_date >= 20220209 AND sysjobsteps.last_run_time >= 190000"

```sql
SELECT 
    sysjobs.name,
    sysjobs.date_created,
    sysjobs.date_modified,
    sysjobsteps.last_run_date,
    sysjobsteps.last_run_time,
    sysjobsteps.last_run_duration,
    sysjobsteps.command
FROM 
    msdb.dbo.sysjobs AS sysjobs
    LEFT JOIN msdb.sys.servers AS servers
        ON sysjobs.originating_server_id = servers.server_id
    LEFT JOIN msdb.dbo.syscategories AS syscategories
        ON sysjobs.category_id = syscategories.category_id
    LEFT JOIN msdb.dbo.sysjobsteps AS sysjobsteps
        ON sysjobs.job_id = sysjobsteps.job_id
        AND sysjobs.start_step_id = sysjobsteps.step_id
    LEFT JOIN msdb.sys.database_principals AS database_principals
        ON sysjobs.owner_sid = database_principals.sid
    LEFT JOIN msdb.dbo.sysjobschedules AS sysjobschedules
        ON sysjobs.job_id = sysjobschedules.job_id
    LEFT JOIN msdb.dbo.sysschedules AS sysschedules
        ON sysjobschedules.schedule_id = sysschedules.schedule_id
WHERE sysjobs.enabled = 1
    AND sysschedules.schedule_uid IS NOT NULL
    AND sysjobsteps.last_run_date >= 20220209
    AND sysjobsteps.last_run_time >= 190000
ORDER BY 
    last_run_time, 
    last_run_duration DESC
```


## Listar as tabelas com maior tamanho no SQL Server

A consulta abaixo lista as maiores tabelas no banco de dados SQL Server, 
ordenando a maior para a menor.

```sql
SELECT
    tables.NAME AS Entidade,
    partitions.rows AS Registros,
    SUM(allocation_units.total_pages) * 8 AS EspacoTotalKB,
    SUM(allocation_units.used_pages) * 8 AS EspacoUsadoKB,
    (SUM(allocation_units.total_pages) - SUM(allocation_units.used_pages)) * 8 AS EspacoNaoUsadoKB
FROM
    sys.tables AS tables
INNER JOIN sys.indexes AS indexes 
    ON tables.OBJECT_ID = indexes.object_id
INNER JOIN sys.partitions AS partitions 
    ON indexes.object_id = partitions.OBJECT_ID 
    AND indexes.index_id = partitions.index_id
INNER JOIN sys.allocation_units AS allocation_units 
    ON partitions.partition_id = allocation_units.container_id
LEFT OUTER JOIN sys.schemas AS schemas 
    ON tables.schema_id = schemas.schema_id
WHERE
    tables.NAME NOT LIKE 'dt%'
    AND tables.is_ms_shipped = 0
    AND indexes.OBJECT_ID > 255
GROUP BY
    tables.Name, 
    partitions.Rows
ORDER BY
    Registros DESC
```


## Listar todos os processos do SQL Server

O comando abaixo lista todos os processos do SQL Server.

O normal é que os processos abaixem a quantidade rapidamente, caso tenha muitos processos (Ex: 30 processos)
que não finalizam rapidamente, provavelmente o SQL Server está com algo travado.

```sql
SELECT
    Processo = spid,
    Computador = hostname,
    Usuario = loginame,
    Status = status,
    BloqueadoPor = blocked,
    TipoComando = cmd,
    Aplicativo = program_name
FROM master..sysprocesses
WHERE status in ('runnable', 'suspended')
ORDER BY blocked desc, status, spid
```

Para matar o processo, basta digitar o seguinte comando:

```sql
KILL numero_do_processo_aqui
```
