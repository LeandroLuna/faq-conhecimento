# Fluxo do Currículo Escolar Digital

## Visão Geral
O Fluxo do Currículo Escolar Digital é a primeira etapa do processo do Diploma Digital, desenvolvido para atender às novas normas do Ministério da Educação. Neste projeto, os currículos dos cursos de graduação da FIAP são cadastrados, seguindo as especificações solicitadas pelo MEC. A versão atual deste projeto é 1.05.

- Documentação do MEC: [Link para a documentação](http://portal.mec.gov.br/diplomadigital/?pagina=pacote-instituicoes) (A partir do Item 2.5)

**Observação:** [Todas as tabelas estão no banco **Educacional**]

## Funcionalidades Principais
1. Informações do Currículo [o Código do Currículo tem um padrão, veja no arquivo .txt abaixo]
Tabelas: CECurriculo e CEXMLInfCurriculo
<br>
    [Padrão Códigos Currículo](C%C3%93DIGO%20DO%20CURR%C3%8DCULO.txt)
    
2. Informações do Curso <br>
Tabelas: CursosCurriculoDigital e CEXMLDadosMinimoCurso

3. Informações da Emissora (FIAP) <br>
Tabela: CEXMLIesEmissora

4. Etiquetas <br>
Tabela: CEXMLEtiquetas

5. Estrutura Curricular [Disciplinas do Curso] <br>
Tabela: CEXMLEstruturaCurricular <br>
Procedure: SP_RetornaDisciplinasCursoCurriculoDigital

```sql
-- Script da Procedure para retornar os cursos

USE Educacional

IF EXISTS (SELECT * FROM sysobjects WHERE type = 'P' and name = 'SP_RetornaDisciplinasCursoCurriculoDigital')
	BEGIN
		PRINT 'Deletando procedure SP_RetornaDisciplinasCursoCurriculoDigital'
		DROP Procedure SP_RetornaDisciplinasCursoCurriculoDigital
	END
GO

PRINT 'Criando procedure SP_RetornaDisciplinasCursoCurriculoDigital'
GO
CREATE PROCEDURE SP_RetornaDisciplinasCursoCurriculoDigital
	@Sigla VARCHAR(3),
	@EAD BIT,
	@Ano INT,
	@Semestre INT,
	@Etapa INT,
	@QtdAnos INT
AS

DECLARE @AnoInicial INT, @AnoFinal INT

IF @Etapa > 1
BEGIN
	SET @AnoInicial = @Ano - (@Etapa-1)
END
ELSE
BEGIN
	SET @AnoInicial = @Ano
END

IF @QtdAnos > @Etapa
BEGIN
	SET @AnoFinal = @Ano + (@QtdAnos - @Etapa)
END
ELSE
BEGIN
	SET @AnoFinal = @Ano
END

PRINT @AnoInicial
PRINT @AnoFinal

SELECT
	Tabela.CodDisciplina as 'CodigoUnidadeCurricular',
	Tabela.Ano,
	Tabela.Etapa,
	Tabela.Disciplina as 'Nome',
	Tabela.CH as 'CargaHorariaEmRelogio',
	SUM(Tabela.CH) OVER (PARTITION BY Tabela.Etapa) as 'TotalCargaHorariaEtapa'
FROM
	(SELECT
		LEFT(RTRIM(LTRIM(Relacao_2004.Turma)), 1) AS 'Etapa',
		Relacao_2004.Ano,
		Relacao_2004.CodDisciplina,
		Disciplina_2004.Descricao AS 'Disciplina',
		Relacao_2004.CH
	FROM
		Site_Fiap..Relacao_2004 AS Relacao_2004 WITH (NOLOCK)
		INNER JOIN Site_Fiap..Disciplina_2004 AS Disciplina_2004 WITH (NOLOCK) ON
			Relacao_2004.CodDisciplina = Disciplina_2004.Codigo
	WHERE
		Relacao_2004.Ativo = 1
		AND Relacao_2004.NanoCourse = 0
		AND Relacao_2004.CodDisciplina <> 3701
		AND Relacao_2004.Unidade = 'F'
		AND Relacao_2004.Tipo = 'N'
		AND Relacao_2004.EAD100 = @EAD
		AND Relacao_2004.Turma LIKE CONCAT('_', @Sigla, '%')
		AND Relacao_2004.Ano BETWEEN @AnoInicial AND @AnoFinal
		AND Relacao_2004.SemestreInicio = @Semestre
	GROUP BY
		LEFT(RTRIM(LTRIM(Relacao_2004.Turma)), 1),
		Relacao_2004.Ano,
		Relacao_2004.CodDisciplina,
		Disciplina_2004.Descricao,
		Relacao_2004.CH) AS Tabela
	INNER JOIN (SELECT
					CLDiasUteis.Ano,
					ROW_NUMBER() OVER (ORDER BY CLDiasUteis.Ano) AS 'Etapa'
				FROM
					BaseEducacional..CLDiasUteis AS CLDiasUteis WITH (NOLOCK)
				WHERE
					CLDiasUteis.Mes = 1
					AND CLDiasUteis.Dia = 1
					AND CLDiasUteis.Ano BETWEEN @AnoInicial AND @AnoFinal) AS TabelaAnos ON
		Tabela.Ano = TabelaAnos.Ano
		AND Tabela.Etapa = TabelaAnos.Etapa
```

6. Critérios de Integralização <br>
Tabela: CEXMLCriteriosIntegralizacao

7. Tabela de Log do Currículo: CELogErro

## Arquitetura
Este projeto foi desenvolvido utilizando a técnica de Reflection e Attributes, com um modelo de CRUD Genérico.

#### UML 1 - Exemplos dos Dados
![UML 01](UML%2001%20-%20Curriculo%20Digital.png)

#### UML 2
![UML 02](UML%202%20-%20Curriculo%20Digital.png)

## Instalação
Certifique-se de ter as seguintes dependências instaladas:

- [API de Assinatura Digital Bry](https://gitlab.fiap.com.br/dotnet/Api.AssinaturaDigitalBry): Sistema responsável pela assinatura dos XMLs. É necessário que essa API esteja em execução para gerar o XML, porém o XML gerado não será assinado, pois requer um cartão físico que está disponível apenas para o Richard.
<br>
- [Intranet do Currículo Digital](https://gitlab.fiap.com.br/dotnet/intranet.curriculodigital): Front-End do sistema utilizado para criar os currículos.
<br>
- [API do Currículo Digital](https://gitlab.fiap.com.br/dotnet/api.curriculodigital): Back-End do sistema, chamado pela Intranet para realizar todas as funcionalidades do currículo.

## Uso
Para utilizar o projeto, siga as etapas abaixo:

1. Configure a Intranet no IIS para utilizar o layout da FIAP.
2. Precisa criar uma pasta no C:/ com o nome de 'Curriculos'