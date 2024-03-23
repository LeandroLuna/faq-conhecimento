# Deploy .NET

Os scripts abaixo são modelos de deploy automatizados para .NET Core e .NET Framework (**Scripts diferentes!!!**)

Criar um arquivo chamado **.gitlab-ci.yml** e colar o conteúdo do modelo.

Todas as alterações necessárias devem ser realizadas na seção "variables" no topo de cada script.

Caso não seja necessário o deploy no Módulo (por exemplo), basta remover o job "deploy_modulo" do script
e as variáveis referentes ao colégio módulo. O mesmo para o ambiente FIAP caso não seja necessário.


**ATENÇÃO!** Proteger a branch master em **Settings > Repository** no GitLab


Descrição das possíveis variáveis de ambiente (Cadastrar em **settings => ci/cd => secrets variables**):

- **FIAP_HOMO_FTP_USERNAME** ==> Usuário de FTP no servidor de Homologação FIAP
- **FIAP_HOMO_FTP_PASSWORD** ==> Senha de FTP no servidor de Homologação da FIAP
- **FIAP_HOMO_FTP_HOST** ==> IP do servidor de FTP de Homologação da FIAP
- **MODULO_HOMO_FTP_USERNAME** ==> Usuário de FTP no servidor de Homologação do Módulo
- **MODULO_HOMO_FTP_PASSWORD** ==> Senha de FTP no servidor de Homologação do Módulo
- **MODULO_HOMO_FTP_HOST** ==> IP do servidor de FTP de Homologação do Módulo
- **FIAP_FTP_USERNAME** ==> Usuário de FTP no servidor da FIAP
- **FIAP_FTP_PASSWORD** ==> Senha de FTP no servidor da FIAP
- **FIAP_FTP_HOST** ==> IP do servidor de FTP da FIAP
- **MODULO_FTP_USERNAME** ==> Usuário de FTP no servidor do Módulo
- **MODULO_FTP_PASSWORD** ==> Senha de FTP no servidor do Módulo
- **MODULO_FTP_HOST** ==> IP do servidor de FTP do Módulo

Descrição das possíveis variáveis do script:

- **nuget** ==> Caminho do nuget.exe no Runner do GitLab
- **FIAP_PATH_DIST** ==> Path da aplicação no servidor de produção FIAP
- **FIAP_ENV_URL** ==> URL de produção para acessar o sistema
- **MODULO_PATH_DIST** ==> Path da aplicação no servidor de produção Módulo 
- **MODULO_ENV_URL** ==> URL de produção para acessar o sistema
- **FIAP_HOMO_PATH_DIST** ==> Path da aplicação no servidor de homologação FIAP
- **FIAP_HOMO_ENV_URL** ==> URL de homologação para acessar o sistema
- **MODULO_HOMO_PATH_DIST** ==> Path da aplicação no servidor de homologação Módulo 
- **MODULO_HOMO_ENV_URL** ==> URL de homologação para acessar o sistema

!!! warning "Atenção"
    Seguir padrão de nome do projeto .TST para projetos de teste, senão o deploy não vai identificar a DLL. 
    Exemplo: **Intranet.Projeto.TST**



??? example ".NET Core e versões superiores (FIAP/Módulo)"
    ```yml
    #
    # Todas as alterações necessárias neste script ficam aqui:
    #
    # NÃO ESQUECER DE CADASTRAR AS VARIÁVEIS SECRETAS NO MENU Settings/Repository do Projeto 
    # (FIAP_FTP_USERNAME, FIAP_FTP_PASSWORD, FIAP_FTP_HOST, MODULO_FTP_USERNAME, MODULO_FTP_PASSWORD e MODULO_FTP_HOST)
    #
    #
    variables:
        FIAP_HOMO_PATH_DIST: ./Colocar/aqui/o/caminho/de/dentro/do/ftp(servidor fiap)
        FIAP_HOMO_ENV_URL: https://www.colocar.aqui.o.endereco.de.acesso.com.br/alguma/coisa
        MODULO_HOMO_PATH_DIST: ./Colocar/aqui/o/caminho/de/dentro/do/ftp(servidor fiap)
        MODULO_HOMO_ENV_URL: https://www.colocar.aqui.o.endereco.de.acesso.com.br/alguma/coisa
        FIAP_PATH_DIST: ./Colocar/aqui/o/caminho/de/dentro/do/ftp(servidor fiap)
        FIAP_ENV_URL: https://www.colocar.aqui.o.endereco.de.acesso.com.br/alguma/coisa
        MODULO_PATH_DIST: ./Colocar/aqui/o/caminho/de/dentro/do/ftp(servidor modulo)
        MODULO_ENV_URL: https://www.colocar.aqui.o.endereco.de.acesso.com.br/alguma/coisa
        REQUIRED_FILES: '"Web.config" "Views/Web.config"'
    cache:
        untracked: true
        key: "%CI_BUILD_REF%"
        paths:
            - packages/
            - "*.Tests"

    before_script:
        - "echo off"

    stages:
        - restore
        - build
        - test
        - homolog
        - deploy

    restore:
        stage: restore
        only:
            - homolog
            - master
        script:
            - if not exist "./%CI_PROJECT_NAME%/Properties/PublishProfiles/Homologacao.pubxml" (
              echo "Arquivo Homologacao.pubxml não existe! Favor criar o publish!" && EXIT /b 5 )
            - "dotnet restore --verbosity quiet"       

    build:
        stage: build
        script:
            - "dotnet build /p:DeployOnBuild=true /p:Configuration=Release /p:PublishProfile=Homologacao.pubxml /p:PublishUrl=%CD%/dist"
        only:
            - homolog
            - master
        artifacts:
            paths:
                - dist/
            expire_in: 1 hour

    test:
        stage: test
        only:
            - homolog
            - master
        script:
            - 'dotnet test'

    deploy_homolog_fiap:
        stage: homolog
        image: alpine:latest
        before_script:
            - apk add --no-cache lftp -q
        script:
            - 'echo "" > app_offline.htm'
            - lftp -u $FIAP_HOMO_FTP_USERNAME,$FIAP_HOMO_FTP_PASSWORD $FIAP_HOMO_FTP_HOST -e "cd $FIAP_HOMO_PATH_DIST; put app_offline.htm; quit"
            - lftp -u $FIAP_HOMO_FTP_USERNAME,$FIAP_HOMO_FTP_PASSWORD $FIAP_HOMO_FTP_HOST -e "mirror --reverse --no-perms --exclude Mudancas.txt --exclude mudancas.txt --exclude appsettings.json --include Views/Web.config --include Views/Web.config dist/ $FIAP_HOMO_PATH_DIST --verbose; quit"
            - lftp -u $FIAP_HOMO_FTP_USERNAME,$FIAP_HOMO_FTP_PASSWORD $FIAP_HOMO_FTP_HOST -e "rm $FIAP_HOMO_PATH_DIST/app_offline.htm; quit"
            # \033[0;31m e \033[0m são usados para mudar a cor do erro no comando abaixo:
            - for i in $REQUIRED_FILES; do lftp -u $FIAP_HOMO_FTP_USERNAME,$FIAP_HOMO_FTP_PASSWORD $FIAP_HOMO_FTP_HOST -e "cd $FIAP_HOMO_PATH_DIST; find $i; quit" || (echo -e "\033[0;31mArquivo $i não existe em produção!\033[0m" && exit 5); done
        only:
            - homolog
        when: manual
        environment:
            name: homolog-fiap
            url: $FIAP_HOMO_ENV_URL
        tags:
            - linux

    deploy_homolog_modulo:
        stage: homolog
        image: alpine:latest
        before_script:
            - apk add --no-cache lftp -q
        script:
            - 'echo "" > app_offline.htm'
            - lftp -u $MODULO_HOMO_FTP_USERNAME,$MODULO_HOMO_FTP_PASSWORD $MODULO_HOMO_FTP_HOST -e "cd $MODULO_HOMO_PATH_DIST; put app_offline.htm; quit"
            - lftp -u $MODULO_HOMO_FTP_USERNAME,$MODULO_HOMO_FTP_PASSWORD $MODULO_HOMO_FTP_HOST -e "mirror --reverse --no-perms --exclude Mudancas.txt --exclude mudancas.txt --exclude appsettings.json --include Views/Web.config --include Views/Web.config dist/ $MODULO_HOMO_PATH_DIST --verbose; quit"
            - lftp -u $MODULO_HOMO_FTP_USERNAME,$MODULO_HOMO_FTP_PASSWORD $MODULO_HOMO_FTP_HOST -e "rm $MODULO_HOMO_PATH_DIST/app_offline.htm; quit"
            # \033[0;31m e \033[0m são usados para mudar a cor do erro no comando abaixo:
            - for i in $REQUIRED_FILES; do lftp -u $MODULO_HOMO_FTP_USERNAME,$MODULO_HOMO_FTP_PASSWORD $MODULO_HOMO_FTP_HOST -e "cd $MODULO_HOMO_PATH_DIST; find $i; quit" || (echo -e "\033[0;31mArquivo $i não existe em produção!\033[0m" && exit 5); done
        only:
            - homolog
        when: manual
        environment:
            name: homolog-modulo
            url: $MODULO_HOMO_ENV_URL
        tags:
            - linux            

    deploy_fiap:
        stage: deploy
        image: alpine:latest
        before_script:
            - apk add --no-cache lftp -q
        script:
            - 'echo "" > app_offline.htm'
            - lftp -u $FIAP_FTP_USERNAME,$FIAP_FTP_PASSWORD $FIAP_FTP_HOST -e "cd $FIAP_PATH_DIST; put app_offline.htm; quit"
            - lftp -u $FIAP_FTP_USERNAME,$FIAP_FTP_PASSWORD $FIAP_FTP_HOST -e "mirror --reverse --no-perms --exclude Mudancas.txt --exclude mudancas.txt --exclude appsettings.json --include Views/Web.config --include Views/Web.config dist/ $FIAP_PATH_DIST --verbose; quit"
            - lftp -u $FIAP_FTP_USERNAME,$FIAP_FTP_PASSWORD $FIAP_FTP_HOST -e "rm $FIAP_PATH_DIST/app_offline.htm; quit"
            # \033[0;31m e \033[0m são usados para mudar a cor do erro no comando abaixo:
            - for i in $REQUIRED_FILES; do lftp -u $FIAP_FTP_USERNAME,$FIAP_FTP_PASSWORD $FIAP_FTP_HOST -e "cd $FIAP_PATH_DIST; find $i; quit" || (echo -e "\033[0;31mArquivo $i não existe em produção!\033[0m" && exit 5); done
        only:
            - master
        when: manual
        environment:
            name: production-fiap
            url: $FIAP_ENV_URL
        tags:
            - linux

    deploy_modulo:
        stage: deploy
        image: alpine:latest
        before_script:
            - apk add --no-cache lftp -q
        script:
            - 'echo "" > app_offline.htm'
            - lftp -u $MODULO_FTP_USERNAME,$MODULO_FTP_PASSWORD $MODULO_FTP_HOST -e "cd $MODULO_PATH_DIST; put app_offline.htm; quit"
            - lftp -u $MODULO_FTP_USERNAME,$MODULO_FTP_PASSWORD $MODULO_FTP_HOST -e "mirror --reverse --no-perms --exclude Mudancas.txt --exclude mudancas.txt --exclude appsettings.json --include Views/Web.config --include Views/Web.config dist/ $MODULO_PATH_DIST --verbose; quit"
            - lftp -u $MODULO_FTP_USERNAME,$MODULO_FTP_PASSWORD $MODULO_FTP_HOST -e "rm $MODULO_PATH_DIST/app_offline.htm; quit"
            # \033[0;31m e \033[0m são usados para mudar a cor do erro no comando abaixo:
            - for i in $REQUIRED_FILES; do lftp -u $MODULO_FTP_USERNAME,$MODULO_FTP_PASSWORD $MODULO_FTP_HOST -e "cd $MODULO_PATH_DIST; find $i; quit" || (echo -e "\033[0;31mArquivo $i não existe em produção!\033[0m" && exit 5); done
        only:
            - master
        when: manual
        environment:
            name: production-modulo
            url: $MODULO_ENV_URL
        tags:
            - linux

    ```

??? example ".NET Framework (FIAP/Módulo)"
    ```yml
    #
    # Todas as alterações necessárias neste script ficam aqui:
    #
    # NÃO ESQUECER DE CADASTRAR AS VARIÁVEIS SECRETAS NO MENU Settings/Repository do Projeto 
    # (FIAP_FTP_USERNAME, FIAP_FTP_PASSWORD, FIAP_FTP_HOST, MODULO_FTP_USERNAME, MODULO_FTP_PASSWORD e MODULO_FTP_HOST)
    #
    #
    variables:
        FIAP_HOMO_PATH_DIST: ./Colocar/aqui/o/caminho/de/dentro/do/ftp(servidor fiap)
        FIAP_HOMO_ENV_URL: https://www.colocar.aqui.o.endereco.de.acesso.com.br/alguma/coisa
        MODULO_HOMO_PATH_DIST: ./Colocar/aqui/o/caminho/de/dentro/do/ftp(servidor fiap)
        MODULO_HOMO_ENV_URL: https://www.colocar.aqui.o.endereco.de.acesso.com.br/alguma/coisa
        FIAP_PATH_DIST: ./Colocar/aqui/o/caminho/de/dentro/do/ftp(servidor fiap)
        FIAP_ENV_URL: https://www.colocar.aqui.o.endereco.de.acesso.com.br/alguma/coisa
        MODULO_PATH_DIST: ./Colocar/aqui/o/caminho/de/dentro/do/ftp(servidor modulo)
        MODULO_ENV_URL: https://www.colocar.aqui.o.endereco.de.acesso.com.br/alguma/coisa
        REQUIRED_FILES: '"Web.config" "Views/Web.config"'
        
    cache:
        untracked: true
        key: "%CI_BUILD_REF%"
        paths:
            - packages/
            - "*.Tests"

    before_script:
        - "echo off"

    stages:
        - restore
        - build
        - test
        - homolog
        - deploy

    restore:
        stage: restore
        only:
            - homolog
            - master
        script:
            - if not exist "./%CI_PROJECT_NAME%/Properties/PublishProfiles/Homologacao.pubxml" (
                echo "Arquivo Homologacao.pubxml não existe! Favor criar o publish!" && EXIT /b 5 )
            - 'nuget restore -verbosity quiet'

    build:
        stage: build
        script:
            - 'msbuild.exe /verbosity:q'
            - "msbuild.exe /p:DeployOnBuild=true /p:Configuration=Release /p:PublishProfile=Homologacao.pubxml /p:PublishUrl=%CD%/dist"
        only:
            - homolog
            - master
        artifacts:
            paths:
                - dist/
            expire_in: 1 hour

    test:
        stage: test
        only:
            - homolog
            - master
        script:
            - 'nunit3-console.exe ./%CI_PROJECT_NAME%.TST/%CI_PROJECT_NAME%.TST.csproj'

    deploy_homolog_fiap:
        stage: homolog
        image: alpine:latest
        before_script:
            - apk add --no-cache lftp -q
        script:
            - lftp -u $FIAP_HOMO_FTP_USERNAME,$FIAP_HOMO_FTP_PASSWORD $FIAP_HOMO_FTP_HOST -e "mirror --reverse --no-perms --exclude Mudancas.txt --exclude mudancas.txt --exclude web.config --exclude Web.config --exclude appsettings.json --include Views/Web.config --include Views/Web.config dist/ $FIAP_HOMO_PATH_DIST --verbose; quit"
            # \033[0;31m e \033[0m são usados para mudar a cor do erro no comando abaixo:
            - for i in $REQUIRED_FILES; do lftp -u $FIAP_HOMO_FTP_USERNAME,$FIAP_HOMO_FTP_PASSWORD $FIAP_HOMO_FTP_HOST -e "cd $FIAP_HOMO_PATH_DIST; find $i; quit" || (echo -e "\033[0;31mArquivo $i não existe em produção!\033[0m" && exit 5); done
        only:
            - homolog
        when: manual
        environment:
            name: homolog-fiap
            url: $FIAP_HOMO_ENV_URL
        tags:
            - linux

    deploy_homolog_modulo:
        stage: homolog
        image: alpine:latest
        before_script:
            - apk add --no-cache lftp -q
        script:
            - lftp -u $MODULO_HOMO_FTP_USERNAME,$MODULO_HOMO_FTP_PASSWORD $MODULO_HOMO_FTP_HOST -e "mirror --reverse --no-perms --exclude Mudancas.txt --exclude mudancas.txt --exclude web.config --exclude Web.config --exclude appsettings.json --include Views/Web.config --include Views/Web.config dist/ $MODULO_HOMO_PATH_DIST --verbose; quit"
            # \033[0;31m e \033[0m são usados para mudar a cor do erro no comando abaixo:
            - for i in $REQUIRED_FILES; do lftp -u $MODULO_HOMO_FTP_USERNAME,$MODULO_HOMO_FTP_PASSWORD $MODULO_HOMO_FTP_HOST -e "cd $MODULO_HOMO_PATH_DIST; find $i; quit" || (echo -e "\033[0;31mArquivo $i não existe em produção!\033[0m" && exit 5); done
        only:
            - homolog
        when: manual
        environment:
            name: homolog-modulo
            url: $MODULO_HOMO_ENV_URL
        tags:
            - linux  

    deploy_fiap:
        stage: deploy
        image: alpine:latest
        before_script:
            - apk add --no-cache lftp -q
        script:
            - lftp -u $FIAP_FTP_USERNAME,$FIAP_FTP_PASSWORD $FIAP_FTP_HOST -e "mirror --reverse --no-perms --exclude Mudancas.txt --exclude mudancas.txt --exclude web.config --exclude Web.config --exclude appsettings.json --include Views/Web.config --include Views/Web.config dist/ $FIAP_PATH_DIST --verbose; quit"
            # \033[0;31m e \033[0m são usados para mudar a cor do erro no comando abaixo:
            - for i in $REQUIRED_FILES; do lftp -u $FIAP_FTP_USERNAME,$FIAP_FTP_PASSWORD $FIAP_FTP_HOST -e "cd $FIAP_PATH_DIST; find $i; quit" || (echo -e "\033[0;31mArquivo $i não existe em produção!\033[0m" && exit 5); done
        only:
            - master
        when: manual
        environment:
            name: production-fiap
            url: $FIAP_ENV_URL
        tags:
            - linux

    deploy_modulo:
        stage: deploy
        image: alpine:latest
        before_script:
            - apk add --no-cache lftp -q
        script:
            - lftp -u $MODULO_FTP_USERNAME,$MODULO_FTP_PASSWORD $MODULO_FTP_HOST -e "mirror --reverse --no-perms --exclude Mudancas.txt --exclude mudancas.txt --exclude web.config --exclude Web.config --exclude appsettings.json --include Views/Web.config --include Views/Web.config dist/ $MODULO_PATH_DIST --verbose; quit"
            # \033[0;31m e \033[0m são usados para mudar a cor do erro no comando abaixo:
            - for i in $REQUIRED_FILES; do lftp -u $MODULO_FTP_USERNAME,$MODULO_FTP_PASSWORD $MODULO_FTP_HOST -e "cd $MODULO_PATH_DIST; find $i; quit" || (echo -e "\033[0;31mArquivo $i não existe em produção!\033[0m" && exit 5); done
        only:
            - master
        when: manual
        environment:
            name: production-modulo
            url: $MODULO_ENV_URL
        tags:
            - linux

    ```


<!-- 


??? example ".NET Core e versões superiores (FIAP/Módulo) versão power shell"
    ```yml
    #
    # Todas as alterações necessárias neste script ficam aqui:
    #
    # NÃO ESQUECER DE CADASTRAR AS VARIÁVEIS SECRETAS NO MENU Settings/Repository do Projeto 
    # (FIAP_FTP_USERNAME, FIAP_FTP_PASSWORD, FIAP_FTP_HOST, MODULO_FTP_USERNAME, MODULO_FTP_PASSWORD e MODULO_FTP_HOST)
    #
    #
    variables:
        FIAP_HOMO_PATH_DIST: ./Colocar/aqui/o/caminho/de/dentro/do/ftp(servidor fiap)
        FIAP_HOMO_ENV_URL: https://www.colocar.aqui.o.endereco.de.acesso.com.br/alguma/coisa
        MODULO_HOMO_PATH_DIST: ./Colocar/aqui/o/caminho/de/dentro/do/ftp(servidor fiap)
        MODULO_HOMO_ENV_URL: https://www.colocar.aqui.o.endereco.de.acesso.com.br/alguma/coisa
        FIAP_PATH_DIST: ./Colocar/aqui/o/caminho/de/dentro/do/ftp(servidor fiap)
        FIAP_ENV_URL: https://www.colocar.aqui.o.endereco.de.acesso.com.br/alguma/coisa
        MODULO_PATH_DIST: ./Colocar/aqui/o/caminho/de/dentro/do/ftp(servidor modulo)
        MODULO_ENV_URL: https://www.colocar.aqui.o.endereco.de.acesso.com.br/alguma/coisa
        REQUIRED_FILES: '"Web.config" "Views/Web.config"'

    cache:
        untracked: true
        key: "%CI_BUILD_REF%"
        paths:
            - packages/
            - "*.Tests"

    before_script:
        - "echo off"

    stages:
        - restore
        - build
        - test
        - homolog
        - deploy
    
    restore:
        stage: restore
        only:
            - homolog
            - master
        script:
            - if (Test-Path "${CI_PROJECT_NAME}/Properties/PublishProfiles/Homologacao.pubxml") { Write-Host 'Homologacao.pubxml exists.', exit 0 } else { Write-Host 'Homologacao.pubxml does not exist.'; exit 5 }
            - dotnet restore

    build:
        stage: build
        script:
            - dotnet build /p:DeployOnBuild=true /p:Configuration=Release /p:PublishProfile=Homologacao.pubxml /p:PublishUrl=$CI_PROJECT_DIR\dist
        only:
            - homolog
            - master
        artifacts:
            paths:
                - dist/
            expire_in: 1 hour

    test:
        stage: test
        only:
            - homolog
            - master
        script:
            - 'dotnet test'

    deploy_homolog_fiap:
        stage: homolog
        image: alpine:latest
        before_script:
            - apk add --no-cache lftp -q
        script:
            - 'echo "" > app_offline.htm'
            - lftp -u $FIAP_HOMO_FTP_USERNAME,$FIAP_HOMO_FTP_PASSWORD $FIAP_HOMO_FTP_HOST -e "cd $FIAP_HOMO_PATH_DIST; put app_offline.htm; quit"
            - lftp -u $FIAP_HOMO_FTP_USERNAME,$FIAP_HOMO_FTP_PASSWORD $FIAP_HOMO_FTP_HOST -e "mirror --reverse --no-perms --exclude Mudancas.txt --exclude mudancas.txt --exclude appsettings.json --include Views/Web.config --include Views/Web.config dist/ $FIAP_HOMO_PATH_DIST --verbose; quit"
            - lftp -u $FIAP_HOMO_FTP_USERNAME,$FIAP_HOMO_FTP_PASSWORD $FIAP_HOMO_FTP_HOST -e "rm $FIAP_HOMO_PATH_DIST/app_offline.htm; quit"
            # \033[0;31m e \033[0m são usados para mudar a cor do erro no comando abaixo:
            - for i in $REQUIRED_FILES; do lftp -u $FIAP_HOMO_FTP_USERNAME,$FIAP_HOMO_FTP_PASSWORD $FIAP_HOMO_FTP_HOST -e "cd $FIAP_HOMO_PATH_DIST; find $i; quit" || (echo -e "\033[0;31mArquivo $i não existe em produção!\033[0m" && exit 5); done
        only:
            - homolog
        when: manual
        environment:
            name: production-fiap
            url: $FIAP_HOMO_ENV_URL
        tags:
            - linux

    deploy_homolog_modulo:
        stage: homolog
        image: alpine:latest
        before_script:
            - apk add --no-cache lftp -q
        script:
            - 'echo "" > app_offline.htm'
            - lftp -u $MODULO_HOMO_FTP_USERNAME,$MODULO_HOMO_FTP_PASSWORD $MODULO_HOMO_FTP_HOST -e "cd $MODULO_HOMO_PATH_DIST; put app_offline.htm; quit"
            - lftp -u $MODULO_HOMO_FTP_USERNAME,$MODULO_HOMO_FTP_PASSWORD $MODULO_HOMO_FTP_HOST -e "mirror --reverse --no-perms --exclude Mudancas.txt --exclude mudancas.txt --exclude appsettings.json --include Views/Web.config --include Views/Web.config dist/ $MODULO_HOMO_PATH_DIST --verbose; quit"
            - lftp -u $MODULO_HOMO_FTP_USERNAME,$MODULO_HOMO_FTP_PASSWORD $MODULO_HOMO_FTP_HOST -e "rm $MODULO_HOMO_PATH_DIST/app_offline.htm; quit"
            # \033[0;31m e \033[0m são usados para mudar a cor do erro no comando abaixo:
            - for i in $REQUIRED_FILES; do lftp -u $MODULO_HOMO_FTP_USERNAME,$MODULO_HOMO_FTP_PASSWORD $MODULO_HOMO_FTP_HOST -e "cd $MODULO_HOMO_PATH_DIST; find $i; quit" || (echo -e "\033[0;31mArquivo $i não existe em produção!\033[0m" && exit 5); done
        only:
            - homolog
        when: manual
        environment:
            name: production-fiap
            url: $MODULO_HOMO_ENV_URL
        tags:
            - linux  

    deploy_fiap:
        stage: deploy
        image: alpine:latest
        before_script:
            - apk add --no-cache lftp -q
        script:
            - 'echo "" > app_offline.htm'
            - lftp -u $FIAP_FTP_USERNAME,$FIAP_FTP_PASSWORD $FIAP_FTP_HOST -e "cd $FIAP_PATH_DIST; put app_offline.htm; quit"
            - lftp -u $FIAP_FTP_USERNAME,$FIAP_FTP_PASSWORD $FIAP_FTP_HOST -e "mirror --reverse --no-perms --exclude Mudancas.txt --exclude mudancas.txt --exclude appsettings.json --include Views/Web.config --include Views/Web.config dist/ $FIAP_PATH_DIST --verbose; quit"
            - lftp -u $FIAP_FTP_USERNAME,$FIAP_FTP_PASSWORD $FIAP_FTP_HOST -e "rm $FIAP_PATH_DIST/app_offline.htm; quit"
            # \033[0;31m e \033[0m são usados para mudar a cor do erro no comando abaixo:
            - for i in $REQUIRED_FILES; do lftp -u $FIAP_FTP_USERNAME,$FIAP_FTP_PASSWORD $FIAP_FTP_HOST -e "cd $FIAP_PATH_DIST; find $i; quit" || (echo -e "\033[0;31mArquivo $i não existe em produção!\033[0m" && exit 5); done
        only:
            - master
        when: manual
        environment:
            name: production-fiap
            url: $FIAP_ENV_URL
        tags:
            - linux

    deploy_modulo:
        stage: deploy
        image: alpine:latest
        before_script:
            - apk add --no-cache lftp -q
        script:
            - 'echo "" > app_offline.htm'
            - lftp -u $MODULO_FTP_USERNAME,$MODULO_FTP_PASSWORD $MODULO_FTP_HOST -e "cd $MODULO_PATH_DIST; put app_offline.htm; quit"
            - lftp -u $MODULO_FTP_USERNAME,$MODULO_FTP_PASSWORD $MODULO_FTP_HOST -e "mirror --reverse --no-perms --exclude Mudancas.txt --exclude mudancas.txt --exclude appsettings.json --include Views/Web.config --include Views/Web.config dist/ $MODULO_PATH_DIST --verbose; quit"
            - lftp -u $MODULO_FTP_USERNAME,$MODULO_FTP_PASSWORD $MODULO_FTP_HOST -e "rm $MODULO_PATH_DIST/app_offline.htm; quit"
            # \033[0;31m e \033[0m são usados para mudar a cor do erro no comando abaixo:
            - for i in $REQUIRED_FILES; do lftp -u $MODULO_FTP_USERNAME,$MODULO_FTP_PASSWORD $MODULO_FTP_HOST -e "cd $MODULO_PATH_DIST; find $i; quit" || (echo -e "\033[0;31mArquivo $i não existe em produção!\033[0m" && exit 5); done
        only:
            - master
        when: manual
        environment:
            name: production-modulo
            url: $MODULO_ENV_URL
        tags:
            - linux

    ```

??? example ".NET Framework (FIAP/Módulo) versão power shell"
    ```yml
    #
    # Todas as alterações necessárias neste script ficam aqui:
    #
    # NÃO ESQUECER DE CADASTRAR AS VARIÁVEIS SECRETAS NO MENU Settings/Repository do Projeto 
    # (FIAP_FTP_USERNAME, FIAP_FTP_PASSWORD, FIAP_FTP_HOST, MODULO_FTP_USERNAME, MODULO_FTP_PASSWORD e MODULO_FTP_HOST)
    #
    #
    variables:
        FIAP_HOMO_PATH_DIST: ./Colocar/aqui/o/caminho/de/dentro/do/ftp(servidor fiap)
        FIAP_HOMO_ENV_URL: https://www.colocar.aqui.o.endereco.de.acesso.com.br/alguma/coisa
        MODULO_HOMO_PATH_DIST: ./Colocar/aqui/o/caminho/de/dentro/do/ftp(servidor fiap)
        MODULO_HOMO_ENV_URL: https://www.colocar.aqui.o.endereco.de.acesso.com.br/alguma/coisa
        FIAP_PATH_DIST: ./Colocar/aqui/o/caminho/de/dentro/do/ftp(servidor fiap)
        FIAP_ENV_URL: https://www.colocar.aqui.o.endereco.de.acesso.com.br/alguma/coisa
        MODULO_PATH_DIST: ./Colocar/aqui/o/caminho/de/dentro/do/ftp(servidor modulo)
        MODULO_ENV_URL: https://www.colocar.aqui.o.endereco.de.acesso.com.br/alguma/coisa
        REQUIRED_FILES: '"Web.config" "Views/Web.config"'
        
    cache:
        untracked: true
        key: "%CI_BUILD_REF%"
        paths:
            - packages/
            - "*.Tests"

    before_script:
        - "echo off"

    stages:
        - restore
        - build
        - test
        - homolog
        - deploy

    restore:
        stage: restore
        only:
            - homolog
            - master
        script:
            - if (Test-Path "${CI_PROJECT_NAME}/Properties/PublishProfiles/Homologacao.pubxml") { Write-Host 'Homologacao.pubxml exists.', exit 0 } else { Write-Host 'Homologacao.pubxml does not exist.'; exit 5 }
            - nuget restore -verbosity quiet

    build:
        stage: build
        script:
            - msbuild.exe /verbosity:q
            - msbuild.exe /p:DeployOnBuild=true /p:Configuration=Release /p:PublishProfile=Homologacao.pubxml /p:PublishUrl=$CI_PROJECT_DIR\dist
        only:
            - homolog
            - master
        artifacts:
            paths:
                - dist/
            expire_in: 1 hour

    test:
        stage: test
        only:
            - homolog
            - master
        script:
            - 'nunit3-console.exe ./%CI_PROJECT_NAME%.TST/%CI_PROJECT_NAME%.TST.csproj'
    
    deploy_homolog_fiap:
        stage: homolog
        image: alpine:latest
        before_script:
            - apk add --no-cache lftp -q
        script:
             - lftp -u $FIAP_HOMO_FTP_USERNAME,$FIAP_HOMO_FTP_PASSWORD $FIAP_HOMO_FTP_HOST -e "mirror --reverse --no-perms --exclude Mudancas.txt --exclude mudancas.txt --exclude web.config --exclude Web.config --exclude appsettings.json --include Views/Web.config --include Views/Web.config dist/ $FIAP_HOMO_PATH_DIST --verbose; quit"
            # \033[0;31m e \033[0m são usados para mudar a cor do erro no comando abaixo:
            - for i in $REQUIRED_FILES; do lftp -u $FIAP_HOMO_FTP_USERNAME,$FIAP_HOMO_FTP_PASSWORD $FIAP_HOMO_FTP_HOST -e "cd $FIAP_HOMO_PATH_DIST; find $i; quit" || (echo -e "\033[0;31mArquivo $i não existe em produção!\033[0m" && exit 5); done
        only:
            - homolog
        when: manual
        environment:
            name: production-fiap
            url: $FIAP_HOMO_ENV_URL
        tags:
            - linux 

    deploy_homolog_modulo:
        stage: homolog
        image: alpine:latest
        before_script:
            - apk add --no-cache lftp -q
        script:
            - lftp -u $MODULO_HOMO_FTP_USERNAME,$MODULO_HOMO_FTP_PASSWORD $MODULO_HOMO_FTP_HOST -e "mirror --reverse --no-perms --exclude Mudancas.txt --exclude mudancas.txt --exclude web.config --exclude Web.config --exclude appsettings.json --include Views/Web.config --include Views/Web.config dist/ $MODULO_HOMO_PATH_DIST --verbose; quit"
            # \033[0;31m e \033[0m são usados para mudar a cor do erro no comando abaixo:
            - for i in $REQUIRED_FILES; do lftp -u $MODULO_HOMO_FTP_USERNAME,$MODULO_HOMO_FTP_PASSWORD $MODULO_HOMO_FTP_HOST -e "cd $MODULO_HOMO_PATH_DIST; find $i; quit" || (echo -e "\033[0;31mArquivo $i não existe em produção!\033[0m" && exit 5); done
        only:
            - homolog
        when: manual
        environment:
            name: production-fiap
            url: $MODULO_HOMO_ENV_URL
        tags:
            - linux     

    deploy_fiap:
        stage: deploy
        image: alpine:latest
        before_script:
            - apk add --no-cache lftp -q
        script:
            - lftp -u $FIAP_FTP_USERNAME,$FIAP_FTP_PASSWORD $FIAP_FTP_HOST -e "mirror --reverse --no-perms --exclude Mudancas.txt --exclude mudancas.txt --exclude web.config --exclude Web.config --exclude appsettings.json --include Views/Web.config --include Views/Web.config dist/ $FIAP_PATH_DIST --verbose; quit"
            # \033[0;31m e \033[0m são usados para mudar a cor do erro no comando abaixo:
            - for i in $REQUIRED_FILES; do lftp -u $FIAP_FTP_USERNAME,$FIAP_FTP_PASSWORD $FIAP_FTP_HOST -e "cd $FIAP_PATH_DIST; find $i; quit" || (echo -e "\033[0;31mArquivo $i não existe em produção!\033[0m" && exit 5); done
        only:
            - master
        when: manual
        environment:
            name: production-fiap
            url: $FIAP_ENV_URL
        tags:
            - linux

    deploy_modulo:
        stage: deploy
        image: alpine:latest
        before_script:
            - apk add --no-cache lftp -q
        script:
            - lftp -u $MODULO_FTP_USERNAME,$MODULO_FTP_PASSWORD $MODULO_FTP_HOST -e "mirror --reverse --no-perms --exclude Mudancas.txt --exclude mudancas.txt --exclude web.config --exclude Web.config --exclude appsettings.json --include Views/Web.config --include Views/Web.config dist/ $MODULO_PATH_DIST --verbose; quit"
            # \033[0;31m e \033[0m são usados para mudar a cor do erro no comando abaixo:
            - for i in $REQUIRED_FILES; do lftp -u $MODULO_FTP_USERNAME,$MODULO_FTP_PASSWORD $MODULO_FTP_HOST -e "cd $MODULO_PATH_DIST; find $i; quit" || (echo -e "\033[0;31mArquivo $i não existe em produção!\033[0m" && exit 5); done
        only:
            - master
        when: manual
        environment:
            name: production-modulo
            url: $MODULO_ENV_URL
        tags:
            - linux

    ``` -->
