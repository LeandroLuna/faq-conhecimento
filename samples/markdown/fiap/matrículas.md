# Matrículas

## Graduação

### Alterar o status de ex-aluno de uma matrícula da Graduação

Para colocar ou remover o desconto de ex-aluno numa matrícula da graduação quando já foi finalizado, deve-se alterar o bit `ExAluno` da tabela **CPTVest** no banco **Educacional**

```sql
UPDATE Educacional..CPTVest SET ExAluno=1 WHERE RM=xxxx
```

!!! warning "Atenção"
    O desconto do _boleto da matrícula_ só entra na **Intranet3**, a ficha financeira não apresenta o desconto, caso o responsável queira pagar no ato com desconto, deve-se fazer o **recebimento e aplicar o desconto de 20%** sobre o valor do boleto.

### Impedimento de rematrícula

Para certos alunos, ao decorrer do ano, é conferido o status de impedimento de rematrícula por débitos inadimplentes, nome no SERASA, etc, a critério da equipe do financeiro.

Para remover o status de impedimento de rematrícula, é necessário acessar o sistema **Liberação de Impedimento de Rematrícula** e realizar a liberação.

O débito de rematrícula deve aparecer na ficha financeira automaticamente devido a ação da trigger _trAlunoImpedimentoRematricula_, caso não apareça, deve-se atualizar o bit Visivel para 1 do débito de rematrícula na tabela **FNDebitos** do banco **BaseEducacional**

```sql
UPDATE BaseEducacional..FNDebitos SET Visivel=1 WHERE RM=xxxx AND Visivel = 0 AND Mes = 1 AND Tipo='Rematrícula'
```

### Re-abertura de matrícula

Caso ao re-abrir uma matrícula o débito não apareca na ficha financeira, pode ser que o campo CPFResponsavel do débito esteja incorreto, para corrigir, basta puxar o CPF correto e atualizar o debito.

```sql
UPDATE BaseEducacional..FNDebitos SET CPFResponsavel='xxxxxxxxxxx' WHERE RM=yyyyy AND Tipo='Rematrícula'
```

### Cláusula do Pro-uni

Para colocar a cláusula do Prouni em um aluno que não tenha, e assim exibir no contrato, deve-se atualizar a tabela CPTVest conforme script:

```sql
-----------------------------------------
--Coloca ProUni em um aluno que não tem--
-----------------------------------------
USE Educacional
GO
DECLARE @RM INT, @Porcentagem INT, @CPF VARCHAR(10), @CodCadastro INT
SET @RM = yyyyy  --Colocar o RM
SET @Porcentagem = xx --Informar a porcentagem 50% ou 100%
SELECT @CPF = CPF FROM Educacional..CptVest WHERE RM = @RM
IF @CPF IS NOT NULL
BEGIN
	SELECT @CodCadastro = Codigo FROM ProUni..Cadastro WHERE CPF = @CPF
	SET @CodCadastro = ISNULL(@CodCadastro, -1)
	UPDATE CptVest SET NumeroProcesso = 10, PorcentagemDesconto=@Porcentagem, promocao='ProUni', CodProUni = @CodCadastro WHERE RM = @RM
END
ELSE
BEGIN
	PRINT 'RM informado não existe na tabela Educacional..CptVest!'
END
```

### Alterar turma/curso manualmente

Para alterar a turma e gerar um novo contrato é preciso atualizar todo o processo do vestibular do candidato.

```sql hl_lines="1 3 23 36"
DECLARE @RM INT = 82435
DECLARE @CodigoAluno INT
DECLARE @TurmaDestino VARCHAR(10) = '1TMKF'
DECLARE @CodigoCursoDestino INT
DECLARE @CodigoRelacaoDestino INT


-- Descobrir o codigo do aluno
SELECT
	@CodigoAluno = Codigo
FROM
	Educacional..vAluno
WHERE
	RM = @RM

-- Descobrir o codigo do curso e relacao destino
SELECT
	@CodigoCursoDestino = CodigoCurso,
	@CodigoRelacaoDestino = Codigo
FROM
	Educacional..vRelacao AS vRelacao
WHERE
	vRelacao.Ano = 2019 AND
	vRelacao.Turma = @TurmaDestino

-- Descobrir o codigo do plano futuro
DECLARE @CodigoPlanoDestino INT = (SELECT
									Codigo
								FROM
									Educacional..vUnidadeServicoPlano
								WHERE
									Codigo IN (SELECT
													CodigoUnidadeServicoPlano
												FROM
													Educacional..vRelacaoUnidadeServicoPlano
												WHERE CodigoRelacao = @CodigoRelacaoDestino) AND NumeroParcelas = 13) -- Setar o plano desejado
-- Atualizar os campos necessarios
UPDATE CPTVEST SET CodigoUnidadeCursoAprovSelecionado=@CodigoCursoDestino, CodigoPlano=@CodigoPlanoDestino WHERE RM = @RM
UPDATE MatriculaRematricula SET TurmaMatriculado=@TurmaDestino, CodigoRelacaoMatriculado=@CodigoRelacaoDestino, CodigoPlano=@CodigoPlanoDestino, CodigoCursoMatricula=@CodigoCursoDestino WHERE CodigoAluno = @CodigoAluno
UPDATE AlunoTurma SET CodigoRelacao=@CodigoRelacaoDestino WHERE CodigoAluno = @CodigoAluno
GO
```

!!! warning "Atenção"
	É necessário apagar o contrato antigo para que o mesmo seja gerado novamente em ```/updown/Contratos/MatriculaVestibular/XXXXX/ContratoMatricula``` sendo XXXXX o RM do aluno
	
	
### Total de matrículas (pagas) por turma de um determinado ano


```sql
USE Educacional;

SELECT 
    vRelacao.Turma,
    COUNT(*) AS 'Total'
FROM vPessoa
INNER JOIN vAluno
    ON vPessoa.Codigo = vAluno.CodigoPessoa
INNER JOIN vAlunoTurma
    ON vAluno.Codigo = vAlunoTurma.CodigoAluno
INNER JOIN vRelacao
    ON vAlunoTurma.CodigoRelacao = vRelacao.Codigo
INNER JOIN vCurso
    ON vRelacao.CodigoCurso = vCurso.Codigo
WHERE vAluno.CodigoUnidade = 1
    AND vRelacao.CodigoUnidade = 1
    AND vRelacao.Ano = 2020
    AND vAlunoTurma.CodigoTipoStatus IN (1, 23)
    AND vRelacao.EAD = 0    
GROUP BY vRelacao.Turma;
```

