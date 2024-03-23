# DevON

Este guia oferece instruções abrangentes para configurar o ambiente de testes do DevON usando o XAMPP. Este ambiente é particularmente valioso, pois, ao contrário do localhost, permite realizar solicitações de API, reproduzir vídeos, carregar as informações do Fast Test e Feedback, acessar informações do capítulo, entre outras funcionalidades, sem qualquer restrição.

## Chocolatey

Chocolatey é uma solução de gerenciamento de software que lhe dá a liberdade de criar um pacote de software simples e implantá-lo em qualquer lugar com o Windows usando qualquer uma de suas ferramentas familiares de configuração ou gerenciamento de sistema.

Se você já usou yum, apt, pacman ou qualquer gerenciador de pacotes no Linux ou Homebrew em um Mac, você já sabe o que é Chocolatey. Chocolatey é o gerenciador de pacotes do Windows, da mesma forma que o RPM é um gerenciador de pacotes para Linux.

### Verificando a instalação do Chocolatey

Certifique-se de que o Chocolatey está instalado abrindo o PowerShell como administrador e executando:

```powershell
choco -v
```

Se o Chocolatey não estiver instalado, execute o seguinte comando:

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

## XAMPP 

O XAMPP é um pacote de software livre que facilita a criação de um ambiente de desenvolvimento local para web.

O software é projetado para ser fácil de instalar e configurar, proporcionando um ambiente de desenvolvimento local que simula as configurações encontradas em servidores web ao vivo. Isso é útil para desenvolvedores web, pois permite que eles testem e depurem seus sites e aplicativos localmente antes de torná-los públicos na internet. Além disso, o XAMPP é uma opção popular para criar servidores web locais em ambientes de aprendizado e treinamento.

### Instalando o XAMPP

Após verificar o Chocolatey, instale o XAMPP usando o seguinte comando no PowerShell:

```powershell
choco install xampp-74
```

Responda com "Yes" quando perguntado se tem certeza de que deseja instalar. Uma mensagem deve aparecer quando a instalação estiver completa.

Anote o caminho de instalação do XAMPP, pois utilizaremos logo mais.

### Configuração do XAMPP

O caminho de instalação padrão do XAMPP é `C:/xampp/`. Caso tenha escolhido um caminho diferente, ajuste os próximos passos conforme necessário.

Inicie o XAMPP Control para acessar o painel de controle.

Abra o arquivo `Httpd-conf`, clicando em `config` em frente ao Apache, no XAMPP.

Modifique as seguintes linhas:

```apache
DocumentRoot "C:/xampp/htdocs"
<Directory "C:/xampp/htdocs">
```
para

```apache
DocumentRoot "C:/xampp/htdocs/ead"
<Directory "C:/xampp/htdocs/ead">
```

Apague todos os arquivos em `C:/xampp/htdocs`.

Dentro dessa mesma pasta (`C:/xampp/htdocs`), execute os seguintes comandos para clonar os repositórios necessários:

```bash
git clone git@gitlab.fiap.com.br:php/ead.git
git clone git@gitlab.fiap.com.br:php/ead_data.git
```

Copie o arquivo `config.php` da pasta `ead_data` para `C:/xampp/htdocs/ead`.

### Configuração do hosts

Vá até `C:/Windows/System32/drivers/etc` e abra o arquivo `hosts` como Administrador.

No final do arquivo, adicione a seguinte linha:

```
127.0.0.1 devon.fiap.com.br
```

### Iniciar serviço Apache

No XAMPP Control, clique em "Start" para iniciar o serviço Apache.

### Testar no navegador

Abra o seu navegador e acesse `devon.fiap.com.br`. 
   
> Lembre-se de utilizar o protocolo HTTP. Do contrário, utilizando HTTPS não irá funcionar. 

Use as seguintes credenciais:

> **Usuário:** {seu cl}

> **Senha:** 123456

Se o login for bem-sucedido, a instalação foi concluída com sucesso.

## Testar conteúdos

Após concluir a configuração do ambiente DevON, você pode testar conteúdos na plataforma seguindo as etapas abaixo:

Certifique-se de ter o Python 3+ instalado na sua máquina. Para tal, execute o seguinte comando no CMD:

```bash
py --version
```

Caso não tenha o Python instalado, baixe-o no site: https://www.python.org/downloads/. Siga a instalação padrão.

Feito isso, navegue até a pasta "conteudos" do repositório `ead_data` - que deve está localizado em `C:/xampp/htdocs`.

Execute o seguinte comando para instalar as dependências:

```bash
py install.py
```

Agora, no capítulo que você queira testar, execute o seguinte comando para iniciar o servidor local:

```bash
npm run start
```

Faça login na plataforma DevON.

Abra qualquer conteúdo desejado na plataforma.

Na URL, substitua "view.php" por "test.php". Por exemplo, altere:

```plaintext
http://devon.fiap.com.br/mod/conteudoshtml/view.php?id=322855&c=9125&sesskey=xxxxxxx
```

para:

```plaintext
http://devon.fiap.com.br/mod/conteudoshtml/test.php?id=322855&c=9125&sesskey=xxxxxxx
```

Após completar essas etapas, todas as alterações realizadas serão refletidas na página de teste.

Agora, você está pronto para testar e validar qualquer modificação feita nos conteúdos da plataforma DevON!