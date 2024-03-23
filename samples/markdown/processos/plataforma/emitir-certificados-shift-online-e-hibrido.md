# Emitir certificados SHIFT On-line e Híbrido

<div style="height: 520px; overflow-x:scroll;">
    <img src="../emitir-certificados-shift-online-e-hibrido.svg" style="max-width: initial;">
</div>

<sup> Mapeado por <a href="https://teams.microsoft.com/l/chat/0/?users=vanessa.marques@fiap.com.br"> Vanessa Marques </a> </sup>

## Links
**Link para o job no Jenkins:**<br />
[FIAPON_CRON_CERTIFICADOS_SHIFT](http://jenkins.fiap.com.br/job/FIAPON/job/CRON/job/CERTIFICADOS/job/FIAPON_CRON_CERTIFICADOS_SHIFT/)
<br />(Mapear no hosts **192.168.60.68 jenkins.fiap.com.br** e acessar via VPN)

##Querys

###Data de inscrição
```sql
SELECT FROM_UNIXTIME(fiapead_user_enrolments.timestart, '%d/%m/%Y %H:%i') AS 'Data de inscrição'
FROM fiapead_enrol
INNER JOIN fiapead_user_enrolments
    ON fiapead_enrol.id = fiapead_user_enrolments.enrolid
WHERE fiapead_enrol.courseid = :course_id
  AND fiapead_user_enrolments.userid = :user_id
```

###Tempo de duração do curso (em dias)
```sql
SELECT fiapead_moodle_relacaoshift.tempocurso
FROM fiapead_moodle_relacaoshift
WHERE fiapead_moodle_relacaoshift.course = :course_id
```

###Visualização do aluno em um curso
```sql
SELECT fiapead_fiap_course_visualizacao.visualizacao
FROM fiapead_fiap_course_visualizacao
WHERE fiapead_fiap_course_visualizacao.courseid = :course_id
  AND fiapead_fiap_course_visualizacao.userid = :user_id
```

## Quem conhece

- Douglas Cabral <douglas.cabral@fiap.com.br>
  ( [Chat do Teams](https://teams.microsoft.com/l/chat/0/?users=douglas.cabral@fiap.com.br) )
- Vanessa Marques <vanessa.marques@fiap.com.br>
  ( [Chat do Teams](https://teams.microsoft.com/l/chat/0/?users=vanessa.marques@fiap.com.br) )