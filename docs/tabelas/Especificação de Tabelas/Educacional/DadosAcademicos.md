# Dados Acadêmicos de Graduação e FIAP School

!!! info "Última modificação"
    **28-11-2023**   Victor Alves Bugueno

Tabelas utilizadas para armazenar os __dados acadêmicos__ dos alunos de
__Graduação e FIAP School__.
Estas tabelas são utilizadas, tanto em sistemas da
Intranet3
quanto da
IntranetNova

!!! warning "Atenção"
    A grande maioria das tabelas do banco **Educacional** não possuem o **Codigo** 
    como **IDENTITY**, além de possuir colunas de controle, como **StatusRegistro**, 
    **Deletado**, **DataStatusInformacao** e **Identificador**. 

    Para mais informações, acesse a 
    [Documentação Completa](TabelasColunasControle.md).

## Tabelas

**Educacional..TipoStatus**: Lista de status dos alunos, como Ativo,
Desistente, Trancado, etc;

```sql {"id":"01HGB9THDJ27FAPHZZ5QGKYKFF"}
SELECT
	Codigo,
	Descricao,
	*
FROM
	Educacional..TipoStatus WITH (NOLOCK)
WHERE
	Deletado = 0
	AND StatusRegistro = 1;
/*
Codigo  Descricao        
1       Ativo            
8       Pré-Matriculado  
2       Desistente       
3       Cancelado        
(...)
*/

```

**Educacional..Pessoa**: Dados pessoais dos alunos, como nome, CPF, endereço,
etc;

```sql {"id":"01HGB9THDJ27FAPHZZ5SC9W1VN"}
SELECT
	Codigo,
	Nome,
	*
FROM
	Educacional..Pessoa WITH (NOLOCK)
WHERE
	Deletado = 0
	AND StatusRegistro = 1
	AND Nome LIKE 'Victor%Alves%Bug%';
/*
Codigo  Nome                  
230981  Victor Alves Bugueno  
187914  Victor Alves Bugueno  
162733  Victor Alves Bugueno  
226389  Victor Alves Bugueno  
163095  Victor Alves Bugueño  
*/

```

**Educacional..Aluno**: Pessoas vinculadas a determinada modalidade de curso,
como Graduação ou FIAP School, relacionada com um RM;

```sql {"id":"01HGB9THDJ27FAPHZZ5XBD74QC"}
SELECT
	Codigo,
	CodigoPessoa,
	RM,
	CodigoTipoStatus,
	*
FROM
	Educacional..Aluno WITH (NOLOCK)
WHERE
	Deletado = 0
	AND StatusRegistro = 1
	AND CodigoPessoa IN 
	(
		230981,
		187914,
		162733,
		226389,
		163095
	)
/*
Codigo  CodigoPessoa  RM      CodigoTipoStatus  
52040   163095        77816   1                 
83056   226389        344690  1                 
85372   230981        345763  1                 
*/

```

**Educacional..AlunoTurma**: Alunos vinculados às turmas de cada ano letivo;

```sql {"id":"01HGB9THDJ27FAPHZZ60Y7TZ5A"}
SELECT
	*
FROM
	Educacional..AlunoTurma WITH (NOLOCK)
WHERE
	Deletado = 0
	AND StatusRegistro = 1
	AND CodigoAluno IN 
	(
		52040,
		83056,
		85372
	)
/*
Codigo  CodigoRelacao  CodigoAluno  CodigoTipoStatus  
71008   6451           52040        6                 
71569   6561           52040        1                 
81477   6861           52040        1                 
88383   7121           52040        1                 
99174   7414           52040        1                 
106930  7736           52040        1                 
*/

```

**Educacional..Relacao**: Turmas relacionadas aos anos letivos;

```sql {"id":"01HGB9THDJ27FAPHZZ62W28KJ1"}
SELECT
	Codigo,
	Ano,
	Periodo,
	Turma,
	Vagas,
	VagasUtilizadasMatricula,
	Unidade,
	*
FROM
	Educacional..Relacao WITH (NOLOCK)
WHERE
	Codigo IN
	(
		6451,
		6561,
		6861,
		7121,
		7414,
		7736
	)
/*
Codigo  Ano   Periodo  Turma  Vagas  VagasUtilizadasMatricula  Unidade    
6451    2017  M        1SIA   50     48                        Aclimação  
6561    2017  M        1EMA   50     20                        Aclimação  
6861    2018  M        2EMA   50     22                        Aclimação  
7121    2019  N        3EMR   50     26                        Aclimação  
7414    2020  N        4EMR   50     25                        Aclimação  
7736    2021  N        5EMR   50     26                        Aclimação  
*/

```

Relação entre as tabelas e exibição dos principais dados:

```sql {"id":"01HGB9THDJ27FAPHZZ63Z18K3B"}
SELECT
	Pessoa.Nome,
	Pessoa.CPF,
	Aluno.RM,
	TipoStatus.Descricao,
	Relacao.Ano,
	Relacao.Turma,
	*
FROM
	Educacional..Pessoa
	INNER JOIN Educacional..Aluno
		ON aluno.CodigoPessoa = Pessoa.Codigo
	INNER JOIN Educacional..AlunoTurma
		ON Aluno.Codigo = AlunoTurma.CodigoAluno
	INNER JOIN Educacional..TipoStatus
		ON TipoStatus.Codigo = AlunoTurma.CodigoTipoStatus
	INNER JOIN Educacional..Relacao
		ON Relacao.Codigo = AlunoTurma.CodigoRelacao
WHERE
	RM = 77816
ORDER BY
	AlunoTurma.DataStatusInformacao
/*
Nome                  CPF          RM     Descricao            Ano   Turma  
Victor Alves Bugueño  47529280864  77816  Transferido - Curso  2017  1SIA   
Victor Alves Bugueño  47529280864  77816  Ativo                2017  1EMA   
Victor Alves Bugueño  47529280864  77816  Ativo                2018  2EMA   
Victor Alves Bugueño  47529280864  77816  Ativo                2019  3EMR   
Victor Alves Bugueño  47529280864  77816  Ativo                2020  4EMR   
Victor Alves Bugueño  47529280864  77816  Ativo                2021  5EMR   
*/

```
