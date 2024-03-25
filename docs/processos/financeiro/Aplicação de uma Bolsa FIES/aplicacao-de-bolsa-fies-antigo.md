# Aplicação de uma Bolsa FIES (Modelo Antigo)

<div style="height: 700px; overflow-x:scroll;">
    <img src="../aplicacao-de-bolsa-fies.svg" style="max-width: initial;">
</div>

## Nota

Esta documentação é um complemento dos procedimentos de 
[**Aplicação de Bolsa**](http://conhecimento.fiap.com.br/processos/financeiro/Aplicação%20de%20Bolsas%20em%20Débitos/aplicacao-de-bolsa/) e 
[**Aplicação de Bolsa FIES**](http://conhecimento.fiap.com.br/processos/financeiro/Aplicação%20de%20uma%20Bolsa%20FIES/aplicacao-de-bolsa-fies/).

---------------------------------------------
## FIES Antigo

Para cada uma das mensalidades que recebem a bolsa **FIES** do modelo 
**antigo**, são **somadas as porcentagens** de todas as bolsas vinculadas a esta 
mensalidade, e a bolsa resultante é aplicada ao débito **de uma só vez**, 
**independentemente do grupo** que as bolsas pertencem 
(**Bolsas prioritárias** ou **demais bolsas**).

Além de alterar o valor final das mensalidades do aluno, são gerados 6 débitos 
do tipo **Repasse Fies**, cada um deles referente a uma **Mensalidade** que 
recebeu a bolsa FIES no modelo antigo. Os **valores** destes débitos de 
**Repasse Fies** são equivalentes ao valor de bolsa total concedido ao débito, 
conforme **Exemplo**.

### Exemplo:
```
Bolsas do aluno:
- 10% de "DP";
- 20% de "Ex-aluno";
- 40% de "FIES";

-------------------------------- Mensalidades ---------------------------------
BolsaResultante = 10% + 20% + 40% = 70%
Será aplicada 70% na coluna "Bolsa" de cada "Mensalidade" do aluno.

- ValorCheioNominal = R$ 1.000,00;
- ValorDescontoNominal = R$ 800,00;
- Bolsa = 70%;
- ValorCheioDebito = 1000 * (1 - 70 / 100.0) = R$ 300,00;
- ValorDescontoDebito = 800 * (1 - 70 / 100.0) = R$ 240,00;

OBS: Lembrar de considerar os valores de Dedução e Acréscimo, caso existam.

-------------------------------- Repasse Fies ---------------------------------
Os 6 débitos de "Repasse Fies" receberão 70% do valor nominal de pontualidade 
da "Mensalidade" correspondente, tanto nos valores-cheios quanto nos 
valores-desconto.

- ValorDescontoNominal_Mensalidade = R$ 800,00;

- ValorCheioNominal = 800 * (70 / 100.0) = R$ 560,00;
- ValorDescontoNominal = 800 * (70 / 100.0) = R$ 560,00;
- Bolsa = 0%;
- ValorCheioDebito = 800 * (70 / 100.0) = R$ 560,00;
- ValorDescontoDebito = 800 * (70 / 100.0) = R$ 560,00;
-------------------------------------------------------------------------------

Desta forma, ao somar os valores desconto de pontualidade do "Repasse Fies" e da 
"Mensalidade", o valor obtido é o mesmo que o valor nominal de pontualidade da 
"Mensalidade":

- ValorDescontoDebito_Mensalidade = R$ 240,00;
- ValorDescontoDebito_RepasseFies = R$ 560,00;

- ValorDescontoNominal_Mensalidade = R$ 800,00; // R$ 240,00 + R$ 560,00
```

O modelo de **FIES antigo não gera** débitos de **Agente Financiador**.

Ao aplicar uma bolsa **FIES** no modelo **antigo** é inserido um registro na 
**FNBolsa**, informando a **porcentagem** de bolsa e o **período** no qual a 
bolsa se aplica, dentre outros campos.

O sistema também insere **6 registros** na **FNBolsaDebitos**, uma para cada 
vínculo entre a **nova bolsa** e um débito de **Mensalidade**.

Na **FNBolsaAplicada** são inseridos **12 registros**:

- 6 registros vinculando cada **Mensalidade** ao tipo de bolsa **FIES**, 
informando a **porcentagem de bolsa concedida**;
- 6 registros vinculando cada **Mensalidade** ao tipo de bolsa **Repasse Fies**,
informando a **porcentagem de bolsa complementar**;

Há também uma tabela chamada **FNControleRepasseFies**, onde é inserida a 
relação entre o débito de **Repasse Fies** e sua **Mensalidade** correspondente 
(de mesmo mês e ano) totalizando **6 registros**.

### Observações:
```
Todas as tabelas citadas são do banco "BaseEducacional".
As informações das colunas "Bolsa" e "Porcentagem" são inseridas na escala de 0 a 100.
```
