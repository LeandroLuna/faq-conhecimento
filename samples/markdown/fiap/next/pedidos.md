# Pedidos NEXT

## Configurações na base de dados

``` sql
UPDATE BaseEducacional.dbo.NTConfiguracao SET QtdConvite = 3, Valor = 20, DataHoraTerminoVenda = '2018-12-25 23:59:00.000', QtdConviteAlunos = 17, Ano = 2017 WHERE Codigo = 1;
```

- Habilitar a trigger trFNDebitos da BaseEducacional
``` sql
ALTER TRIGGER [dbo].[trFNDebitos]
...
```

- Habilitar a caixa do Next no Portal do Aluno
``` sql
UPDATE site_fiap..CanalPortalItem SET Ativo = 1 WHERE Codigo=120; -- Graduação
UPDATE site_fiap..CanalPortalItem SET Ativo = 1 WHERE Codigo=121; -- Pós-graduação

SP_HELPTEXT spLiberaNext; -- Stored-Procedure que libera o acesso para a graduação
SP_HELPTEXT spLiberaNextPos; -- Stored-Procedure que libera o acesso para a pós-graduação
```