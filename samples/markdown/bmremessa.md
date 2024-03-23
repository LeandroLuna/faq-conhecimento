### Representa o funcionamento para enviar boletos para o banco e saber quem pagou ou não

*BM -> Boleto Matrícula*

Todo mês do dia 19 ao 22 aproximadamente, o chicão realiza os seguintes procedimentos: 

* Roda um script.

* Verifica todos os débitos abertos referente ao mês que ele está + 1.

* Gera um arquivo “Remessa” e envia para o banco.

*Exemplo: foi registrado um boleto de 1000 para a pessoa **W**, data de vencimento **X**, para pagar dia **Y** e conceda desconto de **Z** na carteira.*

* Itaú processa esses dados e no dia seguinte afirma que foi registrado os boletos.

* Em um determinado horário o banco que retirou o dinheiro e transferiu para o Itaú (nosso banco) informa que foi pago.

* O Itaú nos devolve um arquivo .txt com todos os boletos pagos.

*Com o 'NossoNumero' consegue identificar o FNDebito e realiza o UPDATE nas colunas 'ValorPago' 'DataPagamento' 'CodigoArquivoRetornoBancoRegistro'*