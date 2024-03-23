# Onboarding de Novos Desenvolvedores na Stack de Back-end

Esta documentação foi desenvolvida a fim de facilitar a **configuração inicial**
da máquina dos **desenvolvedores back-end DotNet** recém-contratados.

Sempre que necessário, sinta-se a vontade para modificar ou adicionar novas 
etapas.

## Acesso ao 192.168.10.41

Para começar, será necessário solicitar a uma das **pessoas abaixo** o acesso às 
pastas do servidor **192.168.10.41**, bem como a inclusão do desenvolvedor ao 
grupo de acesso **Desenvolvimento** no **10.41**:

- [Henrique Lopes - Chat Teams](https://teams.microsoft.com/l/chat/0/?users=henrique.mendonca@fiap.com.br);
- [Douglas Cabral - Chat Teams](https://teams.microsoft.com/l/chat/0/?users=douglas.cabral@fiap.com.br);
- [Francisco Esteves - Chat Teams](https://teams.microsoft.com/l/chat/0/?users=festeves@fiap.com.br);

Não se preocupe, pois é possível continuar boa parte da configuração antes de 
receber o acesso.

### Acesso ao 10.41 concedido

- Pressione **Win+R**;
- Informe o IP "\\\\192.168.10.41\\";
- Realize o login inicial:

    ```
    Usuário: fiap\nome.sobrenome  ou  fiap\clXXXX
    OU
    Usuário: nome.sobrenome  ou  clXXXX

    Senha: mesma senha utilizada no AD
    ```

!!! warning "Observação"
    Verificar se o desenvolvedor está com acesso às pastas **E**, **G** e **P**
    do **10.41**. Caso não tenha acesso, certificar-se de que ele está no grupo 
    **Desenvolvimento** do **10.41**.

## Configuração do Arquivo Hosts

No Windows Explorer (**Win+E**), busque pela pasta 
**C:\Windows\System32\drivers\etc\\** e configure o arquivo **hosts** de acordo
com o arquivo 
[hosts.txt](http://conhecimento.fiap.com.br/processos/onboarding-novos-devs/back-end/hosts.txt).

## Baixar o Visual Studio Community e o SQL Server Management Studio

[Link para Baixar o Visual Studio](https://visualstudio.microsoft.com/pt-br/vs/community/)

[Link para Baixar o SQL Server](https://learn.microsoft.com/pt-br/sql/ssms/download-sql-server-management-studio-ssms?view=sql-server-ver16#download-ssms)

## Habilitando IIS (Serviços de Informações da Internet)

Acesse 
**Menu Windows > Painel de Controle > Programas > Ativar ou desativar recursos do Windows**
e busque por **Serviços de Informações da Internet**.

É indicado configurar a pasta **Serviços da World Wide Web** separadamente 
**após** a configuração e confirmação das outras 2 pastas, para 
**evitar retrabalho** ao selecionar todas as configurações de uma só vez e se 
depara com algum erro. Selecione as opções conforme a imagem abaixo. 

![HabilitandoIIS](http://conhecimento.fiap.com.br/processos/onboarding-novos-devs/back-end/HabilitandoIIS.png)  

## Variáveis de Ambiente

Acesse 
**Menu Windows > Editar as variáveis de ambiente do sistema > Variáveis de Ambiente...** 
e configure as variáveis abaixo:

```
DB_ADDRESS: FPSQLDEV\FPDEV
DB_PASSWORD: !pfgm@07
DB_USER_ID: sa
```

!!! warning "Observação"
    Sempre que for necessário adicionar ou atualizar as variáveis de ambiente, 
    lembre-se de rodar o comando **iisreset** no **CMD** como **Administrador**,
    e também **reiniciar** as instâncias do **Visual Studio** para que as 
    variáveis sejam recarregadas.

## Acesso aos repositórios principais do GitLab

Primeiramente, configure o [Clone via Chave SSH no GitLab](http://conhecimento.fiap.com.br/devops/configuracao-gitlab-clone-ssh/).

Então, conceda (ou solicite) acesso a alguns dos [**Principais Projetos**](http://conhecimento.fiap.com.br/dotnet/principais-projetos/) no GitLab.

Para conceder acesso, no link do repositório vá até 
**Settings > General > Visibility, project features, permissions > Project Members > Invite Member**.

Selecione o usuário que receberá acesso e no campo **role**, selecione 
**Developer**.

Configure os projetos no IIS conforme o **README** dos repositórios.

## Habilitando NuGet da FIAP

Já com ao menos um projeto clonado, abra o projeto no **Visual Studio** e na 
janela **Solution Explorer**, clique com o botão direito na 
**Solution '{Nome.Projeto}' > Manage NuGet Packages for Solution...**.

No canto superior direito do **NuGet - Solution** (janela recém-aberta), clique
na engrenagem do **Package source** e então em **Adicionar (+)**:

```
Name: FIAP
Source: http://nuget.fiap.com.br/nuget
```

Pressione **OK** e o novo **Package source** já estará configurado, pronto para 
utilizar.