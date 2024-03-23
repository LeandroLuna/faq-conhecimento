# Erros comuns - como corrigir

## SqlException

Esse erro pode ocorrer quando o dev está tentando alterar o ambiente (mudar de banco FIAP pra Módulo ou vice-versa), starta a aplicação e tenta logar na Intranet, mesmo com todos os pré requisitos configurados corretamente ( [Alterando o banco das aplicações](http://conhecimento.fiap.com.br/processos/alternar-banco-testes-fiap-modulo/alternar-banco-testes-fiap-modulo/#alternar-entre-fiap-e-modulo) ).

***SqlException: SQL Server blocked access to procedure 'sys.sp_OACreate' of component 'Ole Automation Procedures' because this component is turned off as part of the security configuration for this server. A system administrator can enable the use of 'Ole Automation Procedures' by using sp_configure. For more information about enabling 'Ole Automation Procedures', search for 'Ole Automation Procedures' in SQL Server Books Online.***

É necessário executar o script abaixo dentro do banco que você está tentando acessar através da aplicação:

```
sp_configure 'show advanced options', 1;
GO
RECONFIGURE;
GO
sp_configure 'Ole Automation Procedures', 1;
GO
RECONFIGURE;
GO

```

Caso ocorra algum erro de permissão dentro do SQLServer, será necessário contactar alguém que possua previlégios de administrador para executar esse script.

- [Henrique Lopes - Chat Teams](https://teams.microsoft.com/l/chat/0/?users=henrique.mendonca@fiap.com.br);
- [Douglas Cabral - Chat Teams](https://teams.microsoft.com/l/chat/0/?users=douglas.cabral@fiap.com.br);
- [Francisco Esteves - Chat Teams](https://teams.microsoft.com/l/chat/0/?users=festeves@fiap.com.br);
- [Victor Alves Bugueno - Chat Teams](https://teams.microsoft.com/l/chat/0/?users=victor.bugueno@fiap.com.br)
