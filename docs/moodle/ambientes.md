# Ambientes

Esta página tem como finalidade documentar as principais configurações necessárias para o ambiente 
onde o Moodle será executado.

Aqui encontram-se também dicas para, caso seja necessário, realizar a migração entre servidores.

## Arquivo para o virtual host do Apache

Abaixo um exemplo do virtual host utilizado pelo Moodle em produção.

```
<Directory /var/www/html/pasta.do.projeto>
	Options Indexes FollowSymLinks MultiViews
	AllowOverride All
	Order allow,deny
	allow from all
	
	Redirect "/votacao" "https://www2.fiap.com.br/static/RodadaVotacao/"
</Directory>
<VirtualHost *:80>
	ServerAdmin desenvolvimento@fiap.com.br
	ServerName on.fiap.com.br
	DocumentRoot /var/www/html/pasta.do.projeto
	ErrorLog /var/log/apache2/fiapon-error.log
	CustomLog /var/log/apache2/fiapon-access.log combined
</VirtualHost>
```

## Limite de upload do servidor Apache

O servidor Apache, por padrão, vem habilitado para realizar uploads de arquivos com tamanho de
no máximo 2MB.

Para aumentar este limite, é necessário alterar o mesmo dentro do php.ini, reiniciar o servidor
Apache e depois alterar algumas configurações dentro do Moodle.

Os passos necessários são:

**Passo 01**

Dentro do arquivo php.ini (geralmente localizado em: /etc/php/7.0/apache2/php.ini para ambientes Ubuntu com PHP 7),
editar as seguintes linhas para o valor desejado:
```ini
post_max_size = 100M
...
upload_max_filesize = 100M
```

**Passo 02**

Reiniciar o apache

```shell
sudo service apache2 restart
```

**Passo 03**

Dentro do admin do moodle, acessar o caminho abaixo e alterar o valor:

**Administration > Security > Site Policies > Maximum uploaded file size** (Em inglês)

**Administração do site > Segurança > Políticas do Site > Tamanho máximo de arquivo transmitido** (Em português)

Path no servidor: `/admin/settings.php?section=sitepolicies`

**Mais informações:**

[Moodle - documentação - File upload size](https://docs.moodle.org/22/en/File_upload_size)

## Suporte ao LDAP pelo servidor

Para habilitar suporte ao LDAP ao servidor basta inserir/descomentar a seguinte linha no php.ini.

```ini
extension=php_ldap.dll
```  

Após isto, reiniciar o apache 

```shell
sudo service apache2 restart
```

## Suporte ao Redis pelo PHP

Para adicionar o suporte ao redis pelo PHP, é necessário instalar alguns módulos e realizar algumas 
configurações no php.ini

**Passo 01**

Executar no terminal o seguinte comando:

```shell
pecl uninstall redis; n | pecl install redis
```

**Passo 02**

Nos arquivos php.ini inserir a linha abaixo caso não exista:
(`/etc/php/7.0/apache2/php.ini` e `/etc/php/7.0/cli/php.ini`)

```ini
extension=redis.so
```

**Passo 03**

Alterar também no php.ini as informações do session handler 
(inserir as linhas que não existirem / alterar se existente):

```ini
session.save_handler = redis
....
session.save_path = tcp://caminho.para.o.redis.com:6379
```

**Passo Final**

Restartar o Apache

```shell
sudo service apache2 restart
```

## Arquivo de configuração para suporte ao Redis pelo Moodle

Este arquivo de configuração deve ser colocado na raíz do projeto com o nome config.php.

Nele deve constar todas as configurações necessárias para o ambiente. Ex: Dados de conexão, 
caminho dos arquivos, configurações de sessão, etc.

Atualizar o valor das variáveis para as informações verdadeiras de conexão com o banco em cache.

!!! info "Dica 1"
    Para um arquivo de configuração sem suporte ao Redis, basta remover as linhas referentes 
    no final do arquivo 

!!! info "Dica 2"
    Outros exemplos de configurações estão disponíveis no arquivo config-dist.php presente
    dentro do projeto do Moodle

```php
<?php  // Moodle configuration file

unset($CFG);
global $CFG;
$CFG = new stdClass();

$CFG->dbtype    = 'mysqli';
$CFG->dblibrary = 'native';
$CFG->dbhost    = 'host.para.o.mysql';
$CFG->dbname    = 'nome.do.banco';
$CFG->dbuser    = 'usuario.do.banco';
$CFG->dbpass    = 'senha.do.banco';

$CFG->prefix    = 'fiapead_';
$CFG->dboptions = array (
  'dbpersist' => 0,
  'dbport' => '',
  'dbsocket' => '',
);

//$CFG->reverseproxy = true;
$CFG->sslproxy = true;

$CFG->wwwroot   = 'https://on.fiap.com.br';
$CFG->dataroot  = '/dados/dados';

$CFG->admin     = 'admin';

$CFG->directorypermissions = 0777;

//
// As linhas abaixo são para suporte do Redis
//
$CFG->session_handler_class = '\core\session\redis';
$CFG->session_redis_host = 'host.do.redis.com';
$CFG->session_redis_port = 6379;  // Optional.
$CFG->session_redis_database = 0;  // Optional, default is db 0.
$CFG->session_redis_prefix = ''; // Optional, default is don't set one.
$CFG->session_redis_acquire_lock_timeout = 120;
$CFG->session_redis_lock_expire = 7200;

require_once(dirname(__FILE__) . '/lib/setup.php');
```

## Configuração de cache pelo Redis no admin do Moodle

Após realizar as configurações demonstradas acima para o suporte do Redis ao servidor e do arquivo config.php
é necessário configurar no admin o cache de sessão e de aplicação para usar o Redis por padrão.

Isto é feito acessando o seguinte path na aplicação:
`/cache/admin.php`

ou pelo caminho: `Administração do site > Plugins > Caching > Configuração`

**Passo 01:**

Adicionar uma instância do ponto de armazenagem Redis no link **Adicionar instância** da coluna **Ações** da primeira 
tabela da citada no caminho acima. 
`(Tabela de Armazenagens de cache instaladas)`

**Passo final:**

No final da página haverá um link com o nome `Editar mapeamento`.

Após clicar neste link, alterar os combobox disponíveis, selecionando o Redis onde for possível.

!!! info "Observação"
    Nem todos os combobox terão a opção de utilizar o Redis como cache.   