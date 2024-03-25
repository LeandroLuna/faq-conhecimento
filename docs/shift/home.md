# Home

## Alterar a compra de um aluno para outro (transferir curso)

Ainda não existe ferramenta capaz de transferir a compra de um aluno para outro aluno, no momento, apenas alteramos o Aluno da tabela **AlunoCompra** para o novo aluno, assim seria como se ele tivesse comprado o curso por si só.

```sql hl_lines="3 4 5"
USE Shift
GO
DECLARE @CPFInscrito VARCHAR(11) = '26882933898' -- CPF de origem
DECLARE @CPFTransferir VARCHAR(11) = '42598382889' -- CPF de destino
DECLARE @CodigoCursoTransferir INT = (SELECT Codigo FROM vCurso WHERE Nome LIKE '%Smart Contracts em Blockchain com Ethereum%')
DECLARE @CodigoAlunoInscrito INT = (SELECT Codigo FROM Aluno WHERE CPF=@CPFInscrito)
DECLARE @CodigoAlunoTransferir INT = (SELECT Codigo FROM Aluno WHERE CPF=@CPFTransferir)
DECLARE @CodigoTurma INT
DECLARE @CodigoCompra INT

SELECT
  @CodigoTurma = Turma.Codigo,
  @CodigoCompra = C.Codigo
FROM
  Turma
  INNER JOIN AlunoTurma on Turma.Codigo = AlunoTurma.CodigoTurma
  INNER JOIN AlunoCompra C on AlunoTurma.CodigoAlunoCompra = C.Codigo
WHERE
  C.CodigoAluno = @CodigoAlunoInscrito AND
  Turma.CodigoCurso = @CodigoCursoTransferir

SELECT
  A.Nome,
  A.CPF,
  T.Turma,
  C2.Nome
FROM
  AlunoCompra
  INNER JOIN Aluno A on AlunoCompra.CodigoAluno = A.Codigo
  INNER JOIN AlunoTurma AT2 on AlunoCompra.Codigo = AT2.CodigoAlunoCompra
  INNER JOIN Turma T on AT2.CodigoTurma = T.Codigo
  INNER JOIN Curso C2 on T.CodigoCurso = C2.Codigo
WHERE
  AlunoCompra.Codigo = @CodigoCompra

-- Se os dados Acima estiverem corretos, descomente o update abaixo, também deve haver apenas uma linha do select acima
--UPDATE AlunoCompra SET CodigoAluno=@CodigoAlunoTransferir WHERE Codigo = @CodigoCompra

-- Esse ultimo SQL serve para conferir se realmente foi transferido
SELECT
  A.Nome,
  A.CPF,
  T.Turma,
  C2.Nome
FROM
  AlunoCompra
  INNER JOIN Aluno A on AlunoCompra.CodigoAluno = A.Codigo
  INNER JOIN AlunoTurma AT2 on AlunoCompra.Codigo = AT2.CodigoAlunoCompra
  INNER JOIN Turma T on AT2.CodigoTurma = T.Codigo
  INNER JOIN Curso C2 on T.CodigoCurso = C2.Codigo
WHERE
  A.Codigo = @CodigoAlunoTransferir
```

## Estornar Curso 

Primeiro temos que verificar se o número do pedido informado no chamado tenha mais que 1 curso atrelado, caso tenha apenas 1 curso, já existe uma ferramenta para estornar.
Caso tenha mais que 1, apenas deletamos o registro do curso em analise na tabela **AlunoTurma** e **ExtratoCarrinho** da base Shift

> Obs: O estorno monetário é realizado pela equipe do financeiro a pedido da equipe do Shift

```sql
DELETE Shift..AlunoTurma WHERE Codigo = @CodigoDaTurma

DELETE Shift..ExtratoCarrinho WHERE CodigoTurma = @CodigoDaTurma AND CodigoAlunoCompra = @CodigoDaCompra
```

## Problema na criação de usuários AD (travado)

Algumas vezes, ainda por motivo desconhecido, usuários AD do SHIFT não são criados no AD
e ficam travados, não criando nenhum usuário dali em diante.

Para resolver isso, é necessário achar o registro travado e excluí-lo do AD, para o service 
tentar novamente.

O SQL para saber a lista pendente de usuários SHIFT para criar no AD é:

```
SELECT
    ATurma.UsuarioAD
    , Aluno.*
    , ATurma.Codigo            
    , ATurma.DescontoAntecipado
    , ATurma.EmitiCertificado
    , ATurma.Chave
    , ATurma.CodigoTrilhaCurso
    , ATurma.PorcentagemDescontoEspecial
    , ATurma.EmitirCertificadoAutomatico
    , ATurma.CodigoStatusTurma
    , ATurma.SenhaAD
    , Turma.Codigo
    , Turma.CodigoCurso
    , Turma.CodigoProfessor
    , Turma.CodigoUnidade
    , Turma.Turma
    , Turma.Vagas
    , Turma.PeriodoPorExtenso
    , Turma.DataInicio
    , Turma.DataTermino
    , Turma.CargaHoraria
    , Turma.DataHoraInicioVenda
    , Turma.DataDescontoAntecipado
    , Turma.DataHoraTerminoVenda
    , Turma.DataHoraDesabilitaBoleto
    , Turma.Valor
    , Turma.ValorAntecipado
    , Turma.DescontoAntecipado
    , Turma.DescontoAVista
    , Turma.DescontoAluno
    , Turma.IHelp
    , Turma.Valor1IHelp
    , Turma.Valor2IHelp
    , Turma.Valor3IHelp
    , Turma.ColocarEmDestaque
    , Turma.Ativo
    , Turma.Liberado
    , Turma.ValorCheioPacote
    , Turma.ImportanteVitrine
    , Turma.DatasPorExtenso
    , Turma.MostraCalendario
    , Turma.DescontoColaborador
    , Turma.ImgSummerCourse
    , Turma.Esgotado
    , Turma.QtdDiaNoStop
    , Turma.DataHoraCadastro
    , Turma.CodigoUsuarioCadastro
    , Turma.CustoAluno
    , Turma.FechadoFinanceiro
    , Curso.Codigo
    , Curso.Nome
FROM
    AlunoTurma as ATurma
    INNER JOIN Turma ON ATurma.CodigoTurma = Turma.Codigo
    INNER JOIN AlunoCompra ON ATurma.CodigoAlunoCompra = AlunoCompra.Codigo
    INNER JOIN Aluno ON AlunoCompra.CodigoAluno = Aluno.Codigo
    INNER JOIN Curso ON Turma.CodigoCurso = Curso.Codigo
WHERE
    ATurma.CodigoStatusTurma = 1
    AND CONVERT(DATE, DATEADD(dd, -10, Turma.DataInicio)) <= CONVERT(DATE, GETDATE())
    AND CONVERT(DATE, Turma.DataTermino) >= CONVERT(DATE, GETDATE())
    AND ATurma.UsuarioAD IS NULL
    AND ATurma.SenhaAD IS NULL
    AND Curso.OnlineLive = 1
```