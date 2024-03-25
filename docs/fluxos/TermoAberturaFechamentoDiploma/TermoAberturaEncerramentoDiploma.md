# Funcionamento PDF Termo de Abertura e Encerramento do Diploma Digital

## Visão Geral
Termo de Abertura e Encerramento [...]

- Projeto do Livro Registro: [Link para o projeto no Gitlab](https://gitlab.fiap.com.br/dotnet/LivroRegistroDiploma)

**Observação:** [Todas as tabelas estão no banco **Educacional**]
1. Tabelas: BryLote
2. Tabelas: BryItem

## Funcionalidades Principais

1. Cadastra o lote com o status = 5 (Arquivo Pdf) e registra o Tipo do Termo.
    - a partir do status 5, a intranet de assinatura A3 de PDF, irá puxar apenas os Lotes que são PDF's. <br>
    = Intranet Assinatura PDF Digital: [Link para o projeto no Gitlab](https://gitlab.fiap.com.br/dotnet/Intranet.AssinaturaPDFDigital)

2. Dentro do lote onde se encontra o PDF, abrirá as opções para se assinar no mesmo momento, então a assinatura é feita na hora com o cartão (token) físico. <br>

## Arquitetura
Este projeto foi desenvolvido utilizando a .NET Framework 4.6.1.

## Projetos que utilizam essa API
Certifique-se de ter as seguintes dependências instaladas:

- Para gerar o Termo não precisa de nenhuma outra API ou sistema.

## Os termos vão para esta intranet
- [Intranet.AssinaturaPDFDigital](https://gitlab.fiap.com.br/dotnet/Intranet.AssinaturaPDFDigital): Ler o Readme