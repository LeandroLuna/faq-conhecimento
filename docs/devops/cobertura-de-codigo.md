# Cobertura de Código
Passamos a utilizar o SonarQube como ferramenta de análise de qualidade de código. Uma das características analisadas é a porcentagem de código coberto por testes (code coverage). Entretanto, **o próprio SonarQube não roda os testes e não gera o relatório de cobertura.** Esse texto trata sobre como gerar esse relatório e como exportá-lo em projetos .NET Framework e .NET Core.

## .NET Core
### Requisitos
É necessário **criar um projeto de testes com NUnit seguindo o padrão de nome &lt;Nome do projeto&gt;.Tests** . Nele, é necessário adicionar o pacote **Coverlet.collector** (dependendo das workloads do seu Visual Studio, é possível que ele já venha instalado na criação do projeto NUnit). Instale-o utilizando o gerenciador de pacotes NuGet ou o comando abaixo:
```
dotnet add <Nome do projeto de testes> package coverlet.collector
``` 
O formato do arquivo gerado pelo coverlet não é compatível por default com o SonarQube. Sendo assim, é necessário instalar uma ferramenta global com o dotnet utilizando o comando:
```
dotnet tool install -g dotnet-reportgenerator-globaltool
```
Essa ferramenta é capaz de transformar o relatório gerado pelo coverlet em um formato compatível com o SonarQube.

### Alterações no sonar.bat
Após instalar as ferramentas acima, é necessário alterar o arquivo *sonar.bat* . Primeiro, é necessário alterar o comando:
```
dotnet sonarscanner begin /k:"dotnet:%LAST_WORD%" /d:sonar.host.url="http://sonar.fiap.com.br"  /d:sonar.login=%SONAR_TOKEN%
```
Para:
```
dotnet sonarscanner begin /k:"dotnet:%LAST_WORD%" /d:sonar.host.url="http://sonar.fiap.com.br"  /d:sonar.login=%SONAR_TOKEN%  /d:sonar.coverageReportPaths=".\sonarqubecoverage\SonarQube.xml"
```
Esse parâmetro adicionado informa o local do relatório de cobertura para o SonarQube.

É necessário adicionar o comando **dotnet test** logo abaixo do comando **dotnet build**, conforme abaixo:
```
dotnet sonarscanner begin /k:"dotnet:%LAST_WORD%" /d:sonar.host.url="http://sonar.fiap.com.br"  /d:sonar.login=%SONAR_TOKEN%  /d:sonar.coverageReportPaths=".\sonarqubecoverage\SonarQube.xml"
dotnet build
dotnet test --collect:"XPlat Code Coverage"
``` 
O argumento **--collect:"XPlat Code Coverage"** faz com que o comando **dotnet test** colete o relatório de testes utilizando os coletores do coverlet.

Uma pasta com um guid será criada dentro de TestResults/ todas as vezes que o comando **dotnet test** for executado. Sendo assim, para coletar todos os relatórios nelas e transformá-los com o reportgenerator, é necessário utilizar o comando abaixo:
```
reportgenerator "-reports:*\TestResults\*\coverage.cobertura.xml" "-targetdir:sonarqubecoverage" "-reporttypes:SonarQube"
```

Feitos esses passos, o SonarQube passará a identificar a cobertura de testes da solução.

### Arquivo final
Após a adição dos comandos, o arquivo sonar.bat deve se parecer com o código abaixo:
```
call set PARENT_DIR=%CD%
set PARENT_DIR=%PARENT_DIR:\= %
set LAST_WORD=
for %%i in (%PARENT_DIR%) do set LAST_WORD=%%i
echo dotnet:%LAST_WORD%

echo %LAST_WORD%.Tests

IF EXIST %LAST_WORD%.Tests (
	dotnet sonarscanner begin /k:"dotnet:%LAST_WORD%" /d:sonar.host.url="http://sonar.fiap.com.br"  /d:sonar.login=%SONAR_TOKEN%  /d:sonar.coverageReportPaths=".\sonarqubecoverage\SonarQube.xml"
	dotnet build
	dotnet test --collect:"XPlat Code Coverage"
	reportgenerator "-reports:*\TestResults\*\coverage.cobertura.xml" "-targetdir:sonarqubecoverage" "-reporttypes:SonarQube"
	dotnet sonarscanner end /d:sonar.login=%SONAR_TOKEN%
) ELSE (
	dotnet sonarscanner begin /k:"dotnet:%LAST_WORD%" /d:sonar.host.url="http://sonar.fiap.com.br"  /d:sonar.login=%SONAR_TOKEN%
	dotnet build
	dotnet sonarscanner end /d:sonar.login=%SONAR_TOKEN%
)
```
**IMPORTANTE**: se seu projeto de testes não seguir o padrão &lt;NomeProjeto&gt;.Tests, substitua o nome na linha do IF EXIST.

## .NET Framework
### Requisitos
É necessário **criar um projeto de testes com NUnit seguindo o padrão de nome &lt;Nome do projeto&gt;.Tests** . Nele, é necessário adicionar alguns pacotes:
<br/>
<br/>
_OpenCover (roda os testes e gera o relatório)_
<br/>
_NUNIT.Console e NUNIT.ConsoleRunner (executa os comandos do OpenCover)_
<br/>

Instale-os utilizando o gerenciador de pacotes NuGet.

### Alterações no sonar.bat
Após instalar as ferramentas acima, é necessário alterar o arquivo *sonar.bat* . Primeiro, é necessário adicionar os comandos:
```
  FOR /f "delims=" %%f IN ('dir packages /s /b nunit3-console.exe') DO SET CAMINHO_NUNITCONSOLE="%%f"
  FOR /f "delims=" %%f IN ('dir packages /s /b OpenCover.Console.exe') DO SET CAMINHO_OPENCOVER="%%f"
  mkdir "%CD%\%LAST_WORD%.Test\TestResults"

```
Esses comandos são responsáveis por buscar os executáveis dos pacotes e caso não haja ainda, criar a pasta que vai armazenar os relatórios.

Depois adicionamos o comando para executar o **OpenCover**:
```
%CAMINHO_OPENCOVER% -target:%CAMINHO_NUNITCONSOLE% -targetargs:"%CD%\%LAST_WORD%.Test\bin\Debug\%LAST_WORD%.Test.dll" -output:"%CD%\%LAST_WORD%.Test\TestResults\TestCoverage.xml" -register:user
```
O comando é responsável por gerar o relatório de **Coverage**.

Em seguida é necessario alterar o seguinte comando:
```
SonarScanner.MSBuild.exe begin /k:"dotnet:%LAST_WORD%" /d:sonar.host.url="http://sonar.fiap.com.br" /d:sonar.login=%SONAR_TOKEN%
```
Para:
```
SonarScanner.MSBuild.exe begin /k:"dotnet:%LAST_WORD%" /d:sonar.host.url="http://sonar.fiap.com.br" /d:sonar.login=%SONAR_TOKEN% /d:sonar.cs.opencover.reportsPaths="%CD%\%LAST_WORD%.Test\TestResults\TestCoverage.xml""
```
Esse parâmetro adicionado informa o local do relatório de cobertura para o SonarQube.

Feitos esses passos, o SonarQube passará a identificar a cobertura de testes da solução.

### Arquivo final
Após a adição dos comandos, o arquivo sonar.bat deve se parecer com o código abaixo:
```
@ECHO OFF
call set PARENT_DIR=%CD%
set PARENT_DIR=%PARENT_DIR:\= %
set LAST_WORD=
for %%i in (%PARENT_DIR%) do set LAST_WORD=%%i
echo dotnet:%LAST_WORD%

IF EXIST "%CD%\%LAST_WORD%.Test\" (
  FOR /f "delims=" %%f IN ('dir packages /s /b nunit3-console.exe') DO SET CAMINHO_NUNITCONSOLE="%%f"
  FOR /f "delims=" %%f IN ('dir packages /s /b OpenCover.Console.exe') DO SET CAMINHO_OPENCOVER="%%f"
  mkdir "%CD%\%LAST_WORD%.Test\TestResults"
) ELSE (
  ECHO "Projeto sem testes"
)

IF EXIST "%CD%\%LAST_WORD%.Test\" (
  %CAMINHO_OPENCOVER% -target:%CAMINHO_NUNITCONSOLE% -targetargs:"%CD%\%LAST_WORD%.Test\bin\Debug\%LAST_WORD%.Test.dll" -output:"%CD%\%LAST_WORD%.Test\TestResults\TestCoverage.xml" -register:user
  SonarScanner.MSBuild.exe begin /k:"dotnet:%LAST_WORD%" /d:sonar.host.url="http://sonar.fiap.com.br" /d:sonar.login=%SONAR_TOKEN% /d:sonar.cs.opencover.reportsPaths="%CD%\%LAST_WORD%.Test\TestResults\TestCoverage.xml"
  MSBuild.exe /t:Rebuild
  SonarScanner.MSBuild.exe end /d:sonar.login=%SONAR_TOKEN% 
) ELSE (
  SonarScanner.MSBuild.exe begin /k:"dotnet:%LAST_WORD%" /d:sonar.host.url="http://sonar.fiap.com.br" /d:sonar.login=%SONAR_TOKEN%
  MSBuild.exe /t:Rebuild
  SonarScanner.MSBuild.exe end /d:sonar.login=%SONAR_TOKEN% 
)
```
**IMPORTANTE**: se seu projeto de testes não seguir o padrão &lt;NomeProjeto&gt;.Tests, substitua o nome na linha do IF EXIST.