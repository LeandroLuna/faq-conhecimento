# Template do Merge Request

!!! info "Última modificação"
    **27-11-2023**   Henrique Lopes Mendonça

!!! warning "Informações de uso"
    Criar uma pasta no projeto com seguinte caminho **.gitlab/merge_request_templates**   
    Criar um arquivo dentro dessa pasta com seguinte nome **default.md**

    ```
        # Pré Merge Request

        * [ ] Rodar SonarQube;

        * [ ] Subir em homologação;

        * [ ] Rodar testes unitários;


        ## Qual é o novo comportamento da aplicação?
        - Explicar o funcionamento

        ## Quais tarefas no Azure DevOps contemplam essa MR?
        - [ID da task](link para o azure)

        ## Como testar as mudanças?
        - id-task: como testar

        ## Quem aprovou/validou em homologação?
        - Nome da pessoa, e-mail e data do e-mail confirmando a validação em homolog e 
        aprovando o deploy em produção.

        ## Link do Merge Request de Homologação
        - Link do Merge Request de Homologação, que foi aprovado com as correções.

        ## Número de ticket do Move Desk

        ## Algum comentário adicional
    ``` 