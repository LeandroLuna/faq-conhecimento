# Pessoa Juridica

### Cadastrar empresa como responsavel de um aluno

Basta preencher os valores das variaveis e executar o script abaixo

```sql
USE webadm
GO
DECLARE @RMAluno INT, @CodigoInscricaoProcesso INT, @CodigoInscricao INT, @RazaoSocial VARCHAR(255), @CNPJ VARCHAR(14), @InscricaoEstadual VARCHAR(20), @Logradouro VARCHAR(255), @Numero VARCHAR(50), @Complemento VARCHAR(50), @Bairro VARCHAR(255), @Cidade VARCHAR(255), @Estado CHAR(2), @Cep VARCHAR(50), @Nome VARCHAR(225), @RG VARCHAR(50), @Turma VARCHAR(10), @Plano INT, @Bolsa FLOAT, @CodigoInscricaoProcessoPessoaJuridica INT, @RMEmpresa INT, @BolsaAluno FLOAT, @CodigoDebitoMatriculaEmpresa INT, @DataBase DATE, @CodigoFNDebito INT
SET @RMAluno = 332799
SET @RazaoSocial = 'Feso Fundação Educacional Serra dos Orgãos'
SET @CNPJ = '32190092000106'
SET @InscricaoEstadual = ''
SET @Logradouro = 'Avenida Alberto Torres'
SET @Numero ='111'
SET @Complemento = ''
SET @Bairro = 'Alto'
SET @Cidade = 'Teresopolis'
SET @Estado = 'RJ'
SET @Cep = '25964004'
SET @Nome = ''
SET @RG = ''
SET @Plano = 24
SET @Bolsa = 10
SET @BolsaAluno = 100
SET @DataBase = CONVERT(DATE, GETDATE())
IF EXISTS(SELECT * FROM Pos_Inscricao_Contrato WHERE RM = @RMAluno)
BEGIN
	SELECT @CodigoInscricaoProcesso = codigoInscricaoProcesso, @CodigoInscricao = codigoInscricao, @Turma = Turma FROM Pos_Inscricao_Contrato WHERE RM = @RMAluno
	INSERT INTO PI_InscricaoProcessoPessoaJuridica (codigoInscricaoProcesso, codigoInscricao, RazaoSocial, CNPJ, InscricaoEstadual, Logradouro, Numero, Complemento, Bairro, Cidade, Estado, CEP, Nome, RG, Turma, Plano, Bolsa) VALUES (@CodigoInscricaoProcesso, @CodigoInscricao, @RazaoSocial, @CNPJ, @InscricaoEstadual, @Logradouro, @Numero, @Complemento, @Bairro, @Cidade, @Estado, @Cep, @Nome, @RG, @Turma, @Plano, @Bolsa)
	SET @CodigoInscricaoProcessoPessoaJuridica = @@IDENTITY
	SET @RMEmpresa = WebAdm.Dbo.pegarm()
	PRINT 'RM da empresa: ' + CAST(@RMEmpresa AS VARCHAR)
	INSERT INTO pos_inscricao_contrato (DataHora, RM, Turma, Plano, Bolsa, DocRg, docCpf, docComprovanteResidencia, doc2Fotos3X4, docCurriculumVitae, docHistoricoEscolar, docDiplomaCertificado, docCartaMotivacao, empresa, codigoUsuarioCadastro, codigoPessoaJuridica, docCertificadoConclusao, docTermoWireless, docVinculoEmpresa, PgtoInicioCurso, ConfirmouContratoAssinado, ConfirmouFotoAluno, ConfirmouComprovanteRG, ConfirmouComprovanteCPF, ConfirmouComprovanteResidencia, ConfirmouHistoricoEscolar, ConfirmouCertificadoConclusao, CodStatusMatriculaOnline, BloqueioEmailContrato, LiberaMatriculaOnline, ConfirmouTermoWifi, docTermoWifi, ConfirmouTermoCiencia, docTermoCiencia, ConfirmouRequerimentoMatricula, docRequerimentoMatricula, ConfirmouAditivoShift, ConfirmouAditivoModuloInternacional, ConfirmouDiplomaCertificado, CodStatusDocumentos, ConfirmouComprovanteEmpresaConveniada, docComprovanteEmpresaConveniada, MatriculaOnLine) VALUES (GETDATE(), @RMEmpresa, @Turma, @Plano, @Bolsa, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, @CodigoInscricaoProcessoPessoaJuridica, 0, 0, 0, 'N', 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0)
	SELECT @CodigoDebitoMatriculaEmpresa = CodigoFNDebitos FROM pos_inscricao_contrato WHERE RM = @RMEmpresa
	UPDATE BaseEducacional..FNDebitos SET Abonado = 1, MotivoAbono = 'RM de empresa', DataHoraAbono=GETDATE(), CodigoUsuarioAbono = 1 WHERE Codigo = @CodigoDebitoMatriculaEmpresa
	UPDATE BaseEducacional..FNDebitos SET CPFResponsavel = @CNPJ WHERE RM = @RMEmpresa
	UPDATE Pos_Inscricao_Contrato SET Bolsa = @BolsaAluno, codigoPessoaJuridica = @CodigoInscricaoProcessoPessoaJuridica WHERE RM = @RMAluno
	UPDATE BaseEducacional..FNDebitos SET Bolsa = @BolsaAluno WHERE RM = @RMAluno AND Tipo = 'Mensalidade' AND ValorPago IS NULL AND Abonado = 0 AND Visivel = 1 AND Excluido = 0 AND CONVERT(INT, CONVERT(VARCHAR, Ano) + RIGHT('00' + CONVERT(VARCHAR, Mes), 2)) >= CONVERT(INT, CONVERT(VARCHAR, YEAR(@DataBase)) + RIGHT('00' + CONVERT(VARCHAR, MONTH(@DataBase)), 2))
	DELETE BaseEducacional..FNBolsaAplicada WHERE CodigoDebito IN (SELECT Codigo FROM BaseEducacional..FNDebitos WHERE RM = @RMAluno AND Tipo = 'Mensalidade' AND ValorPago IS NULL AND Abonado = 0 AND Visivel = 1 AND Excluido = 0 AND CONVERT(INT, CONVERT(VARCHAR, Ano) + RIGHT('00' + CONVERT(VARCHAR, Mes), 2)) >= CONVERT(INT, CONVERT(VARCHAR, YEAR(@DataBase)) + RIGHT('00' + CONVERT(VARCHAR, MONTH(@DataBase)), 2)))
	INSERT INTO BaseEducacional..FNBolsaAplicada (CodigoTipoBolsa, CodigoDebito, Porcentagem) SELECT 37, Codigo, @BolsaAluno FROM BaseEducacional..FNDebitos WHERE RM = @RMAluno AND Tipo = 'Mensalidade' AND ValorPago IS NULL AND Abonado = 0 AND Visivel = 1 AND Excluido = 0 AND CONVERT(INT, CONVERT(VARCHAR, Ano) + RIGHT('00' + CONVERT(VARCHAR, Mes), 2)) >= CONVERT(INT, CONVERT(VARCHAR, YEAR(@DataBase)) + RIGHT('00' + CONVERT(VARCHAR, MONTH(@DataBase)), 2))
	DECLARE Ponteiro CURSOR FOR SELECT Codigo FROM BaseEducacional..FNDebitos WHERE RM = @RMAluno AND Tipo = 'Mensalidade' AND ValorPago IS NULL AND Abonado = 0 AND Visivel = 1 AND Excluido = 0 AND CONVERT(INT, CONVERT(VARCHAR, Ano) + RIGHT('00' + CONVERT(VARCHAR, Mes), 2)) >= CONVERT(INT, CONVERT(VARCHAR, YEAR(@DataBase)) + RIGHT('00' + CONVERT(VARCHAR, MONTH(@DataBase)), 2))
	OPEN Ponteiro
	FETCH NEXT FROM Ponteiro INTO @CodigoFNDebito
	WHILE @@FETCH_STATUS = 0
	BEGIN
		EXEC BaseEducacional..spAtualizaDebito @Codigo = @CodigoFNDebito
		FETCH NEXT FROM Ponteiro INTO @CodigoFNDebito
	END
	CLOSE Ponteiro
	DEALLOCATE Ponteiro
	SELECT
		*
	FROM
		(SELECT
			'Aluno' AS 'Tipo',
			Pos_Inscricao_Contrato.RM,
			POs_Inscricao_New.Nome COLLATE Latin1_General_CI_AI AS 'Nome'
		FROM
			Pos_Inscricao_Contrato
			INNER JOIN POs_Inscricao_New ON
				Pos_Inscricao_Contrato.codigoInscricao = POs_Inscricao_New.Codigo
		WHERE
			Pos_Inscricao_Contrato.RM = @RMAluno
		UNION
		SELECT
			'Empresa' AS 'Tipo',
			Pos_inscricao_Contrato.RM,
			PI_InscricaoProcessoPessoaJuridica.RazaoSocial COLLATE Latin1_General_CI_AI AS 'Nome'
		FROM
			Pos_inscricao_Contrato
			INNER JOIN PI_InscricaoProcessoPessoaJuridica ON
				Pos_inscricao_Contrato.codigoPessoaJuridica = PI_InscricaoProcessoPessoaJuridica.Codigo
		WHERE
			Pos_inscricao_Contrato.RM = @RMEmpresa) AS Tabela
	ORDER BY
		Tabela.Tipo
END

```

