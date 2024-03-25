# Consulta

A base da biblioteca da fiap em produção está localizada em outro servidor de banco
de dados com o nome de rede 'sqlbiblioteca', por tanto não temos está base em homo e nem em prod,
respectivos 10.20 e 10.9.

Para realizarmos as consultas na base da Biblioteca precisamos ter em mente que os livros estão
presentes na tabela 'Publicacao' e seus exemplares em 'PublicacaoExemplar', mas existe uma tabela
que indexa campos de outras tabelas como autor e categoria, para facilitar a pesquisa, o nome desta
tabela é 'PublicacaoPesquisa' e usaremos ela para trazer todos os livros e quantidades de exemplares

```sql
SELECT
    PublicacaoPesquisa.Codigo,
    PublicacaoPesquisa.Tipo,
    PublicacaoPesquisa.Titulo,
    PublicacaoPesquisa.Idioma,
    PublicacaoPesquisa.Editora,
    PublicacaoPesquisa.ISBN_ISNN,
    PublicacaoPesquisa.Edicao,
    PublicacaoPesquisa.AnoPublicacao,
    PublicacaoPesquisa.Paginacao,  
    PublicacaoPesquisa.PodeEmprestar,
    PublicacaoPesquisa.Autor,
    PublicacaoPesquisa.Assuntos,
    (SELECT COUNT(*) FROM  PublicacaoExemplar AS PublicacaoExemplar WITH (NOLOCK) WHERE PublicacaoExemplar.Situacao IN (1, 2, 3, 4) AND PublicacaoExemplar.CodigoPublicacao = PublicacaoPesquisa.Codigo AND PublicacaoExemplar.MaterialApoio = 0) AS 'QtExemplares',
    ((SELECT COUNT(*) FROM  PublicacaoExemplar AS PublicacaoExemplar WITH (NOLOCK) WHERE PublicacaoExemplar.Situacao IN (1) AND PublicacaoExemplar.CodigoPublicacao = PublicacaoPesquisa.Codigo AND PublicacaoExemplar.MaterialApoio = 0) - (SELECT COUNT(*) FROM   Reserva_ListaEspera AS Reserva_ListaEspera WITH (NOLOCK) WHERE Reserva_ListaEspera.Baixa = 0 AND Reserva_ListaEspera.Reserva = 1 AND Reserva_ListaEspera.CodigoPublicacao = PublicacaoPesquisa.Codigo)) AS 'QtExemplaresLivres'
FROM PublicacaoPesquisa WITH (NOLOCK)
ORDER BY PublicacaoPesquisa.Titulo
```
