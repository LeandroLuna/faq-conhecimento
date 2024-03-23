# Nagios 

> **URL**: http://nagios.fiap.com.br
> <small> 192.168.60.39 </small>

## O que é?

É o serviço de monitoramento e controle de servidores utilizado na FIAP, atualmente está instalado no servidor 192.168.60.39

## Cadastrar servidores

Para cadastrar um novo servidor ao Nagios, deve-se instalar e configurar o NRPE (Nagios Remote Plugin Executor) no servidor desejado, 
que está disponível para todas as plataformas (Windows, OSX, Linux, etc). 

### Instalar e configurar o NRPE <small> Ubuntu/Linux </small>

```sh
> ssh usuario@192.168.xx.yy # Conectar-se ao novo servidor
$ sudo apt update # Atualizar lista dos repositorios
$ sudo apt-get install nagios-nrpe-server nagios-plugins # Instalar o NRPE e seus plugins
```

Após a instalação, para uma funcionalidade básica, deve-se editar o arquivo ```/etc/nagios/nrpe.cfg``` e adequa-lo aos dispositivos existentes no servidor.

```sh
$ sudo nano /etc/nagios/nrpe.cfg 
  allowed_hosts=127.0.0.1,192.168.60.39
  command[check_hda1]=/usr/lib/nagios/plugins/check_disk -w 20% -c 10% -p /dev/sda1
```

Após a configuração acima, **reiniciar** o serviço do nagios:

```shell
$ sudo service nagios-nrpe-server restart
```

!!! danger "Atenção"
    Deve-se liberar a comunicação TCP/IP na porta **5666** entre o novo servidor e o servidor do Nagios


### Instalar e configurar o NRPE <small> Windows </small>

Para instalar no Windows, é necessário realizar o download do NSClient++.

[Página oficial](https://www.nsclient.org/)

[GitHub](https://github.com/mickem/nscp/)

[Documentação](https://docs.nsclient.org/getting_started/)

**OBSERVAÇÕES:** 

O caminho de instalação padrão é: **C:\Program Files\NSClient++**

Arquivo de configuração: **C:\Program Files\NSClient++\nsclient.ini**. É neste arquivo que deve-se colocar
os comandos personalizados.

Caminho para scripts personalizados: **C:\Program Files\NSClient++\scripts\custom**.

Para reiniciar o NSClient++ no Windows:
```shell
net stop nscp
net start nscp
```


### Adicionar o novo servidor ao Nagios

Para adicionar o novo servidor ao monitoramento do Nagios, deve-se acessar o servidor do Nagios (192.168.60.39) e editar os arquivos de configuração.

1. Adicionar o novo servidor ao hosts do Nagios
    ```sh
    $ sudo nano /etc/hosts
      ...
      192.168.xx.yy servidor2018.fiap.com.br
      ...
    ```

2. Editar o arquivo /usr/local/nagios/etc/objects/localhost.cfg e adicionar o novo host ao members
    ```sh
    $ sudo nano /usr/local/nagios/etc/objects/localhost.cfg
      ...
          members apis.fiap.com.br,servidor2018.fiap.com.br...
      ...
    ```

3. Criar o arquivo referente ao novo servidor na pasta /usr/local/nagios/etc/servers/
    ```sh
    $ sudo nano /usr/local/nagios/etc/servers/servidor2018.cfg
    ```

???- note "servidor2018.cfg"
    ```  hl_lines="3 4 5 10 18 25 33 40 48"
    define host {
      use	linux-server
      host_name	servidor2018.fiap.com.br
      alias		FIAP ON 2018 Server 2
      address		52.203.239.172
    }

    define service{
      use                             local-service         ; Name of service template to use
      host_name                       servidor2018.fiap.com.br
      service_description             Root Partition
      check_command                   check_nrpe!check_xvda1
      }


    define service{
      use                             local-service         ; Name of service template to use
      host_name                       servidor2018.fiap.com.br
      service_description             Current Users
      check_command                   check_nrpe!check_users
      }

    define service{
      use                             local-service         ; Name of service template to use
      host_name                       servidor2018.fiap.com.br
      service_description             Total Processes
      check_command                   check_nrpe!check_total_procs
      }

        
    define service{
      use                             local-service         ; Name of service template to use
      host_name                       servidor2018.fiap.com.br
      service_description             Zombie Process
      check_command                   check_nrpe!check_zombie_procs
      }

    define service{
      use                             local-service         ; Name of service template to use
      host_name                       servidor2018.fiap.com.br
      service_description             SSH
      check_command                   check_ssh
      }


    define service{
      use                             local-service         ; Name of service template to use
      host_name                       servidor2018.fiap.com.br
      service_description             HTTP
      check_command                   check_http
      # notifications_enabled           0
      }
    ```


!!! danger "Atenção"
      Após qualquer alteração no Nagios, deve-se reiniciar o serviço usando **```service nagios restart```**
        