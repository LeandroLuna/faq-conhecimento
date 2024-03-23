#Desenvolvimento IOs

## Erro ao assinar aplicativo direto no IPAD

Ao compilar e assinar o aplicativo direto para o IPAD, caso apareça o erro
relacionado codesign, deve-se seguir os seguites passos:

1 - Abrir o programa "Acesso às chaves" (Keychain access)
2 - Bloquear as chaves de "login"
3 - Desbloquear novemente as chaves de "login"
4 - Clean e Build do projeto novamente

Após estes passos, deverá ser compilado para o IPAD normalmente.


## Confiar em um aplicativo personalizado

Acessar no IOs o ícone "Ajustes" -> "Geral" -> "Gerenciamento de Dispositivo"
e então aceitar o desenvolvedor desejado na lista.

## Inserir bibliotecas de terceiros sem o uso de PODs

Baixar o código-fonte da biblioteca e arrastar para a raiz do Workspace do projeto
que irá utilizar a biblioteca o arquivo "<nome-do-projeto>.xcodeproj".

Após isto, arrastar o arquivo "<nome-do-projeto>.framework", presente dentro da pasta
"Products" da biblioteca para a seção "Embedded Binaries". Deverá aparecer automaticamente
na seção "Linked Frameworks and Libraries".
