# Alteração das Datas de um Débito

<div style="height: 300px; overflow-x:scroll;">
    <img src="../alteracao-das-datas-de-um-debito.svg" style="max-width: initial;">
</div>

## Alterar Vencimento

Para **alterar a data de vencimento de um débito** é necessário utilizar o 
sistema **Alterar Vencimento**, que pode ser encontrado na unidade 
**Help Center** da [Intranet Nova](https://intranet.fiap.com.br/) e 
no [Repositório do GitLab](https://gitlab.fiap.com.br/dotnet/Intranet.Negociacao) 
(**AlteraDataVencimentoController**).

No sistema, **selecione o débito** que deverá ter sua data alterada, defina a 
**nova data**, informe o **motivo** da alteração e selecione a forma mais 
adequada de **recalcular o novo valor** do débito:

- (**Opção 1**) **Manter valor atual** do débito até nova data de vencimento;
- (**Opção 2**) **Recalcular multa + juros** até nova data de vencimento;
- (**Opção 3**) **Utilizar o valor cheio** até nova data de vencimento;
- (**Opção 4**) **Utilizar o valor de pontualidade** até nova data de vencimento;

Defina também **quais datas** do débito serão alteradas:

- **Apenas** a data de **vencimento**;
- **Ambas** as datas (vencimento e pontualidade);

Ao efetivar a alteração, todas as informações preenchidas serão salvas no débito:

- **DataVencimentoPadrao**: não muda, para que o sistema saiba a 
**data de vencimento original** do débito;
- **DataDescontoPadrao**: não muda, para que o sistema saiba a 
**data de pontualidade original** do débito;
- **DataVencimentoDebito**: **nova data**;
- **DataDescontoDebito**: caso o usuário tenha marcado para alterar 
**ambas as datas**, armazena a **nova data**;
- **DataVencimento**: **nova data**;
- **CodigoUsuarioAlteracaoDataVencimento**: **usuário** que alterou a data do 
débito;
- **DataHoraAlteracaoDataVencimento**: momento (**Data e Hora**) que a data do 
débito foi alterada;
- **DataNovoVencimento**: **nova data**;
- **MotivoAlteracaoDataVencimento**: **motivo** preenchido no ato da alteração;
- **OpcaoSelecionadaAlteraDataVencimento**: armazena a **opção** selecionada 
(**de 1 a 4**);
- **ValorDebito**: **valor** a ser cobrado até a nova data, conforme a 
**opção selecionada**;

Além de alterar todos estes campos do débito, o sistema também cadastra um 
registro na tabela **HistoricoPessoa** e outro na **FNLogDebito**, informando a 
alteração de data que foi realizada.

**Diariamente**, o sistema executa um **Job SQL** responsável por retornar o 
débito para as **datas originais**, caso a **nova data** tenha sido **excedida** 
e o débito ainda **não** tenha sido **pago**. Neste caso, 
**todos os campos do débito** que foram preenchidos no ato da alteração de data 
**retornam para o valor original** e é inserido um novo registro na tabela 
**FNLogDebito** com esta informação.

## Alterando as datas de um débito via script:

```sql
-- Buscando o débito que terá sua data alterada:
SELECT
  Codigo,
  RM,
  CPFResponsavel,
  Tipo,
  Ano,
  Mes,
  ValorCheioNominal,
  Bolsa,
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
  AND RM = @RM
  /* Os tipos permitidos estão descritos na variável 'TiposDebitosDataVencimento' */
  /* do Web.config (Intranet.Negociacao) */
  AND Tipo IN @TiposDebitosDataVencimento;

DECLARE @NovaData AS DATE;            -- Nova data no formato 'yyyyMMdd'
DECLARE @OpcaoSelecionada AS INT;     -- De 1 a 4
DECLARE @AlterarAmbasDatas AS BIT;    -- 0 ou 1
DECLARE @Motivo AS TEXT;              -- Motivo da alteração de data

DECLARE @ValorCheioNominalComBolsa AS MONEY = @ValorCheioNominal * (1 - @Bolsa/100.0);

DECLARE @QtDiasAtrasado AS INT = DATEDIFF(DAY, @DataVencimento, @NovaData);

DECLARE @TaxaJuros AS MONEY = ISNULL(TaxaJuros, 0.00033);
DECLARE @TaxaMulta AS MONEY = ISNULL(TaxaMulta, 0.02);

DECLARE @ValorJuros AS MONEY = @ValorCheioNominalComBolsa * @TaxaJuros * @QtDiasAtrasado;
DECLARE @ValorMulta AS MONEY = @ValorCheioNominalComBolsa * @TaxaMulta;

DECLARE @ValorDebitoComMultaJuros AS MONEY = 
  @ValorCheioNominalComBolsa + @ValorJuros + @ValorMulta 
  + ISNULL(@ValorAcrescimo, 0) 
  - ISNULL(@ValorDeducao, 0);

-- Alterando a data do débito
UPDATE
  BaseEducacional..FNDebitos
SET
  DataVencimentoDebito = @NovaData,
  DataDescontoDebito = 
    CASE WHEN 
      @AlterarAmbasDatas = 1 
    THEN 
      @NovaData 
    ELSE 
      DataDescontoDebito 
    END,
  DataVencimento = @NovaData,
  CodigoUsuarioAlteracaoDataVencimento = 1,
  DataHoraAlteracaoDataVencimento = GETDATE(),
  DataNovoVencimento = @NovaData,
  MotivoAlteracaoDataVencimento = @Motivo,
  OpcaoSelecionadaAlteraDataVencimento = @OpcaoSelecionada,
  ValorDebito = 
    CASE @OpcaoSelecionada
      WHEN 1 /* Manter valor atual                */ THEN ValorDebito
      WHEN 2 /* Recalcular multa + juros          */ THEN @ValorDebitoComMultaJuros
      WHEN 3 /* Utilizar o valor cheio            */ THEN ValorCheioDebito
      WHEN 4 /* Utilizar o valor de pontualidade  */ THEN ValorDescontoDebito
      ELSE ValorDebito 
    END
WHERE
  Codigo = @CodigoDebito;

-- Executar a procedure que atualiza o débito como um todo:
EXEC BaseEducacional..spAtualizaDebito @Codigo = @CodigoDebito;

-- Inserindo informação de alteração de data no histórico do aluno:
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
  'Data alterada', 
  @MotivoAlteracaoValor, 
  'Alteração de data', 
  @CodigoUsuario, 
  GETDATE(), 
  1);
```

## Ficha Financeira

Na **Ficha Financeira** do aluno 
([Projeto Intranet.Negociacao](https://gitlab.fiap.com.br/dotnet/Intranet.Negociacao), 
**ListagemDebitosController**), após a alteração da data, o débito aparecerá na 
aba de **A vencer**, e as **informações de alteração de data** ficam disponíveis 
no **informativo** detalhado do **débito** em questão, além do **Histórico**.

### Observação:
```
Todas as tabelas citadas são do banco "BaseEducacional".
```