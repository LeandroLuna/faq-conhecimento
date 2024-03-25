# Configuração para Clonar Repositórios do GitLab via HTTPS

## Gerando Access Token

Para clonar repositórios do GitLab via **HTTPS** é necessário gerar um 
**Access Token**. Para isso, siga os seguintes passos:

- Acesse o [GitLab](https://gitlab.fiap.com.br/);
- No canto superior direito, clique na sua foto de perfil e acesse a opção 
**Edit Profile**;
- No menu lateral esquerdo, clique em **Access Tokens**;
- Informe um **nome de identificação** para o token (este nome é necessário para
facilitar a identificação do token, já que é possível ter mais de um token de
acesso);
- Informar a **data de expiração** do token (para uma maior segurança, é 
recomendado que o token expire em 1 mês);
- Selecione as checkboxes **read_repository** e **write_repository** para que, 
ao utilizar este **Access Token**, seja permitida leitura e escrita nos 
repositórios;
- Clique em **Create personal access token**;

**Guarde** em algum lugar seguro o token gerado, pois ele será utilizado para 
clonar os repositórios via **HTTPS**.

## Clonando Repositório do GitLab via HTTPS

Para clonar os repositórios via **HTTPS**, siga os seguintes passos:

- Acesse a página do repositório que deseja clonar no GitLab e copie o 
**URL** de clone via **HTTPS**;
- Abra o **Terminal do Windows** (**CMD**) na pasta que deseja clonar o 
repositório;
- Execute o comando: 

    ```bash
    git clone <URL HTTPS COPIADA>
    ```

- Quando for solicitado o nome de usuário e a senha, informe seu **CL** (Ex: **cl1660**) no 
**nome de usuário** e o **Access Token** na **senha**. Esta credencial ficará 
salva no Windows e poderá ser alterada no **Gerenciador de Credenciais**;

## Observação

Este **Access Token** expira na **data informada** no ato da emissão, logo, após 
esta data será necessário editar a **Credencial** no 
**Gerenciador de Credenciais** do Windows.
