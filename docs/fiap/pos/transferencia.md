# Tranferência

## Troca de turma da pós

O processo ideal de troca de turma da pós envolve o cancelamento do RM atual
e a criação de um novo RM (Nova matrícula).

Na época da pandemia, foi criada uma exceção para evitar a ida presencial, então
alunos matrículados em um curso poderiam trocar de turma sem a necessidade de 
criar um novo RM.

O script para esses casos especiais é:

**OBS:** Não esquecer de alterar as variáveis necessárias para parametrizar o script!

```sql
DECLARE @RM INT, @TurmaDestino VARCHAR(10), @Plano INT, @CodigoFNTabelaValor INT, @CodigoFNDebitos INT, @ValorPago MONEY, @DataPagamento DATE, @Abonado BIT, @NSer INT, @LCur VARCHAR(5)

SET @RM = 123456
SET @TurmaDestino = '9BIO'
SET @NSer = 9
SET @LCur = 'BIO'
/*
DELETE CBDebitosAtrasados WHERE CodigoFNDebitos IN (SELECT Codigo FROM FNDebitos WHERE RM = 346838)
DELETE CBListaResultadoDebito WHERE CodigoFNDebito IN (SELECT Codigo FROM FNDebitos WHERE RM = 346838)
*/

IF EXISTS(SELECT 
				* 
			FROM 
				WebAdm..Pos_Inscricao_Contrato WITH (NOLOCK) 
			WHERE 
				RM = @RM)
BEGIN
	IF EXISTS(SELECT
					* 
				FROM 
					BaseEducacional..FNDebitos WITH (NOLOCK) 
				WHERE 
					RM = @RM 
					AND Visivel = 1 
					AND Excluido = 0 
					AND Tipo = 'Matrícula - Pós')
	BEGIN

		SELECT 
			@Plano = Plano 
		FROM 
			webadm..pos_inscricao_contrato WITH (NOLOCK)
		WHERE 
			RM = @RM

		SELECT 
			@CodigoFNTabelaValor = CodigoTabelaValor 
		FROM 
			WebAdm..Pos_Inscricao_Planos WITH (NOLOCK) 
		WHERE 
			Turma = @TurmaDestino 
			AND nPlano=@Plano

		SELECT 
			@CodigoFNDebitos = Codigo, 
			@ValorPago = ValorPago, 
			@DataPagamento = DataPagamento, 
			@Abonado = Abonado 
		FROM 
			BaseEducacional..FNDebitos WITH (NOLOCK)
		WHERE 
			RM = @RM 
			AND Visivel = 1 
			AND Excluido = 0 
			AND Tipo = 'Matrícula - Pós'

		UPDATE 
			webadm..pos_inscricao_contrato WITH (ROWLOCK)
		SET 
			Turma = @TurmaDestino 
		WHERE 
			RM = @RM

		UPDATE 
			BaseEducacional..FNDebitos WITH (ROWLOCK)
		SET 
			Visivel = 0, 
			Excluido = 1 
		WHERE 
			RM = @RM 
			AND Tipo = 'Mensalidade'

		UPDATE 
			BaseEducacional..FNBolsa WITH (ROWLOCK)
		SET 
			Ativo = 0 
		WHERE 
			RM = @RM

		UPDATE 
			BaseEducacional..FNDebitos WITH (ROWLOCK)
		SET 
			NSer = @NSer, 
			LCur = @LCur, 
			CodigoTabelaValor = @CodigoFNTabelaValor, 
			ValorPago = NULL, 
			DataPagamento = NULL, 
			Abonado = 0 
		WHERE 
			Codigo = @CodigoFNDebitos

		UPDATE 
			BaseEducacional..FNDebitos WITH (ROWLOCK)
		SET 
			ValorPago = @ValorPago, 
			DataPagamento = @DataPagamento, 
			Abonado = @Abonado
		WHERE 
			Codigo = @CodigoFNDebitos

	END
	ELSE
	BEGIN
		PRINT 'Não foi encontrado o débito de matrícula para o RM informado'
	END
END
ELSE
BEGIN
	PRINT 'RM informado não consta na tabela de pos_inscricao_contrato'
END
```