# Regex

Esta página tem como finalidade separar alguns REGEX úteis no dia a dia.

## RM

Verifica se é uma linha contendo um RM

```
^rm([0-9]{5,6})$
```

```
^([rR][mM])?([0-9]{5,6})$
```

## GUID - 128 bit

Verifica se está no formato de GUID utilizado pelas chaves de portais do aluno e integrações entre sistemas .NET

```
([0-9A-Fa-f]{8})-([0-9A-Fa-f]{4}-){3}([0-9A-Fa-f]{12}
```

## MD5

Verifica se uma determinada linha é uma hash MD5 sem os sinais de hífen. 

Exemplo de hash: **c20ad4d76fe97759aa27a0c99bff6710**

```
^[a-f0-9]{32}$
```

## E-mail

Verifica se um e-mail é válido ou não. 

Exemplo de e-mail válido: **vinicius.oliveira@fiap.com.br**

Exemplo de e-mail inválido: vínão.olivêira@fiap.com.br

```
^([\w-\.]+)@[a-z0-9]+\.[a-z]+(\.[a-z]+)?$
``` 

Para cenários mais completos e complexos como **algum+1@gmail.com** ou **email@dominio-com-hifen.com**, usar:

```
^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$
```


## Minificar código HTML

Usando o Replace (```Ctrl + R```) do PHPStorm com o Regex ativado, substitua:

- ```\n``` por ```" "``` - para tirar as quebras de linhas
    
- ```\s\s+``` por ```" "``` - para trocar dois ou mais espaços por somente um 
    
- ```>\s``` por ```>``` - para retirar espaços depois de fechar tags
    
- ```\s<``` por ```<``` - para retirar espaços antes de abrir tags


## Substituir font-family por variável de de font

Usando o Replace (```Ctrl + R```) do PHPStorm com o Regex ativado, substitua:

```
font: ([0-9a-zA-Z\/\s]*)([0-9a-zA-Z\/\s]\')
``` 

por
```
font: $1 $2 $Nome_da_font
``` 

## Nomes Completos

Verifica se é um nome completo válido ou não.

Exemplos de nome completo válido: **Kelvin Nobre Krull**

Exemplos de nome completo inválido: Kelvin

```
([A-zÀ-ú]+)(\s([A-zÀ-ú]+))+([A-zÀ-ú]+)
``` 

Para cenários mais completos e complexos como nomes com apóstrofo **'Luís d'Mendes Correia'** ou com hífen **Jean-Paul**, usar:

```
^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$
```
  
 
## Referências

[Wikipédia](https://pt.wikipedia.org/wiki/Express%C3%A3o_regular)

[REGEXR](https://regexr.com/)

[Regex101](https://regex101.com/)