# Sonarqube para projetos Html

## Configurando a máquina

* ### Configurando o SonarScanner
    * Baixar o <a href="https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/" target="_blank">SonarScanner</a> de acordo com o SO
    * Criar pasta para a SonarScanner no C:\\ (Caminho padrão: ```C:\sonarqube\sonar-scanner```);
    * Adicionar SonarQube no **"C:\Windows\System32\drivers\etc\hosts"** ```192.168.60.6 sonar.fiap.com.br```;
    * Acessar <a href="http://sonar.fiap.com.br/projects" target="_blank">SonarQube</a> e criar Token para utilização;
    * Adicionar Token nas variáveis de ambiente com o nome de SONAR_TOKEN;
    * Adicionar na variável de ambiente ```PATH``` o caminho **"C:\sonarqube\sonar-scanner\bin"** 

## Configurando o projeto

* Criar projeto no SonarQube;
* Adicionar o trecho a seguir no .gitignore do projeto
> ```gitignore
> # SonarQube
> .scannerwork
> .sonarqube
> ```
* Adicionar o arquivo **sonar.bat** na pasta principal do projeto.


### .HTML

> ```sh
> call set PARENT_DIR=%CD%
> set PARENT_DIR=%PARENT_DIR:\= %
> set LAST_WORD=
> for %%i in (%PARENT_DIR%) do set LAST_WORD=%%i
> echo dotnet:%LAST_WORD%
> 
> sonar-scanner.bat -D "sonar.projectKey=html:%LAST_WORD%" -D "sonar.host.url=http://sonar.fiap.com.br" -D "sonar.login=%SONAR_TOKEN%"
> ```

## Executando

> **Depois de configurar tudo, basta rodar o bat pelo CMD e sucesso!**
