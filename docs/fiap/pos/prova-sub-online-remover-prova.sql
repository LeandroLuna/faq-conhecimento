--Tiket 104206
/*
O aluno entrou em contato pois ao tentar acessar a prova apresentou o erro em anexo e finalizou mesmo sem ter acessado.
Poderia disponibilizar novamente a prova para o aluno por favor?
*/



--BKP Solicitacao
SELECT * FROM BaseEducacional..PTSolicitacao WHERE Codigo = 218221

--Voltando a solicitacao para pendente
UPDATE
	BaseEducacional..PTSolicitacao
SET
	DataHoraConclusao = NULL,
	CodigoUsuarioConclusao = NULL,
	CodigoTipoStatus = 1
WHERE 
	Codigo = 218221



--BKP das etapas da solicitacao
SELECT * FROM BaseEducacional..PTSolicitacaoEtapa WHERE CodigoSolicitacao = 218221

--Alterando a data de encerramento da etapa de pagamento para que aluno tenha mais 15 dias para realizar a prova
UPDATE
	BaseEducacional..PTSolicitacaoEtapa
SET
	DataHoraPegouResponsabilidade = GETDATE()
WHERE 
	CodigoSolicitacao = 218221
	AND CodigoTipoSolicitacaoEtapa = 355


--Alterando a etapa de liberar a prova para aguardando novamente
UPDATE
	BaseEducacional..PTSolicitacaoEtapa
SET
	Acao = '',
	DataHoraPegouResponsabilidade = NULL
WHERE 
	CodigoSolicitacao = 218221
	AND CodigoTipoSolicitacaoEtapa = 356


--Removendo a etapa de conclusão da prova
DELETE 
	BaseEducacional..PTSolicitacaoEtapa 
WHERE 
	CodigoSolicitacao = 218221
	AND CodigoTipoSolicitacaoEtapa = 357
 


--BKP do vinculo da prova
SELECT * FROM BaseEducacional..PTSolicitacaoRelacao WHERE CodigoSolicitacao = 218221

--Removendo o vinculo da prova
UPDATE
	BaseEducacional..PTSolicitacaoRelacao
SET
	CodigoPOProva = NULL
WHERE 
	CodigoSolicitacao = 218221