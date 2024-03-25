# Testes unitários
Testes unitários são testes da menor parte testável de um sistema, no nosso caso, as funções.

Para cada função escrita na plataforma, deve-se escrever seus respectivos testes e cenários,
afim de testar o sistema de forma mais rápida e automatizada.

## Configuração Inicial
O Moodle utilizada o framework PHPUnit para realizar os testes unitários. Para configurá-lo,
siga as instruções abaixo.

### Adicionando configurações básicas ao config.php

Para conseguir rodar os testes unitários, você deve adicionar as seguintes configurações no arquivo
config.php, localizado na raiz do projeto, na etapa **9. PHPUNIT SUPPORT**:

```php
<?php  // Moodle configuration file

...

 $CFG->phpunit_prefix = 'phpu_';
 $CFG->phpunit_dataroot = 'C:\xampp\htdocs\eaddatateste';

...

```

A primeira linha, onde configuramos "phpu_" como prefixo, é utilizado para a criação do banco de testes,
já a segunda, onde adicionamos "C:\xampp\htdocs\eaddatateste", é o caminho para o diretório onde será
armazenado o cache gerado durante os testes. (Esse diretório deve existir na sua máquina).

### Composer install

Caso não tenha feito, rode o comando "composer install" na raiz do projeto, para que o PHPUnit seja
adicionado ao seu projeto.

### INTL

Caso você esteja utilizando o xampp, talvez seja necessário habilitar o *intl*, para isso:

- Descomente a linha extension=intl

- Configure o intl da seguinte forma:

```ini
[intl]
intl.default_locale = en_utf8
; This directive allows you to produce PHP errors when some error
; happens within intl functions. The value is the level of the error produced.
; Default is 0, which does not produce any errors.
intl.error_level = E_WARNING
;intl.use_exceptions = 0
```

### Base de dados para teste
O PHPUnit gera uma base cópia da base de dados que é destinada especificamente para rodar os testes
com os dados desejados. Essa base é criada vazia, e será alimentada a partir dos testes que
serão executados.

Ela é gerada a partir dos arquivos install.xml e install.php, onde são guardadas as estruturas
das tabelas, por isso, é importante que esses arquivos estejam sempre atualizados.

Caso a base de testes não tenha sido gerada ainda, ou algum plugin tenha sido criado ou tenha
a versão atualizada, ao tentar rodar um teste, o PHPUnit irá solicitar que a base de testes
seja gerada com a seguinte mensagem:

```console
php admin/tool/phpunit/cli/init.php
```

Quando isso acontecer, rode este comando na raiz do seu projeto e aguarde sua finalização.

!!! warning "Importante"
    Certifique-se de que há apenas uma pessoa rodando este comando, caso contrário, irá ocorrer um
    erro e a base de testes pode não ser gerada corretamente.

## Metodologias
Agora que já temos o ambiente configurado para que nossos testes possam ser executados, vamos
entender como a escrita dos testes é estruturada. Para isso, vamos utilizar duas metodologias:
TDD e BDD.

###TDD
O TDD (Test Driven Development ou Desenvolvimento Orientado a Testes) é uma metodologia que
nos orienta que, antes mesmo de começarmos a programar a função, iremos definir as 
funcionalidades que ela deve ter, a partir dos testes. Para cada teste, iremos seguir 3 passos:

<br>

**Passo 1**. Escreva o teste para uma das funcionalidades da função. Ao rodá-lo, o teste deve
falhar, pois a função ainda nem mesmo existe.
```php
<?php

public function test_somar_dois_numeros__dois_numeros_inteiros() {
    $soma = somar_dois_numeros(1, 4);
    
    $this->assertEquals(5, $soma);
}
```

<br>

**Passo 2**. Faça o seu teste passar, da maneira mais simples possível. Isso serve como uma forma
de "testar o teste", garantindo que quando a função retornar o que ele espera, ele irá passar.
```php
<?php

public function test_somar_dois_numeros__dois_numeros_inteiros() {
    $soma = somar_dois_numeros(1, 4);
    
    $this->assertEquals(5, $soma);
}

function somar_dois_numeros(int $numero_1, int $numero_2) {
    return 5;
}
```

<br>

**Passo 3**. Por fim, implemente as funcionalidades desejadas na sua função, refatore o que achar
necessário e aplique as melhores práticas.
```php
<?php

public function test_somar_dois_numeros__dois_numeros_inteiros() {
    $soma = somar_dois_numeros(1, 4);
    
    $this->assertEquals(5, $soma);
}

function somar_dois_numeros(int $numero_1, int $numero_2) {
    return ( $numero_1 + $numero_2 );
}
```

###BDD
O BDD (Behavior Driven Development ou Desenvolvimento Guiado por Comportamento) é uma metodologia
utilizada para que as regras de negócio sejam integradas com o nosso código, focando, sobretudo,
no comportamento.

Com ele, nós introduzimos os **cenários** nos nossos testes, que irão ajudar a definir quais testes
fazer, como testar e aumentar a legibilidade do código.

Os cenários do BDD possuem uma estrutura para serem escritos, que normalmente seguem 3 blocos:
**dado**, **quando** e **então**. Para nós, o BDD segue a seguinte estrutura:

**Cenário**: Descrição breve do cenário;

**Dado**: Descrição um pouco mais detalhada da função + o cenário;

**"E"s**: Descrição de itens que compõem aquele cenário, para facilitar o entendimento;

**Então**: O que se espera, qual será o resultado final.
```php
<?php

/**
* Cenário: Somar dois números inteiros e positivos
* 
* - Dado que o usuário tente somar dois números
* - E informe dois números
* - E os dois números são inteiros e positivos
* - Então a função deve retornar a soma dos números
*/
public function test_somar_dois_numeros__dois_numeros_inteiros() {
    $soma = somar_dois_numeros(1, 4);
    
    $this->assertEquals(5, $soma);
}
```

Assim, é muito mais fácil entender o que está sendo testado em cada função de teste, e o que se
espera dele, sem precisar ler o código.

Como dito anteriormente, o BDD serve para integrar as regras de negócio com o código, por isso,
são sempre bem-vindas na descrição, e é fortemente encorajado que cada regra de negócio seja
validada dentro dos testes.

Imagine que seja uma regra do negócio que, ao informar um número negativo, deve ser exibido
um erro para o usuário. Para isso, teríamos um cenário de teste parecido com este:

```php
<?php

/**
* Cenário: Somar dois números inteiros, em que um deles é negativo
* 
* - Dado que o usuário tente somar dois números
* - E informe dois números
* - E os dois são inteiros
* - E um dos números é negativo
* - Então a função deve retornar um erro com a mensagem "Número inválido"
*/
public function test_somar_dois_numeros__dois_numeros_inteiros_com_um_negativo() {
    $this->expectExceptionMessage("Número inválido");

    somar_dois_numeros(-1, 4);
}
```

## Escrevendo os testes
Após entendermos as metodologias utilizadas, podemos iniciar a escrita dos testes. Para os
exemplos abaixo, considere que os testes serão escritos para uma função cujo objetivo é retornar
se um valor informado pelo usuário é um RM de MBA válido para a FIAP. Os RMs de MBA possuem dois
ranges: de 30000 até 49999 ou de 330000 até 499999.

### Estrutura de arquivos
No moodle, os testes devem ficar dentro do plugin a que se referem, numa pasta nomeada *tests*.
Todos os arquivos devem terminar com o sufixo *_test.php*.

É comum que os arquivos de teste sejam separados por contexto, ou por função.

Todos os arquivos de teste devem herdar da classe *advanced_testcase*, classe do PHPUnit com
integrações do Moodle.

O nome da classe deve iniciar com o nome do plugin, seguido pelo nome do arquivo e por fim
com o sufixo *_testcase*.

```php
<?php

/**
 * Este arquivo realiza todos os cenários envolvendo
 * verificar se um valor é um RM válido.
 *
 * @autor Nome do autor <email@fiap.com.br>
 */

global $CFG;

// Importando as funções da plataforma
require_once __DIR__ . '/../../../fiapautoload.php';

class local_meuplugin_is_rm_testcase extends \advanced_testcase {
    // @TODO
}
```

### Cenários
O próximo passo é escrever todos os cenários possíveis (que podem acontecer) e, até mesmo,
alguns impossíveis, em que a função deve estar preparada para tratar e retornar um erro
se necessário.

Para isso, pense no parâmetro que temos neste exemplo e imagine todos
os valores - válidos e inválidos - que podem ser informados por usuários que estejam utilizando
o sistema normalmente e também por usuários que queiram causar erros propositalmente.

Neste caso, podemos considerar que usuários possam informar:

- valores nulos ou vazios (exemplo de usuário que deseja causar um erro propositalmente);
- rm dentro do primeiro range;
- rm dentro do segundo range;
- rm fora dos ranges;
- rm com "rm" na frente (ex: rm12345);
- rm apenas com números;

Perceba que, após mapear os cenários, começamos a ter uma ideia de quais funcionalidades
a função deve atender, e como será a sua estrutura.

Finalizando o mapeamento, vamos criar um teste para cada cenário, utilizando o BDD. O arquivo
de teste irá ficar parecido com algo assim:

```php
<?php

/**
 * Este arquivo realiza todos os cenários envolvendo
 * verificar se um valor é um RM válido.
 *
 * @autor Nome do autor <email@fiap.com.br>
 */

global $CFG;

// Importando as funções da plataforma
require_once __DIR__ . '/../../../fiapautoload.php';

class local_meuplugin_is_rm_testcase extends \advanced_testcase {
    /**
     * Cenário: Informando rm vazio
     * 
     * - Dado que o sistema tente verificar se um RM é válido
     * - E o usuário informe uma string vazia
     * - Então a função deve retornar um erro com a mensagem "Informe um RM"
     */
    public function test_is_rm__rm_vazio() {
        $this->expectExceptionMessage('Informe um RM');
    
        $this->assertTrue(is_rm(''));
    }
    
    ...

    /**
     * Cenário: RM válido no primeiro range
     * 
     * - Dado que o sistema tente verificar se um RM é válido
     * - E o usuário informe um rm
     * - E o rm é válido no primeiro range
     * - Então a função deve true
     */
    public function test_is_rm__rm_valido_primeiro_range() {
        $this->assertTrue(is_rm(345442));
    }
    
    ...
}
```
<sub> Cada teste deve ser nomeado com a seguinte estrutura: test_nome_da_funcao__cenario. </sub>

Com todos os testes escritos, basta seguirmos a metodologia TDD descrita anteriormente: rodamos
os testes para que falhem, fazemos funcionarem com o menor código possível e, por último,
refatoramos a função.

Quando todos os testes passarem, saberemos que a nossa função está funcional, atendendo as
regras do negócio e preparada para todos os cenários descritos.

!!! info "Hora de praticar"
    Escreva cada cenário e teste listado para essa função, afim de praticar as metodologias TDD
    e BDD. Após finalizá-los, escreva a função final e veja se seus testes estão rodando com sucesso.

### setUp
Essa função é utilizada para rodar um comando específico - ou um conjunto de comandos - antes de
cada teste, para que o bloco de código não tenha que ser repetido dentro de cada função.

Ele é muito útil quando estamos realizando integração com o banco de dados, ou precisamos gerar
dados para que o nosso teste funcione adequadamente.

```php
<?php

/**
 * Este arquivo realiza todos os cenários envolvendo
 * verificar se um valor é um RM válido.
 *
 * @autor Nome do autor <email@fiap.com.br>
 */

global $CFG;

// Importando as funções da plataforma
require_once __DIR__ . '/../../../fiapautoload.php';

class local_meuplugin_is_rm_testcase extends \advanced_testcase {
    public function setUp() {
        echo "Iniciando testes";
    }
    
    /**
     * Cenário: Informando rm vazio
     * 
     * - Dado que o sistema tente verificar se um RM é válido
     * - E o usuário informe uma string vazia
     * - Então a função deve retornar um erro com a mensagem "Informe um RM"
     */
    public function test_is_rm__rm_valido_primeiro_range() {
        $this->expectExceptionMessage('Informe um RM');
    
        $this->assertTrue(is_rm(''));
    }
    
    ...
}
```

## Integração com o banco
No exemplo acima não precisamos realizar nenhuma integração com o banco (consultar, inserir, etc.),
porém, é muito comum que essa integração precise acontecer, para que os testes fiquem mais fiéis à
realidade.

Imagine que, ao invés de ter os ranges fixos no código, foi solicitado que os ranges ficassem
armazenados em uma tabela no banco de dados.

Para atender essa solicitação, a função deverá se integrar com o banco de dados, de modo a
consultar e inserir registros, conforme cada cenário.

### Manipulando dados no banco
Quando se está executando testes, todos os dados serão manipulados nas tabelas que possuem
o prefixo *phpu_*, configurado anteriormente.

Nos testes, podemos manipular os dados do banco de duas formas: utilizando funções que
já existem e utilizamos no dia a dia, localizadas dentro da locallib de cada plugin, ou utilizando
os **Generators**.

#### Generators
São funções prontas que geram dados no banco de forma mais rápida e simplificada, para facilitar
a escrita dos testes. Dentro deles, existem dois tipos:

##### Generators nativos
Criados a partir da integração entre o PHPUnit e o Moodle. São funções que manipulam
tabelas nativas, como: user, course, category, etc. Essas funções são chamadas a partir da
função **getDataGenerator()**.

```php
<?php
    ...
    
    public function test_is_usuario_em_curso__usuario_esta_no_curso() {
        $usuario = $this->getDataGenerator()->create_user();
        $curso   = $this->getDataGenerator()->create_course();
        
        $this->getDataGenerator()->enrol_user($usuario->id, $curso->id);
    
        $this->assertTrue(is_usuario_em_curso($usuario->id, $curso->id));
    }
    
    ...
}
```

##### Generators personalizados
Criados pelo time de plataforma dentro de cada plugin, para manipular tabelas próprias
ou para criar generators que não existiam nativamente.

Esses generators ficam dentro da pasta */tests/generator/lib.php* de cada plugin e são chamados
a partir da função **getDataGenerator()->get_plugin_generator('local_meuplugin')**.

```php
<?php
    ...
    
    public function test_listagem_eventos_e_atividades_futuros_sem_filtros_com_eventos(){
        $this->getDataGenerator()->get_plugin_generator('local_calendar')->create_event([
            'user_id'   => $this->user->id,
            'timeopen'  => $this->tomorrow_in_timestamp,
            'timeclose' => $this->tomorrow_in_timestamp
        ]);

        $this->assertEquals(1, get_calendar_events_and_activities_events_total($this->user->id));
    }
    
    ...
}
```
<sup> Exemplo de teste do plugin local_calendar </sup>

### Apagando dados após os testes
O ideal é que, para cada teste criado, o banco seja resetado logo após a sua finalização. Para isso,
utilize o seguinte comando (geralmente alocado dentro do setUp):

```php
<?php

...

class local_meuplugin_is_rm_testcase extends \advanced_testcase {
    public function setUp() {
        $this->resetAfterTest();
    }
    
    ...
}
```

!!! info "Hora de praticar"
    Escreva os novos cenários de teste que surgiram com a integração com o banco e adapte sua função
    para que ela comece a consultar os dados do banco. Além disso, construa um generator para inserir
    os ranges para os testes.

## Erros comuns

### Can not use database for testing, try different prefix

Este erro normalmente ocorre quando mais de uma pessoa tentou gerar a base de testes ao mesmo
tempo, neste caso, rode o seguinte comando na raiz do seu projeto:

```console
php admin/tool/phpunit/cli/util.php --drop
php admin/tool/phpunit/cli/util.php
```

Isso irá apagar a base de testes atual e gerar uma nova logo em seguida.

!!! warning "Importante"
    Certifique-se de que há apenas uma pessoa rodando este comando, caso contrário, irá ocorrer um
    erro e a base de testes pode não ser gerada corretamente.
