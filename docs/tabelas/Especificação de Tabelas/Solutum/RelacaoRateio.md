# RelacaoRateio

Tabela onde são armazenado os tipos de **filtros de um Rateio**. 
Esta tabela é utilizada em alguns sistemas da 
<a href="https://intranet3.fiap.com.br/" target="_blank">Intranet3</a>.

## Colunas

- **CodigoGrupoConta**: Valor que define o **Grupo da Conta**, de acordo com a 
tabela **Solutum..GrupoContaRateio**;
- **CodigoCampus**: Valor que define o **Campus**, de acordo com a tabela 
**Solutum..Campus**;
- **CodigoUnidadeNegocios**: Valor que define a **Unidade de Negócios**, de 
acordo com a tabela **Solutum..UnidadeNegocios**;
- **CodigoSegmento**: Valor que define o **Segmento**, de acordo com a tabela 
**Solutum..Segmento**;
- **CodigoCursos**: Valor que define o **Cursos**, de acordo com a tabela 
**Solutum..Cursos**;
- **CodigoTurno**: Valor que define o **Turno**, de acordo com a tabela 
**Solutum..Turno**;
- **Ativo**: Valor que define se o registro está **ativo** ou não (Ativo = 0 --> 
**exclusão lógica**);
- **TipoSolicitacao**: Valor que define o **Tipo de Solicitação**;
- **ModeloRateio**: Valor que define o **Modelo de Rateio**;

## Buscando filtros já existentes

```sql
SELECT 
    *
FROM 
    Solutum..RelacaoRateio 
WHERE 
    /* Preencher conforme tabela Solutum..Campus */
    CodigoCampus = 4 
    /* Preencher conforme tabela Solutum..UnidadeNegocios */
    AND CodigoUnidadeNegocios = 1 
    /* Preencher conforme tabela Solutum..Segmento */
    AND CodigoSegmento = 12;
```

## Cadastrando um novo cruzamento/filtro de Rateio

Para cadastrar um novo filtro de Rateio, **preencha as variáveis** abaixo e 
insira um registro na tabela **Solutum..RelacaoRateio**:

```sql
--SELECT * FROM Solutum..GrupoContaRateio WHERE Ativo = 1;
-- Utilizar SEMPRE o valor 14
DECLARE @CodigoGrupoConta AS INT = 14;

--SELECT * FROM Solutum..Campus WHERE Ativo = 1 ORDER BY Campus;
-- Exemplo: 'Institucional' --> 8
DECLARE @CodigoCampus AS INT = XX;

--SELECT * FROM Solutum..UnidadeNegocios WHERE Ativo = 1 ORDER BY UnidadeNegocios;
-- Exemplo: 'EAD' --> 5
DECLARE @CodigoUnidadeNegocios AS INT = XX;

--SELECT * FROM Solutum..Segmento WHERE Ativo = 1 ORDER BY Segmento;
-- Exemplo: 'Graduação ON' --> 25
DECLARE @CodigoSegmento AS INT = XX;

--SELECT * FROM Solutum..Cursos WHERE Ativo = 1 ORDER BY CodigoCursos DESC;
-- Exemplo: 'Curso Bacharelado' --> 86
DECLARE @CodigoCursos AS INT = XX;

-- Caso seja necessário adicionar algum curso
--INSERT INTO Solutum..Cursos VALUES ('Curso Bacharelado', 1)

--SELECT * FROM Solutum..Turno WHERE Ativo = 1 ORDER BY Codigo;
-- Exemplo: 'Todos' --> 4
DECLARE @CodigoTurno AS INT = XX;

-- Utilizar SEMPRE o valor 1
DECLARE @Ativo AS BIT = 1;

-- Utilizar SEMPRE o valor NULL (NULL --> Rateio normal; 2 --> Rateio folha de pagamento)
DECLARE @TipoSolicitacao AS TINYINT = NULL;

-- Utilizar SEMPRE o valor NULL
DECLARE @ModeloRateio AS TINYINT = NULL;

-- Inserindo novo cruzamento (filtro)
INSERT INTO Solutum..RelacaoRateio 
	(CodigoGrupoConta, 
	CodigoCampus, 
	CodigoUnidadeNegocios, 
	CodigoSegmento, 
	CodigoCursos, 
	CodigoTurno, 
	Ativo, 
	TipoSolicitacao,
	ModeloRateio)
VALUES 
	(@CodigoGrupoConta,
	@CodigoCampus,
	@CodigoUnidadeNegocios,
	@CodigoSegmento,
	@CodigoCursos,
	@CodigoTurno,
	@Ativo,
	@TipoSolicitacao,
	@ModeloRateio);
```
