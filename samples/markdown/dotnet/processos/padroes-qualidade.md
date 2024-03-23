# Padrões de Qualidade e Processos de Deploy

!!! info "Última modificação"
    **23-11-2023**   Henrique Lopes Mendonça
    **23-11-2023**   Victor Alves Bugueno

??? note "1# Demanda do cliente"
    Solicitada pelo o **Agilista da Squad**, entedimento e análise das necessidades do desenvolvimento.

??? note "2# Criação de Branch"
    Criação de **BugFix** e **Feature** conforme a **[Documentação](https://conhecimento.fiap.com.br/processos/demandas-e-alteracoes-em-sistemas/demandas-e-alteracoes-em-sistemas/)**.  

??? note "3# Desenvolvimento da demanda"
    Caso projeto seja novo utilizar os **[Padrões de Projeto](#)**, caso contrário seguir o máximo possível na hora de criar novas funcionalidades.

??? note "4# Desenvolvimento dos Testes"
    Projetos novos deverão ter suas **regras de negócios** totalmente cobertas por **teste**. Quando realizados **Fetures** e **Bugs** apenas as **regras de négocio** desses trechos deverão ter cobertura de **teste**.

??? note "5# Criar template do Merge Request"
    Adicionar o modelo padrão de **[Merge Request](http://conhecimento.fiap.com.br/dotnet/padroes-de-projetos/template-merge-request/)** e preenchê-lo conforme a atualização realizada, contendo o passo a passo para realizar os **testes em homologação**.

??? note "6# Merge Request da branch na Homolog"
    Enviar o link do **merge** ao grupo de homologação, e aguardar o aceite por **dois Devs** da equipe de qualidade.

??? note "7# Aprovação de dois Devs da equipe de qualidade"
    Será somente enviado para **deploy** após a aprovação dos **dois Devs**. Caso houver uma reprovação, será necessário **revisar os apontamentos** solicitados no próprio MR (**através de comentários**).

??? note "8# Testar no ambiente de homologação"
    Após o aceite do MR, alguém da **mesma squad** deverá testar em **homologação**. Se em caso não funcionar voltar para **início do processo** de MR.

??? note "9# Merge Request para Dev e depois para Master"
    Depois de aprovado e testado, realizar o **merge** para Dev e solicitar ao **Tech Lead** o aceite do MR para master.

??? note "10# Aprovação do Tech Lead"
    Deverá ter a aprovação do MR do **Tech Lead** nessa etapa.

??? note "11# Deploy Produção"
    Após aprovação do **Tech Lead**, realizar o **deploy** no ambiente de produção e **validar a funcionalidade**.

 
     
      

