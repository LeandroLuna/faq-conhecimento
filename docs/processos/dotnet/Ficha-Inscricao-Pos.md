# Testes de Ficha Inscrição Pós

<div  style="height: 600px; overflow-x:scroll;">
    <img  src="../testar-projeto-ficha-inscricao-pos.svg"  style="max-width: initial;">
</div>

## Criado por:
- Marcos Lima <marcos.lima@fiap.com.br> 
([Chat do Teams](https://teams.microsoft.com/l/chat/0/?users=marcos.lima@fiap.com.br))



## Informações de cadastro para teste de inscrição pós

<div  style="height: 600px; overflow-x:scroll;">
    <img  src="../Imagens/CadastroFichaInscricao.JPG"  style="max-width: initial;">
</div>

Cadastro Inscrição


<div  style="height: 600px; overflow-x:scroll;">
    <img  src="../Imagens/EscolherCursoFormatO.JPG"  style="max-width: initial;">
</div>

Escolher Curso e formato


<div  style="height: 600px; overflow-x:scroll;">
    <img  src="../Imagens/EscolherHoraDataEntrevista.JPG"  style="max-width: initial;">
</div>

Escolher data da entrevista

## Informações Adicionais para teste de inscrição pós

- Para Fazer os testes é nescessário consultar as tabelas no banco WebAdm :

```SQL
SELECT * FROM pos_inscricao_new WHERE cic ='63526997071'
```
Consulta se o cpf já foi cadastrado e verifica o cadastro de Nome, CPF,
Email e telefone.

```SQL
SELECT * FROM PI_InscricaoProcesso WHERE codigoInscricao = 116695
```
Verifica codigoTipoStatusIncricaoProcesso. O codigoInscricao usado como exemplo e da tabela pos_inscricao_new.

```SQL
SELECT * FROM PI_Cadastro WHERE codigoInscricao = 116695
```
Verifica DDD e linkdin.

```SQL
SELECT * FROM PI_CursoEscolha WHERE codigoInscricaoProcesso = 159383
```
Verifica a Turma escolhida

```SQL
SELECT * FROM PI_AgendaEntrevista WHERE codigoInscricaoProcesso = 159383
```
Verifica a agenda da entrvista.

## Informações Adicionais para desativação de cadastro 


<div  style="height: 600px; overflow-x:scroll;">
    <img  src="../Imagens/MenuFiapPosGraduacao.png"  style="max-width: initial;">
</div>

Menu Pos Graduação


<div  style="height: 600px; overflow-x:scroll;">
    <img  src="../Imagens/MenuControleInscricao.png"  style="max-width: initial">
</div>

Menu Controle 

<div  style="height: 600px; overflow-x:scroll;">
    <img  src="../Imagens/SelecionaStatusDesativaStatus.png"  style="max-width: initial">
</div>

Filtrar o cpf


<div  style="height: 600px; overflow-x:scroll;">
    <img  src="../Imagens/Intranet3DesativarInscricao.png"  style="max-width: initial">
</div>
