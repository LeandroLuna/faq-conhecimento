# Soft-Opening

Para o lançamento do aplicativo, os acessos foram limitados manualmente.

## Pós-Graduação

Estamos liberando por turmas e datas, os registros de liberação devem ser inseridos na tabela **SoftOpeningTurma**, ajustando com o nome da turma e data que devem ter acesso.

## Graduação

Ainda não estão liberados os testes para alunos de graduação, ajustar a procedure **spSoftOpen** conforme for necessário.

## Colaboradores

O acesso a colaboradores já está liberado na procedure

## Procedure de acesso controlado (spSoftOpen)

```sql
CREATE PROCEDURE [dbo].[spSoftOpen] @Usuario VARCHAR(255)
AS
BEGIN
    IF SUBSTRING(@Usuario, 1, 2) <> 'rm' AND ISNUMERIC(@Usuario) = 0
    BEGIN
        SELECT '1' AS Libera
        --SELECT '0' AS Libera
    END
    ELSE
    BEGIN
        IF @Usuario IN ('rm75008') OR @Usuario IN (
                                                    SELECT
                                                        'rm' + CAST(rm as varchar(7))
                                                    from
                                                        webadm..pos_inscricao_contrato
                                                    where
                                                        turma in (SELECT
                                                                    Turma collate Latin1_General_CI_AS
                                                                FROM
                                                                    SoftOpeningTurma
                                                                WHERE
                                                                    DataHoraLibera < GETDATE()))
        BEGIN
            SELECT '1' AS Libera
        END
        ELSE
        BEGIN
            SELECT '0' AS Libera
        END
    END
END
```
