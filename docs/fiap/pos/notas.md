# Notas

## Lançamento de notas para o MBA Presencial

A tabela que contém o boletim do aluno de MBA Presencial é **BoletimPosLancamento**
dentro do banco **site_fiap**.

A coluna **media** é a nota final do aluno para cada disciplina representada por cada linha.

## Lançamento de notas para o MBA On-line 

A tabela que contém o boletim do aluno de MBA On-line é **BoletimPosLancamentoOnLine** 
dentro do banco **site_fiap**.

!!! warning
    Caso seja alterado manualmente as notas nesta tabela, é necessário colocar a flag de manual 
    correspondente a coluna. Ex: Media alterada manualmente, colocar o valor 1 na coluna MediaManual.

## Lançamento de notas em entrega de trabalho dos Portal do Aluno

Para alterar a nota de alguma entrega de trabalho as tabelas necessárias 
para encontrar o registro são:

site_fiap..EntregaTrabalho 

site_fiap..EntregaTrabalhoArquivo

site_fiap..EntregaTrabalhoIntegrantes