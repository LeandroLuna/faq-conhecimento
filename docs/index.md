# Introdução


## Base de Conhecimento e Documentação

Bem vindo à base de conhecimentos e documentação de software da FIAP, um ambiente ideal para compartilhar conhecimento entre os membros da equipe de TI da FIAP e também de outros departamentos.

## Como acessar?

Esse site está publicado no IIS da máquina de homologação `192.168.10.41`, escutando o domínio `conhecimento.fiap.com.br`

Adicionar ao hosts:
```
192.168.10.41   conhecimento.fiap.com.br
```

## Como a base funciona?

A base funciona utilizando o [mkdocs](http://www.mkdocs.org/), uma ferramenta que gera arquivos estáticos HTML com base em arquivos Markdown `.md`

O projeto está publicado no git, com integração contínua habilitada.

Todo commit que houver no projeto, a base será atualizada e publicada automaticamente.

## Como colaborar?

O projeto está no Git da FIAP, no grupo fiap sob o nome [base-de-conhecimento](https://gitlab.fiap.com.br/fiap/base-de-conhecimento).

Todos os documentos estão localizados na sub-pasta docs, e devem ser arquivos [Markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet).

Cada sub-pasta indica uma categoria, e podem haver hierarquias sobre as categorias, porém, como existe a busca, não é necessário se preocupar muito com as categorias.

O primeiro [heading](https://www.markdownguide.org/basic-syntax/#headings) do markdown será utilizado como título do arquivo.

É necessário ter o [Python](https://www.python.org/) instalado em seu sistema operacional e para conseguir compilar
este projeto deve-se instalar também o [tema Material](https://github.com/squidfunk/mkdocs-material) para o mkdocs utilizando o [pip](https://pypi.python.org/pypi/pip).

```
pip install mkdocs-material
```

## Mais informações
[Site oficial do mkdocs](http://www.mkdocs.org/)

[Github do mkdocs](https://github.com/mkdocs/mkdocs/)

[Github do tema Material](https://github.com/squidfunk/mkdocs-material)

[Outros temas para o mkdocs](https://github.com/mkdocs/mkdocs/wiki/MkDocs-Themes)
  
[Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)

[Site oficial do Python](https://www.python.org/)

[Site oficial do pip](https://pypi.python.org/pypi/pip)