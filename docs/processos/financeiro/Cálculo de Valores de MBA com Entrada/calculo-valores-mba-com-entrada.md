# Cálculo de Valores de MBA com Entrada

Quando o aluno opta pela inclusão de um **valor de entrada** ao realizar a 
matrícula, o sistema realiza a **aplicação de algumas regras** por baixo dos 
panos para obter o valor final de cada uma das mensalidades do aluno.

Para realizar este cálculo, primeiramente encontre a **turma do aluno** e seus 
**planos**:

```sql
SELECT
	Codigo,
	CodigoInscricaoProcesso,
	Turma,
	*
FROM
	WebAdm..PI_CursoEscolha WITH (NOLOCK)
WHERE
	CodigoInscricaoProcesso = 196287

SELECT
	nPlano,
	ValorDesconto,
	*
FROM
	WebAdm..pos_inscricao_planos WITH (NOLOCK)
WHERE
	Turma = '4HTCR'
ORDER BY
	pos_inscricao_planos.nPlano
```

Depois, é realizada a aplicação destes cálculos:

```sql
DECLARE @Turma AS VARCHAR(10) = '4HTCR';
DECLARE @PlanoSelecionado AS INT = 24;
DECLARE @PlanoMaximo AS INT = 36;
DECLARE @Entrada AS MONEY = 5000;
DECLARE @Bolsa AS FLOAT = 10;

-- Valores de Desconto (Pontualidade)

DECLARE @ValorDescontoPlanoSelecionado AS MONEY = (SELECT ValorDesconto FROM WebAdm..pos_inscricao_planos WHERE Turma = @Turma AND nPlano = @PlanoSelecionado);
DECLARE @ValorDescontoPlanoMaximo AS MONEY = (SELECT ValorDesconto FROM WebAdm..pos_inscricao_planos WHERE Turma = @Turma AND nPlano = @PlanoMaximo);

DECLARE @ValorTotalDescontoCurso AS MONEY = @ValorDescontoPlanoMaximo * @PlanoMaximo;
PRINT CONCAT('Valor Total do Curso (Pontualidade): ', FORMAT(@ValorTotalDescontoCurso, 'C', 'pt-BR'));

PRINT CONCAT('Entrada: ', FORMAT(@Entrada, 'C', 'pt-BR'));

DECLARE @ValorDescontoPlanoSelecionadoComBolsa AS MONEY = @ValorDescontoPlanoSelecionado * (1 - @Bolsa/100);
DECLARE @QtdeParcelasAbatidasEntradaDesconto AS INT = ROUND(@Entrada / @ValorDescontoPlanoSelecionadoComBolsa, 0);
DECLARE @PlanoRefEntradaDesconto AS INT = @PlanoSelecionado - @QtdeParcelasAbatidasEntradaDesconto;
DECLARE @ValorDescontoPlanoRefEntrada AS MONEY = (SELECT ValorDesconto FROM WebAdm..pos_inscricao_planos WHERE Turma = @Turma AND nPlano = @PlanoRefEntradaDesconto);
DECLARE @ValorDescontoPlanoRefEntradaComBolsa AS MONEY = ROUND(@ValorDescontoPlanoRefEntrada * (1 - @Bolsa/100.0), 2);
DECLARE @ValorTotalDescontoRefEntrada AS MONEY = @ValorDescontoPlanoRefEntradaComBolsa * @PlanoRefEntradaDesconto;
DECLARE @ValorTotalDescontoRefEntradaMenosEntrada AS MONEY = @ValorTotalDescontoRefEntrada - @Entrada;
DECLARE @ValorDescontoParcela AS MONEY = @ValorTotalDescontoRefEntradaMenosEntrada / @PlanoSelecionado;

PRINT CONCAT('Valor das Parcelas Restantes (Pontualidade): ', @PlanoSelecionado, 'X ', FORMAT(@ValorDescontoParcela, 'C', 'pt-BR'));

PRINT '';

-- Valores Cheios

DECLARE @ValorCheioPlanoSelecionado AS MONEY = (SELECT Valor FROM WebAdm..pos_inscricao_planos WHERE Turma = @Turma AND nPlano = @PlanoSelecionado);
DECLARE @ValorCheioPlanoMaximo AS MONEY = (SELECT Valor FROM WebAdm..pos_inscricao_planos WHERE Turma = @Turma AND nPlano = @PlanoMaximo);

DECLARE @ValorTotalCheioCurso AS MONEY = @ValorCheioPlanoMaximo * @PlanoMaximo;
PRINT CONCAT('Valor Total do Curso (Cheio): ', FORMAT(@ValorTotalCheioCurso, 'C', 'pt-BR'));

PRINT CONCAT('Entrada: ', FORMAT(@Entrada, 'C', 'pt-BR'));

DECLARE @ValorCheioPlanoSelecionadoComBolsa AS MONEY = @ValorCheioPlanoSelecionado * (1 - @Bolsa/100);
DECLARE @QtdeParcelasAbatidasEntradaCheio AS INT = ROUND(@Entrada / @ValorCheioPlanoSelecionadoComBolsa, 0);
DECLARE @PlanoRefEntradaCheio AS INT = @PlanoSelecionado - @QtdeParcelasAbatidasEntradaCheio;
DECLARE @ValorCheioPlanoRefEntrada AS MONEY = (SELECT Valor FROM WebAdm..pos_inscricao_planos WHERE Turma = @Turma AND nPlano = @PlanoRefEntradaCheio);
DECLARE @ValorCheioPlanoRefEntradaComBolsa AS MONEY = ROUND(@ValorCheioPlanoRefEntrada * (1 - @Bolsa/100.0), 2);
DECLARE @ValorTotalCheioRefEntrada AS MONEY = @ValorCheioPlanoRefEntradaComBolsa * @PlanoRefEntradaCheio;
DECLARE @ValorTotalCheioRefEntradaMenosEntrada AS MONEY = @ValorTotalCheioRefEntrada - @Entrada;
DECLARE @ValorCheioParcela AS MONEY = @ValorTotalCheioRefEntradaMenosEntrada / @PlanoSelecionado;

PRINT CONCAT('Valor das Parcelas Restantes (Cheio): ', @PlanoSelecionado, 'X ', FORMAT(@ValorCheioParcela, 'C', 'pt-BR'));
```

## Observação

Caso o aluno não selecione um valor de entrada, basta atribuir **zero (0)** à 
variável ao realizar os cálculos.