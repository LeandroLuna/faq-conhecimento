### TipoAcordo

A coluna TipoAcordo é do tipo **char** de tamanho **1** que armazena o tipo do acordo do débito que está na tabela **FNDebitos** representado pela coluna **CodigoNegociacao** ([vide documentação FNDebitos](http://conhecimento.fiap.com.br/tabelas/financeiro/FNDebitos/).)

As letras que representam os tipos de acordo e sua descrição são: 

- F - Financeiro
- J - Jurídico
- E - Extra Judicial
- S - Seguro Desemprego
- G - Negociação Especial
- N - Agente Financiador
- A - Pagamento Agrupado



### Visualizador de Negociações/Acordos - Relação entre os débitos de Origem e Destino



```
DECLARE @RM AS INT = xxxxx;

SELECT
    FNNegociacao.Codigo AS 'CodigoNegociacao',
    --FNNegociacao.Ativo, FNNegociacao.Cancelado,
    Debitos.Identificador,
    Debitos.Codigo AS 'CodigoDebito',
    Debitos.CPFResponsavel,
    Debitos.RM,
    Debitos.Tipo,
    Debitos.DescricaoDebito,
    Debitos.Ano,
    Debitos.Mes,
    --Debitos.Turma,
    Debitos.Bolsa,
    Debitos.ValorDebito,
    Debitos.ValorPago,
    --Debitos.DebitoEmAcordo, Debitos.CodigoNegociacao,
    --Debitos.Con, Debitos.MesAnoEvd, Debitos.DataOutLan,
    '|' AS '|'
FROM
    (
        SELECT
            DISTINCT FNDebitos.CodigoNegociacao AS 'CodigoNegociacao'
        FROM
            BaseEducacional..FNDebitos WITH (NOLOCK)
        WHERE
            FNDebitos.RM = @RM
            AND Visivel = 1
            AND Excluido = 0
            AND CodigoNegociacao IS NOT NULL
        UNION
        SELECT
            FNNegociacao.Codigo AS 'CodigoNegociacao'
        FROM
            BaseEducacional..FNNegociacao WITH (NOLOCK)
        WHERE
            RM = @RM
            AND FNNegociacao.Ativo = 1
            AND FNNegociacao.Cancelado = 0
    ) AS TabCodigoNegociacao
    INNER JOIN BaseEducacional..FNNegociacao WITH (NOLOCK)
        ON TabCodigoNegociacao.CodigoNegociacao = FNNegociacao.Codigo
    INNER JOIN
        (
            SELECT
                FNNegociacaoDebito.CodigoNegociacao AS 'CodigoNegociacaoComparar',
                FNDebitos.Codigo,
                FNDebitos.CPFResponsavel,
                FNDebitos.RM,
                FNDebitos.Tipo,
                FNDebitos.DescricaoDebito,
                FNDebitos.Ano,
                FNDebitos.Mes,
                CONCAT(FNDebitos.Nser, FNDebitos.LCur, FNDebitos.LSer) AS Turma,
                FNDebitos.Bolsa,
                FNDebitos.ValorDebito,
                FNDebitos.ValorPago,
                FNDebitos.DebitoEmAcordo,
                FNDebitos.CodigoNegociacao,
                FNDebitos.Con, 
                FNDebitos.MesAnoEvd, 
                FNDebitos.DataOutLan,
                FNDebitos.Visivel, 
                FNDebitos.Excluido,
                'Origem' AS Identificador
            FROM
                BaseEducacional..FNNegociacaoDebito WITH (NOLOCK)
                INNER JOIN BaseEducacional..FNDebitos WITH (NOLOCK)
                    ON FNNegociacaoDebito.CodigoDebito = FNDebitos.Codigo
            UNION
            SELECT
                FNDebitos.CodigoNegociacao AS 'CodigoNegociacaoComparar',
                FNDebitos.Codigo,
                FNDebitos.CPFResponsavel,
                FNDebitos.RM,
                FNDebitos.Tipo,
                FNDebitos.DescricaoDebito,
                FNDebitos.Ano,
                FNDebitos.Mes,
                CONCAT(FNDebitos.Nser, FNDebitos.LCur, FNDebitos.LSer) AS Turma,
                FNDebitos.Bolsa,
                FNDebitos.ValorDebito,
                FNDebitos.ValorPago,
                FNDebitos.DebitoEmAcordo,
                FNDebitos.CodigoNegociacao,
                FNDebitos.Con, 
                FNDebitos.MesAnoEvd, 
                FNDebitos.DataOutLan,
                FNDebitos.Visivel, 
                FNDebitos.Excluido,
                'Destino' AS Identificador
            FROM
                BaseEducacional..FNDebitos WITH (NOLOCK)
        ) AS Debitos
        ON FNNegociacao.Codigo = Debitos.CodigoNegociacaoComparar
        AND Debitos.Visivel = 1
        AND Debitos.Excluido = 0
ORDER BY
    TabCodigoNegociacao.CodigoNegociacao,
    Debitos.Identificador DESC,
    Debitos.RM,
    Debitos.Tipo,
    Debitos.Ano,
    Debitos.Mes
```
