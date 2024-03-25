# Atendendo Demandas e Realizando Alteração em Sistemas

Sempre que surgir a demanda ou necessidade de realizar alguma **alteração** em 
um sistema, certifique-se de que esta demanda está vinculada à um Ticket do 
[Movidesk - Service Desk](https://helpdesk-fiap.movidesk.com/) 
ou um Ticket do
[Azure DevOps](https://dev.azure.com/ProjectCenterFiap/). 
Se **não existir** um ticket, peça ao solicitante que 
**envie a demanda por e-mail** para [dev@fiap.com.br](mailto:dev@fiap.com.br), 
ou abra você mesmo o **Ticket**.

Para realizar uma **alteração em um sistema**, atenda às seguintes orientações:

**Criar branch** no sistema para realizar **correção/implementação**:

- Caso seja uma **Correção de Bug**, seguir o padrão: 
`bugfix/numeroticket-breve-descricao`
- Caso seja a **Implementação de uma Nova Funcionalidade**, seguir o padrão: 
`feature/numeroticket-breve-descricao`

Quando a alteração estiver **pronta**, subir para a **branch** `homolog` e 
solicitar validação do usuário.

Quando for **homologado** (validado pelo usuário), subir para a **branch** `dev` 
e então para a `master` (Produção).

## Fluxos das branchs do sistema

**Correção de Bug**:
`bugfix/numeroticket-breve-descricao` **>** `homolog` **>** `dev` **>** `master`

**Implementação de uma Nova Funcionalidade**:
`feature/numeroticket-breve-descricao` **>** `homolog` **>** `dev` **>** `master`