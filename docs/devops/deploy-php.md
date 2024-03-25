# Deploy PHP

Todas as alterações necessárias devem ser realizadas na seção "variables" no topo de cada script.

**ATENÇÃO!** Proteger a branch master em **Settings > Repository** no GitLab

Descrição das possíveis variáveis de ambiente (Cadastrar em **settings => ci/cd => secrets variables**):

- **FTP_USERNAME**   ==> Usuário de FTP no servidor da FIAP
- **FTP_PASSWORD**   ==> Senha de FTP no servidor da FIAP
- **FTP_HOST**       ==> IP do servidor de FTP da FIAP

```
stages:
  - build
  - deploy

variables:
  PATH_DIST: ./caminho/dentro/do/servidor

build:
  stage: build
  image: composer:2.0.4
  script:
    - composer install --no-dev --optimize-autoloader --no-interaction --no-progress --no-suggest
  only:
    - main
  tags:
    - linux
  artifacts:
    paths:
      - vendor/
    expire_in: 1 hour


deploy:
  stage: deploy
  image: alpine:3.12.1
  before_script:
    - apk add --no-cache lftp -q
  script:
    - lftp -u $FTP_USERNAME,$FTP_PASSWORD $FTP_HOST -e "mirror --reverse --dereference --transfer-all --overwrite --no-perms --exclude .env.example --exclude README.md --exclude phpunit.xml --exclude .git --exclude .gitignore --exclude vendor/bin --exclude tests/ ./ $PATH_DIST --verbose; quit"
  only:
    - main
  environment:
    name: production
    url: https://endereco.final.aqui
  tags:
    - linux
```