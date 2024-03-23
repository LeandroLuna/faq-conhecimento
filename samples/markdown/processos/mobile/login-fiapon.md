# Login FIAP ON

<div style="height: 585px; overflow-x:scroll;">
    <img src="../login-fiapon.svg" style="max-width: initial;">
</div>

<sup> Mapeado por <a href="https://teams.microsoft.com/l/chat/0/?users=vanessa.marques@fiap.com.br"> Vanessa Marques </a> </sup>

## Autenticação informando a chave

### Graduação e MBA

#### Verificar se existe chave no carreiras
Conecte-se ao banco Carreiras e execute o seguinte comando:

```sql
SELECT usuario.codigoID
FROM usuario
WHERE usuario.usuario = :rm
```

#### Verificar se chave do Carreiras está relacionada com usuário na plataforma
Conecte-se ao banco do moodle e execute o seguinte comando:

```sql
SELECT *
FROM fiapead_user_info_data
INNER JOIN fiapead_user
    ON fiapead_user_info_data.userid = fiapead_user.id
WHERE fiapead_user_info_data.data = :chave
    AND fiapead_user.username = 'rmxxxxx'
    AND fiapead_user_info_data.fieldid = 5
```

### SHIFT

#### Verificar se existe chave no SHIFT
Conecte-se ao banco SHIFT e execute o seguinte comando:

```sql
SELECT Aluno.ChaveEAD
FROM Aluno
WHERE Aluno.RM = :rm
    OR Aluno.Email = :email
```

#### Verificar se chave do SHIFT está relacionada com usuário na plataforma
Conecte-se ao banco do moodle e execute o seguinte comando:

```sql
SELECT *
FROM fiapead_user_info_data
INNER JOIN fiapead_user
    ON fiapead_user_info_data.userid = fiapead_user.id
WHERE fiapead_user_info_data.data = :chave
    AND fiapead_user.username = 'rmxxxxx'
    AND fiapead_user_info_data.fieldid = 9
```

## Quem conhece
- Douglas Carvalho Cabral <douglas.cabral@fiap.com.br>
  ([Chat do Teams](https://teams.microsoft.com/l/chat/0/?users=douglas.cabral@fiap.com.br))
- João Henrique Damazio <joao.damazio@fiap.com.br>
  ([Chat do Teams](https://teams.microsoft.com/l/chat/0/?users=joao.damazio@fiap.com.br))
- José Victor Borges Leles <jose.leles@fiap.com.br>
  ([Chat do Teams](https://teams.microsoft.com/l/chat/0/?users=jose.leles@fiap.com.br))
- Vanessa Marques <vanessa.marques@fiap.com.br>
  ( [Chat do Teams](https://teams.microsoft.com/l/chat/0/?users=vanessa.marques@fiap.com.br) )