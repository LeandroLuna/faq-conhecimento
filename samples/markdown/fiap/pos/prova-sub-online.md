## Fluxos do sistema
<div style="height: 300px; overflow-x:scroll;">
    <img src="../prova-sub-online.svg" style="max-width: initial;">
</div>


## Regras de negócio
- Apenas alunos de MBA presencial e Live tem acesso a esse sistema.

- O aluno solicita a sub de apenas uma disciplina por protocolo.

- O aluno só pode solicitar a prova sub uma vez por disciplina.

- Alunos corporate tem seu protocolo abonado automaticamente.

- Após o pagamento do protocolo, caso a disciplina possua um banco de questões, o aluno tem até 15 dias para realizar a prova.

- Após o aluno gerar a prova, ele tem até uma hora para respondê-la.

- O banco de questões deve conter no mínimo 10 questões ativas para ser possível seguir o processo como prova online.

- O aluno não pode estar reprovado por nota e falta ao mesmo tempo, na mesma disciplina.

- Caso o aluno esteja reprovado por falta, o número de faltas não pode ser superior ao limite de faltas para ser aprovado mais duas faltas.

    - Exemplo: uma disciplina com carga horaria de 16h, para ser aprovado o aluno deve ter no máximo uma falta, se ele tiver mais do que uma e menos do que três (1 falta para ser aprovado + 2 faltas limites) ele estará reprovado, mas poderá solicitar a prova sub, se a quantidade de faltas for igual ou superior a três o aluno estará reprovado e não poderá fazer prova sub.

- Alunos reprovados por falta e que a prova online esteja disponível para o protocolo:

    - Em caso de aprovação: as faltas são removidas do boletim e a nota permanece a mesma sem ser substituída pela nota da prova online.

    - Em caso de reprovação: as faltas permanecem no boletim e a nota permanece a mesma sem ser substituída pela nota da prova online.

- Alunos reprovados por nota e que a prova online esteja disponível para o protocolo:

    - A nota da prova sub online sempre é lançada no boletim com o tipo 3 (avaliação substitutiva), dessa forma o boletim mantém a nota antiga e caso a nota da prova sub online seja maior do que 7, o boletim já é alterado automaticamente para aprovado.

- O job de publicação das notas, envio dos e-mails e encerramento dos protocolos sempre é executado meia-noite e apenas uma vez por dia.


## Estruturas no banco de dados

| Nome | Banco | Tipo de estrutura | Descrição |
|------|----------------|-----------|----------|
| PTSolicitacao | BaseEducacional | Tabela | Controla as solicitações e protocolos|
| PTSolicitacaoEtapa | BaseEducacional | Tabela | Controla as etapas das solicitações |
| PTTipoSolicitacao | BaseEducacional | Tabela | Controla os tipos de solicitação, o tipo de revisão de notas e faltas tem o código 147 |
| PTTipoSolicitacaoEtapa | BaseEducacional | Tabela | Controla os tipos de etapa que pertencem a um tipo de solicitação |
| PTTipoSolicitacaoTipoPublico | BaseEducacional | Tabela | Controla os públicos que podem solicitar o tipo do protocolo |
| PTTipoSolicitacaoConfiguracaoPagamento | BaseEducacional | Tabela | Controla as configurações de pagamento de um tipo de solicitação |
| PTSolicitacaoRelacao | BaseEducacional | Tabela | Controla a disciplina que pertence à solicitação |
| FNDebitos | BaseEducacional | Tabela | Registra o débito da solicitação com o tipo *Taxa* e descrição *Solicitação x - Revisão de Notas e Faltas* |
| CanalPortalItem | site_fiap | Tabela | Armazena o ícone do sistema no portal do aluno, o código do ícone é 199 |
| spAcessoProvaSubOnlineMba | site_fiap | Procedure | Controla quem tem acesso ao ícone do sistema no portal do aluno |
| spGeraProvaSubOnlineMbaPresencial | site_fiap | Procedure | Gera a prova online da solicitação |
| spAtualizaSituacaoProvaSubOnlineMba | site_fiap | Procedure | Envia e-mails para o aluno para informar os dias restantes do prazo limite, caso o prazo seja encerrado, o protocolo é encerrado |
| spPublicaNotasProvaSubOnlineMbaPresencial | site_fiap | Procedure | Ajusta os boletins conforme as notas das provas online e encerra as solicitações que tem prova |
| [MBA] Notas e Situacao de Prova Sub Online | | Job | Executa as procedures spAtualizaSituacaoProvaSubOnlineMba e spPublicaNotasProvaSubOnlineMbaPresencial todo dia a meia-noite |


## Sistemas envolvidos

[Portal do aluno](https://gitlab.fiap.com.br/dotnet/PortalAluno)
    - Sistema principal e pai do sistema de revisão de notas e faltas.

[Portal Moodle](https://gitlab.fiap.com.br/dotnet/PortalMoodle)
    - Utilizamos a parte de secretaria virtual do portal moodle (sistemas em dotnet utilizados no ON) para fazer o controle das solicitações do aluno, ele é o sistema "Revisão de notas e faltas".

[Intranet Protocolo](https://gitlab.fiap.com.br/dotnet/Intranet.Protocolo)
    - Sistema da Intranet utilizado pelo helpcenter para auxiliar os alunos com as solicitações.

[Api Protocolo](https://gitlab.fiap.com.br/dotnet/Api.Protocolo)
    - Api responsavel por fazer todo o controle das solicitações no banco de dados.

[Boleto](https://gitlab.fiap.com.br/dotnet/Boleto)
    - Responsavel por gerar os boletos no portal do aluno.


## Extras
[Modelos de email e manual dos alunos](https://gitlab.fiap.com.br/html/modelos-emails-oficial/-/tree/dev/ProvaSubMba)

[Script para remover a prova de um aluno](https://gitlab.fiap.com.br/fiap/base-de-conhecimento/-/blob/master/docs/fiap/pos/prova-sub-online-remover-prova.sql)

[Script collab para transformar um Excel de questões em sql](https://gitlab.fiap.com.br/fiap/base-de-conhecimento/-/blob/master/docs/fiap/pos/prova-sub-online-questoes.ipynb)

[Excel de exemplo para cadastro de questões](https://gitlab.fiap.com.br/fiap/base-de-conhecimento/-/blob/master/docs/fiap/pos/prova-sub-online-questoes-excel.xlsx)