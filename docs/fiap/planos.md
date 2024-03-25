# Planos

### Alterar plano do aluno que irá iniciar no próximo ano

Primeiramente, temos que verificar que o aluno em questão não tenha debitos pendentes. 
Não tendo, temos que deleter os registros de **Mensalidade** do RM em questão

```sql
DELETE BaseEducacional..FNDebitos WHERE RM = @Rm AND Tipo = 'Mensalidade' AND ano = @Ano AND Visivel = 1 AND Excluido = 0
```

Depois precisamos atualizar o campo **Plano** e o **CodigoTabelaValor** para o correto e deixar o campo ValorPago e DataPagamento como *null*

```sql
UPDATE BaseEducacional..FNDebitos SET ValorPago = null, DataPagamento = null, Plano = @Plano, CodigoTabelaValor = @CodigoTabelaValor where Codigo = @CodigoReferenteaMatricula
```
E para finalizar voltamos o campo ValorPago e DataPagamento para o que estava, com isso através da trigger ele gera as mensalidades de acordo com o novo plano.

```sql
UPDATE BaseEducacional..FNDebitos SET ValorPago = 690.00, DataPagamento = '2018-09-26' where Codigo = 3631175
```