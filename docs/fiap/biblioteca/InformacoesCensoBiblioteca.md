# Query para extração de informações do Censo Biblioteca 📚

Para extrair informações da biblioteca referente ao Censo, utilize as seguintes querys abaixo no servidor **192.168.60.32** banco **Biblioteca**:

```sql
use Biblioteca
--192.168.60.32

--NUmero de emprestimos
SELECT * FROM Movimentacao WHERE DataEmprestimo >= '20230101' AND DataEmprestimo < '20240101' AND DataPrevistaDevolucao IS NOT NULL AND CodigoAssociado IN (
SELECT 
	AssociadoBiblioteca.Codigo
FROM 
	Pessoa 
	INNER JOIN Associado ON
		Pessoa.Codigo = Associado.CodigoPessoa
	INNER JOIN AssociadoBiblioteca ON
		Associado.Codigo = AssociadoBiblioteca.CodigoAssociado
WHERE 
	Pessoa.CodigoTipoPessoa = 201
	AND ISNUMERIC(Pessoa.Referencia) = 1
	AND (
		CONVERT(int, Pessoa.Referencia) BETWEEN 50000 AND 89999
		OR CONVERT(int, Pessoa.Referencia) BETWEEN 92000 AND 99998
		OR CONVERT(int, Pessoa.Referencia) BETWEEN 500000 AND 599999
	)

	)

--Numeros de Usuarios
SELECT 
	AssociadoBiblioteca.*
FROM 
	Pessoa 
	INNER JOIN Associado ON
		Pessoa.Codigo = Associado.CodigoPessoa
	INNER JOIN AssociadoBiblioteca ON
		Associado.Codigo = AssociadoBiblioteca.CodigoAssociado
WHERE 
	Pessoa.CodigoTipoPessoa = 201
	AND ISNUMERIC(Pessoa.Referencia) = 1
	AND (
		CONVERT(int, Pessoa.Referencia) BETWEEN 50000 AND 89999
		OR CONVERT(int, Pessoa.Referencia) BETWEEN 92000 AND 99998
		OR CONVERT(int, Pessoa.Referencia) BETWEEN 500000 AND 599999
	)
	AND AssociadoBiblioteca.CodigoSituacao <> 3
	

--Qtde exemplares por tipo
SELECT
	Materiais.Descricao,
	COUNT(*)
FROM
	PublicacaoExemplar
	INNER JOIN Publicacao ON
		PublicacaoExemplar.CodigoPublicacao = Publicacao.Codigo
	INNER JOIN Materiais ON
		Publicacao.CodigoTipoMaterial = Materiais.Codigo
WHERE
	PublicacaoExemplar.Situacao <> 5
	AND Publicacao.CodigoUnidade IN (2, 3, 5, 6, 7)
GROUP BY
	Materiais.Descricao
ORDER BY
	Materiais.Descricao

```

