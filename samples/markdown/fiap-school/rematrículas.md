# Rematrículas

## Cancelar Rematrícula

Selecione a rematrícula e os debitos do ano referente a rematrícula e atualize a coluna **Con** e **DataOutLan** .

```sql hl_lines="12"
SELECT * FROM BaseEducacional..FNDebitos WHERE RM = @Rm AND Ano = @Ano

UPDATE BaseEducacional..FNDebitos SET Con = 'D', DataOutLan = GETDATE() WHERE RM = @Rm AND Ano = @Ano
```
Após realizado o update, desative o aluno na futura turma

```sql hl_lines="12"
-- Descobre o código do aluno
SELECT * FROM Educacional..Aluno WHERE RM = @Rm 
-- Descobre as turmas do aluno
SELECT * FROM Educacional..AlunoTurma WHERE CodigoAluno = @CodigoAluno 
-- Verificar qual turma refere-se a turma que será cancelada
SELECT * FROM Educacional..Relacao WHERE Codigo IN (@CodigoRelacao) 


-- Setar CodigoTipoStatus = 2 que significa desistente
UPDATE Educacional..AlunoTurma SET CodigoTipoStatus = 2 WHERE Codigo = @Codigo
```