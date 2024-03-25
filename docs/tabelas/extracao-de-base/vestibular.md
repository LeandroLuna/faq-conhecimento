#Vestibular

## Inscritos no vestibular

**OBS:** Trocar o código do processo do vestibular na SELECT abaixo:

```sql
SELECT Vestibulando.*
FROM civ..ProcessoVestibulando AS ProcessoVestibulando
INNER JOIN civ..Vestibulando AS Vestibulando
	ON ProcessoVestibulando.codvestibulando = Vestibulando.CodVestibulando
WHERE ProcessoVestibulando.codprocesso = 36;
```


## Ação de Saiba Antes

Geralmente é disparado um mailing para quem pediu para ser avisado antes do vestibular,
gerando um desconto para o mesmo.

Para isso, os dados do candidato devem ser inseridos na tabela **civ..AcaoSaibaAntes**

Os dados do candidato podem ser pegos em: **civ..Vestibulando**

A URL para acessar o sistema é: URL: https://vestibular.fiap.com.br/AcaoSaibaAntes.asp?chave=@chave

```sql
INSERT INTO civ..AcaoSaibaAntes (AnoProcesso, Nome, Email, Chave) VALUES (2020, 'Nome do candidato', 'email-do-candidato@fiap.com.br', NEWID());
```