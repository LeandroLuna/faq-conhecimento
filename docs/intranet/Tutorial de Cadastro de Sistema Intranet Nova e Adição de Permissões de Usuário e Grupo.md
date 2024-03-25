# Cadastrando um Sistema Intranet

```
Um sistema normalmente equivale a um Projeto. 
Já um módulo representa uma página que pode dar início na navegação do seu sistema (equivale a uma Controller-Porta-de-Entrada).
Por exemplo: se seu sistema atende a professores e a coordenadores de forma diferente, ELE terá um módulo de acesso para professores e outro para coordenadores.

Com as funcionalidades é possível conceder acesso à determinado campo ou informação no sistema para um grupo mais seleto de pessoas.
Por exemplo: ao cadastrar uma funcionalidade para um botão em um sistema, apenas quem tem acesso àquela funcionalidade consegue visualizar e utilizar o botão.
```

**1)** Entre na intranet em ambiente de desenvolvimento:

URL: [http://intranetdes.fiap.com.br/](http://intranetdes.fiap.com.br/)

Usuário: administrador

Senha: x

**2)** Acesse a unidade onde o sistema deve ser cadastrado.

**3)** Através do menu, entre no sistema "Cadastro de Sistemas e Módulos".

**4)** Caso o sistema a ser cadastrado seja dependente de outro sistema, 
busque pelo nome do sistema-pai, selecione a opção **"Add Sistema"** e 
informe o nome do sistema que deseja cadastrar. Clique em cadastrar e pronto, 
sistema cadastrado.

**5)** Caso o sistema seja independente de outros sistemas já cadastrados 
(além do sistema Intranet), pressione o botão para **"Cadastrar Sistema"**

**6)** Dentro do modal que apareceu, informe o nome do sistema a ser 
cadastrado e um ícone que represente seu propósito. O ícone será exibido 
ao acessar o sistema, logo abaixo da barra de navegação da Intranet, 
juntamente ao seu nome na esquerda e ao seu caminho na direita. 
Pressione em **Cadastrar**.

**7)** Seu sistema será listado junto aos sistemas ja existentes, 
caso não o encontre facilmente, busque pelo seu nome.

**8)** Nessa listagem, seu sistema possui dois botões: 
"Add Módulo" e "Add Sistema". 
Clique em **"Add Módulo"**.

**9)** Informe o título do módulo (aparecerá no menu de busca) e a rota do 
sistema da seguinte forma: 
/net/NomeSistema/NomeControllerCasoNecessario/NomeActionCasoNecessario

OBS: Esta rota deve ser idêntica à informada no Data Annotation da Controller 
do seu projeto, logo acima da classe da Controller.

``` CSharp
[AutorizacaoIntranet("/net/NomeSistema/NomeControllerCasoNecessario/NomeActionCasoNecessario")]
```

**10)** Informe também uma descrição breve do propósito do sistema.
Verifique se precisa de algo relacionado a stored procedure ou a funcionalidades, 
caso necessário acione o Chicão. Caso contrário basta clicar em **"Cadastrar"**.


# Adicionando a lib de Permissão ao projeto

**1)** Abra a Solution Explorer e na camada Web do projeto clique com o botão 
direito e do mouse e abra o **"Manage NuGet Packages..."**.

**2)** No canto direito superior da tela, selecione o Packages source **"Fiap"**. 
Na aba **"Browse"**, busque por **"Permissao"** e instale no projeto.

**3)** Adicione o seguinte Data Annotation logo acima da declaração de cada
uma das controllers so sistema:

``` CSharp
[AutorizacaoIntranet("/net/NomeSistema/NomeControllerCasoNecessario/NomeActionCasoNecessario")]
```

**4)** Pronto, Permissão adicionada ao projeto.


# Permitindo aos usuários que acessem seu sistema

**1)** Ainda na Intranet, no menu, acesse o sistema **"Permissão Usuário"**.

**2)** Busque pelo usuario que deseja permitir acesso.

OBS: Convencionalmente, inicie permitindo acesso ao administrador.

**3)** Clique em **"Add Módulo para usuario"**. Após alguns instantes aparecerá 
um modal com um campo de busca e três culunas. Busque seu sistema (ou módulo) e,
na coluna de "encontrados", selecione o módulo desejado. Clique em salvar e 
pronto, o usuário ja possui acesso ao módulo do seu sistema.

**"4)"** Agora, ao logar com este usuário você consegue acessar seu sistema.



# Permitir acesso para um grupo de usuários

**"1)"** Caso precise permitir acesso para um grupo de pessoas, através do 
menu, acesse o sistema **"Lista de Grupos de Permissões"**.

**"6)"** Busque pelo grupo desejado (Ex: Help Center > Gerência) e clique em 
editar (iconé do lápis).

**"7)"** No modal que apareceu existem duas seções principais: Acima, temos o 
Gerenciamento de usuários que estão no grupo e a baixo o Gerenciamento de módulos
que o grupo tem acesso. Busque por seu sistema (ou módulo) na segunda seção e
selecione-o para conceder este acesso ao grupo. Clique em Editar e pronto,
este grupo ja possue acesso ao módulo do seu sistema.

**"8)"** Para confirmar o acesso, logue com alguns dos usuários do grupo e
tente encontrar seu sistema no menu.



# Tabelas onde os Sistemas, Módulos e Permissões são cadastrados

## Permissão de Usuário

Caso seja feita uma permissão de acesso para um usuário, de forma pontual:

```SQL
SELECT
	AcessoSistema.Descricao AS 'NomeSistema',
	AcessoSistemaModulo.Descricao AS 'NomeModulo',
	AcessoSistemaModulo.[URL] AS 'CaminhoModulo',
	Unidade.Nome AS 'NomeUnidade',
	Pessoa.Nome AS 'NomePessoa'
FROM
	BaseEducacional..AcessoSistema
	INNER JOIN BaseEducacional..AcessoSistemaModulo
		ON AcessoSistemaModulo.CodigoAcessoSistema = AcessoSistema.Codigo
	INNER JOIN BaseEducacional..AcessoUsuarioPermissao
		ON AcessoSistemaModulo.Codigo = AcessoUsuarioPermissao.CodigoAcessoSistemaModulo
	INNER JOIN BaseEducacional..Unidade
		ON AcessoUsuarioPermissao.CodigoUnidade = Unidade.Codigo
	INNER JOIN BaseEducacional..Usuario
		ON AcessoUsuarioPermissao.CodigoUsuario = Usuario.Codigo
	INNER JOIN BaseEducacional..Pessoa
		ON Usuario.CodigoPessoa = Pessoa.Codigo
WHERE
	[URL] = '/net/CentralDocumento'
ORDER BY
	Unidade.Nome,
	Pessoa.Nome
```

### Entendendo a relação entre as tabelas na permissão de usuários:

Você cadastra um AcessoSistema (Projeto), e dentro dele existem 
AcessoSistemaModulo (Controllers-PortaDeEntrada).
Este AcessoSistemaModulo tem um AcessoUsuarioPermissao que é o vínculo com 
a Unidade e com o Usuario que teve a permissão concedida.



## Permissão de Grupo de Usuários

Caso seja feita uma permissão de acesso para determinado grupo de usuários:

```SQL
SELECT
	AcessoSistema.Descricao AS 'NomeSistema',
	AcessoSistemaModulo.Descricao AS 'NomeModulo',
	AcessoSistemaModulo.[URL] AS 'CaminhoModulo',
	Unidade.Nome AS 'NomeUnidade',
	AcessoGrupo.Descricao AS 'NomeGrupo',
	Pessoa.Nome AS 'NomePessoa'
FROM
	BaseEducacional..AcessoSistema
	INNER JOIN BaseEducacional..AcessoSistemaModulo
		ON AcessoSistemaModulo.CodigoAcessoSistema = AcessoSistema.Codigo
	INNER JOIN BaseEducacional..AcessoGrupoPermissao
		ON AcessoSistemaModulo.Codigo = AcessoGrupoPermissao.CodigoAcessoSistemaModulo
	INNER JOIN BaseEducacional..AcessoGrupo
		ON AcessoGrupoPermissao.CodigoAcessoGrupo = AcessoGrupo.Codigo
	INNER JOIN BaseEducacional..Unidade
		ON AcessoGrupo.CodigoUnidade = Unidade.Codigo
	INNER JOIN BaseEducacional..AcessoGrupoUsuario
		ON AcessoGrupo.Codigo = AcessoGrupoUsuario.CodigoAcessoGrupo
	INNER JOIN BaseEducacional..Usuario
		ON AcessoGrupoUsuario.CodigoUsuario = Usuario.Codigo
	INNER JOIN BaseEducacional..Pessoa
		ON Usuario.CodigoPessoa = Pessoa.Codigo
WHERE
	[URL] = '/net/RelatorioTrimestralFund1/ProfessorTitular'
```

## Entendendo a relação entre as tabelas na permissão de grupos de usuários:

Você cadastra um AcessoSistema (Projeto), e dentro dele existem 
AcessoSistemaModulo (Controllers-PortaDeEntrada).
Este AcessoSistemaModulo tem um AcessoGrupoPermissao que é o vínculo com 
um AcessoGrupo (Grupo de pessoas com acesso àquele módulo).
O AcessoGrupo está vinculado a determinada Unidade e a 
um AcessoGrupoUsuario (Lista de usuários daquele grupo).
Este AcessoGrupoUsuario se vincula a cada um dos Usuario's.
