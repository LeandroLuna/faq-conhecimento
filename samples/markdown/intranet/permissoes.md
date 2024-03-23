# Permissões

### Duplicar acessos de usuários

Em alguns casos novos colaboradores precisam ter acesso identico ao de outro colaborador, é mais facil duplicar os acessos copiando todos os registros das tabelas **AcessoUsuarioPermissao** e **AcessoGrupoUsuario**.

```sql hl_lines="3 4"
USE BaseEducacional
GO
DECLARE @CLOrigem VARCHAR(6) = 'cl0887' -- CL do usuário de origem
DECLARE @CLDestino VARCHAR(6) = 'cl1128' -- CL do usuário de destino
DECLARE @CodigoCLOrigem INT
DECLARE @CodigoCLDestino INT

SELECT @CodigoCLOrigem=Codigo FROM vUsuarioPessoa WHERE Login = @CLOrigem
SELECT @CodigoCLDestino=Codigo FROM vUsuarioPessoa WHERE Login = @CLDestino

INSERT INTO AcessoGrupoUsuario
SELECT 
	CodigoAcessoGrupo,
	@CodigoCLDestino,
	GETDATE(),
	1,
	1
FROM
  vAcessoGrupoUsuario
WHERE 
	CodigoUsuario = @CodigoCLOrigem AND -- Pega todos os grupos que esse usuario tem
	CodigoAcessoGrupo NOT IN (SELECT CodigoAcessoGrupo FROM BaseEducacional..vAcessoGrupoUsuario WHERE CodigoUsuario = @CodigoCLDestino) -- E que ainda nao existam no cl destino

INSERT INTO AcessoUsuarioPermissao
SELECT 
	@CodigoCLDestino,
	CodigoUnidade,
	CodigoAcessoSistemaModulo,
	GETDATE(),
	1,
	1
FROM
	AcessoUsuarioPermissao
WHERE 
	CodigoUsuario = @CodigoCLOrigem AND 
	CodigoAcessoSistemaModulo NOT IN (SELECT CodigoAcessoSistemaModulo FROM AcessoUsuarioPermissao WHERE CodigoUsuario = @CodigoCLDestino) AND
	Ativo = 1

INSERT INTO Educacional..AcessoGrupoUsuario
SELECT 
	(SELECT MAX(Codigo)+1 FROM Educacional..AcessoGrupoUsuario),
	CodigoAcessoGrupo,
	@CodigoCLDestino,
	0,
	1,
	GETDATE(),
	1
FROM
  Educacional..AcessoGrupoUsuario
WHERE 
	CodigoUsuario = @CodigoCLOrigem AND -- Pega todos os grupos que esse usuario tem
	CodigoAcessoGrupo NOT IN (SELECT CodigoAcessoGrupo FROM Educacional..AcessoGrupoUsuario WHERE CodigoUsuario = @CodigoCLDestino) AND -- E que ainda nao existam no cl destino
	StatusRegistro=1 AND
	Deletado=0
```