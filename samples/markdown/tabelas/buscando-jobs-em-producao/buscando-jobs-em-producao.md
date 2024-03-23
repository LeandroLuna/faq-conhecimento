# O que é um Job SQL Server

Um **Job no SQL Server** se refere a um **script** (ou conjunto de scripts, 
separados em **steps**) que será executado de acordo com a **data**, 
**dia da semana** e/ou **horário** atual.

Estes Jobs normalmente são responsáveis por **atualizar algo periodicamente**, 
como por exemplo, a baixa de débitos pagos diariamente ou a atualização dos 
valores de débitos vencidos considerando multa e juros.

## Por que não temos acesso aos Jobs nos bancos de Desenvolvimento e Homologação?

Conforme informado pelo 
[Francisco Esteves](https://teams.microsoft.com/l/chat/0/?users=festeves@fiap.com.br), o 
banco de dados de **Produção** (192.168.10.9) fica num **servidor Windows**, 
permitindo a criação de Jobs.

Já os bancos de dados de **Desenvolvimento** e **Homologação** (citados abaixo) 
ficam em **servidores Linux**, onde **não existe** o conceito de Jobs.

- **192.168.11.2\FPDEV**: Banco **FIAP** em ambiente de **Desenvolvimento**;
- **192.168.11.2\MDDEV**: Banco **Módulo** em ambiente de **Desenvolvimento**;
- **192.168.12.2\FPHOMO**: Banco **FIAP** em ambiente de **Homologação**;
- **192.168.12.2\MDHOMO**: Banco **Módulo** em ambiente de **Homologação**;

Desta forma, **não é possível** trazer os Jobs para esses bancos para que 
possamos ter acesso a eles facilmente.

Porém, podemos solicitar que algum desenvolvedor com 
**acesso ao banco de produção** nos envie um Job que estamos precisando analisar
ou alterar.

## Buscando Jobs em Produção

Para **buscar um termo** no conteúdo dos Jobs e identificar quais Jobs podem 
estar realizando o procedimento que estamos procurando, execute a query no 
**Banco de Produção** (ou solicite que algum desenvolvedor com 
**acesso ao banco de produção** a execute):

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
	UPPER(sysjobsteps.command) LIKE '%<INFORME AQUI O TERMO BUSCADO>%'
```

Atualmente, os desenvolvedores com acesso ao banco de produção são:

- [Henrique Lopes - Chat Teams](https://teams.microsoft.com/l/chat/0/?users=henrique.mendonca@fiap.com.br);
- [Douglas Cabral - Chat Teams](https://teams.microsoft.com/l/chat/0/?users=douglas.cabral@fiap.com.br);
- [Francisco Esteves - Chat Teams](https://teams.microsoft.com/l/chat/0/?users=festeves@fiap.com.br);