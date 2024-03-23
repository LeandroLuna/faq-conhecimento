# Tipos de Débitos

## 1 - Mensalidades

* No banco Educacional, tem todas as tabelas dos alunos graduação e colégio.
* Na view vRelacao tem todas as turmas da graduação e colégio desde 2009.
* Se colocar por exemplo where ano = 2019, tem todas as turmas de 2019.
* Se colocar CodigoUnidade = 1 terá todas as turmas que foram parametrizadas no sistema para a graduação

### 1.2 - Graduação

```sql
USE EDUCACIONAL;
SELECT
    *
FROM
    vRelacao
WHERE
    Ano = 2019 AND CodigoUnidade = 1 AND Turma = @TURMA
```

Com isso conseguirá o **código** da relação. Utilize na view vRelacaoUnidadeServicoPlano, para retornar códigos da UnidadeServicoPlano e posteriormente conseguir os planos.

```sql
USE EDUCACIONAL;
SELECT
    CodigoUnidadeServicoPlano
FROM
    vRelacaoUnidadeServicoPlano
WHERE
    CodigoRelacao = @codigoRelacao
```

Para obter os planos **(parcelas, valor anuidade etc)**, utilizar o select:

```sql
SELECT
    *
FROM
    vUnidadeServicoPlano
WHERE
    Codigo IN (@SELECT ANTERIOR)
```

Nesse mesmo select é possível obter o **CodigoTabelaValor** utilizando:

```sql
SELECT
    *
FROM
    BaseEducacional..FNTabelaValor
WHERE
    CODIGO = @CodigoTabelaValor
```

E para finalizar, as mensalidades padrões do plano:

```sql
SELECT
    *
FROM
    BaseEducacional..FNTabelaValorVencimento
WHERE
    CodigoTabelaValor = @CodigoTabelaAnterior
```