# O que é uma Funcionalidade

Uma **Funcionalidade** é um **trecho de uma página HTML** que só será 
renderizado caso o usuário logado tenha determinada **permissão** de acesso.

Para definir uma **Funcionalidade** é necessário ter a **Lib Permissao** nas 
dependências da **Camada Web** do projeto.

Uma funcionalidade pode ser definida de **duas formas** principais:

- Exemplo informando por argumento o **bloco de código** que deverá ser utilizado:

    ```html
    <!-- @Html.Funcionalidade(nomeFuncionalidade, trechoHtmlParaRenderizar) -->
    @Html.Funcionalidade(
        "AlterarDataBaseBolsa", 
        @<div class="col-md-3">
            <div class="form-group">
                <label for="DataBase">
                    Data de Processamento
                </label>
                <input 
                    type="text" 
                    class="form-control" 
                    name="strDataProcessamento" 
                    id="DataBase" 
                />
            </div>
        </div>
    )
    ```

- Exemplo informando por argumento a **ViewPartial** que deverá ser utilizada:

    ```html
    <!-- @Html.Funcionalidade(nomeFuncionalidade, nomePartial, argumentoPartial) -->
    @Html.Funcionalidade("TrocarTipoBolsa", "_BotaoTrocarTipoBolsaPartial", item)
    ```

## Buscando usuários que possuem acessos à determinada Funcionalidade 

Query direta para buscar usuários com acesso à funcionalidade:

```sql
-- Buscando usuários com acesso à funcionalidade 'AlterarDadosResponsavel'
SELECT
	FuncionalidadesUsuario.Alias,
	Pessoa.Nome
FROM
	(
		SELECT  
			AcessoSistemaModuloFuncionalidade.Alias,  
			AcessoUsuarioPermissao.CodigoUsuario,
			Usuario.CodigoPessoa  
		FROM  
			BaseEducacional..AcessoSistemaModuloFuncionalidade  
			INNER JOIN BaseEducacional..AcessoUsuarioPermissaoFuncionalidade 
				ON AcessoUsuarioPermissaoFuncionalidade.CodigoAcessoSistemaModuloFuncionalidade = AcessoSistemaModuloFuncionalidade.Codigo 
				AND AcessoUsuarioPermissaoFuncionalidade.Ativo = 1 
				AND AcessoSistemaModuloFuncionalidade.Ativo = 1  
			INNER JOIN BaseEducacional..AcessoUsuarioPermissao 
				ON AcessoUsuarioPermissao.Codigo = AcessoUsuarioPermissaoFuncionalidade.CodigoAcessoUsuarioPermissao 
				AND AcessoUsuarioPermissao.Ativo = 1  
			INNER JOIN BaseEducacional..Usuario 
				ON AcessoUsuarioPermissao.CodigoUsuario = Usuario.Codigo 
				AND Usuario.Ativo = 1  
		UNION  
		SELECT  
			AcessoSistemaModuloFuncionalidade.Alias,  
			AcessoGrupoUsuario.CodigoUsuario,
			Usuario.CodigoPessoa
		FROM  
			BaseEducacional..AcessoSistemaModuloFuncionalidade  
			INNER JOIN BaseEducacional..AcessoGrupoPermissaoFuncionalidade 
				ON AcessoGrupoPermissaoFuncionalidade.CodigoAcessoSistemaModuloFuncionalidade = AcessoSistemaModuloFuncionalidade.Codigo 
				AND AcessoGrupoPermissaoFuncionalidade.Ativo = 1 
				AND AcessoSistemaModuloFuncionalidade.Ativo = 1  
			INNER JOIN BaseEducacional..AcessoGrupoPermissao 
				ON AcessoGrupoPermissao.Codigo = AcessoGrupoPermissaoFuncionalidade.CodigoAcessoGrupoPermissao 
				AND AcessoGrupoPermissao.Ativo = 1  
			INNER JOIN BaseEducacional..AcessoGrupoUsuario 
				ON AcessoGrupoUsuario.CodigoAcessoGrupo = AcessoGrupoPermissao.CodigoAcessoGrupo 
				AND AcessoGrupoUsuario.Ativo = 1  
			INNER JOIN BaseEducacional..AcessoGrupo 
				ON AcessoGrupo.Codigo = AcessoGrupoUsuario.CodigoAcessoGrupo 
				AND AcessoGrupo.Ativo = 1  
			INNER JOIN BaseEducacional..Usuario 
				ON AcessoGrupoUsuario.CodigoUsuario = Usuario.Codigo 
				AND Usuario.Ativo = 1
	) AS FuncionalidadesUsuario
	INNER JOIN BaseEducacional..Pessoa
		ON FuncionalidadesUsuario.CodigoPessoa = Pessoa.Codigo
WHERE
	FuncionalidadesUsuario.Alias LIKE 'AlterarDadosResponsavel'
ORDER BY
	FuncionalidadesUsuario.Alias,
	Pessoa.Nome
/*
Alias                    Nome                                    
AlterarDadosResponsavel  Administrador                           
AlterarDadosResponsavel  Aldenice Aparecida Breda                
AlterarDadosResponsavel  Aline Cristina Montosa Joazeiro Ortega  
AlterarDadosResponsavel  Amanda da Silva Barros                  
(...)
*/
```

Query para buscar usuários com acesso à funcionalidade utilizando a View 
**vFuncionalidadesUsuario**:

```sql
-- Buscando usuários com acesso à funcionalidade 'AlterarDadosResponsavel'
SELECT
	*
FROM
	BaseEducacional..vFuncionalidadesUsuario WITH (NOLOCK)
WHERE
	Alias LIKE 'AlterarDadosResponsavel'
/*
Alias                    CodigoUsuario  
AlterarDadosResponsavel  1              
AlterarDadosResponsavel  1165           
AlterarDadosResponsavel  1608           
AlterarDadosResponsavel  1627           
(...)
*/
```

## Criando Funcionalidade e/ou Concedendo Permissões de Acesso 

Para permitir acesso a determinada funcionalidade **já existente**, ou criar uma 
**nova funcionalidade**, utilize os scripts abaixo, informando o 
**nome do sistema** onde a funcionalidade será implementada e a 
**lista de usuários** que receberão acesso.

Primeiramente, encontre os nomes do **sistema** e da **funcionalidade** que deseja 
modificar:

```sql
-- Informe o nome do sistema onde a funcionalidade ficará
DECLARE @NomeSistemaModuloLike AS VARCHAR(255) = '%Alterar Plano%';
-- Utilize a query abaixo para identificar exatamente o nome do sistema onde a funcionalidade será implementada
SELECT * FROM BaseEducacional..AcessoSistemaModulo WHERE Titulo LIKE @NomeSistemaModuloLike

-- Informe o nome da funcionalidade (caso não exista, ela será criada)
DECLARE @NomeFuncionalidade AS VARCHAR(30) = 'AlterarDataBaseAlterarPlanoMBA';
-- Utilize a query abaixo para verificar se a funcionalidade já existe no sistema em questão
SELECT * FROM BaseEducacional..AcessoSistemaModuloFuncionalidade WHERE Alias LIKE @NomeFuncionalidade AND CodigoAcessoSistemaModulo IN 
(
	SELECT Codigo FROM BaseEducacional..AcessoSistemaModulo WHERE Titulo LIKE @NomeSistemaModuloLike
)
```

Depois, busque pelo **nome dos usuários** que receberão acesso, e caso encontre 
**mais de um** usuário com o **mesmo nome**, analise pontualmente e verifique 
qual deles deve receber acesso (acesse a IntranetNova com cada um deles e 
identifique qual é mais utilizado):

```sql
SELECT
	Pessoa.Nome,
	COUNT(*) AS 'QtdeUsuariosComEsseNome'
	--, *
FROM
	BaseEducacional..Usuario WITH (NOLOCK)
	INNER JOIN BaseEducacional..Pessoa WITH (NOLOCK)
		ON Usuario.CodigoPessoa = Pessoa.Codigo
WHERE
	Pessoa.Nome IN
	(
		'Administrador',
		'André Araujo Claro',
		'Barbara Barcelos',
		'Bruna Luane Matos de Jesus',
		'Thalita Fidelis Pereira',
		'Rosana Maria Lima de Oliveira',
		'Elaine Ormeni Pereira'
	)
GROUP BY
	Pessoa.Nome
/*
Nome                           QtdeUsuariosComEsseNome  
Administrador                  2                        
André Araujo Claro             1                        
Barbara Barcelos               1                        
Bruna Luane Matos de Jesus     1                        
Elaine Ormeni Pereira          2                        
Rosana Maria Lima de Oliveira  2                        
Thalita Fidelis Pereira        1                        
*/
```

E então, preencha as variáveis **@NomeSistemaModuloLike** e 
**@NomeFuncionalidade** e a **@TabNomeUsuarioLike** com a lista de usuários.

!!! warning "Atenção"
    Muito **cuidado** ao executar a query abaixo, pois ela manterá uma 
    [**Transação**](http://conhecimento.fiap.com.br/outros/banco/Transaction/) 
    **aberta**! Cabe a você analisar a aba **Messages** do **SQL Server** e 
    identificar se a transação deverá ser **commitada** ou **cancelada**.

```sql
----- Definindo os parâmetros para que o acesso à funcionalidade seja concedido --------------------
-- Informe o nome do sistema onde a funcionalidade ficará
DECLARE @NomeSistemaModuloLike AS VARCHAR(255) = '<NOME DO SISTEMA>';
-- Utilize a query abaixo para identificar exatamente o nome do sistema onde a funcionalidade será implementada
--SELECT * FROM BaseEducacional..AcessoSistemaModulo WHERE Titulo LIKE @NomeSistemaModuloLike

-- Informe o nome da funcionalidade (caso não exista, ela será criada)
DECLARE @NomeFuncionalidade AS VARCHAR(30) = '<NOME DA FUNCIONALIDADE>';
-- Utilize a query abaixo para verificar se a funcionalidade já existe no sistema em questão
/*
SELECT * FROM BaseEducacional..AcessoSistemaModuloFuncionalidade WHERE Alias LIKE @NomeFuncionalidade AND CodigoAcessoSistemaModulo IN 
(
	SELECT Codigo FROM BaseEducacional..AcessoSistemaModulo WHERE Titulo LIKE @NomeSistemaModuloLike
)
*/

DECLARE @TabNomeUsuarioLike AS TABLE (NomeUsuarioLike VARCHAR(100))

INSERT INTO @TabNomeUsuarioLike
-- Informe aqui o nome dos usuários que receberão acesso à esta funcionalidade
SELECT '%administrador%' 
UNION SELECT '<NOME USUÁRIO 1>' 
UNION SELECT '<NOME USUÁRIO 2>' 
UNION SELECT '<NOME USUÁRIO 3>' 
UNION SELECT '(...)' 
----------------------------------------------------------------------------------------------------


----- Inicia uma transação para evitar que o processo seja feito pela metade -----------------------
BEGIN TRANSACTION
----------------------------------------------------------------------------------------------------


----- Verifica se existe apenas um sistema-módulo com esse nome ------------------------------------
DECLARE @CodigoSistemaModulo AS INT;
DECLARE @NomeSistemaModulo AS VARCHAR(255);
DECLARE @QtdeSistemasEncontradosComEsteNome AS INT;

SELECT
	@CodigoSistemaModulo = MIN(Codigo),
	@NomeSistemaModulo = MIN(Titulo),
	@QtdeSistemasEncontradosComEsteNome = COUNT(*)
FROM
	BaseEducacional..AcessoSistemaModulo
WHERE
	Titulo LIKE @NomeSistemaModuloLike
	AND Ativo = 1
	
IF @QtdeSistemasEncontradosComEsteNome = 0
BEGIN
	PRINT CONCAT('Sistema "', @NomeSistemaModuloLike, '" não encontrado') 
END
		
IF @QtdeSistemasEncontradosComEsteNome > 1
BEGIN
	PRINT CONCAT('Foram encontrados ',  @QtdeSistemasEncontradosComEsteNome, ' sistemas para o nome "', @NomeSistemaModuloLike, '"') 
END
----------------------------------------------------------------------------------------------------


IF @QtdeSistemasEncontradosComEsteNome = 1
BEGIN
	----- Verifica se existe apenas uma funcionalidade com esse nome e cadastra caso não exista ----
	DECLARE @CodigoFuncionalidade AS INT;
	DECLARE @QtdeFuncionalidadesEncontradasComEsteNome AS INT;

	SELECT
		@CodigoFuncionalidade = MIN(Codigo),
		@QtdeFuncionalidadesEncontradasComEsteNome = COUNT(*)
	FROM
		BaseEducacional..AcessoSistemaModuloFuncionalidade
	WHERE
		CodigoAcessoSistemaModulo = @CodigoSistemaModulo
		AND Alias LIKE @NomeFuncionalidade
		AND Ativo = 1

	IF @QtdeFuncionalidadesEncontradasComEsteNome = 0
	BEGIN
		INSERT INTO BaseEducacional..AcessoSistemaModuloFuncionalidade
			(CodigoAcessoSistemaModulo,
			Alias,
			DataHoraCadastro,
			CodigoUsuarioCadastro,
			Ativo)
		VALUES
			(@CodigoSistemaModulo,
			@NomeFuncionalidade,
			GETDATE(),
			1,
			1);
		SELECT @CodigoFuncionalidade = @@IDENTITY;

		SET @QtdeFuncionalidadesEncontradasComEsteNome = 1;

		PRINT CONCAT('Funcionalidade "', @NomeFuncionalidade, '" foi cadastrada') 
	END
		
	IF @QtdeFuncionalidadesEncontradasComEsteNome > 1
	BEGIN
		PRINT CONCAT('Foram encontradas ',  @QtdeFuncionalidadesEncontradasComEsteNome, ' funcionalidades para o nome "', @NomeFuncionalidade, '"') 
	END
	------------------------------------------------------------------------------------------------

	IF @QtdeFuncionalidadesEncontradasComEsteNome = 1
	BEGIN
		----- Verifica se existe apenas um usuário para cada nome ----------------------------------
		DECLARE @EncontrouApenasUmUsuarioComCadaNome AS BIT = 1;

		DECLARE @TabCodigoUsuario AS TABLE (CodigoUsuario INT, NomeUsuario VARCHAR(100))

		DECLARE @NomeUsuarioLike AS VARCHAR(100);

		DECLARE 
			Ponteiro 
		CURSOR 
			READ_ONLY FORWARD_ONLY FAST_FORWARD 
		FOR 
		SELECT
			NomeUsuarioLike
		FROM
			@TabNomeUsuarioLike

		OPEN Ponteiro

		FETCH NEXT FROM Ponteiro 
		INTO @NomeUsuarioLike

		WHILE @@FETCH_STATUS = 0
		BEGIN
		
			DECLARE @QtdeUsuariosEncontradosComEsteNome AS INT = 1;
			DECLARE @CodigoUsuarioEncontrado AS INT;
			DECLARE @NomeUsuarioEncontrado AS VARCHAR(100);

			SELECT 
				@CodigoUsuarioEncontrado = MIN(Usuario.Codigo),
				@NomeUsuarioEncontrado = MIN(Pessoa.Nome),
				@QtdeUsuariosEncontradosComEsteNome = COUNT(*) 
			FROM 
				BaseEducacional..Usuario 
				INNER JOIN BaseEducacional..Pessoa 
					ON Usuario.CodigoPessoa = Pessoa.Codigo 
			WHERE 
				(
					(
						'Administrador' LIKE @NomeUsuarioLike
						AND Usuario.Codigo = 1 
					)
					OR
                    /* Tratando pontualmente usuários com múltiplos registros */
                    /* Para cada usuário com múltiplos registros, utilize um OR */
					/*(
						'<NomeUsuarioMultiplosRegistros1>' LIKE @NomeUsuarioLike
						AND Usuario.Codigo = <CodigoUsuarioCorreto1> 
					)
					OR*/
					/*(
						'<NomeUsuarioMultiplosRegistros2>' LIKE @NomeUsuarioLike
						AND Usuario.Codigo = <CodigoUsuarioCorreto2> 
					)
					OR*/
					(
                        /* Para cada usuário com múltiplos registros, utilize um AND */
						'Administrador' NOT LIKE @NomeUsuarioLike
                        /* Tratando pontualmente usuários com múltiplos registros */
                        -- AND '<NomeUsuarioMultiplosRegistros1>' NOT LIKE @NomeUsuarioLike
                        -- AND '<NomeUsuarioMultiplosRegistros2>' NOT LIKE @NomeUsuarioLike
						AND Pessoa.Nome LIKE @NomeUsuarioLike
					)
				)
				AND Usuario.[Login] NOT LIKE 'p%' -- Desconsidera usuários de professor (pXXXX)
				AND Usuario.Ativo = 1
				AND Pessoa.Ativo = 1
		
			INSERT INTO @TabCodigoUsuario
				(CodigoUsuario,
				NomeUsuario)
			VALUES
				(@CodigoUsuarioEncontrado,
				@NomeUsuarioEncontrado)

			IF @QtdeUsuariosEncontradosComEsteNome = 0
			BEGIN
				SET @EncontrouApenasUmUsuarioComCadaNome = 0;
				PRINT CONCAT('Usuário "', @NomeUsuarioLike, '" não encontrado') 
			END
		
			IF @QtdeUsuariosEncontradosComEsteNome > 1
			BEGIN
				SET @EncontrouApenasUmUsuarioComCadaNome = 0;
				PRINT CONCAT('Foram encontrados ',  @QtdeUsuariosEncontradosComEsteNome, ' usuários para o nome "', @NomeUsuarioLike, '"') 
			END

			FETCH NEXT FROM Ponteiro 
			INTO @NomeUsuarioLike

		END

		CLOSE Ponteiro
		DEALLOCATE Ponteiro
		--------------------------------------------------------------------------------------------


		IF @EncontrouApenasUmUsuarioComCadaNome = 1
		BEGIN
			----- Cadastra acesso ao sistema e funcionalidade caso não tenham ----------------------
			DECLARE @AbortarExecucao AS BIT = 0;
			DECLARE @CodigoUsuario AS INT;
			DECLARE @NomeUsuario AS VARCHAR(100);

			DECLARE 
				Ponteiro 
			CURSOR 
				READ_ONLY FORWARD_ONLY FAST_FORWARD 
			FOR 
			SELECT
				CodigoUsuario,
				NomeUsuario
			FROM
				@TabCodigoUsuario

			OPEN Ponteiro

			FETCH NEXT FROM Ponteiro 
			INTO @CodigoUsuario, @NomeUsuario

			WHILE @@FETCH_STATUS = 0 
				AND @AbortarExecucao = 0
			BEGIN

				DECLARE @CodigoUsuarioPermissao AS INT = 0;

				SELECT 
					@CodigoUsuarioPermissao = ISNULL(AcessoUsuarioPermissao.Codigo, 0)
				FROM 
					BaseEducacional..AcessoUsuarioPermissao 
				WHERE 
					CodigoUsuario = @CodigoUsuario 
					AND CodigoAcessoSistemaModulo = @CodigoSistemaModulo
					AND Ativo = 1

				-- Caso não exista permissão via usuário, mas exista permissão via grupo
				IF @CodigoUsuarioPermissao = 0
					AND EXISTS
					(
						SELECT
							1
						FROM
							BaseEducacional..AcessoGrupoPermissao
							INNER JOIN BaseEducacional..AcessoGrupo
								ON AcessoGrupoPermissao.CodigoAcessoGrupo = AcessoGrupo.Codigo
								AND AcessoGrupo.Ativo = 1
							INNER JOIN BaseEducacional..AcessoGrupoUsuario
								ON AcessoGrupo.Codigo = AcessoGrupoUsuario.CodigoAcessoGrupo
								AND AcessoGrupoUsuario.Ativo = 1
						WHERE
							AcessoGrupoPermissao.Ativo = 1
							AND AcessoGrupoUsuario.CodigoUsuario = @CodigoUsuario 
							AND AcessoGrupoPermissao.CodigoAcessoSistemaModulo = @CodigoSistemaModulo
					)
				BEGIN
					-- Insere permissão via usuário, pois as funcionalidades precisam deste tipo de permissão
					INSERT INTO BaseEducacional..AcessoUsuarioPermissao 
						(CodigoUsuario, 
						CodigoUnidade, 
						CodigoAcessoSistemaModulo, 
						DataHoraCadastro, 
						CodigoUsuarioCadastro, 
						Ativo)
					VALUES 
						(@CodigoUsuario, 
						13, -- Help Center 
						@CodigoSistemaModulo, 
						GETDATE(), 
						1, 
						1);
					SELECT @CodigoUsuarioPermissao = @@IDENTITY;
				END

				-- Caso exista permissão via usuário neste ponto
				IF @CodigoUsuarioPermissao > 0
				BEGIN
					-- Caso usuário não tenha acesso à funcionalidade, insere o acesso
					IF NOT EXISTS
					(
						SELECT
							1
						FROM
							BaseEducacional..AcessoUsuarioPermissaoFuncionalidade
						WHERE
							CodigoAcessoUsuarioPermissao = @CodigoUsuarioPermissao
							AND CodigoAcessoSistemaModuloFuncionalidade = @CodigoFuncionalidade
					)
					BEGIN
						INSERT INTO BaseEducacional..AcessoUsuarioPermissaoFuncionalidade 
							(CodigoAcessoUsuarioPermissao, 
							CodigoAcessoSistemaModuloFuncionalidade, 
							DataHoraCadastro, 
							CodigoUsuarioCadastro, 
							Ativo)
						VALUES 
							(@CodigoUsuarioPermissao, 
							@CodigoFuncionalidade, 
							GETDATE(), 
							1, 
							1)
					END
				END
				ELSE
				BEGIN
					SET @AbortarExecucao = 1;
					PRINT CONCAT('Usuário "', @NomeUsuario, '" não possui nenhum tipo de acesso ao sistema "', @NomeSistemaModulo, '"')
				END
				

				FETCH NEXT FROM Ponteiro 
				INTO @CodigoUsuario, @NomeUsuario

			END

			CLOSE Ponteiro
			DEALLOCATE Ponteiro

			IF @AbortarExecucao = 0 
			BEGIN
				-- Efetiva alterações 
				PRINT 'OBS: Favor executar o comando "COMMIT TRANSACTION"'
				-- COMMIT TRANSACTION
			END
			ELSE
			BEGIN
				-- Desfaz tudo que já foi feito até então
				PRINT 'OBS: Favor executar o comando "ROLLBACK TRANSACTION"'
				-- ROLLBACK TRANSACTION
			END
			----------------------------------------------------------------------------------------
		END
		ELSE
		BEGIN
			-- Desfaz tudo que já foi feito até então
			PRINT 'OBS: Favor executar o comando "ROLLBACK TRANSACTION"'
			-- ROLLBACK TRANSACTION
		END

	END
	ELSE
	BEGIN
		-- Desfaz tudo que já foi feito até então
		PRINT 'OBS: Favor executar o comando "ROLLBACK TRANSACTION"'
		-- ROLLBACK TRANSACTION
	END

END
ELSE
BEGIN
	-- Desfaz tudo que já foi feito até então
	PRINT 'OBS: Favor executar o comando "ROLLBACK TRANSACTION"'
	-- ROLLBACK TRANSACTION
END
```