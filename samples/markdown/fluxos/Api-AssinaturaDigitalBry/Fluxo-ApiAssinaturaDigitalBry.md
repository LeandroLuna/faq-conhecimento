# Fluxo da Api de Assinatura Digital Bry

## Visão Geral
Atualmente, até o dia 06/03/2024, essa API é usada para cadastrar as assinaturas na tabela BryLote, BryAssinatura e BryItem.
Essas assinaturas são A3, assim sendo necessário ter o token (cartão físico) para poder assinar os lotes criados.

- Projeto: [Link para o projeto no Gitlab](https://gitlab.fiap.com.br/dotnet/Api.AssinaturaDigitalBry)

**Observação:** [Todas as tabelas estão no banco **Educacional**]

## Funcionalidades Principais
1. Cadastrar um novo lote que será puxado Intranet.AssinaturaDigital
Tabelas: BryLote

- Intranet.AssinaturaDigital: [Link para o projeto no Gitlab](https://gitlab.fiap.com.br/dotnet/Api.AssinaturaDigitalBry)
    
2. Salvar os itens dentro do lote criado acima <br>
Tabelas: BryLoteItem

3. Salvar as assinaturas enviadas, para cada item do novo lote <br>
Tabela: BryAssinatura

## Arquitetura
Este projeto foi desenvolvido utilizando a .NET 6, no padrão repository.

## Projetos que utilizam essa API
Certifique-se de ter as seguintes dependências instaladas:

- [Api.CurriculoDigital](https://gitlab.fiap.com.br/dotnet/api.curriculodigital): A Api do Curriculo envia os itens para criar o lote, e envia também as assinaturas necessárias, no método "FinalizaCurriculo" dentro de CurriculoService.
<br>
- [Api.HistoricoDigital](https://gitlab.fiap.com.br/dotnet/api.HistoricoDigital): A Api do Histórico envia os itens para criar o lote, e envia também as assinaturas necessárias, no método "Finalizar" dentro de LoteBLL.
<br>
- [Intranet.AssinaturaPDFDigital](https://gitlab.fiap.com.br/dotnet/Intranet.AssinaturaPDFDigital): Ler o Readme