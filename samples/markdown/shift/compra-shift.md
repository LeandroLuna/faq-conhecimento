
# Compra Shift

## Criado por:
- Marcos Lima ([marcos.lima@fiap.com.br](mailto:marcos.lima@fiap.com.br))
- [Chat do Teams](https://teams.microsoft.com/l/chat/0/?users=marcos.lima@fiap.com.br)

Efetuando uma compra para terceiros no site do Shift utilizando um chamado como exeplo.



<div style="height: 600px; overflow-x:scroll;">
    <img src="../compra-shift/exemploticketcompra.png" style="max-width: initial;">
</div>


## Compra feita pela intranet: 

Entrar no cadastro de aluno na intranet e marcar o campo atrelar a empresa.


<div style="height: 600px; overflow-x:scroll;">
    <img src="../compra-shift/alunoatrelarempresa.png" style="max-width: initial;">
</div>


Depos de salvar o aluno navegar no menu até de carrinho, selecionar o aluno, turma, adicionar o cupom de desconto, não marcar a opção de desconto antecipado, escolher o tipo de compra como aluno e depois efetuar a compra.



<div style="height: 600px; overflow-x:scroll;">
    <img src="../compra-shift/efetuando-compra-intranet.png" style="max-width: initial;">
</div>


Navegar até o controle de pedidos e verificar a compra.


<div style="height: 600px; overflow-x:scroll;">
    <img src="../compra-shift/compra-efetuada.png" style="max-width: initial;">
</div>



## Compra efetuada via ambiente de dev: 


Na Intranet, em turmas remover o desconto atecipado alterando a data do campo de "desconto antecipado". Alterar para uma data menor que a data atual.


<div style="height: 600px; overflow-x:scroll;">
    <img src="../compra-shift/desconto-atecipado.png" style="max-width: initial;">
</div>


No ambiente de desenvolvimento, efetuar uma compra utilizando o cupom de desconto e escolher o tipo de pagamento boleto bancário.


<div style="height: 600px; overflow-x:scroll;">
    <img src="../compra-shift/compra-site.png" style="max-width: initial;">
</div>



Na tela de pedidos do aluno pegar o codigo da compra e selecionar as seguintes tabelas: 

```SQL
USE SHIFT

SELECT * FROM AlunoCompra WHERE CodigoAluno = 47473
SELECT * FROM AlunoTurma WHERE codigoAlunoCompra = 41938
SELECT * FROM IntegracaoBrasPag WHERE codigoAlunoCompra = 41938
SELECT * FROM ExtratoCarrinho WHERE codigoAlunoCompra = 41938
```

Selecionar o dados das tabelas e inserir na query de compras

```SQL

USE Shift


INSERT INTO AlunoCompra (
CodigoAluno, DataHoraCompra, CodigoStatusCompra, CodigoPromocional, 
DescontoAVista, DescontoAluno, DataCancelamento, MotivoCancelamento, CodigoUsuarioCancelamento, DescontoColaborador, 
TamanhoCamisa, GeneroCamisa, ParcelamentoRestante, CodigoCompraResponsavel, CodigoUsuarioAtivacao, DataAtivacao, MotivoAtivacao, 
DataEmailDeficiente, EmitirNotaFiscal,MotivoAtualizacaoEmitirNotaFiscal,CodigoUsuarioAtualizacaoEmitirNotaFiscal
)
VALUES
(
47473,	GETDATE(), 	3, ' 7f40po' , 0,	NULL, NULL,	NULL, NULL,	NULL, 'm','n',NULL,NULL,NULL,NULL,NULL,NULL,0,
NULL, NULL
)

DECLARE @UltimoId INT = (SELECT MAX(Codigo) fROM AlunoCompra)

INSERT INTO AlunoTurma (
CodigoAlunoCompra, CodigoTurma, DescontoAntecipado, EmitiCertificado, Chave,
CodigoTrilhaCurso, PorcentagemDescontoEspecial, EmitirCertificadoAutomatico, CodigoStatusTurma, UsuarioAD, SenhaAD)
VALUES 
(@UltimoId,1606,NULL,0,'775D6967-D546-4617-B924-EB30DCBF0A60',NULL,NULL,0,3,NULL,NULL)



INSERT INTO IntegracaoBraspag (
CodigoAlunoCompra,CodigoTransacao, FormaPagamento, Valor, QtVezes,
NumeroBoleto, CodigoArquivoRetornoBancoRegistro,ValorPagoBoleto, DataVencimentoBoleto, DataPagamentoBoleto, 
URLBoleto, CodigoRetornoBoleto, MensagemBoleto, StatusBoleto, TipoCartao,NomeCartao, 
NumeroAutorizacaoCartao, MensagemCartao, CodigoRetornoCartao, StatusCartao, NumeroTransacaoCartao, 
DataHoraCadastro, IdPagCoin, StatusPagamentoPagCoin, DataHoraRespostaPagCoin, ChaveBoleto, 
PaymentId, ValorTotalBoletoParcelado,OrdemCartao, Agrupador, Cancelado
)
VALUES
(
@UltimoId,833549,1, 1294.20, 1,NULL,NULL,NULL,'2023-10-09 00:00:00.000',NULL,	
NULL,
0,'Successful',1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,GETDATE(),
NULL,NULL,NULL,'3419f58c-57f1-4ab8-bc80-08ba2919ab92',NULL,0,0,NULL,NULL
)


INSERT INTO ExtratoCarrinho (
CodigoAlunoCompra, CodigoTurma, Ordem, Valor, CodigoPromocional, Desconto, CodigoMotivoDesconto,
Tipo, Importado
)
VALUES
(
@UltimoId,NULL,2, 1294.20,'7f40po',10,4,'CF',0
)


INSERT INTO ExtratoCarrinho (CodigoAlunoCompra, CodigoTurma, Ordem, Valor, CodigoPromocional, Desconto, CodigoMotivoDesconto,
Tipo, Importado)
VALUES
(
@UltimoId,NULL,1,1438.00,NULL,NULL,NULL,'CP',0
)

INSERT INTO ExtratoCarrinho (
CodigoAlunoCompra, CodigoTurma, Ordem, Valor, CodigoPromocional, Desconto, CodigoMotivoDesconto,
Tipo, Importado
)
VALUES
(
@UltimoId,1606,2, 1294.20,'7f40po',10,4,'CF',0
)


INSERT INTO ExtratoCarrinho (CodigoAlunoCompra, CodigoTurma, Ordem, Valor, CodigoPromocional, Desconto, CodigoMotivoDesconto,
Tipo, Importado)
VALUES
(
@UltimoId,1606,1,1438.00,NULL,NULL,NULL,'CP',0
)

```

Navegar até o controle de pedidos e verificar a compra e depois rodar em produção.

<div style="height: 600px; overflow-x:scroll;">
    <img src="../compra-shift/compra-efetuada.png" style="max-width: initial;">
</div>