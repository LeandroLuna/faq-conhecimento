#Usuários

Está página tem como finalidade documentar os detalhes dos perfis de usuários do LimeSurvey.

!!! warning "Importante!!"
    O padrão de nome de usuário é o mesmo do e-mail da FIAP. **Ex:** `fulano.de.tal@fiap.com.br` será `fulano.de.tal`

## Permissões

Para o maior controle do acesso das funcionalidades do sistema, são definidos algumas permissões
específicas para cada perfil de usuário.

Considerar abaixo as permissões para o tipo de usuário que você quer:

#### Analista de Dados, Business Intelligence

Esses são os usuários que apenas possuem acesso aos relatórios

##### Permissões
- Questionários: ("Ver/ler") 
- Usar autenticação do banco de dados interno




#### 	Integração com sistemas

Esses são os usuários usados dentro de sistemas para integração com o LimeSurvey

##### Permissões
- Questionários: ("Criar", "Ver/ler", "Atualizar")
- Usar autenticação do banco de dados interno	




#### Gerenciador 1

Esses são os usuários gerenciadores com a menor número de permissões

##### Permissões
- Questionários: ("Criar", "Ver/ler", "Atualizar", "Exportar")
- Usar autenticação do banco de dados interno	




#### Gerenciador 2

São os usuários gerenciadores com o maior número de permissões, porém abaixo do admin

##### Permissões
- Banco de dados central de participantes:  ("Criar", "Ver/ler", "Atualizar", "Apagar", "Importar", "Exportar")
- Questionários:  ("Criar", "Ver/ler", "Atualizar", "Apagar", "Exportar")
- Usar autenticação do banco de dados interno	