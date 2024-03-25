# Criando uma Conta Corrente

Sempre que uma **nova modalidade** é criada existe a necessidade de criar uma 
**conta corrente** para receber os pagamentos referentes a esta nova modalidade.

Para criar esta **conta corrente**, é necessário utilizar o **passo a passo** a 
seguir.

## 1 - Inserir o registro na Educacional..CDContas 

```sql

/* Ex: 'ITAU' */
DECLARE @Banco AS VARCHAR(50) = 'ITAU';

/* Ex: 'VSTP Educação Ltda' */
DECLARE @Favorecido AS VARCHAR(255) = 'VSTP Educação Ltda';	

/* Ex: '0167' */
DECLARE @Agencia AS VARCHAR(10) = '0167';	

/* Ex: 'Pós Tech' */
DECLARE @Escola AS VARCHAR(50) = '{NomeConta}';	

/* Ex: 0 OU 1 */
/* Obs: Questionar quem solicitou a criação da conta, para saber se a conta terá ou não arquivo retorno */
DECLARE @TemArquivoRetorno AS BIT = 0;

/* Ex: '99604' (N° da Conta sem Dígito) */
DECLARE @ContaSeparada AS CHAR(5) = '{NumConta}';

/* Ex: '0' (Dígito da Conta) */
DECLARE @DacContaSeparada AS CHAR(1) = '{DigitoConta}';	

/* Ex: '99604-0' ({conta}-{digito}) */
DECLARE @Conta AS VARCHAR(50);
SET @Conta = CONCAT(@ContaSeparada, '-', @DacContaSeparada);	

INSERT INTO Educacional..CDContas
	(Escola,
	Banco,
	Conta,
	Favorecido,
	Agencia,
	TemArquivoRetorno,
	ContaSeparada,
	DacContaSeparada)
VALUES
	(@Escola,
	@Banco,
	@Conta,
	@Favorecido,
	@Agencia,
	@TemArquivoRetorno,
	@ContaSeparada,
	@DacContaSeparada);

```

## 2 - Inserir o registro na BaseEducacional..FNContaCorrente

```sql

/* Ex: 167 */
DECLARE @Agencia AS INT = '0167';

/* Ex: 99604 (N° da Conta sem Dígito) */
DECLARE @Conta AS INT = '{NumConta}';

/* Ex: '' */
DECLARE @DigitoAgencia AS VARCHAR(5) = '';

/* Ex: '0' */
DECLARE @DigitoConta AS VARCHAR(5) = '{DigitoConta}';

/* Ex: GETDATE() (Data da inserção) */
DECLARE @DataHoraCadastro AS DATETIME = GETDATE();

/* Ex: 1 */
DECLARE @CodigoUsuarioCadastro AS INT = 1;

/* Ex: 1 */
DECLARE @Ativo AS BIT = 1;

/* Ex: '' */
DECLARE @Chave AS VARCHAR(20) = '{NomeConta}';

/* Ex: NULL */
DECLARE @CodigoUnidade AS INT = NULL;

/* Ex: 'J0113195260001550000000001' */
DECLARE @CodigoCedente AS CHAR(26) = 'J0113195260001550000000001';

/* Ex: 'DA5S6E9R8H21N0C3' */
DECLARE @ChaveCedente AS CHAR(16) = 'DA5S6E9R8H21N0C3';

/* Ex: 'VSTP Educação LTDA' */
DECLARE @RazaoSocial AS VARCHAR(255) = 'VSTP Educação LTDA';

/* Ex: '11319526000155' */
DECLARE @CNPJ AS VARCHAR(14) = '11319526000155';

/* Ex: 'Pós Tech' */
DECLARE @DescricaoUnidade AS VARCHAR(255) = '{NomeConta}';

INSERT INTO BaseEducacional..FNContaCorrente
	(Agencia,
	Conta,
	DigitoAgencia,
	DigitoConta,
	DataHoraCadastro,
	CodigoUsuarioCadastro,
	Ativo,
	Chave,
	CodigoUnidade,
	CodigoCedente,
	ChaveCedente,
	RazaoSocial,
	CNPJ,
	DescricaoUnidade)
VALUES
	(@Agencia,
	@Conta,
	@DigitoAgencia,
	@DigitoConta,
	@DataHoraCadastro,
	@CodigoUsuarioCadastro,
	@Ativo,
	@Chave,
	@CodigoUnidade,
	@CodigoCedente,
	@ChaveCedente,
	@RazaoSocial,
	@CNPJ,
	@DescricaoUnidade);

```

## 3 - Inserir o registro na Educacional..ControleArquivoRetorno com os dias anteriores ao dia atual

```sql

DECLARE @LoteControleArquivoRetornoInserir AS INT; 

SELECT
    @LoteControleArquivoRetornoInserir = ISNULL(MAX(Lote), 0) + 1
FROM
    Educacional..ControleArquivoRetorno;
    
/* Ex: 1 */
DECLARE @LoteProcessado AS BIT = 1;

/* Ex: '0167' */
DECLARE @Agencia AS CHAR(4) = '0167';

/* Ex: '99604' (N° da Conta sem Dígito) */
DECLARE @Conta AS CHAR(5) = '{NumConta}';

/* Ex: '0' (Dígito da Conta) */
DECLARE @DacConta AS CHAR(1) = '{DigitoConta}';

/* Ex: NULL */
DECLARE @NomeArquivo AS VARCHAR(40) = NULL;

/* Ex: NULL */
DECLARE @NomeArquivoOriginal AS VARCHAR(20) = NULL;

/* Ex: GETDATE() (Data da inserção) */
DECLARE @DataHoraCadastro AS DATETIME(8) = GETDATE();

/* Ex: 1 */
DECLARE @CodigoUsuarioCadastro AS INT = 1;

/* Ex: 1 */
DECLARE @Valido AS BIT = 1;

/* Ex: 'INFO - Não há documento para esta conta neste dia' */
DECLARE @MensagemValidacao AS VARCHAR(255) = 'INFO - Não há documento para esta conta neste dia';

INSERT INTO Educacional..ControleArquivoRetorno 
    (Lote, 
    LoteProcessado, 
    Agencia, 
    Conta, 
    DacConta,
    [Data], 
    NomeArquivo,
    NomeArquivoOriginal,
    DataHoraCadastro, 
    CodigoUsuarioCadastro, 
    Valido, 
    MensagemValidacao) 
SELECT
    @LoteControleArquivoRetornoInserir, 
    @LoteProcessado, 
    @Agencia, 
    @Conta, 
    @DacConta,
    CLDiasUteis.[Data], 
    @NomeArquivo,
    @NomeArquivoOriginal,
    @DataHoraCadastro, 
    @CodigoUsuarioCadastro, 
    @Valido, 
    @MensagemValidacao 
FROM
    BaseEducacional..CLDiasUteis AS CLDiasUteis
WHERE
    CLDiasUteis.DiaUtilFinanceiro = 1
    AND CLDiasUteis.Data < CONVERT(DATE, GETDATE())

```
