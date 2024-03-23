# Planos de Pagamento

Os **planos de pagamento** são informados na coluna **Plano** da **FNDebitos** e 
são diferentes para cada modalidade de curso:

- Para alunos de **MBA**, a coluna **Plano** dos débitos armazena um valor 
**de 1 a 36**, informando exatamente o **número de parcelas** que o aluno pagará
(**de 1 a 36 parcelas**);
- Para alunos de **Pós Tech**, a coluna **Plano** dos débitos armazena um dos 
seguintes valores: **1**, **12** ou **18**, informando exatamente o 
**número de parcelas** que o aluno pagará
(**À Vista**, em **12x** ou em **18x**);
- Para alunos de **Colégio** (FIAP School e Módulo), independente do valor 
armazenado na coluna **Plano**, o **único plano possível** é o **Anual**, de 
forma que todos os alunos pagam a anuidade em **13 parcelas** (não existe 
alteração de plano para colégio);
- Já para alunos de **Graduação**, a coluna **Plano** possui um valor que pode 
variar **de 1 a 4**, conforme a tabela a seguir:

| Plano | Nome do plano                     | Quantidade de Parcelas para cada Ano                                                                                 |
|-------|-----------------------------------|----------------------------------------------------------------------------------------------------------------------|
| **1** | **Anual** ou Normal               | **1 Matrícula** (ou Renovação) + **12 Mensalidades** no próprio ano                                                  |
| **2** | **Estendido** *                   | **1 Matrícula** (ou Renovação) + **12 Mensalidades** no próprio ano + **de 2 a 6 Mensalidades** no ano excedente     |
| **3** | **Estendidão** ** ou Entendido II | **1 Matrícula** (ou Renovação) + **12 Mensalidades** no próprio ano + **de 4 a 12 Mensalidades** nos anos excedentes |
| **4** | **À Vista**                       | **1 Matrícula** (ou Renovação) + **1 Mensalidade** no próprio ano                                                    |

## (*) Plano Estendido - Graduação

O **plano estendido** é pago em **1 ano a mais** que a duração do curso do 
aluno.

### Exemplos: 

* Um **curso de 2 anos** terá seu plano estendido **pago em 3 anos** e as 
**12 mensalidades** do ano excedente são compostas por:
    * **6 mensalidades** referentes ao **1° ano** do curso;
    * **6 mensalidades** referentes ao **2° ano** do curso.

* Um **curso de 4 anos** terá seu plano estendido **pago em 5 anos** e as 
**12 mensalidades** do ano excedente são compostas por:
    * **3 mensalidades** referentes ao **1° ano** do curso;
    * **3 mensalidades** referentes ao **2° ano** do curso;
    * **3 mensalidades** referentes ao **3° ano** do curso;
    * **3 mensalidades** referentes ao **4° ano** do curso.

* Um **curso de 5 anos** terá seu plano estendido **pago em 6 anos** e as 
**12 mensalidades** do ano excedente são compostas por:
    * **3 mensalidades** referentes ao **1° ano** do curso;
    * **3 mensalidades** referentes ao **2° ano** do curso;
    * **2 mensalidades** referentes ao **3° ano** do curso;
    * **2 mensalidades** referentes ao **4° ano** do curso;
    * **2 mensalidades** referentes ao **5° ano** do curso.

## (**) Plano Estendidão - Graduação

O **plano estendidão** é pago em **2 anos a mais** que a duração do curso do 
aluno.

### Exemplos: 

* Um **curso de 2 anos** terá seu plano estendido **pago em 4 anos** e as 
**24 mensalidades** dos anos excedentes são compostas por:
    * **12 mensalidades** referentes ao **1° ano** do curso;
    * **12 mensalidades** referentes ao **2° ano** do curso.

* Um **curso de 4 anos** terá seu plano estendido **pago em 6 anos** e as 
**24 mensalidades** dos anos excedentes são compostas por:
    * **6 mensalidades** referentes ao **1° ano** do curso;
    * **6 mensalidades** referentes ao **2° ano** do curso;
    * **6 mensalidades** referentes ao **3° ano** do curso;
    * **6 mensalidades** referentes ao **4° ano** do curso.

* Um **curso de 5 anos** terá seu plano estendido **pago em 7 anos** e as 
**24 mensalidades** dos anos excedentes são compostas por:
    * **6 mensalidades** referentes ao **1° ano** do curso;
    * **6 mensalidades** referentes ao **2° ano** do curso;
    * **4 mensalidades** referentes ao **3° ano** do curso;
    * **4 mensalidades** referentes ao **4° ano** do curso;
    * **4 mensalidades** referentes ao **5° ano** do curso.

## Representação visual dos planos para cursos de Graduação de 2, 4 e 5 anos de duração

<div style="height: 320px;">
    <img src="../planosDeGraduacao.png" style="max-width: 100%;">
</div>

```
Nos planos Estendido e Estendidão, as mensalidades excedentes têm seus valores 
alinhados às mensalidades do ano em que se referem, recebendo a média das bolsas 
concedidas no período.
Estas mensalidades excedentes são geradas por um script executado pelo Chicão 
anualmente.
```
