# Home

Esta página contempla detalhes e conhecimentos necessários para se trabalhar com o 
Portal do Aluno da FIAP / FIAP School e Colégio Módulo.

## Habilitar/desabilitar ícone no Portal do Aluno FIAP

Para habilitar algum ícone para os alunos é necessário o cadastro/edição do ícone 
na tabela **site_fiap.dbo.CanalPortalItem**.

Caso o ícone seja apenas para alguns alunos específicos, há a possibilidade de 
inserir o nome de uma procedure que SEMPRE receberá por parâmetro o **RM** do aluno
logado no Portal para verificar se ele tem permissão de visualização.
