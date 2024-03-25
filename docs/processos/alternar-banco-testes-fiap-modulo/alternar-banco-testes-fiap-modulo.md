# Alternar Banco de Testes entre FIAP e Módulo

Temos alguns servidores de banco, com estruturas similares:

- **192.168.11.2\FPDEV**: Banco **FIAP** em ambiente de **Desenvolvimento**;
- **192.168.11.2\MDDEV**: Banco **Módulo** em ambiente de **Desenvolvimento**;
- **192.168.12.2\FPHOMO**: Banco **FIAP** em ambiente de **Homologação**;
- **192.168.12.2\MDHOMO**: Banco **Módulo** em ambiente de **Homologação**;

## Acessando banco no SQL Server

A forma de login no **SQL Server** em todos eles é a seguinte:

```
Server name: {Ex: 192.168.11.2\FPDEV}
Authentication: SQL Server Authentication
Login: sa
Password: !pfgm@07
```

## Alternar entre FIAP e Módulo

Alterar IP de acordo com o que deseja utilizar: 

Ex: "192.168.11.2\FPDEV"

Lembrar de:

- Alterar IP no **Intranet** (atenção à **ConnectionString** do sessionState **SQLServer**);
- Alterar IP no **Intranet.PesquisaAluno**;
- Alterar IP no **Intranet.{SistemaInterno}**;
- Alterar a variável de ambiente **DB_ADDRESS**;
- **Após** atualizar a variável de ambiente, rodar **iisreset** no **CMD** como 
**Administrador** e reinicializar todas as **instâncias de Visual Studio**
abertas, para que as variáveis sejam recarregadas.