# Aplicação de uma Bolsa FIES

<div style="height: 700px; overflow-x:scroll;">
    <img src="../aplicacao-de-bolsa-fies.svg" style="max-width: initial;">
</div>

## Nota

Esta documentação é um complemento do procedimento de 
[**Aplicação de Bolsa**](http://conhecimento.fiap.com.br/processos/financeiro/Aplicação%20de%20Bolsas%20em%20Débitos/aplicacao-de-bolsa/).


---------------------------------------------
## Manutenção de Bolsa FIES

Acima de tudo, é necessário saber que existem **dois modelos** de aplicação de 
**Bolsa FIES**:

- [**FIES Antigo**](http://conhecimento.fiap.com.br/processos/financeiro/Aplicação%20de%20uma%20Bolsa%20FIES/aplicacao-de-bolsa-fies-antigo/) - FIES 
anterior a 2018;
- [**FIES Novo**](http://conhecimento.fiap.com.br/processos/financeiro/Aplicação%20de%20uma%20Bolsa%20FIES/aplicacao-de-bolsa-fies-novo/) - FIES de 
2018 em diante;

**Ambos** os modelos ainda **estão em uso**, pois um aluno que já teve uma bolsa 
**FIES** do modelo **antigo** em algum momento, caso receba o direito ao FIES 
novamente, esta bolsa será aplicada de acordo com as regras do **FIES antigo**.

## Script para identificar o modelo de FIES que deverá ser aplicado para um aluno

```sql
SELECT
	CASE WHEN 
		COUNT(FNBolsaDebitos.Codigo) = 0 
	THEN
		'FIES Novo'
	ELSE
		'FIES Antigo'
	END AS 'Modelo FIES'
FROM
	BaseEducacional..FNBolsaDebitos WITH (NOLOCK)
	INNER JOIN BaseEducacional..FNBolsa WITH (NOLOCK)
		ON FNBolsaDebitos.CodigoBolsa = FNBolsa.Codigo
	INNER JOIN BaseEducacional..FNBolsa AS FNBolsaAux WITH (NOLOCK)
		ON FNBolsa.RM = FNBolsaAux.RM
	INNER JOIN BaseEducacional..FNTipoBolsa WITH (NOLOCK)
		ON FNBolsaAux.CodigoTipoBolsa = FNTipoBolsa.Codigo
	INNER JOIN BaseEducacional..FNDebitos WITH (NOLOCK)
		ON FNDebitos.Codigo = FNBolsaDebitos.CodigoDebito
WHERE
	FNDebitos.RM = @RM
	AND FNTipoBolsa.GeraAgenteFinanciador = 1
	AND FNBolsaAux.AnoInicio < 2018
	AND FNBolsa.Ativo = 1
```

Ao aplicar uma **bolsa FIES** a partir do sistema de 
[**Manutenção de Bolsa**](https://gitlab.fiap.com.br/dotnet/Intranet.Bolsa), 
já é identificado automaticamente o **modelo de FIES** que deve ser aplicado. 
Dessa forma, tanto a **simulação** da bolsa quando a efetivação de seu 
**cadastro**, ficarão de acordo com as **regras** do modelo de 
**FIES mais adequado**. 
