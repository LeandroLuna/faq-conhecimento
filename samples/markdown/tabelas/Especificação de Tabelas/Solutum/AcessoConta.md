# AcessoConta

Tabela onde são armazenadas as **relações de acessos entre contas e usuários**. 
Esta tabela é utilizada em alguns sistemas da 
<a href="https://intranet3.fiap.com.br/" target="_blank">Intranet3</a>.

## Colunas

- **CodigoUsuario**: Valor que define o **Usuário que terá acesso**, de acordo 
com as views **Educacional..vUsuario** e **Educacional..vPessoa**;
- **CodigoConta**: Valor que define a **Conta Corrente**, de acordo com a tabela 
**Solutum..Conta**;
- **Conta**: Valor que define o **Nome da Conta Corrente**, de acordo com a 
tabela **Solutum..Conta**;
- **TipoSolicitacao**: Valor que define o **Tipo de Solicitação**, de acordo com
alguma tabela que não encontrei (**Questionar Chicão**);

## Buscando uma conta corrente

```sql
SELECT 
	Codigo,
	Conta,
	* 
FROM 
	Solutum..Conta 
WHERE 
	Conta LIKE '%99.604%';
/*
Codigo  conta                                    
79      VSTP (BCO ITAÚ / AG. 167 / CC 99.604-0)  
*/
```

## Buscando acessos já existentes

Para buscar os **acessos** de determinada conta, **preencha as variáveis** 
abaixo:

```sql
--SELECT * FROM Solutum..Conta;
DECLARE @CodigoConta AS INT = 79;
DECLARE @Conta AS NVARCHAR(510) = 'VSTP (BCO ITAÚ / AG. 167 / CC 99.604-0)';

SELECT 
	AcessoConta.Codigo, 
	vPessoa.Nome,
	AcessoConta.*
FROM 
	Educacional..vUsuario AS vUsuario 
	INNER JOIN Educacional..vPessoa AS vPessoa 
		ON vUsuario.CodigoPessoa = vPessoa.Codigo 
	INNER JOIN Solutum..AcessoConta 
		ON AcessoConta.CodigoUsuario = vUsuario.Codigo 
		AND AcessoConta.CodigoConta = @CodigoConta 
WHERE 
	vUsuario.Ativo = 1
ORDER BY 
	AcessoConta.Codigo,
	vPessoa.Nome;
```

## Cadastrando novos acessos à conta

Para cadastrar um novo acesso à conta, **preencha as variáveis** abaixo e 
utilize os **inserts gerados**:

```sql
--SELECT * FROM Solutum..Conta;
DECLARE @CodigoConta AS INT = 79;
DECLARE @Conta AS NVARCHAR(510) = 'VSTP (BCO ITAÚ / AG. 167 / CC 99.604-0)';

SELECT 
	AcessoConta.Codigo, 
	vPessoa.Nome,
	CASE WHEN 
		AcessoConta.Codigo IS NULL 
	THEN 
		CONCAT('INSERT INTO Solutum..AcessoConta (CodigoUsuario, CodigoConta, Conta, TipoSolicitacao) VALUES (', vUsuario.Codigo, ', ', @CodigoConta, ', ''', @Conta, ''', NULL);') 
	ELSE 
		CONCAT('-- OK: Acesso já concedido para ', vPessoa.Nome)
	END AS 'QueryInsert'
FROM 
	Educacional..vUsuario AS vUsuario 
	INNER JOIN Educacional..vPessoa AS vPessoa 
		ON vUsuario.CodigoPessoa = vPessoa.Codigo 
	LEFT JOIN Solutum..AcessoConta 
		ON AcessoConta.CodigoUsuario = vUsuario.Codigo 
		AND AcessoConta.CodigoConta = @CodigoConta 
WHERE 
	vUsuario.Ativo = 1
	AND 
	(
		vPessoa.Nome IN 
		(
			'<Informe aqui a lista de usuários que receberão acesso à conta>',
			'Victor Alves Bugueno',
			'Francisco Esteves'
		)
		/* Descomente essa linha  para ver também os acessos já concedidos */
		-- OR AcessoConta.Codigo IS NOT NULL 
	)
ORDER BY 
	CASE WHEN AcessoConta.Codigo IS NULL THEN 1 ELSE 2 END,
	vPessoa.Nome;
```
