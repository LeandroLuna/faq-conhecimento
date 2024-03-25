# Ficha de inscrição

Para que um aluno inicie uma pós na FIAP, seja MBA ou Pós Tech, ele deve se inscrever através de uma ficha de inscrição, selecionar
um curso e realizar uma auto avaliação, que dirá se ele está apto ou não a realizar o curso desejado. Caso ele seja aprovado na auto
avaliação, já pode iniciar a matrícula.

<div style="height:980px; overflow-x:scroll;">
    <img src="/processos/inscricao-pos/inscricao-pos.svg" style="max-width: initial;">
</div>
<sup> Processo <a href="http://conhecimento.fiap.com.br/processos/inscricao-pos/inscricao-pos/"> Inscrição pós </a> </sup>

## Preenchimento da ficha

<div style="height:370px; overflow-x:scroll;">
    <img src="/processos/inscricao-pos/preenchimento-ficha.svg" style="max-width: initial;">
</div>
<sup> Processo <a href="http://conhecimento.fiap.com.br/processos/inscricao-pos/preenchimento-ficha/"> Preenchimento ficha </a> </sup>

Como a etapa de preenchimento é comum entre os dois tipos de ficha (Inscrição e Entrevista), ao finalizar essa etapa, o usuário
tem o seu status e etapa atualizados para o próximo, conforme a ficha que está preenchendo.

Veja [aqui](http://conhecimento.fiap.com.br/fiap/pos/ficha-inscricao/#especificacoes-por-ficha) a ordem de status e etapas de acordo
com cada ficha.

## Seleção de cursos

Após realizar o preenchimento dos dados, o usuário deve selecionar um curso de sua preferência. Serão listados apenas cursos que estejam
abertos, independente do processo.

*Para MBA, não são listados cursos das unidades Corporate e On-line, mesmo que estejam abertos.*

<div style="height:370px; overflow-x:scroll;">
    <img src="/processos/inscricao-pos/selecao-curso.svg" style="max-width: initial;">
</div>
<sup> Processo <a href="http://conhecimento.fiap.com.br/processos/inscricao-pos/selecao-curso/"> Seleção de curso </a> </sup>

## Autoavaliações

As auto avaliações são provas que o usuário deve realizar para que se prove apto para iniciar o curso desejado. Elas são exibidas conforme
a turma selecionada, e possuem perguntas de múltipla escolha ou escolha única.

<div style="height:550px; overflow-x:scroll;">
    <img src="/processos/inscricao-pos/auto-avaliacao.svg" style="max-width: initial;">
</div>
<sup> Processo <a href="http://conhecimento.fiap.com.br/processos/inscricao-pos/auto-avaliacao/"> Auto avaliação </a> </sup>

Ao finalizar a auto avaliação, é chamada uma procedure para verificar se o usuário atingiu os requisitos necessários e a situação - aprovado
ou reprovado - é exibida para ele.

Para verificar a procedure utilizada pela auto avaliação, utilize a query abaixo:

```sql
USE webadm

SELECT
    pos_inscricao_turmas.Turma,
    PI_Avaliacao.Descricao,
    PI_Avaliacao.ProcedureAprovacao
FROM pos_inscricao_turmas
INNER JOIN PI_Avaliacao
    ON pos_inscricao_turmas.CodigoAvaliacao = PI_Avaliacao.Codigo
WHERE pos_inscricao_turmas.Turma = :sigla

```

## Entrevista

Para alunos do MBA, a opção de agendar uma entrevista com um coordenador é disponibilizada nos seguintes casos:

- Usuário não seja aprovado na auto avaliação;
- Turma selecionada pelo usuário não possui uma auto avaliação relacionada;
- Usuário realize a inscrição através da Ficha de Entrevista.

<div style="height:460px; overflow-x:scroll;">
    <img src="/processos/inscricao-pos/entrevista.svg" style="max-width: initial;">
</div>
<sup> Processo <a href="http://conhecimento.fiap.com.br/processos/inscricao-pos/entrevista/"> Entrevista </a> </sup>

Exemplo de chamada da procedure que lista os horários.

```sql
USE site_fiap

-- Caso deseje listar horários para usuários que realizaram a inscrição
-- através da ficha de entrevista, informe codigoCurso = -1

EXEC [dbo].[spHorariosEntrevista]
@CodigoCursoInscricao = :codigoCurso,
@Unidade = 'on-line'

```

*São listados apenas horários on-line de hoje + 2 dias até hoje + 35 dias. Ou seja, caso hoje seja dia 14/09, serão listados horários
do dia 16/09 até o dia 19/10.*

Caso o usuário não compareça no dia e horários marcados na entrevista, o status dele será alterado para 17 (pendente) pelo Job
**[Pós-Graduação] Volta entrevistas on-line que não aconteceram, para liberar reagendamento**. Este job roda diariamente no SQL Server e,
ao alterar o status, permite que ele reagende a entrevista ou refaça a auto avaliação caso deseje.

## Especificações por ficha

Cada tipo de ficha possui etapas e status específicos por quais um usuário irá passar até completá-la. Esses status e etapas servem para
localizar o usuário dentro da ficha e identificar quais ações ele pode - ou não - realizar, sempre seguindo a ordem.

Exemplo: Um usuário que está na Ficha de Inscrição do MBA, não pode realizar uma entrevista antes de realizar a auto avaliação, porém,
se esse mesmo usuário está na Ficha de Entrevista, essa ação é válida.

_A etapa e o status de um usuário pode ser consultado na tabela PI_InscricaoProcesso._

###Ficha de Entrevista MBA
**Ordem dos status**

- 28 - Pré inscrição
- 24 - Ficha incompleta
- 17 e 7 - Pendente e Entrevista

**Ordem das etapas**

- 1 - Ficha de inscrição
- 5 - Entrevista

###Ficha de Inscrição MBA
**Ordem dos status**

- 28 - Pré inscrição
- 24 - Ficha incompleta
- 37 - Avaliação
- 4 e 3 - Aprovado e Reprovado
- 17 e 7 - Pendente e Entrevista

**Ordem das etapas**

- 1 - Ficha de inscrição
- 2 - Seleção de curso
- 3 - Avaliação
- 4 - Matrícula
- 5 - Entrevista

###Ficha de Inscrição Pós Tech
**Ordem dos status**

- 28 - Pré inscrição
- 24 - Ficha incompleta
- 37 - Avaliação
- 4 e 3 - Aprovado e Reprovado
- 17 e 7 - Pendente e Entrevista

**Ordem das etapas**

- 1 - Ficha de inscrição
- 2 - Seleção de curso
- 3 - Avaliação
- 4 - Matrícula
- 6 - Contato

## Excluir testes realizados nos sistemas Ficha de Inscrição e Matrícula de MBA e Pós Tech

```sql
USE WebAdm
GO

DISABLE TRIGGER ALL 
ON PI_AgendaEntrevista
GO

DECLARE @TabelaInscricaoProcessoDeletar 
TABLE (CodigoInscricaoProcesso INT);

DECLARE @TabelaInscricaoDeletar 
TABLE (CodigoInscricao INT);

BEGIN TRY

	BEGIN TRANSACTION
	
	INSERT INTO @TabelaInscricaoProcessoDeletar 
		(CodigoInscricaoProcesso) 
	SELECT 
		Codigo 
	FROM 
		PI_InscricaoProcesso 
	WHERE 
		Codigo IN 
		(
			219278, 219280, 219281, 219282, 219283, 219284, 
			219285, 219286, 219287, 219290, 219291, 219292, 
			219293, 219311, 219324, 219325, 219329, 219331, 
			219333, 219335, 219336, 219339, 219340, 219342, 
			219343, 219344, 219346, 219348, 219349, 219350, 
			219351, 219354, 219355, 219357, 219358, 219361
		);
	
	DELETE 
		PI_AgendaEntrevistaIntegracaoMicrosoftTeams 
	WHERE 
		CodigoAgendaEntrevista IN 
		(
			SELECT 
				Codigo
			FROM 
				PI_AgendaEntrevista 
			WHERE 
				codigoInscricaoProcesso IN 
				(
					SELECT 
						CodigoInscricaoProcesso 
					FROM 
						@TabelaInscricaoProcessoDeletar
				)
		);

	DELETE 
		PI_AgendaEntrevista 
	WHERE 
		codigoInscricaoProcesso IN 
		(
			SELECT 
				CodigoInscricaoProcesso 
			FROM 
				@TabelaInscricaoProcessoDeletar
		);

	DELETE 
		PI_HistoricoInscricaoProcesso 
	WHERE 
		codigoInscricaoProcesso IN 
		(
			SELECT 
				CodigoInscricaoProcesso 
			FROM 
				@TabelaInscricaoProcessoDeletar
		);

	DELETE 
		PI_CursoEscolha 
	WHERE 
		codigoInscricaoProcesso IN 
		(
			SELECT 
				CodigoInscricaoProcesso 
			FROM 
				@TabelaInscricaoProcessoDeletar
		);

	DELETE 
		PI_AvaliacaoTentativaResposta 
	WHERE 
		CodigoAvaliacaoTentativa IN 
		(
			SELECT 
				Codigo 
			FROM 
				PI_AvaliacaoTentativa 
			WHERE 
				CodigoInscricaoProcesso IN 
				(
					SELECT 
						CodigoInscricaoProcesso 
					FROM 
						@TabelaInscricaoProcessoDeletar
				)
		);

	DELETE 
		PI_AvaliacaoTentativa 
	WHERE 
		CodigoInscricaoProcesso IN 
		(
			SELECT 
				CodigoInscricaoProcesso 
			FROM 
				@TabelaInscricaoProcessoDeletar
		);

	DELETE 
		PI_ContratoAntesConfirmacao 
	WHERE 
		CodigoInscricaoProcesso IN 
		(
			SELECT 
				CodigoInscricaoProcesso 
			FROM 
				@TabelaInscricaoProcessoDeletar
		);

	DELETE 
		PI_EscolhaMidia 
	WHERE 
		CodigoInscricaoProcesso IN 
		(
			SELECT 
				CodigoInscricaoProcesso 
			FROM 
				@TabelaInscricaoProcessoDeletar
		);

	DELETE 
		IntegracaoBraspag 
	WHERE 
		CodigoInscricaoProcesso IN 
		(
			SELECT 
				CodigoInscricaoProcesso 
			FROM 
				@TabelaInscricaoProcessoDeletar
		);

	DELETE 
		PI_ControleEnvioEmailMBA 
	WHERE 
		CodigoInscricaoProcesso IN 
		(
			SELECT 
				CodigoInscricaoProcesso 
			FROM 
				@TabelaInscricaoProcessoDeletar
		);

	DELETE 
		PI_ControleEnvioEmailPosTech 
	WHERE 
		CodigoInscricaoProcesso IN 
		(
			SELECT 
				CodigoInscricaoProcesso 
			FROM 
				@TabelaInscricaoProcessoDeletar
		);

	DELETE 
		BaseEducacional..CDDocumentoDigital 
	WHERE 
		Codigo IN 
		(
			SELECT 
				CodigoDocumentoDigital 
			FROM 
				pos_inscricao_contrato 
			WHERE 
				codigoInscricaoProcesso IN 
				(
					SELECT 
						CodigoInscricaoProcesso 
					FROM 
						@TabelaInscricaoProcessoDeletar
				) 
				AND CodigoDocumentoDigital IS NOT NULL 
			UNION
			SELECT 
				CodigoDocumentoDigitalAditivoContrato 
			FROM 
				pos_inscricao_contrato 
			WHERE 
				codigoInscricaoProcesso IN 
				(
					SELECT 
						CodigoInscricaoProcesso 
					FROM 
						@TabelaInscricaoProcessoDeletar
				) 
				AND CodigoDocumentoDigitalAditivoContrato IS NOT NULL 
			UNION
			SELECT 
				CodigoDocumentoDigitalAditivoModuloInternacional 
			FROM 
				pos_inscricao_contrato 
			WHERE 
				codigoInscricaoProcesso IN 
				(
					SELECT 
						CodigoInscricaoProcesso 
					FROM 
						@TabelaInscricaoProcessoDeletar
				) 
				AND CodigoDocumentoDigitalAditivoModuloInternacional IS NOT NULL 
			UNION
			SELECT 
				CodigoDocumentoDigitalAditivoShift 
			FROM 
				pos_inscricao_contrato 
			WHERE 
				codigoInscricaoProcesso IN 
				(
					SELECT 
						CodigoInscricaoProcesso 
					FROM 
						@TabelaInscricaoProcessoDeletar
				) 
				AND CodigoDocumentoDigitalAditivoShift IS NOT NULL 
			UNION
			SELECT 
				CodigoDocumentoDigitalRequerimento 
			FROM 
				pos_inscricao_contrato 
			WHERE 
				codigoInscricaoProcesso IN 
				(
					SELECT 
						CodigoInscricaoProcesso 
					FROM 
						@TabelaInscricaoProcessoDeletar
				) 
				AND CodigoDocumentoDigitalRequerimento IS NOT NULL 
			UNION
			SELECT 
				CodigoDocumentoDigital 
			FROM 
				pos_inscricao_contrato_cancelamento 
			WHERE 
				codigoInscricaoProcesso IN 
				(
					SELECT 
						CodigoInscricaoProcesso 
					FROM 
						@TabelaInscricaoProcessoDeletar
				) 
				AND CodigoDocumentoDigital IS NOT NULL 
			UNION
			SELECT 
				CodigoDocumentoDigitalAditivoContrato 
			FROM 
				pos_inscricao_contrato_cancelamento 
			WHERE 
				codigoInscricaoProcesso IN 
				(
					SELECT 
						CodigoInscricaoProcesso 
					FROM 
						@TabelaInscricaoProcessoDeletar
				) 
				AND CodigoDocumentoDigitalAditivoContrato IS NOT NULL 
			UNION
			SELECT 
				CodigoDocumentoDigitalAditivoModuloInternacional 
			FROM 
				pos_inscricao_contrato_cancelamento 
			WHERE 
				codigoInscricaoProcesso IN 
				(
					SELECT 
						CodigoInscricaoProcesso 
					FROM 
						@TabelaInscricaoProcessoDeletar
				) 
				AND CodigoDocumentoDigitalAditivoModuloInternacional IS NOT NULL 
			UNION
			SELECT 
				CodigoDocumentoDigitalAditivoShift 
			FROM 
				pos_inscricao_contrato_cancelamento 
			WHERE 
				codigoInscricaoProcesso IN 
				(
					SELECT 
						CodigoInscricaoProcesso 
					FROM 
						@TabelaInscricaoProcessoDeletar
				) 
				AND CodigoDocumentoDigitalAditivoShift IS NOT NULL 
			UNION
			SELECT 
				CodigoDocumentoDigitalRequerimento 
			FROM 
				pos_inscricao_contrato_cancelamento 
			WHERE 
				codigoInscricaoProcesso IN 
				(
					SELECT 
						CodigoInscricaoProcesso 
					FROM 
						@TabelaInscricaoProcessoDeletar
				) 
				AND CodigoDocumentoDigitalRequerimento IS NOT NULL
		);

	DELETE 
		ADControleDocumento 
	WHERE 
		RM IN 
		(
			SELECT 
				RM 
			FROM 
				pos_inscricao_contrato_cancelamento 
			WHERE 
				codigoInscricaoProcesso IN 
				(
					SELECT 
						CodigoInscricaoProcesso 
					FROM 
						@TabelaInscricaoProcessoDeletar
				)
		);

	DELETE 
		ADControleDocumento 
	WHERE 
		RM IN 
		(
			SELECT 
				RM 
			FROM 
				pos_inscricao_contrato 
			WHERE 
				codigoInscricaoProcesso IN 
				(
					SELECT 
						CodigoInscricaoProcesso 
					FROM 
						@TabelaInscricaoProcessoDeletar
				)
		);

	DELETE 
		BaseEducacional..FNBolsaDebitos 
	WHERE 
		CodigoBolsa IN 
		(
			SELECT 
				Codigo 
			FROM 
				BaseEducacional..FNBolsa 
			WHERE 
				RM IN 
				(
					SELECT 
						RM 
					FROM 
						pos_inscricao_contrato 
					WHERE 
						codigoInscricaoProcesso IN 
						(
							SELECT 
								CodigoInscricaoProcesso 
							FROM 
								@TabelaInscricaoProcessoDeletar
						)
				)
		);

	DELETE 
		BaseEducacional..FNBolsa 
	WHERE 
		RM IN 
		(
			SELECT 
				RM 
			FROM 
				pos_inscricao_contrato 
			WHERE 
				codigoInscricaoProcesso IN 
				(
					SELECT 
						CodigoInscricaoProcesso 
					FROM 
						@TabelaInscricaoProcessoDeletar
				)
		);

	DELETE 
		BaseEducacional..FNBolsaAplicada 
	WHERE 
		CodigoDebito IN 
		(
			SELECT 
				Codigo 
			FROM 
				BaseEducacional..FNDebitos 
			WHERE 
				RM IN 
				(
					SELECT 
						RM 
					FROM 
						pos_inscricao_contrato 
					WHERE 
						codigoInscricaoProcesso IN 
						(
							SELECT 
								CodigoInscricaoProcesso 
							FROM 
								@TabelaInscricaoProcessoDeletar
						)
				)
		);

	DELETE 
		BaseEducacional..CBDebitosAtrasados 
	WHERE 
		CodigoFNDebitos IN 
		(
			SELECT 
				Codigo 
			FROM 
				BaseEducacional..FNDebitos 
			WHERE 
				RM IN 
				(
					SELECT 
						RM 
					FROM 
						pos_inscricao_contrato 
					WHERE 
						codigoInscricaoProcesso IN 
						(
							SELECT 
								CodigoInscricaoProcesso 
							FROM 
								@TabelaInscricaoProcessoDeletar
						)
				)
		);

	DELETE 
		BaseEducacional..FNDebitos 
	WHERE 
		RM IN 
		(
			SELECT 
				RM 
			FROM 
				pos_inscricao_contrato 
			WHERE 
				codigoInscricaoProcesso IN 
				(
					SELECT 
						CodigoInscricaoProcesso 
					FROM 
						@TabelaInscricaoProcessoDeletar
				)
		);

	DELETE 
		pos_inscricao_contrato 
	WHERE 
		codigoInscricaoProcesso IN 
		(
			SELECT 
				CodigoInscricaoProcesso 
			FROM 
				@TabelaInscricaoProcessoDeletar
		);

	DELETE 
		BaseEducacional..FNBolsaDebitos 
	WHERE 
		CodigoBolsa IN 
		(
			SELECT 
				Codigo 
			FROM 
				BaseEducacional..FNBolsa 
			WHERE 
				RM IN 
				(
					SELECT 
						RM 
					FROM 
						pos_inscricao_contrato_cancelamento 
					WHERE 
						codigoInscricaoProcesso IN 
						(
							SELECT 
								CodigoInscricaoProcesso 
							FROM 
								@TabelaInscricaoProcessoDeletar
						)
				)
		);

	DELETE 
		BaseEducacional..FNBolsa 
	WHERE 
		RM IN 
		(
			SELECT 
				RM 
			FROM 
				pos_inscricao_contrato_cancelamento 
			WHERE 
				codigoInscricaoProcesso IN 
				(
					SELECT 
						CodigoInscricaoProcesso 
					FROM 
						@TabelaInscricaoProcessoDeletar
				)
		);

	DELETE 
		BaseEducacional..FNBolsaAplicada 
	WHERE 
		CodigoDebito IN 
		(
			SELECT 
				Codigo 
			FROM 
				BaseEducacional..FNDebitos 
			WHERE 
				RM IN 
				(
					SELECT 
						RM 
					FROM 
						pos_inscricao_contrato_cancelamento 
					WHERE 
						codigoInscricaoProcesso IN 
						(
							SELECT 
								CodigoInscricaoProcesso 
							FROM 
								@TabelaInscricaoProcessoDeletar
						)
				)
		);

	DELETE 
		BaseEducacional..CBDebitosAtrasados 
	WHERE 
		CodigoFNDebitos IN 
		(
			SELECT 
				Codigo 
			FROM 
				BaseEducacional..FNDebitos 
			WHERE 
				RM IN 
				(
					SELECT 
						RM 
					FROM 
						pos_inscricao_contrato_cancelamento 
					WHERE 
						codigoInscricaoProcesso IN 
						(
							SELECT 
								CodigoInscricaoProcesso 
							FROM 
								@TabelaInscricaoProcessoDeletar
						)
				)
		);
		
	DELETE 
		BaseEducacional..FNDebitos 
	WHERE 
		RM IN 
		(
			SELECT 
				RM 
			FROM 
				pos_inscricao_contrato_cancelamento 
			WHERE 
				codigoInscricaoProcesso IN 
				(
					SELECT 
						CodigoInscricaoProcesso 
					FROM 
						@TabelaInscricaoProcessoDeletar
				)
		);

	DELETE 
		pos_inscricao_contrato_cancelamento 
	WHERE 
		codigoInscricaoProcesso IN 
		(
			SELECT 
				CodigoInscricaoProcesso 
			FROM 
				@TabelaInscricaoProcessoDeletar
		);

	
	INSERT INTO @TabelaInscricaoDeletar 
		(CodigoInscricao) 
	SELECT 
		PI_InscricaoProcesso.codigoInscricao 
	FROM 
		PI_InscricaoProcesso 
	WHERE 
		Codigo IN 
		(
			SELECT 
				CodigoInscricaoProcesso 
			FROM 
				@TabelaInscricaoProcessoDeletar
		) 
		AND NOT EXISTS
		(
			SELECT 
				* 
			FROM 
				PI_InscricaoProcesso AS PI_InscricaoProcesso2 
			WHERE 
				PI_InscricaoProcesso2.codigoProcesso <> PI_InscricaoProcesso.codigoProcesso 
				AND PI_InscricaoProcesso2.codigoInscricao = PI_InscricaoProcesso.codigoInscricao
		);

	DELETE 
		PI_OrigemInscricaoMatricula 
	WHERE 
		codigoInscricaoProcesso IN 
		(
			SELECT 
				CodigoInscricaoProcesso 
			FROM 
				@TabelaInscricaoProcessoDeletar
		)

	DELETE 
		PI_InscricaoProcesso 
	WHERE 
		Codigo IN 
		(
			SELECT 
				CodigoInscricaoProcesso 
			FROM 
				@TabelaInscricaoProcessoDeletar
		);

	DELETE 
		PI_Cadastro 
	WHERE 
		codigoInscricao IN 
		(
			SELECT 
				CodigoInscricao 
			FROM 
				@TabelaInscricaoDeletar
		);

	DELETE 
		Pos_Inscricao_New 
	WHERE 
		Codigo IN 
		(
			SELECT 
				CodigoInscricao 
			FROM 
				@TabelaInscricaoDeletar
		);

	COMMIT TRANSACTION

END TRY
BEGIN CATCH
	SELECT
		ERROR_LINE() AS 'LINE',
		ERROR_MESSAGE() AS 'MESSAGE',
		ERROR_NUMBER() AS 'NUMBER',
		ERROR_PROCEDURE() AS 'PROCEDURE',
		ERROR_SEVERITY() AS 'SEVERITY',
		ERROR_STATE() AS 'STATE';

	ROLLBACK TRANSACTION
END CATCH
GO

ENABLE TRIGGER ALL 
ON PI_AgendaEntrevista;
```
