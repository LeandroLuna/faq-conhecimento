### Gerar débitos de seguro desemprego fora da regra do sistema

Algumas vezes se faz necessário abrir exceções para alguns alunos que pedem para ter o benefício do seguro desemprego em parcelas que estão vencidas e não entram na regra do sistema e a gerencia do financeiro acaba acatando o pedido e autoriza a geração desses débitos, para realizar o lançamento desses novos débitos de seguro desemprego basta usar o script abaixo:

???- note "gerar-debitos-seguro-desemprego.sql"
	```sql hl_lines="7 8 16 20 21 25 26"
	USE BaseEducacional
	GO
	SET NOCOUNT ON
	GO
	DECLARE @CodigoDebito INT, @CodigoDebitoNovo INT, @MesInicio SMALLINT, @AnoInicio INT, @DataVencimentoNovo DATE, @DataDescontoNovo DATE, @Agrupador CHAR(32)
	--Sempre informar qual é o mês e ano de inicio do seguro desemprego
	SET @MesInicio = 7
	SET @AnoInicio = 2014
	SET @Agrupador = REPLACE(NEWID(), '-', '')
	--Sempre mudar a condição para pegar as mensalidades que serão feitas os seguro desemprego
	DECLARE Ponteiro CURSOR FOR SELECT 
									FNDebitos.Codigo
								FROM 
									FNDebitos 
								WHERE 
									RM = 70552 
									AND 
									(
										(
											Mes = 13 
											AND Ano = 2013
										)
										OR 
										(
											Mes IN (2, 3)
											AND Ano = 2014
										)
									)
	OPEN Ponteiro
	FETCH NEXT FROM Ponteiro INTO @CodigoDebito
	WHILE @@FETCH_STATUS = 0
	BEGIN
		SET @DataDescontoNovo = BaseEducacional.Dbo.fnRetornaDiaUtilFinanceiro(CAST(@AnoInicio AS VARCHAR) + RIGHT('00' + CAST(@MesInicio AS VARCHAR), 2) + '05')
		SET @DataVencimentoNovo = BaseEducacional.Dbo.fnRetornaDiaUtilFinanceiro(CAST(@AnoInicio AS VARCHAR) + RIGHT('00' + CAST(@MesInicio AS VARCHAR), 2) + '15')

		INSERT INTO FNDebitos (Tipo, 
								AgrupadorDebito, 	
								RM, 	
								Nser, 	
								LSer, 	
								LCur, 	
								Per, 	
								SemAno, 	
								Con, 	
								MesAnoEvd, 	
								Externa, 	
								SPC, 	
								DataHoraEntrouSPC, 	
								DP, 	
								Adap, 	
								CodigoTabelaValor, 	
								CodigoTabelaValorVencimento, 	
								TaxaMulta, 	
								TaxaJuros, 	
								TabPreco, 	
								Plano, 	
								Bolsa, 	
								ParcelaComplemento, 	
								Mes, 	
								Ano, 	
								ValorCheioNominal, 	
								ValorDescontoNominal, 	
								DataVencimentoPadrao, 	
								DataDescontoPadrao, 	
								ValorCheioDebito, 	
								ValorDescontoDebito, 	
								ValorJuros, 	
								ValorMulta, 	
								DataVencimentoDebito, 	
								DataDescontoDebito, 	
								DataVencimento, 	
								ValorDebito, 	
								ValorPago, 	
								DataPagamento, 	
								DataOutLan, 	
								DataAtualizado, 	
								QtDiasAtrasado, 	
								UsoEmpresa, 	
								NossoNumero, 	
								NumDoc, 	
								CodigoNegociacao, 	
								CodigoPessoaRespFinanceiro, 	
								DataHoraCadastro, 	
								CodigoUsuarioCadastro, 	
								Excluido, 	
								Abonado, 	
								DataHoraAbono, 	
								DebitoEmAcordo, 	
								CodigoUsuarioAbono, 	
								CPFResponsavel, 	
								DescricaoDebito, 	
								Visivel, 	
								MotivoExclusao, 	
								MotivoAbono, 	
								CodigoBMRemessa, 	
								CodigoArquivoRetornoBancoRegistro, 	
								ValidadoBaixa, 	
								DataHoraValidadoBaixa, 	
								MotivoAlteracaoDataVencimento, 	
								DataHoraAlteracaoDataVencimento, 	
								CodigoUsuarioAlteracaoDataVencimento, 	
								RecalculouMultaJuros, 	
								Controle, 	
								IDDebito, 	
								Bolsa1, 	
								Motivo1, 	
								Bolsa2, 	
								Motivo2, 	
								Bolsa3, 	
								Motivo3, 	
								Bolsa4, 	
								Motivo4, 	
								Bolsa5, 	
								Motivo5, 	
								CodigoBaixaAvulso, 	
								CodigoContaCorrente, 	
								CodigoLogCriacao, 	
								OrgaoSPC, 	
								DataNovoVencimento, 	
								OpcaoSelecionadaAlteraDataVencimento, 	
								CodigoFNRecebimento, 	
								ValorAcrescimo, 	
								DescricaoValorAcrescimo, 	
								ValorDeducao, 	
								DescricaoValorDeducao, 	
								DataHoraEstorno, 	
								MotivoEstorno, 	
								CodigoUsuarioEstorno, 	
								NRPS, 	
								AnoReferencia) 
		SELECT
			'Seguro Desemprego' AS 'Tipo', 
			@Agrupador AS 'AgrupadorDebito', 
			RM, 
			Nser, 
			LSer, 
			LCur, 
			Per, 
			SemAno, 
			'A' AS 'Con', 
			NULL AS 'MesAnoEvd', 
			NULL AS 'Externa', 
			0 AS 'SPC', 
			NULL AS 'DataHoraEntrouSPC', 
			DP, 
			Adap, 
			CodigoTabelaValor, 
			CodigoTabelaValorVencimento, 
			TaxaMulta, 
			TaxaJuros, 
			TabPreco, 
			Plano, 
			Bolsa, 
			ParcelaComplemento, 
			@MesInicio AS 'Mes', 
			@AnoInicio AS 'Ano', 
			ValorCheioNominal, 
			ValorDescontoNominal, 
			@DataVencimentoNovo AS 'DataVencimentoPadrao', 
			@DataDescontoNovo AS 'DataDescontoPadrao', 
			ValorCheioNominal AS 'ValorCheioDebito', 
			ValorDescontoNominal AS 'ValorDescontoDebito', 
			NULL AS 'ValorJuros', 
			NULL AS 'ValorMulta', 
			@DataVencimentoNovo AS 'DataVencimentoDebito', 
			@DataDescontoNovo AS 'DataDescontoDebito', 
			@DataDescontoNovo AS 'DataVencimento', 
			ValorDescontoNominal AS 'ValorDebito', 
			NULL AS 'ValorPago', 
			NULL AS 'DataPagamento', 
			NULL AS 'DataOutLan', 
			GETDATE() AS 'DataAtualizado', 
			0 AS 'QtDiasAtrasado', 
			NULL AS 'UsoEmpresa', 
			NULL AS 'NossoNumero', 
			NumDoc, 
			NULL AS 'CodigoNegociacao', 
			NULL AS 'CodigoPessoaRespFinanceiro', 
			GETDATE() AS 'DataHoraCadastro', 
			1 AS 'CodigoUsuarioCadastro', 
			0 AS 'Excluido', 
			0 AS 'Abonado', 
			NULL AS 'DataHoraAbono', 
			0 AS 'DebitoEmAcordo', 
			NULL AS 'CodigoUsuarioAbono', 
			CPFResponsavel, 
			'Seguro desemprego mensalidade ' + RIGHT('00' + CAST(Mes AS VARCHAR), 2) + '/' + CAST(Ano AS VARCHAR) + ' - Cód. ' + CAST(Codigo AS VARCHAR) AS 'DescricaoDebito', 
			1 AS 'Visivel', 
			NULL AS 'MotivoExclusao', 
			NULL AS 'MotivoAbono', 
			NULL AS 'CodigoBMRemessa', 
			NULL AS 'CodigoArquivoRetornoBancoRegistro', 
			0 AS 'ValidadoBaixa', 
			NULL AS 'DataHoraValidadoBaixa', 
			NULL AS 'MotivoAlteracaoDataVencimento', 
			NULL AS 'DataHoraAlteracaoDataVencimento', 
			NULL AS 'CodigoUsuarioAlteracaoDataVencimento', 
			0 AS 'RecalculouMultaJuros', 
			Controle, 
			IDDebito, 
			Bolsa1, 
			Motivo1, 
			Bolsa2, 
			Motivo2, 
			Bolsa3, 
			Motivo3, 
			Bolsa4, 
			Motivo4, 
			Bolsa5, 
			Motivo5, 
			NULL AS 'CodigoBaixaAvulso', 
			NULL AS 'CodigoContaCorrente', 
			NULL AS 'CodigoLogCriacao', 
			NULL AS 'OrgaoSPC', 
			NULL AS 'DataNovoVencimento', 
			NULL AS 'OpcaoSelecionadaAlteraDataVencimento', 
			NULL AS 'CodigoFNRecebimento', 
			ValorAcrescimo, 
			DescricaoValorAcrescimo, 
			ValorDeducao, 
			DescricaoValorDeducao, 
			NULL AS 'DataHoraEstorno', 
			NULL AS 'MotivoEstorno', 
			NULL AS 'CodigoUsuarioEstorno', 
			NULL AS 'NRPS', 
			NULL AS 'AnoReferencia'
		FROM 
			FNDebitos 
		WHERE 
			Codigo = @CodigoDebito

		SET @CodigoDebitoNovo = @@IDENTITY
		
		EXEC spAtualizaDebito @Codigo = @CodigoDebitoNovo
		
		UPDATE FNDebitos SET Visivel = 0, Excluido = 1 WHERE Codigo = @CodigoDebito

		SET @MesInicio = @MesInicio + 1
		IF @MesInicio = 14
		BEGIN
			SET @MesInicio = 2
			SET @AnoInicio = @AnoInicio + 1
		END
		FETCH NEXT FROM Ponteiro INTO @CodigoDebito
	END
	CLOSE Ponteiro
	DEALLOCATE Ponteiro
	GO
	SET NOCOUNT OFF
	```

!!! warning "Atenção"
    Fique atento nos comentários do script, pois tem algumas variaveis que precisam ter os seus valores alteradas e a select que retorna os débitos que serão convertidos em seguro desemprego é necessário alterar a condição do **WHERE**.
