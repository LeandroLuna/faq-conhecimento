# Grupo-Bot de Scripts para Rodar em Produção

!!! info "Última modificação"
    **29-11-2023**   Victor Alves Bugueno

Atualmente, a maior parte dos desenvolvedores tem acesso apenas aos banco de 
**Desenvolvimento** e **Homologação**. Dessa forma, quando for necessária alguma 
atualização de dados em **Produção**, deve-se desenvolver um script e 
encaminhá-lo ao **Grupo-Bot de Scripts** a fim de que este script seja avaliado
e executado no **ambiente produtivo**.

Estes scripts deverão estar de acordo com as seguintes regras:

1. O nome do arquivo no modelo: **"Ticket {N° do Ticket} - {Breve descrição}"**.
**Exemplo:** "Ticket 12345 - Atualizando valores de Mensalidade do RM 54321";

2. Utilize sempre o **caminho absoluto** para tabelas, e outros objetos SQL, 
facilitando o processo de execução.

    **Exemplo:** 
    ```sql
    -- Utilize:
    SELECT
        *
    FROM
        BaseEducacional..FNDebitos;
        
    -- Ao invés de:
    USE BaseEducacional;

    SELECT
        *
    FROM
        FNDebitos;
    ```

3. Nos filtros (**WHERE**), utilize sempre que possível a coluna **IDENTITY** da 
tabela (normalmente a coluna **Codigo**), assegurando que os 
**registros manipulados** são realmente os que **precisam ser alterados**.

4. **Evite** a inclusão de **comentários e querys auxiliares**. Deixe no script 
    apenas:

    - A query de **backup** (se possível, com **UNION ALL**), com o 
    **mesmo filtro** da query a ser executada;
    - A **query de execução** (INSERT, UPDATE, DELETE, ALTER PROCEDURE…);

5. Em **INSERTs**, inclua sempre a lista de **nome das colunas** que estão sendo 
preenchidas na query.

    **Exemplo:** 
    ```sql
    -- Utilize:
    INSERT INTO Banco..Aluno
        (Nome,
        DataNascimento,
        CPF)
    VALUES
        ('Victor Alves',
        '1999-01-10',
        '12345678910');
        
    -- Ao invés de:
    INSERT INTO 
        Banco..Aluno
    VALUES
        ('Victor Alves',
        '1999-01-10',
        '12345678910');
    ```

!!! warning "Observações"
    **Não é necessária** query de **backup** para **INSERT’s** e alterações de 
    estrutura como ALTER PROCEDURE (**DDL**).
    Tabelas do banco **Educacional**, apesar de não possuirem a coluna 
    **Codigo** como **IDENTITY**, possuem a coluna **Identificador IDENTITY**, 
    facilitando a seleção de **um registro em específico**.
    Para mais informações sobre as tabelas do banco Educacional, confira a 
    **[Documentação Completa](http://conhecimento.fiap.com.br/tabelas/Especifica%C3%A7%C3%A3o%20de%20Tabelas/Educacional/TabelasColunasControle/)**