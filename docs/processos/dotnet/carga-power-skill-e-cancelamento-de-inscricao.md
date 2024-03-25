# Realização de carga para power skills e cancelamento de inscrição

<div style="height: 640px; overflow-x:scroll;">
    <img src="../carga-power-skill-e-cancelamento-de-inscricao.svg" style="max-width: initial;">
</div>


## Extração de base de usuários que terão acesso a plataforma Power Skill

A Query Abaixo, será possivel identificar quais chaves terão acesso a plataforma.

Usada também para o e-mail marketing disparado para os alunos pelo Marketing.

Geralmente turmas de Coorporate e Pós Tech não participam. A consulta abaixo já remove eles. Mas **SEMPRE CONFIRMAR** antes de gerar a base!

```sql
SELECT  
    pos_inscricao_contrato.rm,
    pos_inscricao_new.nome,
    pos_inscricao_new.email,
    pos_inscricao_turmas.Turma,
    PI_InscricaoProcesso.ChaveValidacao,
    MAX(pos_inscricao_turmas.codigoProcesso) AS 'codigoProcesso',
    CONCAT('https://www2.fiap.com.br/mba-power-skills/key/', PI_InscricaoProcesso.ChaveValidacao) AS link
FROM  
    webadm..pos_inscricao_contrato AS pos_inscricao_contrato WITH (NOLOCK)
INNER JOIN webadm..pos_inscricao_new AS pos_inscricao_new WITH (NOLOCK)
    ON pos_inscricao_contrato.codigoInscricao = pos_inscricao_new.codigo
INNER JOIN WebAdm..PI_InscricaoProcesso AS PI_InscricaoProcesso WITH (NOLOCK) 
    ON pos_inscricao_contrato.codigoInscricaoProcesso = PI_InscricaoProcesso.Codigo  
INNER JOIN webadm..pos_inscricao_turmas AS pos_inscricao_turmas WITH (NOLOCK) 
    ON pos_inscricao_contrato.Turma = pos_inscricao_turmas.Turma
INNER JOIN webadm..PI_Processo AS PI_Processo
    ON pos_inscricao_turmas.codigoProcesso = PI_Processo.codigo
    AND PI_Processo.Tipo = 'MBA'
WHERE 
    pos_inscricao_turmas.Liberado = 1
    AND (
        (
            pos_inscricao_turmas.ano = 2022
            AND pos_inscricao_turmas.semestre = 2
        )
        OR 
        (
            pos_inscricao_turmas.ano = 2023
            AND pos_inscricao_turmas.semestre = 1
        )
    )
    AND pos_inscricao_turmas.Unidade <> 'Corp. VO'
GROUP BY  
    pos_inscricao_contrato.rm,
    pos_inscricao_new.nome,
    pos_inscricao_new.email,
    pos_inscricao_turmas.Turma,
    PI_InscricaoProcesso.ChaveValidacao,
    CONCAT('https://www2.fiap.com.br/mba-power-skills/key/', PI_InscricaoProcesso.ChaveValidacao)
ORDER BY 
    pos_inscricao_turmas.Turma,
    pos_inscricao_new.nome
```

## Inserção de rm e chave que precisa visualizar o PowerSkill no FIAP ON (Depreciado)

**Desde 05/2023, a etapa abaixo não é mais necessária, pois é consultado no SQL Server via API. Está apenas para documentação.**

```sql
    INSERT INTO moodle.fiapead_chave_validacao (username, chave, timecreated) VALUES ('rmXXXXXX', 'CHAVE-DO-USUARIO-AQUI', UNIX_TIMESTAMP())
```

## Exibição de ícone no Portal do Aluno

É necessário ajustar as turmas que podem ver o ícone de PowerSkill no Portal do Aluno presencial conforme as procedures abaixo:

```sql 
    ALTER PROCEDURE [dbo].[spAcessoPowerSkill] @rm INT AS  
    BEGIN  
        DECLARE @Retorno INT  
        SET @Retorno = 0  
      
        IF EXISTS(
            SELECT  
                *  
            FROM  
                webadm..PI_Processo AS PI_Processo  
            INNER JOIN webadm..pos_inscricao_turmas AS pos_inscricao_turmas 
                ON PI_Processo.codigo = pos_inscricao_turmas.codigoProcesso 
            INNER JOIN webadm..pos_inscricao_contrato AS pos_inscricao_contrato 
                ON pos_inscricao_turmas.Turma = pos_inscricao_contrato.turma
            WHERE
                pos_inscricao_contrato.rm = @rm
                AND pos_inscricao_turmas.Liberado = 1
                AND pos_inscricao_contrato.turma IN (
                    'SIGLA1',
                    'SIGLA2'
                )
        )
        BEGIN
            SET @Retorno = 1
        END
        
        SELECT @Retorno AS total
    END;
```

Ou de forma mais específica:

```sql 
    ALTER PROCEDURE [dbo].[spAcessoPowerSkill] @rm INT AS  
    BEGIN  
        DECLARE @Retorno INT  
        SET @Retorno = 0  
      
        IF EXISTS(
            SELECT  
                1 
            FROM  
                webadm..PI_Processo AS PI_Processo  
            INNER JOIN webadm..pos_inscricao_turmas AS pos_inscricao_turmas 
                ON PI_Processo.codigo = pos_inscricao_turmas.codigoProcesso 
            INNER JOIN webadm..pos_inscricao_contrato AS pos_inscricao_contrato 
                ON pos_inscricao_turmas.Turma = pos_inscricao_contrato.turma
            WHERE
                pos_inscricao_contrato.rm = @rm
                AND pos_inscricao_turmas.Liberado = 1
                AND (
                    pos_inscricao_contrato.rm = 345389 -- Marcão
                    OR
                    (
                        CONVERT(date, GETDATE()) >= '2023-05-15' 
                        AND pos_inscricao_contrato.rm IN (
                            RM1,
                            RM2,
                            ETC
                        )
                    )
                    OR 
                    (
                        CONVERT(date, GETDATE()) >= '2023-05-18'
                        AND pos_inscricao_contrato.turma IN (
                            'SIGLA1',
                            'SIGLA2'
                        )
                    )
                )
        )
        BEGIN
            SET @Retorno = 1
        END
        
        SELECT @Retorno AS total
    END;
```

Ou pela forma mais utilizada recentemente:

```sql
    ALTER PROCEDURE [dbo].[spAcessoPowerSkill] @rm INT AS  
    BEGIN  
        DECLARE @Retorno INT  
        SET @Retorno = 0  
      
        IF EXISTS(
            SELECT  
                1 
            FROM  
                webadm..PI_Processo AS PI_Processo  
            INNER JOIN webadm..pos_inscricao_turmas AS pos_inscricao_turmas 
                ON PI_Processo.codigo = pos_inscricao_turmas.codigoProcesso 
            INNER JOIN webadm..pos_inscricao_contrato AS pos_inscricao_contrato 
                ON pos_inscricao_turmas.Turma = pos_inscricao_contrato.turma
            WHERE
                pos_inscricao_contrato.rm = @rm
                AND PI_Processo.Tipo = 'MBA'
                AND pos_inscricao_turmas.Liberado = 1
                AND (
                    (
                        pos_inscricao_turmas.ano = 2022
                        AND pos_inscricao_turmas.semestre = 2
                    )
                    OR 
                    (
                        pos_inscricao_turmas.ano = 2023
                        AND pos_inscricao_turmas.semestre = 1
                    )
                )
                AND pos_inscricao_turmas.Unidade <> 'Corp. VO'
            )
        BEGIN
            SET @Retorno = 1
        END
        
        SELECT @Retorno AS total
    END;
```

## Página do ícone do Portal do Aluno

Editar a consulta SQL existente em: **/programas/login/alunos_2004/powerskill/default.asp**


## Links
**Api.PSTrilhas:** [https://gitlab.fiap.com.br/dotnet/Api.PSTrilhas.git](https://gitlab.fiap.com.br/dotnet/Api.PSTrilhas.git) 

**Intranet.PowerSkill ADM:** [https://gitlab.fiap.com.br/dotnet/Intranet.PowerSkill.git](https://gitlab.fiap.com.br/dotnet/Intranet.PowerSkill.git) 

**Front Power Skill** [https://gitlab.fiap.com.br/dotnet/Intranet.PowerSkill.git](https://gitlab.fiap.com.br/dotnet/Intranet.PowerSkill.git) 

## Quem criou
- Henrique Lopes <henrique.mendonca@fiap.com.br> 
( [Chat do Teams](https://teams.microsoft.com/l/chat/0/?users=henrique.mendonca@fiap.com.br) )

## Quem conhece
- Henrique Lopes <henrique.mendonca@fiap.com.br> 
( [Chat do Teams](https://teams.microsoft.com/l/chat/0/?users=henrique.mendonca@fiap.com.br) )
- Douglas Cabral <douglas.cabral@fiap.com.br> 
( [Chat do Teams](https://teams.microsoft.com/l/chat/0/?users=douglas.cabral@fiap.com.br) )
- Gustavo Cardoso <gustavo.silvac@fiap.com.br> 
( [Chat do Teams](https://teams.microsoft.com/l/chat/0/?users=gustavo.silvac@fiap.com.br) )
