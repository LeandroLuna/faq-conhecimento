# Autenticação

Passo a passo da cadeia de autenticação do aplicativo FIAP ON

1. Aluno digita usuário e senha
    - Caso a API não retorne o token, deve exibir a mensagem "Usuário ou Senha inválidos"
    - Caso não haja conexão com a internet, deve-se exibir a mensagem "Sem conexão com a internet
    - Caso a API retorne erro, deve-se exibir "Erro ao consultar dados, tente novamente"
2. Guarda-se o token e busca os dados do perfil do usuário
3. Guarda-se os dados do perfil do usuário no banco de dados
    - Associa no banco de dados o token ao usuario, se já tiver o usuario (userid), deve-se atualizar o mesmo.
4. Prosseguir para a tela principal