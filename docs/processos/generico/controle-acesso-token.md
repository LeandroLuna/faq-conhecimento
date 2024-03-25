#Controle de acesso via Token

Por questões de segurança, alguns sistemas como a Ficha de Inscrição da Pós, por exemplo, é solicitado ao usuário que ele informe um
token, para que seja possível confirmar a sua identidade.

Abaixo como esse processo ocorre.

<div style="height: 360px; overflow-x:scroll;">
  <img src="../controle-acesso-token.svg" style="max-width: initial;">
</div>

<sup> Mapeado por <a href="https://teams.microsoft.com/l/chat/0/?users=vanessa.marques@fiap.com.br"> Vanessa Marques </a> </sup>

## Procedures

### Envio
Para realizar a chamada da procedure de envio, é necessário informar alguns dados:

**Sistema de origem e codigoIdentificador**

De qual sistema a procedure deve procurar os dados do usuário e qual código será utilizado para identificar o usuário. Atualmente, a
procedure atende a esses sistemas:

- **InscricaoVestibular**: Recupera os dados da tabela *Civ..Vestibulando*. O código identificador deve ser o CodVestibulando

- **InscricaoMBA**: Recupera os dados das tabelas *webadm..pos_inscricao_new* e *webadm..PI_Cadastro*. O código identificador deve ser o
código da tabela *pos_inscricao_new*

- **ProUni**: Recupera os dados da tabela *proUni..cadastro*. O código identificador deve ser o Codigo

- **MatriculaOnLineGraduacao**: Recupera os dados da tabela *Civ..Vestibulando*. O código identificador deve ser o CodProcessoVestibulando 
da tabela *ProcessoVestibulando*

- **ResultadoVestibular**: Recupera os dados da tabela *Civ..Vestibulando*. O código identificador deve ser o CodProcessoVestibulando
  da tabela *ProcessoVestibulando*

**Reenviar**

Se está o usuário solicitou por um reenvio do token.

```sql
DECLARE @TokenOut CHAR(6), @MensagemRetornoOut VARCHAR(1000);
SET NOCOUNT ON;
EXEC Site_Fiap..spGeraControleAcessoToken
    @SistemaOrigem = :sistemaDeOrigem,
    @CodigoIdentificadorSistemaOrigem = :codigoIdentificador,
    @Reenviar = 0,
    @Token = @TokenOut OUTPUT,
    @MensagemRetorno = @MensagemRetornoOut OUTPUT;
SELECT @MensagemRetornoOut AS mensagem
```

A procedure possui dois retornos: **@TokenOut** (o token gerado) e **@MensagemRetornoOut** mensagem que deve ser exibida para o usuário.

### Validação

Para realizar a chamada da procedure de validação, é necessário informar alguns dados:

**Sistema de origem e codigoIdentificador**

Os mesmos informados na etapa anterior, servem para que a procedure encontre o registro na tabela de tokens.

**Token**

O token informado pelo usuário ao sistema, que será utilizado para confirmar sua identidade.

```sql
DECLARE @ValidadoOut BIT;
SET NOCOUNT ON;
EXEC Site_Fiap..spValidaControleAcessoToken
    @SistemaOrigem = :sistemaOrigem,
    @CodigoIdentificadorSistemaOrigem = :codigoIdentificador,
    @Token = :token,
    @Validado = @ValidadoOut OUTPUT;
SELECT @ValidadoOut AS validado
```

A procedure irá retornar se o token foi validado ou não.

## Consulta

Ao realizar testes locais, é comum necessitar recuperar o token de um usuário para verificar se o fluxo está correto.
Todos os tokens são armazenados na tabela *site_fiap..ControleAcessoToken*.

Abaixo, algumas consultas para facilitar esse processo de consulta:

**InscricaoMBA**
```sql
USE webadm

SELECT
    pos_inscricao_new.codigo,
    ControleAcessoToken.Token,
    ControleAcessoToken.DataHoraValidade,
    ControleAcessoToken.DataHoraValidado
FROM pos_inscricao_new
INNER JOIN site_fiap..ControleAcessoToken AS ControleAcessoToken
    ON pos_inscricao_new.codigo = ControleAcessoToken.CodigoIdentificadorSistemaOrigem
    AND ControleAcessoToken.SistemaOrigem = 'InscricaoMBA'
WHERE pos_inscricao_new.cic = :CPF
```
