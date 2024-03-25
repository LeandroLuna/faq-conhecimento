# Cupons Fiscais

Todos os pedidos que são **confirmados** e **retirados**, com valor maior que zero, são emitidos cupom fiscal junto à _GarçomWeb_.

## Serviço

O serviço responsável pela gerência dos pedidos é o [Service.IntegracaoKitchenetGW](https://gitlab.fiap.com.br/dotnet/Service.IntegracaoKitchenetGW), uma aplicação feita em C# .NET. Ela importa os pedidos a cada 3 minutos para o PDV, e verifica a cada 10 minutos se o cupom fiscal foi emitido.

## Importação de pedido

Os dados do pedido são importados para o PDV, são cadastrados dados básicos do consumidor, como Nome e CPF, e dados de pagamento, que são montados da seguinte forma:

- Valor Pago via Cartão de Crédito: Consta o valor como pagamento em cartão de crédito.
- Valor Pago usando saldo na Kitchenet: Consta o valor como pagamento realizado via dinheiro.

Caso haja um misto, os valores são preenchidos conforme uso.

## Emissão de cupom fiscal

Os cupons são emitidos automaticamente após aproximadamente 10 minutos da importação. A tabela **IntegracaoGW** é responsável por guardar o XML dos cupons emitidos.

!!! warning "Atenção"
    Os pedidos só são importados e contabilizados se o "Gerenciador PDV" estiver aberto nas unidades (_aplicativo com ícone de iFood instalado no PDV da unidade_)

## E-mail com cupom fiscal

Existe uma trigger na tabela **IntegracaoGW** chamada **trIntegracaoCupomFiscal** que envia o e-mail para o respectivo aluno/funcionário quando o cupom fiscal está pronto.
