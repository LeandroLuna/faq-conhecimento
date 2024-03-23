# Backup de alterações (UPDATE's) via tabela de backup

## Gerando uma tabela de backup com base na tabela original

Muitas vezes, ao realizar **alterações no banco de dados**, criamos uma 
**tabela de backup** logo antes de executarmos a alteração, para o caso de 
precisarmos revertê-la.

### Script de exemplo

```sql
-- Neste comando estamos criando uma tabela de backup 
-- 'BaseEducacional_FNDebitosBAK20220815' na base 'Desativados' e preenchendo-a 
-- com os dados da tabela 'FNDebitos' que encontra-se na base 'BaseEducacional'.
SELECT 
	* 
INTO 
	Desativados..BaseEducacional_FNDebitosBAK20220815 
FROM 
	BaseEducacional..FNDebitos;
```

## Revertendo alteração (UPDATE) com base na tabela de backup

Para **reverter a alteração**, basta atualizar novamente os **campos alterados** 
para os **valores salvos** na tabela de backup.

### Script de exemplo

```sql
-- Neste comando é realizado o 'ROLLBACK' das colunas alteradas erroneamente, 
-- reatribuindo os valores corretos previamente salvos na tabela de backup.
UPDATE
    BaseEducacional..FNDebitos
SET
    FNDebitos.ValorPago = FNDebitosBackup.ValorPago,
    FNDebitos.DataPagamento = FNDebitosBackup.DataPagamento
FROM
    (
		SELECT 
			Codigo, 
			ValorPago, 
			DataPagamento
		FROM 
			Desativados..BaseEducacional_FNDebitosBAK20220815
	) AS FNDebitosBackup
WHERE
    FNDebitos.Codigo = FNDebitosBackup.Codigo
```