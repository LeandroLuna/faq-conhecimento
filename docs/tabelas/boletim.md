#Boletim

##Graduação Presencial e On-line
Conecte-se ao banco Educacional e execute o seguinte comando:

```sql
SET @rm = <rm_aqui>;

SELECT *
FROM LancamentoNotasFiap
WHERE LancamentoNotasFiap.rm = @rm
	AND LancamentoNotasFiap.cond = 'A';
```

As notas da Graduação On-line da coluna "AD" dessa tabela, são uma soma das notas que estão armazenadas
na tabela "LancamentoNacFiap". Para visualizá-las, execute o seguinte comando:

```sql
SET @rm = <rm_aqui>;

SELECT *
FROM LancamentoNacFiap
WHERE LancamentoNacFiap.rm = @rm;
```

##MBA Presencial
Conecte-se ao banco site_fiap e execute o seguinte comando:

```sql
SET @rm = <rm_aqui>;

SELECT *
FROM BoletimPosLancamento
WHERE BoletimPosLancamento.rm = @rm
	AND BoletimPosLancamento.ativo = 1;
```

##MBA On-line
Conecte-se ao banco site_fiap e execute o seguinte comando:

```sql
SET @rm = <rm_aqui>;

SELECT *
FROM BoletimPosLancamentoOnLine
WHERE BoletimPosLancamentoOnLine.rm = @rm;
```

##PWC (MBA Híbrido)
Alunos de PWC consomem os conteúdos do curso de modo On-Line - pela plataforma -
porém possuem o boletim de forma presencial (por isso o nome MBA Híbrido).

Para consultar as notas desses alunos, conecte-se ao banco site_fiap e execute
o seguinte comando:

```sql
SET @rm = <rm_aqui>;

SELECT *
FROM BoletimPosLancamento
WHERE BoletimPosLancamento.rm = @rm
	AND BoletimPosLancamento.ativo = 1;
```