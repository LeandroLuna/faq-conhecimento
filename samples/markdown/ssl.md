# SSL

## Domínios FIAP que precisam de certificado WildCard

- bancodeimagens.fiap.com.br (192.168.60.11)
- carreiras.fiap.com.br (192.168.10.10)
- cdn.fiap.com.br (192.168.10.10)
- compilador.fiap.com.br (192.168.60.39)
- gitlab.fiap.com.br (172.31.44.247 - AWS)
- homo.fiap.com.br (192.168.12.5)
- homointranet.fiap.com.br (192.168.12.3)
- homointranet3.fiap.com.br (192.168.12.3)
- homoon.fiap.com.br (192.168.12.5)
- homoon1.fiap.com.br (192.168.12.3)
- homovestibular.fiap.com.br (192.168.12.3)
- homowww2.fiap.com.br (192.168.12.3)
- intranet.fiap.com.br (192.168.10.10)
- intranet3.fiap.com.br (192.168.10.10)
- llm.fiap.com.br (192.168.17.1)
- on1.fiap.com.br (192.168.10.10)
- sonar.fiap.com.br (192.168.11.3)
- survey.fiap.com.br (192.168.60.105)
- www2.fiap.com.br (192.168.10.10)
- www4.fiap.com.br (192.168.10.10)
- zoom.fiap.com.br (192.168.60.5)

## Domínios Módulo que precisam de certificado WildCard

- www2.colegiomodulo.com.br (192.168.10.16)
- homo.colegiomodulo.com.br (192.168.12.5)

## Gerar solicitação de assinatura de certificado (CSR) - Linux

Siga as instruções abaixo para gerar uma solicitação de assinatura de certificado:

1 - Realizar o login no terminal do servidor;

2 - Digitar o comando dentro da pasta desejada para salvar a chave (key) e o CSR:
```bash
$ openssl req -new -newkey rsa:4096 -nodes -keyout seudominio.key -out seudominio.csr
```

**Obs:** Substitua **seudominio.key** e **seudominio.csr** pelas informações do seu domínio.

3 - Insira as informações adicionais que serão requisitadas: 

**Nome comum:** o nome de domínio totalmente qualificado. Para certificado curinga, adicione um asterisco (*) à esquerda do nome comum onde você deseja:, *.fiap.com.br.

**Empresa:** Razão social. Para pessoa física, insirir o nome da pessoa.

**Unidade da empresa:** Nome fantasia.

**Cidade ou localidade:** Cidade aonde a empresa esta localizada. Não use abreviaturas.

**Estado:** Estado aonde a empresa esta localizada. Não use abreviaturas.

**País:** duas letras no formato da Organização Internacional para Padronização (ISO) do país empresa.


**OBS:** Não é obrigatório informar uma senha.

## Criar a cadeia de certificados

Para criar a cadeia de certificados basta concatenar o certificado emitido + o certificado intermediário + certificado root, exatamente nesta ordem
em um novo arquivo.

## Certificado digital para o compilador.fiap.com.br

Os certificados deste servidor ficam armazenados em **/certificados/**

Atualmente está separado em pastas contendo o ano de emissão. Ex: /certificados/2019/....

Os arquivos do NGINX que devem ser alterados recebendo o caminho do certificado e da chave que foi usada para gerar o certificado são:

```
/etc/nginx/sites-available/wetty
/etc/nginx/sites-available/alunos
```

Após isto, reiniciar o Nginx através dos comandos:

```
# systemctl restart nginx
```

## Certificado digital para o gitlab.fiap.com.br

Os certificado deste servidor ficam armazenados em **/etc/gitlab/ssl**

O nome do certificado deve ter exatamente o nome do domínio. 
Ex: **gitlab.fiap.com.br.crt** e **gitlab.fiap.com.br.key** para o arquivo
de certificado e a chave privada respectivamente.


Após a substituição dos novos certificados, rodar:
```shell
sudo gitlab-ctl stop
sudo gitlab-ctl reconfigure
sudo gitlab-ctl start
```

## Conferir informações do certificado via linha de comando 

Para visualizar o certificado digital de um domínio:

```shell
openssl s_client -showcerts -connect dominio.com:443
```

Para saber a data de expiração de um SSL de um domínio:

```shell
openssl s_client -connect dominio.com:443 2>/dev/null | openssl x509 -noout -dates
```

## Gerar chave pública a partir de arquivo .pem

```
openssl rsa -in chave_privada.pem -pubout -out chave_publica.pem
```

## Gerar arquivo .crt para instalar no Windows (equivalente ao .pfx) a partir de cadeia de certificados .pem

Com o arquivo abaixo é possível dar dois cliques e instalar no Windows, equivalente instalar via .pfx.

```
openssl x509 -outform der -in cadeia-de-certificados.pem -out arquivo-final.crt
```

## Gerar chave pública e privada a partir de .pfx

Para extrair a chave pública:

```
openssl pkcs12 -in arquivo.pfx -clcerts -nokeys -out certificado.pem
```

Para extrair a chave privada com uma senha para protegê-la:

```
openssl pkcs12 -in arquivo.pfx -nocerts -out chave-privada.pem
```

Para extrair a chave privada sem a necessidade de fornecer uma senha:

```
openssl pkcs12 -in arquivo.pfx -nocerts -out chave-privada.pem -nodes
``` 

## Gerar arquivo .pfx a partir de chaves públicas e privadas
Ver em <http://conhecimento.fiap.com.br/processos/iis/gerar-pfx-a-partir-de-arquivo-cer-e-key/>


## Instalar certificados intermediários e root em servidor Linux

Caso o certificado intermediário e root não esteja instalado no servidor, necessita copiar os
certificados em formato PEM (texto) em:

```shell
sudo cp seu-certificado-raiz.crt /usr/local/share/ca-certificates/
```

e depois executar o seguinte comando:

```shell
sudo update-ca-certificates
```
