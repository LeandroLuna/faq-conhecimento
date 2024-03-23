# Aplicação de Bolsas em Débitos

<div style="height: 500px; overflow-x:scroll;">
    <img src="../aplicacao-de-bolsa.svg" style="max-width: initial;">
</div>

## Manutenção de Bolsa

As **bolsas** de um aluno são aplicadas a partir do sistema 
"**Manutenção de Bolsa**", que pode ser encontrado na unidade **Help Center** 
da [Intranet Nova](https://intranet.fiap.com.br/) e 
no [Repositório do GitLab](https://gitlab.fiap.com.br/dotnet/Intranet.Bolsa).

Ao iniciar a aplicação de uma bolsa neste sistema, é exibida uma **simulação** 
informando quais **débitos** serão **afetados** e qual será o **valor final** 
a ser cobrado em cada um deles.

Ao **confirmar** a aplicação de uma bolsa o usuário deve informar **quem autorizou** 
este cadastro e para alguns tipos de bolsa também devem ser preenchidos:

- **Justificativa**;
- **Nome da empresa parceira**;
- **Arquivo comprobatório**;

## Tipos de Bolsa

Diversos **tipos de bolsa** podem ser aplicados, e cada um deles tem uma **regra** 
a ser seguida. Na tabela **FNTipoBolsa** são descritas as regras da maior parte 
das bolsas.

As bolsas podem ser categorizadas em relação ao **período de aplicação**:

- **Anual**;
- **Semestral**;
- **Todas as mensalidades**;
- **Livre**, permitindo que o usuário selecione exatamente o período desejado;

As colunas **CalculaPrimeiro** e **CalculoPrioridade** da **FNTipoBolsa** 
(colunas utilizadas com o mesmo propósito) separam os tipos de bolsa em **2 grupos**:

- **Bolsas prioritárias**, que devem ser **aplicadas primeiro**;
- **Demais bolsas**;

Caso o aluno possua **apenas bolsas de um mesmo grupo** aplicadas a determinado 
débito, as bolsas são **somadas** e a porcentagem resultante é aplicada ao débito, 
conforme **Exemplo 1**.

### Exemplo 1:
```
Bolsas do aluno:
- 10% de "Convênio" (Grupo: Demais bolsas);
- 20% de "Ex-aluno" (Grupo: Demais bolsas);

10% + 20% = 30%
Será aplicada uma porcentagem de 30% na coluna "Bolsa" dos débitos do aluno.
```

Se o aluno possui **uma ou mais bolsas de cada um dos grupos**, as bolsas de um 
**mesmo grupo** são **somadas** entre si e aplicadas ao débito de forma 
**escalonada** (uma por vez), conforme **Exemplo 2**.

### Exemplo 2:
```
Bolsas do aluno:
- 10% de "DP" (Grupo: Bolsas prioritárias);
- 30% de "Fim de Período" (Grupo: Demais bolsas);
- 20% de "Dificuldade Financeira" (Grupo: Demais bolsas);

// Valor de referência (não influencia no cálculo da porcentagem resultante):
valorSemBolsa = R$ 1.000,00

// Somando bolsas do grupo "Demais bolsas":
demaisBolsas = 30% + 20% 
demaisBolsas = 50%

// Aplicando bolsa de 10% de "DP" (Grupo: Bolsas prioritárias):
valorComDP = valorSemBolsa * (1 - bolsaDP/100)
valorComDP = 1000 * (1 - 10/100)
valorComDP = R$ 900,00

// Aplicando "Demais Bolsas" (50%):
valorFinal = valorComDP * (1 - demaisBolsas/100)
valorFinal = 900 * (1 - 50/100)
valorFinal = R$ 450,00

// Calculando porcentagem resultante das bolsas:
porcentagemResultante = (valorSemBolsa - valorFinal) / valorSemBolsa
porcentagemResultante = (1000 - 450) / 1000
porcentagemResultante = 0,55 = 55%

// Prova real (confirmando que a porcentagem resultante está correta):
valorFinal = valorSemBolsa * (1 - porcentagemResultante/100)
450 = 1000 * (1 - 55/100)
450 = 450

Será aplicada uma porcentagem de 55% na coluna "Bolsa" dos débitos do aluno.
```

A tabela **FNTipoBolsa** possui também algumas **flags** (campos BIT - 0 ou 1) 
que definem se, ao cadastrar uma bolsa, é necessário preencher:

- **Justificativa**;
- **Empresa parceira**;
- **Documento comprobatório**;

## Porcentagens dos Tipos de Bolsa

**Alguns tipos de bolsa** só podem receber determinadas porcentagens. 
As **porcentagens permitidas** para cada tipo de bolsa podem ser encontradas na 
tabela **FNTipoBolsaPorcentagem**, a partir do código do tipo de bolsa.

Caso não exista nenhum registro na tabela **FNTipoBolsaPorcentagem** vinculada à 
determinada **FNTipoBolsa**, significa que este tipo de bolsa pode receber 
qualquer porcentagem entre 0,01 e 100.

## Bolsa Aplicada

A tabela **FNBolsaAplicada** foi implementada para agilizar a busca das 
**bolsas vinculadas** a determinado débito.

## Aplicando uma bolsa via script:

```sql
-- Buscando os débitos que receberão a bolsa:
SELECT
  Codigo,
  Ano, 
  Mes, 
  Tipo,
  Bolsa,
  ValorCheioNominal
  ValorDescontoNominal,
  ValorCheioDebito
  ValorDescontoDebito,
  ValorDebito,
  ValorPago,
  ValorAcrescimo,
  ValorDeducao,
  Abonado,
  * 
FROM
  BaseEducacional..FNDebitos
WHERE
  Con = 'A'
  AND Visivel = 1
  AND Excluido = 0
  AND MesAnoEvd IS NULL
  AND DataOutLan IS NULL
  AND Externa IS NULL
  AND Tipo IN 
  (
    'Mensalidade', 
    'Agente Financiador', 
    'Repasse Fies', 
    'Mensalidade DP'
  )
  AND ISNULL(LSer, '') != 'P'
  AND ValorCheioNominal != 0
  AND Bolsa != 100
  AND RM = @RM
ORDER BY
  FNDebitos.Tipo,
  FNDebitos.Ano,
  FNDebitos.Mes;

-- Buscando bolsas que o aluno possui atualmente:
SELECT 
  FNTipoBolsa.Descricao,
  FNBolsa.* 
FROM 
  BaseEducacional..FNBolsa
  INNER JOIN BaseEducacional..FNTipoBolsa
    ON FNBolsa.CodigoTipoBolsa = FNTipoBolsa.Codigo
WHERE
  FNBolsa.RM = @RM
  AND FNBolsa.Ativo = 1
ORDER BY
  FNBolsa.DataHoraCadastro;

-- Buscando os tipos de bolsas que podem ser aplicados:
SELECT
  *
FROM
  BaseEducacional..FNTipoBolsa
WHERE
  Ativo = 1

-- Cadastrando uma bolsa para o aluno:
INSERT INTO BaseEducacional..FNBolsa
  (CodigoTipoBolsa,
  RM,
  Porcentagem,
  Justificativa,
  Semestre,
  Ano,
  MesInicio,
  AnoInicio,
  MesTermino,
  AnoTermino,
  CodigoUsuarioCadastro,
  DataHoraCadastro,
  Ativo,
  CodigoPessoaAutorizou,
  NomeEmpresaParceira,
  Arquivo)
VALUES
  (@CodigoTipoBolsa,
  @RM,
  @Porcentagem,
  @Justificativa,
  @Semestre,
  @Ano,
  @MesInicio,
  @AnoInicio,
  @MesTermino,
  @AnoTermino,
  @CodigoUsuarioCadastro,
  @DataHoraCadastro,
  @Ativo,
  @CodigoPessoaAutorizou,
  @NomeEmpresaParceira,
  @Arquivo);
SELECT @CodigoBolsa = @@IDENTITY;
-- OBS: Este código é necessário para podermos relacionar a bolsa aos débitos

-- Vinculando a nova bolsa aos débitos desejados (via FNBolsaDebitos):
INSERT INTO BaseEducacional..FNBolsaDebitos
  (CodigoBolsa, CodigoDebito)
VALUES
  (@CodigoBolsa, @CodigoDebito1),
  (@CodigoBolsa, @CodigoDebito2),
  (@CodigoBolsa, @CodigoDebito3);

-- Vinculando o tipo da nova bolsa aos débitos desejados (via FNBolsaAplicada):
INSERT INTO BaseEducacional..FNBolsaAplicada
  (CodigoTipoBolsa, CodigoDebito, Porcentagem)
VALUES
  (@CodigoTipoBolsa, @CodigoDebito1, @Porcentagem),
  (@CodigoTipoBolsa, @CodigoDebito2, @Porcentagem),
  (@CodigoTipoBolsa, @CodigoDebito3, @Porcentagem);

-- Alterando a porcentagem de bolsa resultante nos débitos:
UPDATE
  BaseEducacional..FNDebitos
SET
  Bolsa = @BolsaResultante, /* De acordo com as regras de aplicação de bolsa */
  ValorCheioDebito = 
    ValorCheioNominal * (1 - @BolsaResultante/100.0) 
    - ISNULL(ValorDeducao, 0)
    + ISNULL(ValorAcrescimo, 0),
  ValorDescontoDebito = 
    ValorDescontoNominal * (1 - @BolsaResultante/100.0) 
    - ISNULL(ValorDeducao, 0)
    + ISNULL(ValorAcrescimo, 0),
  ValorDebito = 
    ValorDescontoNominal * (1 - @BolsaResultante/100.0) 
    - ISNULL(ValorDeducao, 0)
    + ISNULL(ValorAcrescimo, 0)
WHERE
  Codigo IN 
  (
    @CodigoDebito1,
    @CodigoDebito2,
    @CodigoDebito3
  );

-- Executar a procedure que atualiza o débito como um todo:
EXEC BaseEducacional..spAtualizaDebito @Codigo = @CodigoDebito1;
EXEC BaseEducacional..spAtualizaDebito @Codigo = @CodigoDebito2;
EXEC BaseEducacional..spAtualizaDebito @Codigo = @CodigoDebito3;
```

## Ficha Financeira

Na **Ficha Financeira** do aluno 
([Projeto Intranet.Negociacao](https://gitlab.fiap.com.br/dotnet/Intranet.Negociacao), 
**ListagemDebitosController**) podemos visualizar a **porcentagem resultante** 
aplicada a cada um dos débitos do aluno, além de ser possível identificar as 
**bolsas que compõem** este valor.

Caso o débito possua **100% de bolsa**, ele não será cobrado, então este débito 
ficará na aba de **Pagos**.

### Observações:
```
Todas as tabelas citadas são do banco "BaseEducacional".
As informações das colunas "Bolsa" e "Porcentagem" são inseridas na escala de 0 a 100.
```
