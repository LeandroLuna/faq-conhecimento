# Deploy HTML

O script abaixo é um modelo de deploy automatizado para repositórios de HTML, como Modelos-Email e Modelos-Contratos

Todas as alterações necessárias devem ser realizadas na seção "variables" no topo de cada script.

Caso não seja necessário o deploy no Módulo (por exemplo), basta remover o job "deploy_modulo" do script
e as variáveis referentes ao Colégio Módulo. O mesmo para o ambiente FIAP caso não seja necessário.

**ATENÇÃO!** Proteger a branch master em **Settings > Repository** no GitLab

Descrição das possíveis variáveis de ambiente (Cadastrar em **settings => ci/cd => secrets variables**):

- __FIAP_HOMO_FTP_USERNAME__ ==> Usuário de FTP no servidor de Homologação FIAP
- __FIAP_HOMO_FTP_PASSWORD__ ==> Senha de FTP no servidor de Homologação da FIAP
- __FIAP_HOMO_FTP_HOST__ ==> IP do servidor de FTP de Homologação da FIAP
- __MODULO_HOMO_FTP_USERNAME__ ==> Usuário de FTP no servidor de Homologação do Módulo
- __MODULO_HOMO_FTP_PASSWORD__ ==> Senha de FTP no servidor de Homologação do Módulo
- __MODULO_HOMO_FTP_HOST__ ==> IP do servidor de FTP de Homologação do Módulo
- __FIAP_FTP_USERNAME__ ==> Usuário de FTP no servidor da FIAP
- __FIAP_FTP_PASSWORD__ ==> Senha de FTP no servidor da FIAP
- __FIAP_FTP_HOST__ ==> IP do servidor de FTP da FIAP
- __MODULO_FTP_USERNAME__ ==> Usuário de FTP no servidor do Módulo
- __MODULO_FTP_PASSWORD__ ==> Senha de FTP no servidor do Módulo
- __MODULO_FTP_HOST__ ==> IP do servidor de FTP do Módulo

Descrição das possíveis variáveis do script:

- __FIAP_PATH_DIST__ ==> Path da aplicação no servidor de produção FIAP
- __MODULO_PATH_DIST__ ==> Path da aplicação no servidor de produção Módulo
- __FIAP_HOMO_PATH_DIST__ ==> Path da aplicação no servidor de homologação FIAP
- __MODULO_HOMO_PATH_DIST__ ==> Path da aplicação no servidor de homologação Módulo

## HTML (FIAP/Módulo)

```yml
#
# Todas as alterações necessárias neste script ficam aqui:
#
# NÃO ESQUECER DE CADASTRAR AS VARIÁVEIS SECRETAS NO MENU Settings/Repository do Projeto 
# (FIAP_FTP_USERNAME, FIAP_FTP_PASSWORD, FIAP_FTP_HOST, MODULO_FTP_USERNAME, MODULO_FTP_PASSWORD e MODULO_FTP_HOST)
#
#
image: alpine:3.14.0

variables:
  FIAP_HOMO_PATH_DIST: ./CaminhoDoServidorDeProducaoFiapEmHomolog
  MODULO_HOMO_PATH_DIST: ./CaminhoDoServidorDeProducaoModuloEmHomolog
  FIAP_PATH_DIST: ./CaminhoDoServidorDeProducaoFiapEmProd
  MODULO_PATH_DIST: ./CaminhoDoServidorDeProducaoModuloEmProd

stages:
  - homolog
  - deploy

deploy_homolog_fiap:
  stage: homolog
  before_script:
    - apk add --no-cache lftp -q
  script:
    - lftp -u $FIAP_HOMO_FTP_USERNAME,$FIAP_HOMO_FTP_PASSWORD $FIAP_HOMO_FTP_HOST -e "mirror --reverse --no-perms --exclude .git --exclude .gitlab-ci.yml --exclude .gitignore --exclude README.md --exclude readme.md  --exclude Mudancas.txt --exclude mudancas.txt ./ $FIAP_HOMO_PATH_DIST --verbose; quit"
  environment:
    name: homolog_fiap
  when: manual
  only:
  - homolog
  tags:
  - linux
  
deploy_homolog_modulo:
  stage: homolog
  before_script:
    - apk add --no-cache lftp -q
  script:
    - lftp -u $MODULO_HOMO_FTP_USERNAME,$MODULO_HOMO_FTP_PASSWORD $MODULO_HOMO_FTP_HOST -e "mirror --reverse --no-perms --exclude .git --exclude .gitlab-ci.yml --exclude .gitignore --exclude README.md --exclude readme.md  --exclude Mudancas.txt --exclude mudancas.txt ./ $MODULO_HOMO_PATH_DIST --verbose; quit"
  environment:
    name: homolog_modulo
  when: manual
  only:
   - homolog
  tags:
   - linux

deploy_fiap:
  stage: deploy
  before_script:
    - apk add --no-cache lftp -q
  script:
    - lftp -u $FIAP_FTP_USERNAME,$FIAP_FTP_PASSWORD $FIAP_FTP_HOST -e "mirror --reverse --no-perms --exclude .git --exclude .gitlab-ci.yml --exclude .gitignore --exclude README.md --exclude readme.md  --exclude Mudancas.txt --exclude mudancas.txt ./ $FIAP_PATH_DIST --verbose; quit"
  environment:
    name: production_fiap
  when: manual
  only:
  - master
  tags:
  - linux
  
deploy_modulo:
  stage: deploy
  before_script:
    - apk add --no-cache lftp -q
  script:
    - lftp -u $MODULO_FTP_USERNAME,$MODULO_FTP_PASSWORD $MODULO_FTP_HOST -e "mirror --reverse --no-perms --exclude .git --exclude .gitlab-ci.yml --exclude .gitignore --exclude README.md --exclude readme.md  --exclude Mudancas.txt --exclude mudancas.txt ./ $MODULO_PATH_DIST --verbose; quit"
  environment:
    name: production_modulo
  when: manual
  only:
   - master
  tags:
   - linux

```