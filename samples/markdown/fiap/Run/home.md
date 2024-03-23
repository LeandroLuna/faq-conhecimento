# FIAP Run

### Mandar SMS para os inscritos

Basta preencher a variável com a mensagem com até 150 caracteres e sem nenhuma acentuação.

```sql
DECLARE @Mensagem VARCHAR(150)
SET @Mensagem = ''
INSERT INTO Site_Fiap..ControleSMS (Mensagem, Enviado, Celular, Ativo, DataCadastro, SistemaOrigem) SELECT 
	@Mensagem,
	0,
	REPLACE(REPLACE(REPLACE(REPLACE(FiapRunUsuario.Telefone, '(', ''), ')', ''), ' ', ''), '-', ''),
	1,
	GETDATE(),
	'FIAP Run'
FROM 
	Site_Fiap..FiapRunUsuario AS FiapRunUsuario
WHERE 
	LEN(REPLACE(REPLACE(REPLACE(REPLACE(FiapRunUsuario.Telefone, '(', ''), ')', ''), ' ', ''), '-', '')) = 11 
	AND ISNUMERIC(REPLACE(REPLACE(REPLACE(REPLACE(FiapRunUsuario.Telefone, '(', ''), ')', ''), ' ', ''), '-', '')) = 1
```