## Listagem de coordenadores dos curso

```sql
SELECT 
    Coordenador_2004.*,
    Professor_2004.Nome,
    Curso_2004.Descricao
FROM Coordenador_2004
INNER JOIN Professor_2004
    ON Coordenador_2004.CodProfessor = Professor_2004.Codigo
INNER JOIN Curso_2004
    ON Coordenador_2004.CodCurso = Curso_2004.Codigo
ORDER BY Coordenador_2004.Codigo;
```