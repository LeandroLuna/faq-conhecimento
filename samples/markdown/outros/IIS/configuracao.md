# Configurações iniciais

## Configurando Application Pool

IIS > Application Pool > Selecione uma > Botão direito > Advanced Settings.. > Na seção Process Model > Identity > ... > Custom Account > Set...

Informar o mesmo usuário e senha existente no servidor 192.168.10.41. Para adicionar ou editar um usuário neste servidor basta acessá-lo com uma 
conta de administrador remotamente através do comando **mstsc** do executar do Windows.


## Adicionar aplicações dentro da Intranet (Site) do IIS

Sites > Intranet > pasta net > botão direito > Add Application... > preencher **Alias** com o nome do projeto que será 
adicionado **SEM** o prefixo **"Intranet."** normalmente existente nos nomes dos projetos no Git > apontar o caminho da camada web do projeto no **Physical Path** 


Para aplicações que foram adicionadas tenham o mesmo layout que a Intranet deve se adicionar na pasta Views uma pasta chamada Shared:

Ir na application adicionada > Views > botão direito > Add Virtual Directory... > Preencher o **Alias** com 
"Shared" > Preencher o **Physical Path** com o caminho da pasta do projeto clonado de [Intranet no GitLab](https://gitlab.fiap.com.br/dotnet/Intranet). 
Ex: **C:\Git\Intranet\Intranet\Views\Shared** 

!!! warning
    Para conseguir rodar o projeto, não esquecer de realizar o build do mesmo. No Visual Studio > Build > Build Solution or F6.


## Permitir uso de verbos HTTP PUT, PATCH e DELETE em APIs

Para permitir o uso dos verbos HTTP PUT, PATCH, DELETE em APIs RESTFul, evitando desta forma o erro 405 Method Not Allowed
colocar no web.config do projeto as seguintes tags para desativar o WebDAV:

```
<configuration>
    <system.webServer>
		<modules>
		  <remove name="WebDAVModule"/>
		</modules>
	<system.webServer
</configuration>
```
