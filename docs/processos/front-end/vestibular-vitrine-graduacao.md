# Vestibular Vitrine Graduação

<div style="height: 300px; overflow-x:scroll;">
    <img src="../vestibular-vitrine-graduacao.svg" style="max-width: initial;">
</div>

## Links
**PS3 de exemplo** [PPT](https://fiapcom-my.sharepoint.com/:p:/g/personal/cl1871_fiap_com_br/EQIl9oQOTpJNl-m78G5_iv4BtuBFN99IHOQ2tS490wM8LQ) <br />
**Documentação Miro** [Miro](https://miro.com/app/board/o9J_l0uDI8w=/) 


### 1. Equipe do Marketing passa as informações para o Vestibular
- Período de Inscrição
- Data da Prova
- Resultado
- Período da Matrícula
- Período de Condições Especiais


### 2. Padrões
- Período de Inscrição - termina na quinta-feira antes da prova
- Data da Prova - sábado às 10h
- Resultado (lista de aprovados) - terça-feira depois da prova, às 10h
- Período da matrícula - inicia com a liberação da lista de aprovados



### 3. Alterar Datas de acordo com cada Processo Seletivo (PS1, PS2, PS3 e PS4)
**wp-content/themes/fiap2016/_config/vestibular.php**

```
VESTIBULAR_PS*_TIMESTAMP_INICIO_INSCRICAO
VESTIBULAR_PS*_TIMESTAMP_FIM_INSCRICAO
VESTIBULAR_PS*_TIMESTAMP_DIA_PROVA
VESTIBULAR_PS*_TIMESTAMP_DIA_RESULTADO
VESTIBULAR_PS*_TIMESTAMP_INICIO_MATRICULA_PRESENCIAL
VESTIBULAR_PS*_TIMESTAMP_FIM_MATRICULA_PRESENCIAL
VESTIBULAR_PS*_TIMESTAMP_INICIO_MATRICULA_ONLINE
VESTIBULAR_PS*_TIMESTAMP_FIM_MATRICULA_ONLINE
VESTIBULAR_PS*_TIMESTAMP_PEDIDO_CONDICOES_ESPECIAIS
VESTIBULAR_PS*_TIMESTAMP_FIM_ENTREVISTA_ONLINE
```


### 4. Alterar Datas
**wp-content/themes/fiap2016/assets/scripts/graduacao/home/contador.js**

Exemplo:
Altera a data para o do último dia de inscrição no processo seletivo.<br />
```
const date = new Date('Feb 03, 2022 23:59:59').getTime()
```

### 5. Alterar datas nos twigs em Desktop e Mobile

### 6. Datas a serem alteradas nos templates (twigs)
Em:
```
wp-content/themes/fiap2016/views/fiap/home/vitrine/graduacao.twig
```
Ver cada template referente a datas nos passos abaixo - **Desktop e Mobile***

## Exemplo PS3 (Fevereiro 2022)

### 7. 28/01 - "Inscreva-se - ÚLTIMOS DIAS"
Início do Banner com Contagem Regressiva (\views\fiap\home\vitrine\graduacao\vestibular\vestibular-counter.twig)<br />
Link do botão redireciona para página de Graduação (https://www.fiap.com.br/graduacao/)

No código em "vestibular.php":
```
define('VESTIBULAR_INSCRICOES_ULTIMOS_DIAS', time() >= mktime(0, 0, 0, JANEIRO, 28, 2022) && time() <= mktime(23, 59, 59, JANEIRO, 31, 2022));
```

Habilita essa página, somente após envio de credenciais. O envio depende da criação dos acessos.<br />
Descomentar no código:
```
define('VESTIBULAR_VESTIBULANDO_FAIXA', false);
```

e comentar:

```
// define('VESTIBULAR_VESTIBULANDO_FAIXA', time() > mktime(0, 0, 0, JANEIRO, 28, 2022) && time() < mktime(23, 0, 0, FEVEREIRO, 5, 2022));
```

Ou vice versa. Para esse caso, Dia 31/01 - Habilita faixa e página para Informações da Prova.<br />

Twig referente a faixa de Informações de Vestibular:
**(\views\graduacao\shared\aviso-vestibulando.twig)**
Alterar datas nesse twig.<br />
O botão dessa faixa redireciona para a página de Informações de Vestibular - https://www.fiap.com.br/graduacao/vestibular/#informacoes


### 8. 02/02 - Penúltimo dia para inscrição
Banner com a contagem regressiva: **"Amanhã é o último dia"**<br />
Twig: vestibular-counter.php<br />
Variavél: VESTIBULAR_INSCRICOES_PENULTIMO_DIA<br />
Em vestibular.php:
```
define('VESTIBULAR_INSCRICOES_PENULTIMO_DIA', time() >= mktime(0, 0, 0, FEVEREIRO, 2, 2022) && time() <= mktime(23, 59, 59, FEVEREIRO, 2, 2022));
```
Botão do banner redireciona para página de Graduação e Botão da Faixa redireciona para Informações de Vestibular.


### 9. 03/02 - Último dia para inscrição <br />
Banner com a contagem regressiva: **"HOJE é o último dia".**<br />
As inscrições devem encerrar às 23h59 e some botão de Inscreva-se e aparece faixa "Saiba Antes" - para abrir modal de lead.<br />

Twig: vestibular-counter.php<br />
Variavél: VESTIBULAR_INSCRICOES_ULTIMO_DIA<br />
Em vestibular.php:<br />
```
define('VESTIBULAR_INSCRICOES_ULTIMO_DIA', time() >= mktime(0, 0, 0, FEVEREIRO, 3, 2022) && time() <= mktime(23, 59, 59, FEVEREIRO, 3, 2022));
```
Botão do banner redireciona para página de Graduação e Botão da Faixa redireciona para Informações de Vestibular.<br />


### 10. 04/02 - Sexta-feira (dia anterior a prova)<br />
Banner (retira contagem regressiva) e mensagem: **"Acontece nesse sábado" - 05/02**<br />
Twig: vestibular-dia-prova.twig<br />
Variavél: VESTIBULAR_PROVA_DIA_ANTERIOR<br />
Em vestibular.php:<br />
```
define('VESTIBULAR_PROVA_DIA_ANTERIOR', time() > mktime(0, 0, 0, FEVEREIRO, 4, 2022) && time() <= mktime(11, 00, 0, FEVEREIRO, 5, 2022));
```
Botão do banner e faixa redireciona para página Informações de Vestibular.<br />


### 11. 05/02 - Prova<br />
Banner **"Resultado da Prova - 08 de Fevereiro"**<br />
twig: vestibular-resultado.twig<br />
Variável: VESTIBULAR_PROVA<br />
Em vestibular.php:<br />
```
define('VESTIBULAR_PROVA', time() > mktime(23, 00, 0, FEVEREIRO, 5, 2022) && time() < mktime(10, 0, 0, FEVEREIRO, 8, 2022));
```
Botão do banner redireciona para página de Graduação.<br />

### 12. 08/02 - Lista aprovados<br />
Banner **"Resultado da Prova | Confira Lista de Aprovados | Matrícula até 18 de fevereiro"**<br />

twigs: vestibular-aprovados.twig<br />
vestibular-inscreva-se.twig<br />

Libera Menu /graduacao/vestibular<br />

*Faixa na Home redireciona para página:<br />
/graduacao/resultado-e-matricula/<br />

Variável: VESTIBULAR_PROVA_RESULTADO<br />
em vestibular.php<br />
```
define('VESTIBULAR_PROVA_RESULTADO', time() < mktime(10, 0, 0, FEVEREIRO, 8, 2022));
```
Botão encaminha para página:<br />
/graduacao/lista-de-aprovados-vestibular/ + Faixa "Saiba Antes"<br />


### 13. Na página de "Graduação" no item "Vestibular"<br />
Links: <br />
- Informações Gerais - /graduacao/vestibular/ <br />
- Lista de aprovados - /graduacao/lista-de-aprovados-vestibular/<br />
- Matrícula Online - /graduacao/matricula-online/<br />

### 14 - Banner **"Resultado da Prova"** permanece até o dia 18 de fevereiro até 23h59<br />



## Quem conhece esse processo

- Priscila Alavarce Bottaro <priscila.bottaro@fiap.com.br> 
( [Chat do Teams](https://teams.microsoft.com/l/chat/0/?users=priscila.bottaro@fiap.com.br) )<br />
- Daniela Verissimo <daniela.verissimo@fiap.com.br>
( [Chat do Teams](https://teams.microsoft.com/l/chat/0/?users=daniela.verissimo@fiap.com.br) )
