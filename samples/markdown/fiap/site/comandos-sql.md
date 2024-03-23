# Comandos SQL

Esta página é referente aos comandos SQL comuns para a base de dados do site da FIAP. 

!!! warning "Cuidados importantes"
    Antes de executar em produção qualquer comando SQL desta página, o ideal é executar em
    um ambiente de testes para confirmar o resultado esperado!
    
    Para isto temos disponível em *192.168.60.11* um banco de homologação. 
    
    Acesse com seu usuário e senha para realizar os devidos testes.

## Extrair base de Lead

Os leads captados pelo site da fiap são armazenados em duas tabelas:

- **fiap_lead**: Armazena os meta-dados do lead, como os campos que compõem os registros,
descrição do formulário que gerou o lead, url da página para retorno após o cadastro,
etc.
- **fiap_lead_informacao**: Tabela relacionada com a citada anteriormente, no qual contém 
os dados dos campos informados na tabela **fiap_lead**. Esta tabela deve ser pivotada para 
obter a informação de todos os campos que formam o registro.

Abaixo um exemplo de como extrair dados de alguns campos de um determinado formulário com `ID 5`.

Observe que os campos que serão pivotados devem existir no formulário que gerou o lead
e correspondem aos campos informados na coluna `campos` da tabela **fiap_lead**.

!!! warning
    Trocar os campos e o ID para atender a sua necessidade.

```sql
SELECT * FROM (
    SELECT
      fiap_lead_informacao.key,
      MIN(CASE WHEN fiap_lead_informacao.campo = 'nome' THEN fiap_lead_informacao.valor ELSE NULL END) AS 'nome',
      MIN(CASE WHEN fiap_lead_informacao.campo = 'email' THEN fiap_lead_informacao.valor ELSE NULL END) AS 'email',
      MIN(CASE WHEN fiap_lead_informacao.campo = 'telefone' THEN fiap_lead_informacao.valor ELSE NULL END) AS 'telefone',
      MIN(CASE WHEN fiap_lead_informacao.campo = 'curso' THEN fiap_lead_informacao.valor ELSE NULL END) AS 'curso',
      DATE_SUB(fiap_lead_informacao.data, INTERVAL 3 HOUR) AS data
    FROM fiap_lead_informacao
    WHERE fiap_lead_informacao.id_lead = 5
    GROUP BY fiap_lead_informacao.key
) AS tb 
GROUP BY tb.nome, tb.email, tb.curso
ORDER BY tb.data
```

Exemplo com alguns filtros

```sql
SELECT * FROM (
    SELECT
      fiap_lead_informacao.key,
      MIN(CASE WHEN fiap_lead_informacao.campo = 'nome' THEN fiap_lead_informacao.valor ELSE NULL END) AS 'nome',
      MIN(CASE WHEN fiap_lead_informacao.campo = 'email' THEN fiap_lead_informacao.valor ELSE NULL END) AS 'email',
      MIN(CASE WHEN fiap_lead_informacao.campo = 'telefone' THEN fiap_lead_informacao.valor ELSE NULL END) AS 'telefone',
      MIN(CASE WHEN fiap_lead_informacao.campo = 'curso' THEN fiap_lead_informacao.valor ELSE NULL END) AS 'curso',
      DATE_SUB(fiap_lead_informacao.data, INTERVAL 3 HOUR) AS data
    FROM fiap_lead_informacao
    WHERE fiap_lead_informacao.id_lead = 5
    GROUP BY fiap_lead_informacao.key
) AS tb 
WHERE tb.data >= '2022-02-01 00:00:00'
    AND tb.email NOT IN 
    (
        'x01mp3rx0z@mailto.plus', 
        'wityneii@gmail.com', 
        'puschnoishura@andreicutie.com',
        'trex500@2wslhost.com',
        'samano@massagefin.site',
        'masterosho@hotmail.red',
        'sample@email.tst', 
        'wapiti2021@mailinator.com', 
        'foo-bar@example.com', 
        'dedklokkk@ffo.kr', 
        'pbrendaleeo0c7dpu8uk857e8@outlook.com',
        'AudiaOhlinger836@aol.com'
    )
    AND tb.nome NOT IN ('ZAP')
    AND tb.nome NOT LIKE '%response%'
    AND tb.nome NOT LIKE '%print(%'
    AND tb.nome NOT LIKE '%click%'
    AND LENGTH(tb.nome) > 0
GROUP BY tb.nome, tb.email, tb.curso
ORDER BY tb.data
```

## Extrair lead de MBA

```sql
SELECT 
    nome, email, MAX(data) AS data
FROM mba_novidades
WHERE mba_novidades.email NOT IN 
(
    'x01mp3rx0z@mailto.plus', 
    'wityneii@gmail.com', 
    'puschnoishura@andreicutie.com',
    'trex500@2wslhost.com',
    'samano@massagefin.site',
    'masterosho@hotmail.red',
    'sample@email.tst', 
    'wapiti2021@mailinator.com', 
    'foo-bar@example.com', 
    'dedklokkk@ffo.kr', 
    'pbrendaleeo0c7dpu8uk857e8@outlook.com',
    'AudiaOhlinger836@aol.com',
    'AyeshaNajera500@yahoo.com',
    'qewwekatoq@outlook.com',
    'bajkogefaw@outlook.com',
    'carrqlottie@outlook.com',
    'olegrzyka@outlook.com',
    'teste@fiap.com.br',
    'chkheidzea83@mail.ru',
    'evlasov3zr@outlook.com',
    'nikitapavlov0p@outlook.com',
    'talor2m0n1ey4uy@outlook.com',
    'htiera2h5758uy0o@outlook.com',
    'klehuaai6d26i7q8kj@outlook.com',
    'hjonnellh879a47@outlook.com',
    'oleyna5bv9co818a3o@outlook.com',
    'lakeith7y6ai4u7c@outlook.com',
    'josue90bei7m7k@outlook.com',
    'xlois7u3x4w0@outlook.com',
    'zrobynne50z2r21ko4@outlook.com',
    'arlethau13loy9y1u2m@outlook.com',
    'mano.rasta@mail.ru',
    'donor090722@mail.ru',
    'tveronia5ut6ueu3is@outlook.com',
    'bretton85e209e0y9@outlook.com',
    'ideliae5c1i046@outlook.com',
    'foo-bar@example.com0W45pz4p',
    'Onadjaedonnaex7364@gmail.com',
    'tienlienhunggz155@gmail.com',
    'rgerron3uv518r80@outlook.com',
    'Adashkaibettyec3370@gmail.com',
    'Iviktorijaususanun3412@gmail.com',
    'vaytripo66@gmail.com',
    'immanuelleonard79@gmail.com',
    'bereniceevarana@gmail.com',
    'jsjsjsjsnsb29@gmail.com',
    'joey28154@gmail.com',
    'yankovskirahal7@gmail.com',
    'cbastror@gmail.com',
    'adamsgytc@gmail.com',
    'blick13.bermuda@gmail.com',
    'arianazmmrmn@gmail.com',
    'alvarezwolf254638@gmail.com',
    'kimabbott10981@gmail.com',
    'clyndon855@gmail.com',
    'ashleeatkins67@gmail.com',
    'cava2563@gmail.com',
    'elsiejbairde@gmail.com',
    'guystewart852947@gmail.com',
    'teste@teste.com',
    'henrycox249203@gmail.com',
    'GabriellePButlerj@gmail.com',
    'AngelRobertsT@gmail.com',
    'margaretheomhve18@gmail.com',
    'maryannandrum82@gmail.com',
    'rochellecjpdd82@gmail.com',
    'shirline9zjna57@gmail.com',
    'sherioycq411@gmail.com',
    'jessalynh8dkl69@gmail.com',
    'tristanrobenay27lb1fj@gmail.com',
    'dagmarromeoe93k6z2@gmail.com',
    'leahtolbeverley31g56y@gmail.com',
    'ffrancine988@gmail.com',
    'barrettg282@gmail.com',
    'eha07799@gmail.com',
    'teste_novo@teste.com',
    'gm1210538@gmail.com',
    'cousequessw@gmail.com',
    'moodydebra980@gmail.com',
    'colinwilkinson618@gmail.com',
    'markitalinseymarkita259@gmail.com',
    'minervapayne418@gmail.com',
    'ixtudf57a1foivusiqvvwalh780ervjoi58u@burpcollaborator.net',
    'rfj2tkjyk7xa6mvy3qu14fubjacg3xvqu7kw@burpcollaborator.net',
    'jQurtJCb@burpcollaborator.net',
    'yUvLRAgW@burpcollaborator.net',
    'rm6803077@gmail.com',
    'lenardbarker0@gmail.com',
    'marknichols7140@gmail.com',
    'estimated1992195rabe@gmail.com',
    'supiciansbc@gmail.com',
    'mosidicejd@gmail.com',
    'officrieryss@gmail.com',
    'winter@example.com',
    '2f9a237b627180361f3abd61172bee1e.roopert@ssemarketing.net',
    '0b290c8fc7e480385e6e11b7cf25e9bf.roopert@ssemarketing.net',
    'vendas@v3brindes.com.br',
    '95e713d17a7eff8e12099aa977284addprx@ssemarketing.net',
    'ae7d4516a04bec8b5229edbad49f8890prx@ssemarketing.net',
    'contato@anndobrasil.net.br',
    'comercial@m7vida.com.br',
    'contato@jota.info',
    'contato@fastsold.com.br',
    'agenciadesolucoesdigitais@gmail.com',
    'fabiotavares@estudiosp.com.br',
    'netsparker@example.com',
    'raimonoliver@yahoo.com',
    'vendas@qapbrindes.com.br',
    'atendimento@fenixmult.com.br',
    'parceriasescritoriodigital@gmail.com',
    'builderall.rivello@gmail.com',
    '2chdigital@gmail.com',
    'convite@conhecimentoesucesso.com.br',
    'jjuridico9@gmail.com',
    'apjosesantanaprofessor@gmail.com',
    'bit10ads@bit10ads.io',
    'bit10@bit10.io',
    'iranjunior1980@gmail.com',
    'camilinhacosta1@hotmail.com',
    'contatocelular@zipmail.com.br',
    'rodrigo_antoni@hotmail.com',
    'contatocelular@zipmail.com.br',
    'queops_souza@yahoo.com.br',
    'creditoparaempresasnegativadas@gmail.com',
    'contato@leandroreis.adv.br',
    'praticaeleitoral@casadodireito.com.br',
    'egterraplenagem@hotmail.com',
    'honestidadeequalidade@gmail.com',
    'investirelucrar@ig.com',
    'david.martin@ilvekpnmwdgj.tv',
    'jhonwigleff2013@hotmail.com',
    'contato@aumentopenianorapido.com.br',
    'oliveiramarcus20@yahoo.com.br',
    'sara.costa28@zebyinbox.com',
    'glennie.reinger27@devaza.id',
    'tertuliano.silva51@globizsolution.com',
    'socialfire@yahoo.com',
    'investimentozurc@gmail.com',
    'a.l.e.x.fir.st.ano.vof.ficework@gmail.com',
    'lgvg10@gmail.com',
    'trafegosec2019@gmail.com',
    'contato@totemmania.com.br',
    'iammihack@mitakian.com',
    'cadqumiroy@outlook.com',
    'aprilp81pcira@outlook.com',
    'donovan.j100@yahoo.com',
    'beytadocel@outlook.com',
    'teste@email.com',
    'vanrhea369@aol.com',
    'jejbeqisaf@outlook.com',
    'teste@mail.com',
    'aaa@aaa.com',
    'testeprodws@email.com',
    'teste@apiprodreact.com'
) 
AND mba_novidades.email NOT LIKE '%fiap.com.br'
AND mba_novidades.email NOT LIKE '%example.com'
GROUP BY nome, email
ORDER BY data
```

## Duplicar a grade de uma disciplina (Graduação Presencial e ON)

Caso haja alteração da grade de disciplinas de algum curso em Graduação, por motivo de histórico,
é duplicado os registros da base (tabelas no script abaixo) e o código alterado no admin do WordPress.

Para realizar a duplicação, basta executar o SQL abaixo alterando apenas as duas primeiras variáveis.

```sql
# ************************************************************************************
# Alterar somente estas variáveis abaixo
#
SET @id_curso = 1234; # ID do curso atual. Ex: 1234
SET @ano = 2018;
# ************************************************************************************

# Variáveis inicializadas pelo Script
SET @fator = 0;
SET @id_novo_curso = 0;

SELECT MAX(cod_disciplina) INTO @fator FROM vestibular_disciplina;

SELECT MAX(cod_curso) + 1 INTO @id_novo_curso FROM vestibular_curso;

INSERT INTO vestibular_curso (cod_curso, nome, cod_coordenador, cod_diretor, ano) 
SELECT @id_novo_curso, nome, 1, 2, @ano FROM vestibular_curso WHERE cod_curso = @id_curso;

INSERT INTO vestibular_disciplina (cod_disciplina, cod_curso, nome, descricao, serie)
SELECT (cod_disciplina + @fator), @id_novo_curso, nome, descricao, serie
FROM vestibular_disciplina WHERE cod_curso = @id_curso;

INSERT INTO vestibular_disciplina_informacao (cod_disciplina, cod_informacao)
SELECT (vestibular_disciplina_informacao.cod_disciplina + @fator), vestibular_disciplina_informacao.cod_informacao
FROM vestibular_disciplina 
INNER JOIN vestibular_disciplina_informacao ON vestibular_disciplina.cod_disciplina = vestibular_disciplina_informacao.cod_disciplina
WHERE vestibular_disciplina.cod_curso = @id_curso; 

# O id para o novo curso será exibido com o comando abaixo
SELECT @id_novo_curso;
```

## Inscritos no Eu Capacito ou Learn Tech (Antigo Ceará Tech) e com graduação completa

```sql
SELECT 
    CONCAT(fiapead_user.firstname, fiapead_user.lastname) AS nome,
    fiapead_user.email,
    fiapead_user_info_data.data
FROM fiapead_user 
INNER JOIN fiapead_user_info_data
    ON fiapead_user.id = fiapead_user_info_data.userid
    AND fiapead_user_info_data.fieldid = 18
    AND fiapead_user_info_data.data IN (
        'Graduação - Completo', 
        'Pós-graduação, Mestrado ou Doutorado - Completo',
        'Pós-graduação, Mestrado ou Doutorado - Incompleto'
    )
INNER JOIN fiapead_user_info_field
    ON fiapead_user_info_data.fieldid = fiapead_user_info_field.id
WHERE fiapead_user.id IN (
    SELECT fiapead_user_info_data.userid
    FROM fiapead_user_info_data
    WHERE fiapead_user_info_data.fieldid = 12
        AND fiapead_user_info_data.data IN ('Programa de Parceria Ceará Tech')
);


SELECT 
    CONCAT(fiapead_user.firstname, fiapead_user.lastname) AS nome,
    fiapead_user.email,
    fiapead_user_info_data.data
FROM fiapead_user 
INNER JOIN fiapead_user_info_data
    ON fiapead_user.id = fiapead_user_info_data.userid
    AND fiapead_user_info_data.fieldid = 18
    AND fiapead_user_info_data.data IN (
        'Graduação - Completo', 
        'Pós-graduação, Mestrado ou Doutorado - Completo',
        'Pós-graduação, Mestrado ou Doutorado - Incompleto'
    )
INNER JOIN fiapead_user_info_field
    ON fiapead_user_info_data.fieldid = fiapead_user_info_field.id
WHERE fiapead_user.id IN (
    SELECT fiapead_user_info_data.userid
    FROM fiapead_user_info_data
    WHERE fiapead_user_info_data.fieldid = 12
        AND fiapead_user_info_data.data IN ('Programa Eu Capacito')
)
```
## Lead do SHIFT

```sql
SELECT *
FROM Lead
ORDER BY Codigo DESC;
```
