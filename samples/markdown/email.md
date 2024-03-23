# Envio de e-mails modelo

Para enviar um e-mail utilizando um modelo deve-se:
 
1. Preparar o modelo do e-mail substituindo todos os campos placeholder para o padrão do Razor. Exemplo: **@NOME** para **@Model.Nome**
2. Adicionar esse modelo no [**repositório do Git**](https://gitlab.fiap.com.br/html/modelos-email) de modelos de e-mail, na pasta do **SistemaOrigem**
3. Deixar os modelos nessa pasta em HTML com nome condizente ao conteúdo do e-mail.
 
Existem basicamente três formas de utilizar esse sistema, via banco de dados, via API e via .NET.
 
### API (RESTful)
 
Basta fazer um POST em https://apis.fiap.com.br/envio-email/v1/
 
Passando uma chave KeyAuth (abaixo o consumer Portal no Kong)
 
```Authorization: Pegar no Kong Token Valido```
 
E o corpo em JSON contendo os dados para o envio do e-mail, exemplo:
```json
{
    "De": "angelo.m.bartolome@gmail.com",
    "Para": [ "angelo.bartolome@fiap.com.br" ],
    "SistemaOrigem": "Autenticacao",
    "Modelo": "RecuperacaoSenha",
    "Assunto": "[FIAP] - Recuperação de Senha",
    "Dados" : { 
        "Nome": "Angelo",
        "Url": "http://www2.fiap.com.br"
    }
}
``` 

### Banco de Dados (SQL)
 
Para enviar usando SQL, deve-se inserir uma linha na tabela ControleEmailModelo do Site_Fiap que pede os seguintes parâmetros:
 
- SistemaOrigem – O nome do sistema que você criou a pasta no ModelosEmail
- Modelo – O nome do modelo que está na pasta (sem o .html)
- DadosEnvio – Linha XML contendo os dados do destinatário e do email em geral
- Processado – Marcar como 0
- DadosModelo - Linha XML contendo os dados que substituirão os placeholders do email
 
Para montar o XML do DadosEnvio:
 
```sql
(SELECT TOP 1
    'Assunto do E-mail' AS 'Assunto',
    'Destinatários do E-mail' AS 'Para',
    'Destinatários com cópia' AS 'ComCopia',
    'Remetente do E-mail' AS 'De'
FOR XML RAW)
```
 
Para montar o XML do DadosModelo, você precisa incluir todos os campos que estão no **@Model** do modelo do e-mail, aqui usando o exemplo de ter o campo *Nome* e *Chave* no modelo do email:
```sql
(SELECT TOP 1
    'Nome' AS Nome',
    'Chave' AS Chave'
FOR XML RAW)
```

Agora para enviar o e-mail com todos os campos completos:

```sql 
INSERT INTO
Site_Fiap..ControleEmailModelo
SELECT
       'Shift', -- Sistema Origem
       'emkt_2016_inicio-curso', -- Modelo
       (SELECT TOP 1
            'Assunto do E-mail' AS 'Assunto',
            'Destinatários do E-mail' AS 'Para',
            'Destinatários com cópia' AS 'ComCopia',
            'Remetente do E-mail' AS 'De'
        FOR XML RAW), -– DadosEnvio
        0, -- Processado
        (SELECT TOP 1
            'Nome' AS 'Nome',
            'Chave' AS 'Chave'
        FOR XML RAW) -- DadosModelo
```
 
### C# .NET
 
Basta adicionar o pacote **EnviaMail** do *Nuget* da FIAP.
 
Criar uma instancia da classe AcessoNegocio, chamar o método EnviaEmail passando um objeto do tipo EnviaEmail.Negocio.Email contendo os dados para envio.
 
Exemplo:
```csharp
var enviaEmail = new EnviaMail.Email();
var email = enviaEmail.Enviar(new EnviaMail.Negocio.EmailMOD
{
    CodigoUsuarioEnvio = new CamposSessao().CodigoUsuario, // Opcional, preencher com 1 caso não tenha
    Assunto = "FIAP - Matrícula On-line",
    De = "naoresponda@fiap.com.br",
    Para = destinatarios.ToArray(), // Array de strings com os destinatários
    ComCopia = new string[] { "helpcenter@fiap.com.br" },
    SistemaOrigem = "MatriculaVestibular",
    Modelo = "ContratoPronto",
    Dados = modelo // Objeto com os dados do modelo
});
```

## Serviço que envia os e-mails

O Windows Service que envia e-mails que utilizam modelo está instalado no 
**servidor Web de produção da FIAP (192.168.10.10)**
com o nome de **ControleEmailModelo**.

## Dicas

É possível saber através da tabela **ControleEmailModeloNagios** quando foi o 
momento aproximado em que parou de funcionar, caso aconteça.
