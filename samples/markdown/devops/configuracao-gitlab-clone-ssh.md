# Configuração para Clonar Repositórios do GitLab via SSH

## Gerando Chave SSH

Para clonar repositórios do GitLab via **SSH** é necessário gerar uma 
**chave SSH**. Para isso, siga os seguintes passos:

- Acesse o [GitLab](https://gitlab.fiap.com.br/);
- No canto superior direito, clique na sua foto de perfil e acesse a opção 
**Edit Profile**;
- No menu lateral esquerdo, clique em **SSH Keys**;
- É possível acessar a página do link 
[Learn More](https://gitlab.fiap.com.br/help/user/ssh.md) para mais informações, 
mas para facilitar o procedimento, abra o **Terminal do Windows** (**CMD**) em 
qualquer pasta e execute o comando abaixo, para gerar uma **chave SSH** com 
**criptografia RSA**:

    ```bash
    ssh-keygen -t rsa -b 2048 -C "<IDENTIFICADOR DA CHAVE>"
    ```

    É necessário informar um **identificador da chave SSH**, pois é 
    possível ter mais de uma chave SSH, para computadores diferentes, por 
    exemplo.

- Ao executar o comando acima, será solicitado um **nome de arquivo** para 
salvar a chave. **Não é necessário** informar um nome, então apenas pressione 
**Enter**;
- Será solicitada também uma senha de acesso (**passphrase**) para a chave SSH 
gerada. Informe uma senha (não será exibida no terminal ao digitar), e na 
confirmação informe a mesma senha; 

    Por segurança, é recomendado colocar uma **senha** na 
    **chave SSH**, apesar de ser possível deixá-la **sem senha**;

- Copie o caminho do arquivo exibido, onde se encontra sua chave pública 
(**public key**)
e execute o comando abaixo (lembrar de utilizar barras invertidas no caminho):

    ```bash
    notepad <caminho\da\chave\publica.pub>
    ```

- Copie toda a chave exibida (desde "ssh-rsa" até o &lt;idenficador da chave&gt;) 
e informe no campo **Key** da página **SSH Keys** do **GitLab**;
- Remova a **data de expiração** e clique em **Add key**;

## Clonando Repositório do GitLab via SSH

Para clonar os repositórios via **SSH**, siga os seguintes passos:

- Acesse a página do repositório que deseja clonar no GitLab e copie o 
**URL** de clone via **SSH**;
- Abra o **Terminal do Windows** (**CMD**) na pasta que deseja clonar o 
repositório;
- Execute o comando: 

    ```bash
    git clone <URL SSH COPIADA>
    ```

- Quando for solicitada a **senha da chave SSH** informe a senha criada no ato 
da emissão da chave e pressione **Enter**;
