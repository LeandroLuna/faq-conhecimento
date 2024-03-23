#Configuração Servidor Linux .Net

#Instalação Docker
> O Docker sera responsavel por gerenciar as apis .net 

Atualizar pacotes do sistema 
- `sudo apt update`

Atualizar alguns pacotes para utilizar pacotes via https
- `sudo apt install apt-transport-https ca-certificates curl software-properties-common`

Adicionar o pacote oficial do docker ao sistema
- `curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -`
- `sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"`

Verificar se foi o pacote foi adicionado corretamente
- `apt-cache policy docker-ce`

Exemplo:
```
docker-ce:
  Installed: (none)
  Candidate: 5:19.03.9~3-0~ubuntu-focal
  Version table:
     5:19.03.9~3-0~ubuntu-focal 500
        500 https://download.docker.com/linux/ubuntu focal/stable amd64 Packages
```

Instalar Docker
- `sudo apt install docker-ce`

Verificar se o serviço do docker esta rodando Ok
- `sudo systemctl status docker`

Criando um usuario proprio para o docker
- `sudo useradd -m [NomeUsuario]`
- `sudo passwd [NomeUsuario]`

Adicionar usuario criado ao grupo do docker para nao utilizar o sudo no comando docker
- `sudo usermod -aG docker [NomeUsuario]`

# Instalação Portainer
> Portainer e um gerenciador de containers com interface graficar e gerenciamento de usuarios, sem a necessidade de utilizar commandos no shell do linux.

Comando responsavel por criar a instancia do portainer no docker
- `docker run -d -p 8000:8000 -p 9443:9443 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest`

!!! info Atenção aos Pontos
    - Porta **9443** e a porta https com certificado auto assinado
    - Porta **9000** e a porta http não necessario utilizar ela
    - Caso necessario alterar o certificado para proprio e possivel atravez do UI do portainer na aba de settings

# Baixar Imagens Docker Necessarias
- `docker pull node:18-alpine`
- `docker pull quay.io/debezium/server:latest`
- `docker pull mcr.microsoft.com/dotnet/sdk:8.0`
- `docker pull mcr.microsoft.com/dotnet/sdk:7.0`
- `docker pull mcr.microsoft.com/dotnet/sdk:6.0`
- `docker pull mcr.microsoft.com/dotnet/aspnet:8.0`
- `docker pull mcr.microsoft.com/dotnet/aspnet:7.0`
- `docker pull mcr.microsoft.com/dotnet/aspnet:6.0`

!!! info Atenção
    -  mcr.microsoft.com/dotnet/sdk:[verison] sdk do .net para fazer o build no container
    - mcr.microsoft.com/dotnet/aspnet:[version] runtime para rodar o publish do container

# Instalar Nginx - WebServer e ProxyServer
> Nginx sera responsavel por genreciar as requisições as api's e ser o webserver

> Antes de instalar verrificar se contem atualização do sistema.

Comando de Instalar o Nginx
- `sudo apt install nginx`

Verificar se o serviço do nginx esta rodando Ok
- `sudo systemctl status nginx`

!!! caution Atenção
    -  Liberar as portas **HTTP** e **HTTPS** no firewall do linux

Agorar configurar o **Nginx** como proxy reverso, primeiro desvincular a configuração principal
- `sudo unlink /etc/nginx/sites-enabled/default`

Criar o arquivo de configuração do seu dominio
- `sudo nano /etc/nginx/sites-available/domain.conf`

Exemplo de uma configuração Nginx

```
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /path/to/ssl_certificate.crt;
    ssl_certificate_key /path/to/ssl_private_key.key;

    location /api/v1/Financeiro {
        proxy_pass http://backend_server_ip1:backend_server_port;
        # ...
    }

    location /api/v1/ChallengeSprint {
        proxy_pass http://backend_server_ip2:backend_server_port;
        # ...
    }
}
```

Criar link simbolico para o arquivo de configuração
- `sudo ln -s /etc/nginx/sites-available/domain.conf /etc/nginx/sites-enabled/`

Testar a configuração
- `sudo service nginx configtest`

Reiniciar o serviço do nginx para aplicar as configurações
- `sudo service nginx restart`

# Liberar que esse servidor consiga se comunicar com esses outros  servidores
- 10.10 WEB Prod
- 10.9 SQL Prod
- Servidor RabbitMQ
- Liberar Protocolo SMTP