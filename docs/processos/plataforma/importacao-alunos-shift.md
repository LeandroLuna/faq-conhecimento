#Importação de alunos SHIFT

<div style="height: 630px; overflow-x:scroll;">
    <img src="../importacao-alunos-shift.svg" style="max-width: initial;">
</div>

<sup> Mapeado por <a href="https://teams.microsoft.com/l/chat/0/?users=vanessa.marques@fiap.com.br"> Vanessa Marques </a> </sup>

##Links

**Link para ferramenta de relacionar cursos e turmas do SHIFT:**<br />
<https://on.fiap.com.br/local/importadoralunos/index.php>

**Como acessar direto pelo menu**<br />
Ferramentas **>** Relação SHIFT **>** Gerenciar

**Link para o job no Jenkins:**<br />
[FIAPON_CRON_IMPORTACAO_SHIFT](http://jenkins.fiap.com.br/job/FIAPON/job/CRON/job/IMPORTACAO/job/FIAPON_CRON_IMPORTACAO_SHIFT/)
<br />(Mapear no hosts **192.168.60.68 jenkins.fiap.com.br** e acessar via VPN)

##Querys

###Alunos para serem importados em uma turma
Conecte-se ao 10.20 para executar esta query.

```sql
USE Shift;
GO

SELECT
    Aluno.RM,
    CONCAT(Aluno.Nome, ' ', Aluno.Sobrenome) AS Nome,
    Aluno.CPF,
    Aluno.Email,
    AlunoCompra.DataHoraCompra,
    StatusCompra.Descricao AS StatusCompra
FROM AlunoTurma
INNER JOIN AlunoCompra
    ON AlunoTurma.CodigoAlunoCompra =AlunoCompra.Codigo
INNER JOIN Aluno
    ON AlunoCompra.CodigoAluno = Aluno.Codigo
INNER JOIN StatusCompra
    ON AlunoCompra.CodigoStatusCompra =StatusCompra.Codigo
INNER JOIN UsuarioMoodleNoStop
    ON Aluno.Codigo = UsuarioMoodleNoStop.CodigoAluno
    AND AlunoTurma.CodigoTurma = UsuarioMoodleNoStop.CodigoCurso
WHERE AlunoTurma.CodigoTurma = @cursoSHIFT
  AND UsuarioMoodleNoStop.Acao = 'Incluir'
  AND UsuarioMoodleNoStop.Processado = 0
ORDER BY
    Aluno.Nome,
    Aluno.Sobrenome;
```

###Encontrar usuário por chave SHIFT

```sql
SELECT
    fiapead_user.username,
    CONCAT(fiapead_user.firstname, ' ', fiapead_user.lastname) AS 'Nome completo'
FROM fiapead_user_info_data
INNER JOIN fiapead_user
    ON fiapead_user_info_data.userid = fiapead_user.id
WHERE fiapead_user_info_data.fieldid = 9
    AND fiapead_user_info_data.data = @chave_shift
```

##Problemas comuns

###Usuário sem item "Plataforma On-line"
O item "Plataforma On-line" é exibido para o aluno no site do SHIFT quando ele possui "Processado = 1" na
tabela UsuarioMoodleNoStop. Por isso, quando o usuário não possui esse item, ele ainda não foi importado
ou não foi inserido na tabela para ser importado. Neste caso, o INSERT deve ser realizado manualmente.

**Apenas execute este script se possui certeza que o aluno deve estar nessa turma.**

```sql
USE Shift;
GO

INSERT INTO UsuarioMoodleNoStop (CodigoAluno, CodigoCurso, Acao, Ativo)
VALUES (@codigo_aluno, @codigo_curso, 'Incluir', 1);
```

###Usuário sem chave SHIFT
Caso o aluno possua usuário na plataforma mas a chave SHIFT não esteja associada com nenhum usuário, ele
conseguirá visualizar o item "Plataforma On-line" no menu do site do SHIFT mas não conseguirá realizar
o login.