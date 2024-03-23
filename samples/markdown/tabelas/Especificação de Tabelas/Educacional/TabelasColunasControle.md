# Tabelas com Colunas de Controle

!!! info "Última modificação"
    **28-11-2023**   Victor Alves Bugueno

Grande parte das tabelas do banco **Educacional** possuem uma regra bem 
específica que permite guardar **histórico** dos registros na **própria tabela**.

Para isso, foi necessária a criaçao das colunas de controle **Deletado**, 
**StatusRegistro** e **DataStatusInformacao**, que identificam o
registro mais atual.

## Planilha explicando como funcionam as Colunas de Controle

![Printscreen da Planilha explicando como funcionam as Colunas de Controle](Arquivos/Printscreen%20-%20Explicação%20das%20colunas%20de%20controle%20(Deletado,%20StatusRegistro%20e%20DataStatusInformacao)%20das%20tabelas%20do%20banco%20Educacional.png)

Caso necessário, utilize a [Planilha Excel](Arquivos/Explicação%20das%20colunas%20de%20controle%20(Deletado,%20StatusRegistro%20e%20DataStatusInformacao)%20das%20tabelas%20do%20banco%20Educacional.xlsx) em anexo.

## Inserindo um novo registro numa tabela com colunas de controle

**Insira** o registro conforme orientação abaixo:

- **Identificador**: coluna **IDENTITY** (valor auto-gerado);
- **Codigo**: identifique o **maior código** já inserido na tabela e utilize 
o **valor subsequente**;
- **Deletado**: recebe o valor **0**, pois o registro 
**não está sendo desativado**;
- **StatusRegistro**: recebe o valor **1**, indicando que este é o registro 
**mais atual** do histórico;
- **DataStatusInformacao**: Data e hora do momento atual (**GETDATE()**);
- **Demais colunas** da tabela deverão receber os valores normalmente;

## Atualizando registros numa tabela com colunas de controle

**Altere** a coluna StatusRegistro do registro mais atual **de 1 para 0**:

- **StatusRegistro**: recebe o valor **0**, indicando que este **não é** o 
registro **mais atual** do histórico;
- **Demais colunas** da tabela não deverão ser alteradas;

E **insira** um novo registro, com as informações atualizadas:

- **Identificador**: coluna **IDENTITY** (valor auto-gerado);
- **Codigo**: recebe o **mesmo valor** do registro recém-alterado;
- **Deletado**: recebe o valor **0**, pois o registro 
**não está sendo desativado**;
- **StatusRegistro**: recebe o valor **1**, indicando que este é o registro 
**mais atual** do histórico;
- **DataStatusInformacao**: Data e hora do momento atual (**GETDATE()**);
- **Demais colunas** da tabela deverão receber os valores atualizados;

## Desativando registros numa tabela com colunas de controle

**Altere** a coluna StatusRegistro do registro mais atual **de 1 para 0**:

- **StatusRegistro**: recebe o valor **0**, indicando que este **não é** o 
registro **mais atual** do histórico;
- **Demais colunas** da tabela não deverão ser alteradas;

E **insira** um novo registro, com as mesmas informações, porém com a coluna
**Deletado = 1**:

- **Identificador**: coluna **IDENTITY** (valor auto-gerado);
- **Codigo**: recebe o **mesmo valor** do registro recém-alterado;
- **Deletado**: recebe o valor **1**, pois o registro 
**está sendo desativado**;
- **StatusRegistro**: recebe o valor **1**, indicando que este é o registro 
**mais atual** do histórico, mesmo que esteja desativado;
- **DataStatusInformacao**: Data e hora do momento atual (**GETDATE()**);
- **Demais colunas** da tabela não deverão ser alteradas;