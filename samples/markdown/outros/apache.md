# Apache

Esta página tem como finalidade documentar configurações e processos comuns no uso diário do Apache.

## Virtual Hosts (modelo)

Modelo de virtual hosts para domínios diferentes hospedados na mesma máquina.

```
<VirtualHost *:80>
	ServerAdmin webmaster@localhost
	ServerName algumdominio.fiap.com.br
	DocumentRoot /diretorio/para/o/projeto/
	ErrorLog /var/log/apache2/error.log
	CustomLog /var/log/apache2/access.log combined
</VirtualHost>
```


## Virtual Hosts - HTTPS (modelo)

Modelo de virtual hosts para domínios diferentes hospedados na mesma máquina e que 
utilize HTTPS. Já força o redirecionamento para o HTTPS quando vindo de HTTP.

O chainfile é um arquivo no qual é concatenado a chave pública do servidor seguido 
da chave pública do certificado intermediário enviado pela certificadora.

Repare que são 02 tags \<VirtualHost\>, cada uma ouvindo em um porta (HTTPS e HTTP).

```
<VirtualHost *:443>
  ServerAdmin webmaster@localhost
  ServerName algumdominio.fiap.com.br
  DocumentRoot /diretorio/para/o/projeto/

  SSLEngine on
  SSLCertificateFile /caminho/para/o/certificado_publico.crt
  SSLCertificateKeyFile /caminho/para/o/certificado_privado.key
  SSLCACertificateFile /caminho/para/o/chainfile_intermediario.crt
  
  #Algumas versões do Apache (> 2.4.8) utilizam a linha abaixo no lugar da linha acima
  #SSLCertificateChainFile /caminho/para/o/chained_intermediario.crt

  ErrorLog /var/log/apache2/error.log
  CustomLog /var/log/apache2/access.log combined
</VirtualHost>
<VirtualHost *:80>
   ServerName algumdominio.fiap.com.br
   Redirect permanent / https://algumdominio.fiap.com.br/
</VirtualHost>
```

Ativar o módulo de ssl (caso ainda não esteja ativo) do apache e restartá-lo com os respectivos comandos:

```
a2enmod ssl
service apache2 restart
```

## Bloquear acesso ao arquivo pelo navegador 

Para evitar acesso pelo navegador para algum arquivo especifico, basta colocar no arquivo **.htaccess**
as seguintes configurações:

```
<Files "nome_do_arquivo.extensao">
Order Allow,Deny
Deny from all
</Files>
```

## Bloquear listagem de arquivos do git e arquivos ocultos

No caso de deploys realizados via GIT é interessante que a pasta .git não esteja
acessível no navegador e muito menos outros diretórios/arquivos ocultos.

Para não permitir o acesso, basta inserir as linhas abaixo no .htaccess do projeto.

```
RedirectMatch 404 /\\.git(/|$)
RedirectMatch 404 (?i)/\..+
```


## Bloquear listagem de arquivos 

Para evitar que ao acessar o endereço de um diretório que não possua um arquivo index, 
os arquivos dentro do mesmo sejam listados, basta colocar no arquivo **.htaccess** as 
seguintes configurações:

```
Options -Indexes
```