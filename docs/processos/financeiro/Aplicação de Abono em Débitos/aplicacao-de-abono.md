# Aplicação de Abono em Débitos

<div style="height: 200px; overflow-x:scroll;">
    <img src="../aplicacao-de-abono.svg" style="max-width: initial;">
</div>

## Abonar Débitos

Para **abonar um débito** é necessário utilizar o sistema **Abonar Débitos**, 
que pode ser encontrado na unidade **Help Center** 
da [Intranet Nova](https://intranet.fiap.com.br/) e 
no [Repositório do GitLab](https://gitlab.fiap.com.br/dotnet/Intranet.Negociacao) 
(**AbonoController**).

Para abonar um débito a partir deste sistema, basta **selecionar o débito** 
desejado, informar o **motivo do abono**, selecionar os **documentos comprobatórios** 
(caso necessário) e efetivar o abono.

Quando um débito é abonado as seguintes colunas da **FNDebitos** são preenchidas:

- **Abonado** = 1 (Campo BIT - 0 ou 1);
- **CodigoUsuarioAbono** = (Código do usuário que efetuou o abono);
- **DataHoraAbono** = (Momento que o débito foi abonado);
- **MotivoAbono** = (Motivo preenchido via sistema no ato do abono);

Caso seja **anexado** um ou mais **documentos**, os arquivos são salvos na 
**FNArquivoAbonoDebito**, vinculados ao débito.

O sistema também cadastra um registro na tabela **HistoricoPessoa**, informando 
que o abono foi realizado.

## Abonando um débito via script

```sql
-- Buscando o débito que será abonado:
SELECT
  Codigo,
  RM,
  CPFResponsavel,
  Tipo,
  Ano,
  Mes,
  *
FROM
  BaseEducacional..FNDebitos
WHERE
  MesAnoEvd IS NULL
  AND DataOutLan IS NULL
  AND Visivel = 1
  AND Excluido = 0
  AND Abonado = 0
  AND Con = 'A'
  AND DebitoEmAcordo = 0
  AND ValorDebito > 0
  AND ValorPago IS NULL
  AND RM = @RM;

-- Aplicando abono no débito:
UPDATE
  BaseEducacional..FNDebitos
SET
  Abonado = 1,
  CodigoUsuarioAbono = @CodigoUsuario,
  DataHoraAbono = GETDATE(),
  MotivoAbono = @MotivoAbono
WHERE
  Codigo = @CodigoDebito;

-- Executar a procedure que atualiza o débito como um todo:
EXEC BaseEducacional..spAtualizaDebito @Codigo = @CodigoDebito;

-- Inserindo informação de abono no histórico do aluno:
INSERT INTO BaseEducacional..HistoricoPessoa
  (CPFCNPJ, 
  RM, 
  Cabecalho, 
  Observacao, 
  Origem, 
  CodigoUsuarioCadastro, 
  DataHoraCadastro, 
  Ativo)
VALUES
  (@CPFResponsavel, 
  @RM, 
  '', 
  @MotivoAbono, 
  'Abono', 
  @CodigoUsuario, 
  GETDATE(), 
  1);
```

## Ficha Financeira

Na **Ficha Financeira** do aluno 
([Projeto Intranet.Negociacao](https://gitlab.fiap.com.br/dotnet/Intranet.Negociacao), 
**ListagemDebitosController**) podemos visualizar o **débito recém-abonado** na 
aba de **Pagos**, e a informação de abono no **Histórico**.

Como débitos **abonados** não são cobrados, eles ficarão na aba de **Pagos**.

### Observações:
```
Todas as tabelas citadas são do banco "BaseEducacional".
```