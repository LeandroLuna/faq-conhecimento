# Contratos

Para gerar um contrato utilizando um modelo deve-se:
 
1. Preparar o modelo do contrato substituindo todos os campos placeholder para o padrão do Razor. Exemplo: **@NOME** para **@Model.Nome**
2. Adicionar esse modelo no [**repositório do Git**](https://gitlab.fiap.com.br/html/modelos-contratos) de modelos de e-mail, na pasta do **SistemaOrigem**
3. Deixar os modelos nessa pasta em HTML com nome condizente ao conteúdo do contrato.
 
Existem basicamente duas formas de utilizar esse sistema, via API e via Lib .NET.
 
### API (RESTful)
 
Existem três rotas na API que gera os contratos.

1. Gerar o Contrato e retornar o HTML: 
    - ```v1/Gerar/RetornarHtml?sistema=MatriculaPos```
2. Gerar o Contrato e retornar o PDF: 
    - ```v1/Gerar/RetornarPdf?sistema=MatriculaPos```
3. Gerar o Contrato, salvar o PDF e retornar o caminho: 
    - ```v1/Gerar/GerarPdf?sistema=MatriculaPos&rm=712345```

Em todas essas rotas, basta fazer um POST em https://apis.fiap.com.br/contrato/v1/
 
Passando uma chave de autorização (abaixo como exemplo o consumer *Portal* no Kong)
 
```Authorization: 0b9d173a6c2fac4652ffbd42991510d6```
 
E o corpo em JSON contendo os dados para que o contrato seja gerado:
```json hl_lines="6 9 20"
{
    "Header": {
        "Dados": {
            // Alguns modelos de cabeçalho aceitam dados, caso necessário, popular aqui
        },
        "Modelo": "FIAP"
    },
    "Conteudo": {
        "Modelo": "TermoCienciaOnline",
        "Dados": {
            "Nome": "Angelo Stefanos Mavridis Bartolome",
            "RM": "75008",
            "Curso": "Engenharia de Computação (noturno)"
        }
    },
    "Footer": {
        "Dados": {
            // Alguns modelos de rodapé aceitam dados, caso necessário, popular aqui
        },
        "Modelo": "FiapLins"
    }
}
``` 

!!! warning "Atenção"

    1. Deve-se sempre fazer um cast explicito quando não tratar de tipos string no modelo do contrato. 
        - Exemplo: ```@if((bool) Model.AlunoAtivo)``` ao invés de ```@if(Model.AlunoAtivo)```
    2. Observar qual modelo de [**cabeçalho**](https://gitlab.fiap.com.br/html/modelos-contratos/tree/master/Headers) e [**rodapé**](https://gitlab.fiap.com.br/html/modelos-contratos/tree/master/Footers) utilizar quando for gerar o contrato, e popular conforme o modelo.
    3. Sempre popular corretamente a propriedade Dados do JSON.
    4. Na rota **GerarPdf**, é obrigatório passar o **RM**, pois o PDF é salvo por padrão na pasta de contratos do aluno pelo RM seguindo o modelo: ```/updown/Contratos/sistema/rm/modelo/md5Contrato.pdf```
 
### C# .NET
 
Basta adicionar o pacote **Contrato** do *Nuget* da FIAP.
 
Criar uma instancia da classe AcessoNegocio, chamar o método EnviaEmail passando um objeto do tipo EnviaEmail.Negocio.Email contendo os dados para envio.
 
Exemplo:
```csharp
var urlContrato = new GeradorContrato().Gerar(rm, contrato, sistema);
```