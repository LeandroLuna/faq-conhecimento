# Créditos

Para inserir créditos para os alunos, basta criar um registro na tabela **ExtratoCredito** com as informações necessárias, conforme exemplo:

```sql
INSERT INTO ExtratoCredito (Usuario, DataHoraCadastro, Valor, Motivo, CodigoUsuarioCadastro, CodigoPedido)
VALUES ('rmXXXXX', GETDATE(), 5, 'Bem-vindo ao app Kitchenet', 1, NULL);
```

## Cálculo do saldo

O cálculo do saldo é feito realizando a soma de todos os valores da tabela **ExtratoCredito** filtrando pelo usuário

```sql
SELECT SUM(Valor) FROM ExtratoCredito WHERE Usuario='rmXXXXX'
```
