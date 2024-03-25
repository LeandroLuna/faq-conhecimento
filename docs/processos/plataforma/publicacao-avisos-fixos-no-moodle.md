# Publicar avisos fixos no Moodle

<div style="height: 950px; overflow-x:scroll;">
    <img src="../publicacao-avisos-fixos-no-moodle.svg" style="max-width: initial;">
</div>

## Informações adicionais

O nome da "tag" que usamos para nomear um aviso segue um padrão: **anomesdia-nome-do-aviso**<br />
**Ex:** 20220204-lembrete-para-os-alunos-de-dp

## Insert em lote de alunos das turmas que precisam ver

```sql
INSERT INTO fiapead_avisos ( user, tag, timecreated )
SELECT
    vAlunoCursoResumeRegra.username,
    'nome-da-tag-aqui',
    UNIX_TIMESTAMP()
FROM vAlunoCursoResumeRegra
WHERE vAlunoCursoResumeRegra.nivel5 IN ('sigla', 'das', 'turmas', 'aqui')
    AND vAlunoCursoResumeRegra.nivel3 = '2021/1'
    AND vAlunoCursoResumeRegra.username REGEXP '^rm'
GROUP BY
    vAlunoCursoResumeRegra.username
```

## Quem conhece

- Douglas Cabral <douglas.cabral@fiap.com.br> 
( [Chat do Teams](https://teams.microsoft.com/l/chat/0/?users=douglas.cabral@fiap.com.br) )
- Vanessa Marques <vanessa.marques@fiap.com.br> 
( [Chat do Teams](https://teams.microsoft.com/l/chat/0/?users=vanessa.marques@fiap.com.br) )
- Nícolas Maloucaze <nicolas.pereira@fiap.com.br> 
( [Chat do Teams](https://teams.microsoft.com/l/chat/0/?users=nicolas.pereira@fiap.com.br) )
- Carlos Toledo <carlos.toledo@fiap.com.br>
( [Chat do Teams](https://teams.microsoft.com/l/chat/0/?users=carlos.toledo@fiap.com.br) )
- Gabriel Aparecido Cassalho Xavier <gabriel.xavier@fiap.com.br>
( [Chat do Teams](https://teams.microsoft.com/l/chat/0/?users=gabriel.xavier@fiap.com.br) )
- Rafael Guilherme de Oliveira Vieira <rafael.vieira@fiap.com.br>
( [Chat do Teams](https://teams.microsoft.com/l/chat/0/?users=rafael.vieira@fiap.com.br) )