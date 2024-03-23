# Criar tabelas de sessão

A criação das tabelas de sessão no SQL Server geralmente deve ser feita quando o banco é resetado ou o servidor é alterado.

Algumas aplicações ASP e .NET só funcionam se essas tabelas existirem, então caso elas não existem no banco, é comum ocorrer o erro **ASPStateTempApplications**

## Script para criar as tabelas
````sql
USE [ASPState]
GO
 
DECLARE @return_value int
 
EXEC    @return_value = [dbo].[CreateTempTables]
 
SELECT  'Return Value' = @return_value
 
GO
````