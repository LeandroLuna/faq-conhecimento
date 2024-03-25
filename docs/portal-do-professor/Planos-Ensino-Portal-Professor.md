# Planos de ensino de cursos - Portal do professor 📚

Para atender a solicitação de extração de plano de ensino de algum curso da graduação, pode ser utilizado as querys abaixo apenas alterando as condições de filtros no **WHERE**.

Nas condições das querys, em **Relacao_2004.Turma**, é possível colocar a sigla da turma que deseja extrair os dados e em **Relacao_2004.Ano**, colocar o ano que deseja analisar o plano de estudo. Para sempre vir planos ativos, manter a condição 
**Relacao_2004.Ativo = 1**.

Para selecionar os planos sem a data que foram lecionados, pode ser utilizado a query abaixo:

```sql
SELECT 
       Curso_2004.Descricao AS 'Curso',
       ConteudoNovo.Descricao AS 'Turma',
       ConteudoNovo.Ano,
       Disciplina_2004.Descricao AS 'Disciplina',
       ConteudoNovoProgramacao.Ordem,
       ConteudoNovoProgramacao.Descricao AS 'Conteúdo',
       Professor_2004.Nome AS 'NomeProfessor'
FROM Curso_2004 
    INNER JOIN Relacao_2004
        ON Curso_2004.Codigo = Relacao_2004.CodCurso
    INNER JOIN Disciplina_2004
        ON Disciplina_2004.Codigo = Relacao_2004.CodDisciplina
    INNER JOIN Professor_2004
        ON Professor_2004.Codigo = Relacao_2004.CodProfessor
    INNER JOIN ConteudoNovoRelacao
        ON ConteudoNovoRelacao.CodigoRelacao = Relacao_2004.Codigo
    INNER JOIN ConteudoNovo
        ON ConteudoNovo.Codigo = ConteudoNovoRelacao.CodigoConteudo
    INNER JOIN ConteudoNovoProgramacao
        ON ConteudoNovoProgramacao.CodigoConteudo = ConteudoNovo.Codigo
WHERE 
    Relacao_2004.Turma LIKE '%TIA%'
    AND Curso_2004.TipoFormacaoCurso = 'T'
    AND Relacao_2004.Ano IN (2021, 2022)
    AND Relacao_2004.Ativo = 1
ORDER BY 
    Curso_2004.Descricao,
    Relacao_2004.Turma,
    Professor_2004.Nome,
    ConteudoNovo.Ano DESC,
    ConteudoNovoProgramacao.Ordem
```

Para extrair os planos de estudo incluindo a data na qual foram lecionados, basta utilizar a query abaixo:

```sql
SELECT 
       Curso_2004.Descricao AS 'Curso',
       ConteudoNovo.Descricao AS 'Turma',
       ConteudoNovo.Ano,
       Disciplina_2004.Descricao AS 'Disciplina',
       ConteudoNovoProgramacao.Ordem,
       ConteudoNovoProgramacao.Descricao AS 'Conteúdo',
       CONVERT(CHAR(10), ConteudoNovoRealizado.Data1, 103) AS 'Data',
       Professor_2004.Nome AS 'NomeProfessor'
FROM Curso_2004 
    INNER JOIN Relacao_2004
        ON Curso_2004.Codigo = Relacao_2004.CodCurso
    INNER JOIN Disciplina_2004
        ON Disciplina_2004.Codigo = Relacao_2004.CodDisciplina
    INNER JOIN Professor_2004
        ON Professor_2004.Codigo = Relacao_2004.CodProfessor
    INNER JOIN ConteudoNovoRelacao
        ON ConteudoNovoRelacao.CodigoRelacao = Relacao_2004.Codigo
    INNER JOIN ConteudoNovo
        ON ConteudoNovo.Codigo = ConteudoNovoRelacao.CodigoConteudo
    INNER JOIN ConteudoNovoProgramacao
        ON ConteudoNovoProgramacao.CodigoConteudo = ConteudoNovo.Codigo
    LEFT JOIN ConteudoNovoRealizado ON
        Relacao_2004.Codigo = ConteudoNovoRealizado.CodigoRelacao
        AND ConteudoNovoProgramacao.Codigo = ConteudoNovoRealizado.CodigoConteudoProgramacao
WHERE 
    Relacao_2004.Turma LIKE '%TIA%'
    AND Curso_2004.TipoFormacaoCurso = 'T'
    AND Relacao_2004.Ano IN (2021, 2022)
    AND Relacao_2004.Ativo = 1
ORDER BY 
    Curso_2004.Descricao,
    Relacao_2004.Turma,
    Relacao_2004.Ano,
    Disciplina_2004.Descricao,
    ISNULL(ConteudoNovoRealizado.Data1, '99991231')

```
