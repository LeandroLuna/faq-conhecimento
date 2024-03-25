# Modelo preditivo de evasão cursos online 🔮

Com o objetivo de **reduzir o número de evasão de estudantes** da graduação online e presencial, foi criado um estudo para levantar algumas hipóteses sobre quais **variáveis** poderiam discriminar o comportamento de um estudante que evadiu versus um estudante que se formou. Esse estudo trouxe alguns insights e features importantes para ser implementado um modelo preditivo de evasão. 

## Motivação do projeto 🚀

A questão da evasão é um ponto muito importante para a melhorar a qualidade dos cursos e da faculdade como um todo. A evasão pode tanto afetar de forma acadêmica, como financeira. Visando melhorar a taxa de retenção, que em **2022 tivémos uma taxa de 4%**, foi criado um **modelo preditivo de evasão** visando identificar quem são esses possíveis alunos que poderiam vir a evadir, para que a equipe do Talent Lab e acadêmica possam entrar em contato com esses estudantes e realizar alguma ação preventiva com o objetivo de **retenção**.

Com base no estudo realizado sobre a evasão, foi identificado que a graduação online possui uma tendência de **crescimento exponencial** no número de saídas ao longo do ano. Com base nessa evidência, o primeiro modelo preditivo foi direcionado para os cursos onlines e posteriromente foi replicado para a graduação presencial.

## Sobre a base de dados 📊 

Para determinar a evasão de um estudante, é necessário analisar alguns "rastros" de comportamento que são evidênciados ao longo do curso. Como temos uma grande base histórica de dados, foram analisados dados sobre notas, consumo de conteúdos na plataforma online (para os estudantes online), frequência de presença (para estudantes presenciais) e débitos financeiros. 

Para o estudo dos cursos online, a base de dados contém dados de 2017 até 2022. Para o estudo dos cursos presenciais, a base de dados contém dados de 2014 até 2022.

## Requisitos do ambiente 📋

Para executar os códigos desse projeto e não houver nenhum problema de dependências, as bibliotecas utilizadas devem estar nas seguintes versões no ambiente python:

- Pandas version: 2.0.3
- Scikit-learn version: 1.3.2
- NumPy version: 1.24.3
- Seaborn version: 0.12.2
- Matplotlib version: 3.7.2
- XGBoost version: 2.0.0
- Joblib version: 1.2.0

## Link do projeto 🎯

Para encontrar o projeto completo, acesse este link:

https://gitlab.fiap.com.br/cl1476/modelo-preditivo-evasao-fiap-on

Este projeto contém o notebook python **"Algoritmo_preditivo_de_evasão_-_Graduação_Online.ipynb"** com toda a criação do algoritmo preditivo e a aplicação "Aplicação_do_modelo_preditivo.py" para ser executada localmente no VSCODE e utilizar o modelo preditivo.

Para utilizar o modelo, basta subir a pasta do projeto localmente em uma IDE de texto (como o VSCODE por exemplo) e executar os seguintes comandos no terminal:

``` python

python -m venv venv
Set-ExecutionPolicy Unrestricted -scope process
venv\Scripts\activate
pip install -r requirements.txt
streamlit run Aplicação_do_modelo_preditivo.py

```
Ao executar a aplicação, o modelo está disponível para uso.

⚠️ Lembre-se que para o modelo preditivo **funcionar corretamente**, os **dados de entrada devem conter todas as variáveis** (exceto a Predição e Ranking) na mesma ordem descrita abaixo no dicionário de dados.

## Dicionário de dados 📖

**Modelo preditivo online:**

- **RM:** Matrícula do estudante.
- **MediaNotasAtividadesUpload:** Média de notas dos estudantes dentro da fase observada. Essa média é calculada com base na soma da nota obtida em cada atividade da fase pela contagem total de atividades entregue pelos estudantes. A fim de facilitar o entendimento, essa medida está normalizada em uma escala de 0 a 100%.
- **PercentualEntregaAtividadeUpload:** Porcentagem de entregas das atividades com base no total esperado dentro da fase.
- **TotalDisciplinas:** Número total de disciplinas (fases) acessadas até o momento da execução do algoritmo.
- **MediaPorcentagemVisualizacao:** Porcentagem de visualização média de conteúdos atingida. Essa medida está relacionada com a coluna “TotalDisciplinas”.
- **QtdDebitosDevedor:** Número total de débitos ativos devedores.
- **Predição:** Resultado do algoritmo preditivo de evasão.
- **Ranking:** O Ranking atribui um peso de importância para selecionar os estudantes com maior risco de evasão. O ranking utiliza a seguinte lógica sobre os status "Propenso a evadir":

    - Se **MediaNotasAtividadesUpload = 0**, então recebe peso 5.
    - Se **MediaNotasAtividadesUpload <= 50%**, então recebe peso 4.
    - Se **PercentualEntregaAtividadeUpload < 90%**, então recebe peso 3.
    - Se **MediaPorcentagemVisualizacao <= 40%**, então recebe peso 2.
    - Se **QtdDebitosDevedor >= 3**, então recebe peso 1.
    - Se nenhuma das condições, recebe 0.

A idéia é utilizar essas variáveis dentro de uma fase (em específico, fase 3) para analisar o desempenho dos estudantes logo no início do curso.

## Pré-processamento de dados 🛠️

Para o modelo de machine learning não obter resultados enviesados, foi aplicado a técnica de normalização **MinMaxScaler**. Essa técnica visa a transformação dos dados em uma mesma escala. Como temos dados em diversas escalas, essa técnica foi utilizada para transformar os dados e reduzir o viés introduzido por diferentes escalas entre atributos, contribuindo para um modelo mais preciso. 

Fórmula aplicada da normalização (onde x é igual ao valor do dado processado):

>
> y = (x – min) / (max – min)
>

**Desafios com a amostra de dados e desequilíbrio de classes** ⚠️

O volume total da amostra de dados após ser realizado o cruzamento das bases foi em um total de **1244 amostras para alunos formandos** e **470 alunos evadidos**. Esse volume é pouco representativo para criar um modelo de aprendizado de máquina, então foi realizado a técnica de oversampling nos dados (subamostragem) com o objetivo de aumentar o volume da base.

## Modelagem do algoritmo preditivo 🔮

Foram realizados várias técnicas de aprendizado de máquina supervisionado, tais como **KNeighborsClassifier, LogisticRegression, DecisionTreeClassifier, RandomForestClassifier, SVM** e **GradientBoostingClassifier(XGBoost)** em conjunto a **validação cruzada** para avaliar o desempenho do modelo.

Resultados do R-quadrado (R^2) da validação cruzada + algoritmos:

- KNN (R^2): 0.9931920781190412
- Regressão Logística (R^2): 0.9409196666400593
- SVM (R^2): 0.9489388120726202
- Random Forest (R^2): 0.9912473799197642
- Árvore de Decisão (R^2): 0.9912476755564622
- XGBoost (R^2): 0.974226688307273

O melhor modelo é: KNN com o valor 0.9931920781190412

**Foi selecionado o XGBoost pois seu R^2 de 0.97 não está enviesado.**

O XGBoost é um algoritmo de aprendizado supervisionado que implementa um processo chamado **Boosting** para gerar modelos precisos. Assim como outros algoritmos de boosting, o XGBoost usa árvores de decisão para seu modelo de conjunto. Cada árvore é um aprendiz fraco. O algoritmo segue construindo sequencialmente mais árvores de decisão, cada uma corrigindo o erro da árvore anterior até que uma condição de parada seja alcançada. Inclui diferentes penalidades de regularização para evitar overfitting onde essas regularizações de penalidade produzem treinamento bem-sucedido para que o modelo possa generalizar adequadamente. 

Para nosso modelo na qual 73% das amostras é de estudantes formandos e 27% evadidos, o XGBoost consegue lidar bem com o **desiquilíbrio de classes** pois o modelo atribui pesos mais altos às instâncias da classe minoritária, se concentrando mais na aprendizagem dessa classe, ajudando a compensar o desequilíbrio.

**Hiperparâmetros do modelo:**

``` python
model = XGBClassifier(scale_pos_weight=1, 
                      eval_metric="mlogloss",
                      booster="gbtree", 
                      n_estimators = 1000, 
                      n_features=20, 
                      gamma=1, 
                      min_split_loss=1, 
                      reg_lambda=1, 
                      colsample_bytree = 0.3, 
                      learning_rate=0.01, 
                      max_depth = 5, 
                      subsample =1, 
                      random_state=2, 
                      verbosity=0)
```

    
**Resultados do modelo:** ✅

> Acurácia: 94%
> 
> Curva ROC: 97%
>  
> Classe propenso a evadir: F1-Score: 87%
> 
> Classe propenso a se formar: F1-Score: 96%
> 

## Passo a passo da criação do projeto 📝

**Extração dos dados ⛏️**

_Extração dos dados no banco do Moodle:_

A seguir estão as querys utilizadas para construir a base histórica de dados utilizadas no notebook python:

**Notas**
Extração dos dados para construir a base de dados de notas dos estudantes online:

``` sql
SELECT 
    AtividadesEsperadas.NomeCurso,
    AtividadesEsperadas.Fase,
    AtividadesEsperadas.IdFase,

    ResumoAtividade.RM,
    ResumoAtividade.TotalAtividadesUploadEntregues,
    ResumoAtividade.MediaNotas AS 'MediaNotasAtividadesUpload',
    AtividadesEsperadas.TotalAtividadeseUploadEsperadas,
    ROUND((ResumoAtividade.TotalAtividadesUploadEntregues / AtividadesEsperadas.TotalAtividadeseUploadEsperadas), 2) AS 'PercentualEntregaAtividadeUpload',

    FastTestsResumo.TotalFastTestRealizados,
    FastTestsResumo.MediaNotas AS 'MediaNotasFastTest',
    AtividadesEsperadas.TotalQuizEsperados,
    ROUND((FastTestsResumo.TotalFastTestRealizados / AtividadesEsperadas.TotalQuizEsperados), 2) AS 'PercentualrealizadoFastTest' 
FROM    
(
    /*Sumarizando o total de atividades e quiz esperados por fase*/
    SELECT 
          fiapead_course_categories_resume.breadcrumb  AS 'NomeCurso',
          fiapead_course.fullname AS 'Fase',
          fiapead_course.id AS 'IdFase',
          COUNT(fiapead_assign.id) AS 'TotalAtividadeseUploadEsperadas',
          COUNT(fiapead_quiz.id) AS 'TotalQuizEsperados'
    FROM fiapead_course
    INNER JOIN fiapead_fiap_regras_course
        ON fiapead_fiap_regras_course.courseid = fiapead_course.id
        AND fiapead_fiap_regras_course.regraid = 2 
    INNER JOIN fiapead_course_categories_resume
        ON fiapead_course.category = fiapead_course_categories_resume.categorieid  
    INNER JOIN fiapead_course_modules
        ON fiapead_course_modules.course = fiapead_course.id 
        AND fiapead_course_modules.visible = 1
    INNER JOIN fiapead_modules 
        ON fiapead_modules.id  = fiapead_course_modules.module 
        AND fiapead_modules.id IN (1, 17)
    INNER JOIN fiapead_course_sections
        ON fiapead_course_modules.course = fiapead_course_sections.course
        AND fiapead_course_modules.`section` = fiapead_course_sections.id
    LEFT JOIN fiapead_assign 
        ON fiapead_assign.id = fiapead_course_modules.instance
        AND fiapead_course_modules.module = 1
        AND fiapead_assign.id NOT IN (  
            SELECT fiapead_assign.id
            FROM fiapead_assign 
            INNER JOIN fiapead_fiap_assign_config
                ON fiapead_fiap_assign_config.assignid  = fiapead_assign.id 
                AND (
                    (
                        fiapead_fiap_assign_config.configname = 'type'
                        AND fiapead_fiap_assign_config.value IN ('atividade_sub', 'DP_1', 'DP_2','sub-encontro-presencial-1', 'sub-encontro-presencial-2')
                    ) 
                    OR 
                    (
                        fiapead_fiap_assign_config.configname IN ('atividade_sub', 'DP_1', 'DP_2','sub-encontro-presencial-1', 'sub-encontro-presencial-2')
                    )
                )
    )           
    LEFT JOIN fiapead_quiz
        ON fiapead_quiz.id = fiapead_course_modules.instance
        AND fiapead_quiz.course = fiapead_course.id
        AND fiapead_course_modules.module = 17
        AND fiapead_quiz.id NOT IN (
            SELECT fiapead_quiz.id
            FROM fiapead_quiz 
            INNER JOIN fiapead_fiap_quiz_config
                ON fiapead_fiap_quiz_config.quizid = fiapead_quiz.id 
                    AND fiapead_fiap_quiz_config.configname IN (
                        'atividade_presencial',
                        'atividade_sub',
                        'course_assigns',
                        'DP_1',
                        'DP_2',
                        'EXAME_DP'
                    )
        )
    GROUP BY 
        fiapead_course_categories_resume.breadcrumb,
        fiapead_course.fullname,
        fiapead_course.id
) AS AtividadesEsperadas
LEFT JOIN 
( 
    /*Sumarizar total de atividades entregues*/
    SELECT 
        EntregasAtividade.Curso,
        EntregasAtividade.Fase,
        EntregasAtividade.IdFase,
        EntregasAtividade.RM,
        COUNT(EntregasAtividade.IdAtividade) AS 'TotalAtividadesUploadEntregues',
        SUM(EntregasAtividade.NormalizacaoNota) / COUNT(EntregasAtividade.IdAtividade) AS 'MediaNotas'
    FROM 
    ( SELECT 
            fiapead_course_categories_resume.breadcrumb  AS 'Curso',
            fiapead_course.fullname AS 'Fase',
            fiapead_course.id AS 'IdFase',
            fiapead_user.username AS 'Rm',
            fiapead_assign.name AS 'Atividade',
            fiapead_assign.id  AS 'IdAtividade',
            ROUND(IF(fiapead_grade_grades.finalgrade IS NULL, 0, ROUND(fiapead_grade_grades.finalgrade, 2)), 2) AS 'NotaFinal',
            ROUND(fiapead_grade_grades.rawgrademax, 2) AS 'NotaMaxima',
            ROUND(ROUND(IF(fiapead_grade_grades.finalgrade IS NULL, 0, ROUND(fiapead_grade_grades.finalgrade, 2)), 2)/ROUND(fiapead_grade_grades.rawgrademax, 2),2) AS 'NormalizacaoNota'
        FROM fiapead_course
        INNER JOIN fiapead_course_categories_resume
            ON fiapead_course.category = fiapead_course_categories_resume.categorieid  
        INNER JOIN fiapead_fiap_regras_course
            ON fiapead_fiap_regras_course.courseid = fiapead_course.id
            AND fiapead_fiap_regras_course.regraid = 2
        INNER JOIN fiapead_course_modules
            ON fiapead_course_modules.course = fiapead_course.id 
                AND fiapead_course_modules.visible = 1
                AND fiapead_course_modules.module = 1
        INNER JOIN fiapead_assign
            ON fiapead_assign.id = fiapead_course_modules.instance
                AND fiapead_assign.id NOT IN (  
                    SELECT fiapead_assign.id
                    FROM fiapead_assign 
                    INNER JOIN fiapead_fiap_assign_config
                        ON fiapead_fiap_assign_config.assignid  = fiapead_assign.id 
                            AND (
                                (
                                    fiapead_fiap_assign_config.configname = 'type'
                                    AND fiapead_fiap_assign_config.value IN ('atividade_sub', 'DP_1', 'DP_2','sub-encontro-presencial-1', 'sub-encontro-presencial-2')
                                ) 
                                OR 
                                (
                                    fiapead_fiap_assign_config.configname IN ('atividade_sub', 'DP_1', 'DP_2','sub-encontro-presencial-1', 'sub-encontro-presencial-2')
                                )
                            )
                )
        INNER JOIN fiapead_grade_items
            ON fiapead_grade_items.iteminstance  = fiapead_assign.id 
                AND fiapead_grade_items.courseid  = fiapead_course.id 
                AND fiapead_grade_items.itemmodule = 'assign'
        INNER JOIN fiapead_grade_grades
            ON fiapead_grade_grades.itemid = fiapead_grade_items.id
        INNER JOIN fiapead_user
            ON fiapead_grade_grades.userid = fiapead_user.id  
            AND fiapead_user.username LIKE 'RM%'
        /* Usar esse left join no local destacado */
        LEFT JOIN fiapead_assign_submission
            ON fiapead_assign.id  = fiapead_assign_submission.assignment
                AND fiapead_assign_submission.status = 'submitted'
                AND fiapead_user.id = fiapead_assign_submission.userid
                AND fiapead_course_modules.groupmode = 0
        LEFT JOIN fiapead_groups
            ON fiapead_assign_submission.groupid = fiapead_groups.id
        LEFT JOIN fiapead_groups_members
            ON fiapead_groups_members.groupid = fiapead_groups.id
                AND fiapead_user.id = fiapead_groups_members.userid
        LEFT JOIN (
            SELECT
                        fiapead_groups.id  AS 'idgrupo',
                        fiapead_user.id AS 'idusuario',
                        fiapead_assign.id AS 'idatividade',
                        'Atividade em grupo' AS 'Status'
                    FROM 
                    fiapead_user
                    INNER JOIN fiapead_groups_members
                        ON fiapead_groups_members.userid = fiapead_user.id 
                    INNER JOIN fiapead_groups
                        ON fiapead_groups.id = fiapead_groups_members.groupid
                    INNER JOIN fiapead_assign_submission
                        ON fiapead_assign_submission.groupid = fiapead_groups.id
                        AND fiapead_assign_submission.groupid > 0
                    INNER JOIN fiapead_assign 
                        ON fiapead_assign.id  = fiapead_assign_submission.assignment
                    INNER JOIN fiapead_course_modules
                        ON fiapead_course_modules.instance = fiapead_assign.id
                    INNER JOIN fiapead_course
                        ON fiapead_course.id = fiapead_course_modules.course
                        AND fiapead_course_modules.visible = 1
                        AND fiapead_course_modules.module = 1
                        AND fiapead_course_modules.groupmode = 1
                    INNER JOIN fiapead_fiap_regras_course
                        ON fiapead_fiap_regras_course.courseid = fiapead_course.id
                            AND fiapead_fiap_regras_course.regraid = 2
                    
        ) AS AtividadesGrupos
            ON fiapead_assign_submission.groupid = AtividadesGrupos.idgrupo
            AND fiapead_assign.id = AtividadesGrupos.idatividade
        /* Colocar aqui o left join citado acima e mudar a condição */
    ) AS EntregasAtividade
    GROUP BY 
        EntregasAtividade.Curso,
        EntregasAtividade.Fase,
        EntregasAtividade.IdFase,
        EntregasAtividade.RM
) AS ResumoAtividade
    ON AtividadesEsperadas.IdFase = ResumoAtividade.IdFase
LEFT JOIN 
( 
    /*Sumarizar total de quiz entregues*/
    SELECT 
        FastTestsRealizados.Curso,
        FastTestsRealizados.Fase,
        FastTestsRealizados.IdFase,
        FastTestsRealizados.RM,
        COUNT(FastTestsRealizados.Idquiz) AS 'TotalFastTestRealizados',
        SUM(FastTestsRealizados.NormalizaçãoNotaFastTest) / COUNT(FastTestsRealizados.Idquiz) AS 'MediaNotas'
    FROM 
    (
        SELECT  
            fiapead_course_categories_resume.breadcrumb AS Curso,
            fiapead_course_categories_resume.nivel5 AS Turma,
            fiapead_course.fullname AS Fase,
            fiapead_course.id  AS IdFase,
            CONCAT(fiapead_user.firstname, ' ', fiapead_user.lastname) AS NomeAluno, 
            fiapead_user.username AS RM,
            MAX(ROUND(IF(fiapead_grade_grades.finalgrade IS NULL, 0, ROUND(fiapead_grade_grades.finalgrade, 2)), 2)) AS 'NotaFinal',
            fiapead_quiz_attempts.state AS Status,  
            fiapead_quiz.name AS Quiz,
            fiapead_quiz.id  AS Idquiz,
            ROUND(fiapead_grade_grades.rawgrademax, 2) AS 'NotaMáxima',
            MAX(ROUND(IF(fiapead_grade_grades.finalgrade IS NULL, 0, ROUND(fiapead_grade_grades.finalgrade, 2)), 2)) / ROUND(fiapead_grade_grades.rawgrademax, 2) AS 'NormalizaçãoNotaFastTest'
        FROM fiapead_grade_grades
        INNER JOIN fiapead_grade_items
            ON fiapead_grade_grades.itemid = fiapead_grade_items.id
            AND fiapead_grade_items.itemmodule = 'quiz'
        INNER JOIN fiapead_quiz
                ON fiapead_grade_items.iteminstance = fiapead_quiz.id
                AND fiapead_grade_items.courseid = fiapead_quiz.course 
                AND fiapead_quiz.id  NOT IN 
                ( 
                    SELECT fiapead_quiz.id
                    FROM fiapead_quiz 
                    INNER JOIN fiapead_fiap_quiz_config
                        ON fiapead_fiap_quiz_config.quizid = fiapead_quiz.id 
                            AND fiapead_fiap_quiz_config.configname IN 
                            (
                                'atividade_presencial',
                                'atividade_sub',
                                'course_assigns',
                                'DP_1',
                                'DP_2',
                                'EXAME_DP'
                            )
                )
        INNER JOIN fiapead_course
            ON fiapead_grade_items.courseid = fiapead_course.id
        INNER JOIN fiapead_user
            ON fiapead_grade_grades.userid = fiapead_user.id
        INNER JOIN fiapead_course_modules
            ON fiapead_course_modules.course = fiapead_course.id 
                AND fiapead_course_modules.instance = fiapead_quiz.id 
                AND fiapead_course_modules.visible = 1
        INNER JOIN fiapead_course_categories_resume
            ON fiapead_course_categories_resume.categorieid = fiapead_course.category 
        INNER JOIN fiapead_quiz_attempts
            ON fiapead_user.id = fiapead_quiz_attempts.userid
                AND fiapead_quiz.id = fiapead_quiz_attempts.quiz
        WHERE 
                fiapead_quiz_attempts.state = 'finished'
                AND fiapead_user.username LIKE 'RM%'
        GROUP BY 
                fiapead_course_categories_resume.breadcrumb,
                fiapead_course_categories_resume.nivel5,
                fiapead_course.fullname,
                fiapead_course.id,
                CONCAT(fiapead_user.firstname, ' ',fiapead_user.lastname), 
                fiapead_user.username,
                fiapead_quiz_attempts.state,    
                fiapead_quiz.name,
                fiapead_quiz.id,
                fiapead_grade_grades.rawgrademax
    ) AS FastTestsRealizados
    GROUP BY 
        FastTestsRealizados.Curso,
        FastTestsRealizados.Fase,
        FastTestsRealizados.IdFase,
        FastTestsRealizados.RM
) AS FastTestsResumo
    ON AtividadesEsperadas.IdFase = FastTestsResumo.IdFase
        AND ResumoAtividade.RM = FastTestsResumo.RM
```
**Consumo na plataforma**

Extração dos dados de acesso aos conteúdos para construir a base de conusmo dos estudantes online:

``` sql
SELECT  vAlunoCursoResumeRegra.breadcrumb AS 'Curso',
        vAlunoCursoResumeRegra.nivel5 AS 'Turma',
        vAlunoCursoResumeRegra.username AS 'RM',
        COUNT(vAlunoCursoResumeRegra.fullname) AS 'TotalDisciplinas',
        ROUND(SUM(fiapead_fiap_course_visualizacao.visualizacao) / COUNT(vAlunoCursoResumeRegra.fullname),2) / 100  AS 'MediaPorcentagemVisualizacao'
FROM vAlunoCursoResumeRegra
INNER JOIN fiapead_fiap_course_visualizacao        
ON vAlunoCursoResumeRegra.id = fiapead_fiap_course_visualizacao.userid
AND vAlunoCursoResumeRegra.courseid = fiapead_fiap_course_visualizacao.courseid
WHERE vAlunoCursoResumeRegra.breadcrumb LIKE '%On-line%'
      AND vAlunoCursoResumeRegra.username LIKE 'rm%'
      AND vAlunoCursoResumeRegra.breadcrumb NOT LIKE '%MBA%'
      AND vAlunoCursoResumeRegra.breadcrumb NOT LIKE '%Homologação%'
      AND vAlunoCursoResumeRegra.breadcrumb NOT LIKE '%Nano Courses%'
      AND vAlunoCursoResumeRegra.breadcrumb NOT LIKE '%Nivelamento%'
      AND vAlunoCursoResumeRegra.breadcrumb NOT LIKE '%Fiap Onboard%'
GROUP BY vAlunoCursoResumeRegra.breadcrumb,
        vAlunoCursoResumeRegra.nivel5,
        vAlunoCursoResumeRegra.username
```

_Extração dos dados no banco do SQL Server:_

**Débitos**

Extração dos débitos inadimplêntes de estudantes para construir a base de débitos dos estudantes online:

``` sql
use BaseEducacional

SELECT 
	FNDebitos.RM,
	vRelacao.Turma,
	SUM(CASE WHEN FNDebitos.Codigo IS NOT NULL THEN 1 ELSE 0 END) AS 'QtdDebitosDevedor'
FROM 
	FNDebitos WITH (NOLOCK) 
INNER JOIN Educacional..vAluno
	ON vAluno.RM = FNDebitos.RM
INNER JOIN Educacional..vAlunoTurma  
	ON vAluno.Codigo = vAlunoTurma.CodigoAluno
INNER JOIN Educacional..vRelacao 
	ON vAlunoTurma.CodigoRelacao = vRelacao.Codigo
WHERE
	FNDebitos.Visivel = 1  
	AND FNDebitos.Excluido = 0  
	AND FNDebitos.Con  <> 'E'
	AND FNDebitos.Bolsa < 100 
	AND FNDebitos.ValorDebito > 0 
	AND FNDebitos.DebitoEmAcordo = 0 
	AND FNDebitos.Tipo NOT IN ('Taxa', 'Matrícula', 'Renovação de Matrícula', 'Matrícula - Pós', 'Repasse Fies')  
	AND FNDebitos.Tipo NOT LIKE '%Produto%' 
	AND FNDebitos.ValorPago IS NULL  
	AND FNDebitos.Abonado = 0  
	AND FNDebitos.Ano BETWEEN 2017 AND YEAR(GETDATE()) 
	AND FNDebitos.Mes <= 13 
	AND FNDebitos.DataVencimento < CONVERT(DATE, GETDATE())
GROUP BY FNDebitos.RM,
		 vRelacao.Turma

```

Após todas as bases forem extraídas, em cada uma das bases (Notas, Consumo e Débitos) foi criado uma **chave artificial** contendo o **RM + Turma** para cruzar esses dados com a base de _Evadidos_ que foi extraída pela query abaixo:

``` sql
USE Educacional

SELECT
		vAluno.Rm,
		vRelacao.Turma,
		vRelacao.Ano,
		vRelacao.Semestre,
		vCurso.Descricao,
		vCurso.Sigla,
		vRelacao.Unidade,
		ISNULL((SELECT vMatriculaRematricula.Tipo FROM vMatriculaRematricula WHERE vMatriculaRematricula.CodigoAluno = vAluno.Codigo AND vMatriculaRematricula.Ano = vRelacao.Ano AND ISNULL(vMatriculaRematricula.Semestre, 1) = vRelacao.Semestre AND vMatriculaRematricula.Tipo <> 'E'), 'R') AS 'Tipo',
		CONVERT(DATE, ISNULL(vAlunoTurma.DataEntrada, CONCAT(vRelacao.Ano, '0101'))) AS 'DataMatricula',
		CASE WHEN vAlunoTurma.CodigoTipoStatus NOT IN (1, 23) THEN
			ISNULL(vAlunoTurma.DataSaida, vAlunoTurma.DataStatusInformacao)
		ELSE
			NULL
		END AS 'DataSaida',
		CASE WHEN ProUni.Codigo IS NOT NULL THEN 1 ELSE 0 END AS 'ProUni',
		CASE WHEN Formandos.RM IS NOT NULL THEN 
			1
		ELSE
			0
		END AS 'Formando',
		vAlunoTurma.CodigoTipoStatus
	FROM
		vAluno
		INNER JOIN vAlunoTurma ON
			vAluno.Codigo = vAlunoTurma.CodigoAluno
		INNER JOIN vRelacao ON
			vAlunoTurma.CodigoRelacao = vRelacao.Codigo
		INNER JOIN vCurso ON
			vRelacao.CodigoCurso = vCurso.Codigo
		LEFT JOIN Site_Fiap..Formandos AS Formandos ON
			vAluno.RM = Formandos.RM
			AND vRelacao.Ano = Formandos.Ano
		LEFT JOIN CPTVEST AS ProUni ON
			vAluno.RM = ProUni.RM
			ANd ProUni.CodProcesso = 29
	WHERE
		vAluno.CodigoUnidade = 1
		AND vRelacao.CodigoUnidade = 1
		AND vRelacao.Turma NOT LIKE '%EXT%'
		AND (
			vRelacao.Ano>= 2015
		)
		AND vAlunoTurma.CodigoTipoStatus NOT IN (8, 4, 6, 22)
```

Essa query de evadidos mostra todo o histórico de evasão, cancelamento e alunos ativos. Com essa base, é extraído apenas os alunos com a data de saída maior que a data de corte definida:

>
> **22/02** para graduação do inicio do ano (1º semestre).
>
> **01/08** para turmas do meio do ano na graduação (2º semestre).
>

## **ETL dos dados**🧹

Com o merge do pandas todas as bases são conectadas desde que tenham a mesma chave artificial. A ideia aqui é identificar qual foi o comportamento desses estudantes:

``` python
import pandas as pd

# Subindo as bases de dados
df_notas = pd.read_excel("df_notas.xlsx")          # Subindo a base de notas
df_consumo = pd.read_excel("df_consumo.xlsx")      # Subindo a base de consumo na plataforma
df_debitos = pd.read_excel("df_debitos.xlsx")      # Subindo a base de débitos
df_status = pd.read_csv("BaseEvasão.csv", sep=",") # Subindo a base de evasão da graduação online

# Tratamento dos dados
df_notas['RM'] = df_notas['RM'].str.replace('rm', '') 
df_consumo['RM'] = df_consumo['RM'].str.replace('rm', '') 

# Criando uma chave artificial para cruzar os dados
df_notas['Chave'] = df_notas['Turma'] + "-" + df_notas['RM']
df_consumo['Chave'] = df_consumo['Turma'] + "-" + df_consumo['RM']

df_debitos['RM'] = df_debitos['RM'].astype(str)
df_debitos['Chave'] = df_debitos['Turma'] + "-" + df_debitos['RM']

df_status['Rm'] = df_status['Rm'].astype(str)
df_status['Chave'] = df_status['Turma'] + "-" + df_status['Rm']

# Armazenando apenas dados que serão utilizados
df_status = df_status[['Chave', 'Status Final']]

# Limpando duplicados
df_status = df_status.drop_duplicates()

# Normalizando strings necessárias
import nltk
from unicodedata import normalize

class DataCleaner:
    """
    Função para limpar strings em dataframes
    
    Atributos:
        dataframe: recebe um dataframe pandas
        column_name: recebe o nome da coluna que deve ser limpa
        
    Métodos:
        text_lower(): transformar palavras em letra minúscula e remove espaços em branco
        remover_acentos(): remover acentos no texto 
        clean_data(): aplica as funções
    """      
        
    def __init__(self, dataframe, column_name):
        self.dataframe = dataframe
        self.column_name = column_name
        
    
    def text_lower(self, text):
        text = str(text)
        text = text.strip()
        text = text.lower()
        return text
    
    
    def remover_acentos(self, text):
        text = normalize('NFKD', text).encode('ASCII','ignore').decode('ASCII')
        return text
    
    
    def clean_data(self):
        if self.column_name in self.dataframe.columns:
            self.dataframe[self.column_name] = self.dataframe[self.column_name].apply(self.text_lower)
            self.dataframe[self.column_name] = self.dataframe[self.column_name].apply(self.remover_acentos)
        else:
            raise KeyError(f"A coluna '{self.column_name}' não existe no DataFrame.")

 # Aplicando a classe de normalização nas bases

DataCleaner_df_notas = DataCleaner(dataframe=df_notas, column_name='Chave')
DataCleaner_df_notas.clean_data()

DataCleaner_df_consumo = DataCleaner(dataframe=df_consumo, column_name='Chave')
DataCleaner_df_consumo.clean_data()

DataCleaner_df_status = DataCleaner(dataframe=df_status, column_name='Chave')
DataCleaner_df_status.clean_data()

DataCleaner_df_debitos = DataCleaner(dataframe=df_debitos, column_name='Chave')
DataCleaner_df_debitos.clean_data()

# Realizar o merge apenas quando as colunas 'Chave' são iguais

df_evasao = df_notas.merge(df_consumo, on='Chave', how='left')
df_evasao_final = df_evasao.merge(df_debitos, on='Chave', how='left')
df_evasao_final_status = df_evasao_final.merge(df_status, on='Chave', how='left')

# Filtrando apenas o status de evadidos e formandos
df_evasao_final_status = df_evasao_final_status[(df_evasao_final_status['Status Final'] == 'Evaded') | (df_evasao_final_status['Status Final'] == 'Formando')]

# Removendo colunas duplicadas
df_oficial = df_evasao_final_status.drop(['Curso', 'Turma_y', 'RM_y', 'RM', 'Turma'], axis=1)

# Renomeando a coluna
df_oficial.rename(columns={'RM_x': 'RM', 'Turma_x':'Turma'}, inplace=True)

# Filtrandos os dados que não são de 2023
# Aqui queremos analisar apenas o histórico e não alunos ativos
df_filtrado = df_oficial.loc[~df_oficial['NomeCurso'].str.contains('2023')]

# Agregando dados de fases em um único resumo

df_agregado = df_filtrado.groupby(['NomeCurso', 'Turma', 'RM', 'Chave'], as_index=False).agg({
    'TotalAtividadesUploadEntregues': 'sum', 
    'MediaNotasAtividadesUpload': 'mean',
    'TotalAtividadeseUploadEsperadas': 'sum',
    'PercentualEntregaAtividadeUpload': 'mean',
    'TotalFastTestRealizados': 'sum',
    'MediaNotasFastTest': 'mean',
    'TotalQuizEsperados': 'sum',
    'PercentualrealizadoFastTest': 'mean'
}).sort_values(by='NomeCurso', ascending=True)


# Realizar o merge apenas quando as colunas 'Chave' são iguais
df_agregado = df_agregado.merge(df_consumo, on='Chave', how='left')
df_agregado = df_agregado.merge(df_debitos, on='Chave', how='left')
df_agregado = df_agregado.merge(df_status, on='Chave', how='inner')

# Renomeando a coluna
df_agregado.rename(columns={'RM_x': 'RM', 'Turma_x':'Turma'}, inplace=True)

df_agregado = df_agregado.drop(['Turma_y', 'RM_y', 'Curso'], axis=1) # Apagando colunas irrelavantes

df_agregado = df_agregado.dropna(subset=['MediaPorcentagemVisualizacao']) # Apagando as colunas nulas para MediaPorcentagemVisualizacao

df_agregado = df_agregado.drop(['TotalFastTestRealizados', 'TotalQuizEsperados', 'PercentualrealizadoFastTest'], axis=1)

df_agregado = df_agregado.dropna(subset=['MediaNotasFastTest']) # Apagando os nulos de MediaNotasFastTest

df_agregado = df_agregado.fillna(0) # Substituindo os valores nulos por 0 em QtdDebitosDevedor (alunos sem somatória de débitos, não é inadimplente, então recebe 0)

df_agregado['RM'] = df_agregado['RM'].astype(int)

# Tratando as variáveis de texto

from sklearn.preprocessing import LabelEncoder

label_encoder = LabelEncoder()
df_agregado['NomeCurso'] = label_encoder.fit_transform(df_agregado['NomeCurso'])
df_agregado['Turma'] = label_encoder.fit_transform(df_agregado['Turma'])
df_agregado['Chave'] = label_encoder.fit_transform(df_agregado['Chave'])
df_agregado['Status Final'] = label_encoder.fit_transform(df_agregado['Status Final'])

```
## **Criando o algoritmo preditivo 🔮**

Depois dos dados serem estruturados, abaixo está todo o pipeline de criação do algoritmo preditivo de evasão:

``` python
from sklearn.model_selection import train_test_split

df_embaralhado = df_agregado.sample(frac=1).reset_index(drop=True) # Evitar enviesamento 

x = df_embaralhado.drop(['RM','NomeCurso', 'Turma','Status Final', 'TotalAtividadesUploadEntregues', 'TotalAtividadeseUploadEsperadas', 
                        'Chave'], axis=1)

y = df_embaralhado['Status Final']

# Separando em bases de treino e teste
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, stratify=y, random_state=7)

import numpy as np
from sklearn.metrics import recall_score

df_train = pd.merge(y_train, x_train, left_index=True, right_index=True)

newdf_evadidos = pd.DataFrame(np.repeat(df_train[df_train['Status Final']==0].values,2,axis=0))
newdf_formandos = pd.DataFrame(np.repeat(df_train[df_train['Status Final']==1].values,2,axis=0))

newdf_evadidos.columns = df_train.columns
newdf_formandos.columns = df_train.columns

df_train_resample = pd.concat([df_train, newdf_evadidos, newdf_formandos])

X_train_resample = df_train_resample.iloc[:,1:]
y_train_resample = df_train_resample.iloc[:,0]

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()

scaler.fit(X_train_resample)

x_train_escalonado = scaler.transform(X_train_resample)
x_test_escalonado = scaler.transform(x_test)

def AplicaValidacaoCruzada(x_axis, y_axis):
    
    """
    Função para aplicar a validação cruzada e treinar diversos tipos de algoritmos.
    
    Atributos:
        x_axis: recebe um dataframe para os dados característica de treino.
        y_axis: recebe um dataframe com as as labels de treinamento.      
    """   
    from sklearn.neighbors import KNeighborsClassifier      # k-vizinhos mais próximos (KNN)
    from sklearn.linear_model import LogisticRegression     # Regressão Logística
    from sklearn.tree import DecisionTreeClassifier         # Decision tree
    from sklearn.ensemble import RandomForestClassifier     # RandomForest
    from sklearn.svm import SVC                             # Máquina de Vetor Suporte SVM
    from sklearn.ensemble import GradientBoostingClassifier # XGBoost (Extreme Gradient Boosting)


    # Cross-Validation models
    from sklearn.model_selection import cross_val_score
    from sklearn.model_selection import KFold

    # Configuração de KFold
    kfold  = KFold(n_splits=5, shuffle=True)

    # Axis
    x = x_axis
    y = y_axis

    # Criando os modelos
    # KNN
    knn = KNeighborsClassifier(n_neighbors=3, metric= 'euclidean', weights='distance')
    knn.fit(x, y)

    # Regressão Logística
    lr = LogisticRegression()
    lr.fit(x, y)

    # SVM
    svm = SVC()
    svm.fit(x, y)

    # RandomForest
    rf = RandomForestClassifier()
    rf.fit(x, y)

    # Decision Tree
    dt = DecisionTreeClassifier()
    dt.fit(x, y)

    # Extreme Gradient Boosting
    xgb = GradientBoostingClassifier()
    xgb.fit(x,y)


    # Applyes KFold to models
    knn_result = cross_val_score(knn, x, y, cv = kfold)
    lr_result = cross_val_score(lr, x, y, cv = kfold)
    svm_result = cross_val_score(svm, x, y, cv = kfold)
    rf_result = cross_val_score(rf, x, y, cv = kfold)
    dt_result = cross_val_score(dt, x, y, cv = kfold)
    xgb_result = cross_val_score(xgb, x, y, cv = kfold)

    # Creates a dictionary to store Linear Models
    dic_models = {
        "KNN": knn_result.mean(),
        "LR": lr_result.mean(),
        "SVM": svm_result.mean(),
        "RF": rf_result.mean(),
        "DT": dt_result.mean(),
        "XGB": xgb_result.mean()
                }

    # Select the best model
    melhorModelo = max(dic_models, key=dic_models.get)

    print("KNN (R^2): {0}\nRegressão Logística (R^2): {1}\nSVM (R^2): {2}\nRandom Forest (R^2): {3}\nÁrvore de Decisão (R^2): {4}\nXGBoost (R^2): {5}".format(knn_result.mean(),lr_result.mean(), svm_result.mean(), rf_result.mean(), dt_result.mean(), xgb_result.mean()))
    print("O melhor modelo é : {0} com o valor: {1}".format(melhorModelo, dic_models[melhorModelo]))

def evaluate_model(model, X_val, y_val):        
    """
    Função para validar a performance dos algoritmos.
    
    Atributos:
        model: recebe o modelo treinado.
        X_val: recebe um dataframe para os dados característica da base de validação.
        y_val: recebe um dataframe com as as labels da base de validação.
    """   
    from sklearn.metrics import roc_curve, roc_auc_score, classification_report

    # Fazer previsões de probabilidades
    y_pred_probs = model.predict_proba(X_val)[:, 1]

    # Calcular a curva ROC
    fpr, tpr, thresholds = roc_curve(y_val, y_pred_probs)

    # Calcular a AUC (área sob a curva ROC)
    auc = roc_auc_score(y_val, y_pred_probs)

    # Plotar a curva ROC
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='blue', lw=2, label=f'ROC curve (AUC = {auc:.2f})')
    plt.plot([0, 1], [0, 1], color='gray', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('Taxa de Falso Positivo')
    plt.ylabel('Taxa de Verdadeiro Positivo')
    plt.title('Curva ROC')
    plt.legend(loc='lower right')
    plt.show()

    # Converter probabilidades em classes preditas (0 ou 1)
    y_pred = (y_pred_probs > 0.5).astype(int)

    # Gerar o classification report
    report = classification_report(y_val, y_pred)
    print("Classification Report:")
    print(report)

from xgboost import XGBClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import precision_score

# Instantiate the XGB
model = XGBClassifier(scale_pos_weight=1, 
                      eval_metric="mlogloss",
                      booster="gbtree", 
                      n_estimators = 1000, 
                      n_features=20, 
                      gamma=1, 
                      min_split_loss=1, 
                      reg_lambda=1, 
                      colsample_bytree = 0.3, 
                      learning_rate=0.01, 
                      max_depth = 5, 
                      subsample =1, 
                      random_state=2, 
                      verbosity=0)

# Fit xg_reg to training set
model.fit(x_train_escalonado, y_train_resample)

# Predict labels do test set, y_pred
y_pred = model.predict(x_test_escalonado)

score = precision_score(y_test, y_pred, average='weighted')

print(confusion_matrix(y_test, y_pred))

print(classification_report(y_test, y_pred))

print(score)

from joblib import dump, load # Salvando o modelo escolhido
dump(model, 'modelo_xgb.joblib') 

```

## Aplicação do modelo preditivo 📱

A aplicação para instanciar o modelo preditivo do XGBClassifier foi construída utilizando o **Streamlit**. Abaixo está o código da aplicação e a classe criada para normalizar os dados.

**Aplicação:**

``` python
# Libraries to import
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from utils import MinMax, MinMaxPresencial  
from sklearn.pipeline import Pipeline
import joblib
from joblib import load
import io

st.markdown("<h1 style='text-align: center; color: lightgreen; '> Sistema preditivo de evasão FIAP</h1>", unsafe_allow_html=True)
st.write('### Resultados modelo preditivo')

key1 = "file_uploader_1"
key2 = "file_uploader_2"

# Layout from application
tab0, tab1 = st.tabs(["Modelo preditivo onlline","Modelo preditivo presencial"])

with tab0:
    st.write('# Algoritmo preditivo graduação online')
    
    # Title from application
    st.write("Upload de Arquivo Excel")

    # Upload an excel file
    uploaded_file = st.file_uploader("Carregue um arquivo Excel contendo a base de dados", type=["xlsx"], key=key1)

    # Function to apply preprocessing in inputed dataframe
    def pipeline(df):
        """
        Function to apply preprocessing in dataframe. 

        Args:
            df: Input a dataframe.

        Returns:
            Normalized dataframe.
        """
        pipeline_obj = Pipeline([
            ('min_max_scaler', MinMax())
        ])
        df_pipeline = pipeline_obj.fit_transform(df)
        return df_pipeline

    # Function to mapping target values
    def mapear_valor(valor):
        """
        Function to mapping target values into dataframe and create a label representation. 

        Args:
            df: Input a value.

        Returns:
            label transformed.
        """
        if valor == 0:
            return 'Propenso a evadir'
        elif valor == 1:
            return 'Propenso a se formar'
        else:
            return 'Desconhecido'  
        
    # Function to create ranking
    def calcula_ranking(df):
        """
        Function to create a ranking with evaded results analyzing some conditions and giving weights to specification conditions.
        Args:
            df: Input a dataframe.

        Returns:
            Dataframe with ranking values.
            
        """
        rankings = []  

        for index, row in df.iterrows():
            ranking = 0  

            MediaNotasAtividadesUpload = row['MediaNotasAtividadesUpload']
            PercentualEntregaAtividadeUpload = row['PercentualEntregaAtividadeUpload']
            MediaPorcentagemVisualizacao = row['MediaPorcentagemVisualizacao']
            QtdDebitosDevedor = row['QtdDebitosDevedor']
            Predição = row['Predição']

            # Conditions
            if (Predição == 'Propenso a evadir'and MediaNotasAtividadesUpload == 0):
                ranking += 5
            if (Predição == 'Propenso a evadir' and MediaNotasAtividadesUpload <= 0.50):
                ranking += 4
            if (Predição == 'Propenso a evadir' and PercentualEntregaAtividadeUpload < 0.90):
                ranking += 3
            if (Predição == 'Propenso a evadir' and MediaPorcentagemVisualizacao <= 0.40):
                ranking += 2
            if (Predição == 'Propenso a evadir' and QtdDebitosDevedor >= 3):
                ranking += 1
            else:
                ranking += 0

            rankings.append(ranking)  # Adiciona o ranking calculado para a linha atual

        df['Ranking'] = rankings  # Adiciona a coluna 'Ranking' ao DataFrame
        return df


    # Predictions
    if uploaded_file is not None:
        data = pd.read_excel(uploaded_file)
        data_original_com_RM = pd.read_excel(uploaded_file)
        data_original = data_original_com_RM.drop(['RM'], axis=1)
        data_normalized = pipeline(data_original)
        model = joblib.load('modelo_xgb.joblib')
        final_pred = model.predict(data_normalized)
        data_original_com_RM['Predição'] = [mapear_valor(valor) for valor in final_pred]
        data_original_com_RM['Predição'] = data_original_com_RM['Predição'].astype('category')
        data_original_com_RM = calcula_ranking(data_original_com_RM)
        

        # Show data processed
        st.write("Dados Processados:")
        st.write(data_original_com_RM.sort_values(by='Ranking', ascending=False))

        # Create a botton to download data
        output = io.StringIO()
        data_original_com_RM.to_csv(output, index=False)
        csv_data = output.getvalue()
        st.download_button(label="Baixar CSV", data=csv_data, file_name="dados_predição.csv")
        #st.balloons()

with tab1:
    st.write('# Algoritmo preditivo graduação presencial')
    
    # Title from application
    st.write("Upload de Arquivo Excel")

    # Upload an excel file
    uploaded_file_presencial = st.file_uploader("Carregue um arquivo Excel contendo a base de dados", type=["xlsx"], key=key2)

    # Function to apply preprocessing in inputed dataframe
    def pipeline_presencial(df):
        """
        Function to apply preprocessing in dataframe. 

        Args:
            df: Input a dataframe.

        Returns:
            Normalized dataframe.
        """
        pipeline_obj = Pipeline([
            ('min_max_scaler', MinMaxPresencial())
        ])
        df_pipeline = pipeline_obj.fit_transform(df)
        return df_pipeline

# Function to create ranking
    def calcula_ranking_presencial(df):
        """
        Function to create a ranking with evaded results analyzing some conditions and giving weights to specification conditions.
        Args:
            df: Input a dataframe.

        Returns:
            Dataframe with ranking values.
            
        """
        rankings = []  

        for index, row in df.iterrows():
            ranking = 0  

            TotalDisciplinas = row['TotalDisciplinas']
            MediaNac1 = row['MediaNac1']
            MediaPS1 = row['MediaPS1']
            NotaFalta = row['NotaFalta']
            Predição = row['Predição']

            # Conditions
            if (Predição == 'Propenso a evadir'and NotaFalta >= 1):
                ranking += 5
            if (Predição == 'Propenso a evadir' and MediaPS1 <= 60.00):
                ranking += 4
            if (Predição == 'Propenso a evadir' and MediaNac1  <= 60.00):
                ranking += 2
            else:
                ranking += 0

            rankings.append(ranking)  # Adiciona o ranking calculado para a linha atual

        df['Ranking'] = rankings  # Adiciona a coluna 'Ranking' ao DataFrame
        return df
    

    # Predictions
    if uploaded_file_presencial is not None:
        data_presencial = pd.read_excel(uploaded_file_presencial)
        data_presencial_original_com_RM = pd.read_excel(uploaded_file_presencial)
        data_original_presencial = data_presencial_original_com_RM.drop(['RM'], axis=1)
        data_normalized_presencial = pipeline_presencial(data_original_presencial)
        model_rf = joblib.load('modelo_adaboosting_presencial.joblib')
        final_pred_presencial = model_rf.predict(data_normalized_presencial)
        data_presencial_original_com_RM['Predição'] = [mapear_valor(valor) for valor in final_pred_presencial]
        data_presencial_original_com_RM['Predição'] = data_presencial_original_com_RM['Predição'].astype('category')
        data_presencial_original_com_RM = calcula_ranking_presencial(data_presencial_original_com_RM)
        

        # Show data processed
        st.write("Dados Processados:")
        st.write(data_presencial_original_com_RM)

        # Create a botton to download data
        output_presencial = io.StringIO()
        data_presencial_original_com_RM.to_csv(output_presencial, index=False)
        csv_data_presencial = output_presencial.getvalue()
        st.download_button(label="Baixar CSV", data=csv_data_presencial, file_name="dados_predição_presencial.csv")
        #st.balloons()
```

**Arquivo Utils:**

Este arquivo contém a criação da classe de normalização para ser incluído no pipeline do modelo.
 
``` python

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

# Class to create data normalization

class MinMax(BaseEstimator,TransformerMixin):
    

    def __init__(self,min_max_scaler  = ['MediaNotasAtividadesUpload', 
                                         'PercentualEntregaAtividadeUpload', 
                                         'TotalDisciplinas',
                                         'MediaPorcentagemVisualizacao', 
                                         'QtdDebitosDevedor']):
        self.min_max_scaler = min_max_scaler

    def fit(self,df):
        return self

    def transform(self,df):
        min_max_enc = MinMaxScaler()
        df[self.min_max_scaler] = min_max_enc.fit_transform(df[self.min_max_scaler])
        return df

class MinMaxPresencial(BaseEstimator,TransformerMixin):
    

    def __init__(self,min_max_scaler  = ['TotalDisciplinas', 
                                         'MediaNac1',
                                         'MediaPS1',
                                         'NotaFalta']):
        self.min_max_scaler = min_max_scaler

    def fit(self,df):
        return self

    def transform(self,df):
        min_max_enc = MinMaxScaler()
        df[self.min_max_scaler] = min_max_enc.fit_transform(df[self.min_max_scaler])
        return df


```

## Modelo preditivo de evasão cursos presenciais 🔮

Para os cursos da modalidade presencial, foi utilizado a mesma lógica e os mesmos passos realizados no pipeline do modelo preditivo online, alterando apenas a base de dados. A base de treinamento do modelo foi utilizado a seguinte query abaixo no banco do SQL Server:


``` sql

use site_Fiap

---Notas - Academico + Inadimplência

SELECT
		CONVERT(FLOAT, ROUND(((CONVERT(FLOAT, Tabela.SomaFalta1)/Tabela.CH)*10), 2)) AS 'NotaFalta',
		SUM(CASE WHEN FNDebitos.Codigo IS NOT NULL THEN 1 ELSE 0 END) AS 'QtdDebitosDevedor',
		Tabela.RM,
		Tabela.Turma,
		Tabela.TotalDisciplinas,
		Tabela.SomaNac1,
		Tabela.QtdNac1,
		Tabela.MediaNac1,
		Tabela.SomaAM1,
		Tabela.QtdAM1,
		Tabela.MediaAM1,
		Tabela.SomaPS1,
		Tabela.QtdPS1,
		Tabela.MediaPS1,
		Tabela.SomaFalta1,
		Tabela.SomaNac2,
		Tabela.QtdNac2,
		Tabela.MediaNac2,
		Tabela.SomaAM2,
		Tabela.QtdAM2,
		Tabela.MediaAM2,
		Tabela.SomaPS2,
		Tabela.QtdPS2,
		Tabela.MediaPS2,
		Tabela.SomaFalta2,
		Tabela.CH,
		Tabela.Ano,
		Tabela.Semestre,
		Tabela.RegraNota
	FROM
(SELECT
			Tabela.RM,
			Tabela.Turma,
			Tabela.TotalDisciplinas,
			Tabela.SomaNac1,
			Tabela.QtdNac1,
			Tabela.MediaNac1,
			Tabela.SomaAM1,
			Tabela.QtdAM1,
			Tabela.MediaAM1,
			Tabela.SomaPS1,
			Tabela.QtdPS1,
			Tabela.MediaPS1,
			Tabela.SomaFalta1,

			Tabela.SomaNac2,
			Tabela.QtdNac2,
			Tabela.MediaNac2,
			Tabela.SomaAM2,
			Tabela.QtdAM2,
			Tabela.MediaAM2,
			Tabela.SomaPS2,
			Tabela.QtdPS2,
			Tabela.MediaPS2,
			Tabela.SomaFalta2,

			Tabela.CH,
			Tabela.Ano,
			Tabela.Semestre,
			Tabela.RegraNota
		FROM
			(SELECT
				Tabela.RM,
				Tabela.Turma,
				Tabela.TotalDisciplinas,
				Tabela.SomaNac1,
				Tabela.QtdNac1,
				CASE WHEN Tabela.QtdNac1 > 0 THEN ROUND((Tabela.SomaNac1 / Tabela.QtdNac1), 2) ELSE 0 END AS 'MediaNac1',
				Tabela.SomaAM1,
				Tabela.QtdAM1,
				CASE WHEN Tabela.QtdAM1 > 0 THEN ROUND((Tabela.SomaAM1 / Tabela.QtdAM1), 2) ELSE 0 END AS 'MediaAM1',
				Tabela.SomaPS1,
				Tabela.QtdPS1,
				CASE WHEN Tabela.QtdPS1 > 0 THEN ROUND((Tabela.SomaPS1 / Tabela.QtdPS1), 2) ELSE 0 END AS 'MediaPS1',
				Tabela.SomaFalta1,

				Tabela.SomaNac2,
				Tabela.QtdNac2,
				CASE WHEN Tabela.QtdNac2 > 0 THEN ROUND((Tabela.SomaNac2 / Tabela.QtdNac2), 2) ELSE 0 END AS 'MediaNac2',
				Tabela.SomaAM2,
				Tabela.QtdAM2,
				CASE WHEN Tabela.QtdAM2 > 0 THEN ROUND((Tabela.SomaAM2 / Tabela.QtdAM2), 2) ELSE 0 END AS 'MediaAM2',
				Tabela.SomaPS2,
				Tabela.QtdPS2,
				CASE WHEN Tabela.QtdPS2 > 0 THEN ROUND((Tabela.SomaPS2 / Tabela.QtdPS2), 2) ELSE 0 END AS 'MediaPS2',
				Tabela.SomaFalta2,


				Tabela.CH,
				Tabela.Ano,
				Tabela.Semestre,
				Tabela.RegraNota
			FROM
				(SELECT
					vAluno.Rm,
					vRelacao.Turma,
					COUNT(*) AS 'TotalDisciplinas',
					SUM(ISNULL(LancamentoNotasFiap.Nac1, 0)) AS 'SomaNac1',
					SUM(CASE WHEN LancamentoNotasFiap.Nac1 IS NOT NULL THEN 1 ELSE 0 END) AS 'QtdNac1',
					SUM(ISNULL(LancamentoNotasFiap.AM1, 0)) AS 'SomaAM1',
					SUM(CASE WHEN LancamentoNotasFiap.AM1 IS NOT NULL THEN 1 ELSE 0 END) AS 'QtdAM1',
					SUM(ISNULL(LancamentoNotasFiap.PS1, 0)) AS 'SomaPS1',
					SUM(CASE WHEN LancamentoNotasFiap.PS1 IS NOT NULL THEN 1 ELSE 0 END) AS 'QtdPS1',
					SUM(ISNULL(LancamentoNotasFiap.Falta1, 0)) AS 'SomaFalta1',

					SUM(ISNULL(LancamentoNotasFiap.Nac2, 0)) AS 'SomaNac2',
					SUM(CASE WHEN LancamentoNotasFiap.Nac2 IS NOT NULL THEN 1 ELSE 0 END) AS 'QtdNac2',
					SUM(ISNULL(LancamentoNotasFiap.AM2, 0)) AS 'SomaAM2',
					SUM(CASE WHEN LancamentoNotasFiap.AM2 IS NOT NULL THEN 1 ELSE 0 END) AS 'QtdAM2',
					SUM(ISNULL(LancamentoNotasFiap.PS2, 0)) AS 'SomaPS2',
					SUM(CASE WHEN LancamentoNotasFiap.PS2 IS NOT NULL THEN 1 ELSE 0 END) AS 'QtdPS2',
					SUM(ISNULL(LancamentoNotasFiap.Falta2, 0)) AS 'SomaFalta2',

					SUM(LancamentoNotasFiap.CH)/2.0 AS 'CH',
					vRelacao.Ano,
					vRelacao.Semestre,
					Relacao_2004.RegraNota
				FROM
					Educacional..vAluno AS vAluno
					INNER JOIN Educacional..vAlunoTurma AS vAlunoTurma ON 
						vAluno.Codigo = vAlunoTurma.CodigoAluno
					INNER JOIN Educacional..vRelacao AS vRelacao ON 
						vAlunoTurma.CodigoRelacao = vRelacao.Codigo
					INNER JOIN Educacional..LancamentoNotasFiap AS LancamentoNotasFiap WITH (NOLOCK) ON 
						vAluno.RM = LancamentoNotasFiap.RM 
						AND vRelacao.Ano = LancamentoNotasFiap.Ano 
						-- AND LancamentoNotasFiap.Cond = 'A' /*Eu tirei essa condição porque eu quero pegar alunos que sairam (os evadidos)*/
						AND LancamentoNotasFiap.dispensado = 0
						AND (
								LancamentoNotasFiap.TurmaPrincipal = 1
							OR (
								LancamentoNotasFiap.CursandoDP = 1
							AND LancamentoNotasFiap.DP = 1
								)
							)
					INNER JOIN Site_Fiap..Relacao_2004 AS Relacao_2004 WITH (NOLOCK) ON
						LancamentoNotasFiap.CodRelacao = Relacao_2004.Codigo
						AND vRelacao.Semestre = Relacao_2004.SemestreInicio
						AND Relacao_2004.NanoCourse = 0
						AND Relacao_2004.Ativo = 1

				WHERE
					vAlunoTurma.CodigoTipoStatus NOT IN (4, 6, 8, 22) AND
					vRelacao.Ano BETWEEN 2014 AND YEAR(GETDATE()) AND
					vAluno.CodigoUnidade = 1 AND
					vRelacao.CodigoUnidade = 1 AND
					vRelacao.EAD = 0
				GROUP BY
					vAluno.Rm,
					vRelacao.Turma,
					vRelacao.Ano,
					vRelacao.Semestre,
					Relacao_2004.RegraNota) AS Tabela) AS Tabela
		GROUP BY
			Tabela.RM,
			Tabela.Turma,
			Tabela.TotalDisciplinas,
			Tabela.SomaNac1,
			Tabela.QtdNac1,
			Tabela.MediaNac1,
			Tabela.SomaAM1,
			Tabela.QtdAM1,
			Tabela.MediaAM1,
			Tabela.SomaPS1,
			Tabela.QtdPS1,
			Tabela.MediaPS1,
			Tabela.SomaFalta1,

			Tabela.SomaNac2,
			Tabela.QtdNac2,
			Tabela.MediaNac2,
			Tabela.SomaAM2,
			Tabela.QtdAM2,
			Tabela.MediaAM2,
			Tabela.SomaPS2,
			Tabela.QtdPS2,
			Tabela.MediaPS2,
			Tabela.SomaFalta2,

			Tabela.CH,
			Tabela.Ano,
			Tabela.Semestre,
			Tabela.RegraNota) AS Tabela 
LEFT JOIN BaseEducacional..FNDebitos AS FNDebitos WITH (NOLOCK) ON 
					Tabela.RM = FNDebitos.RM AND 
					FNDebitos.Visivel = 1 AND 
					FNDebitos.Excluido = 0 AND 
					FNDebitos.Con <> 'E' AND
					FNDebitos.Bolsa < 100 AND
					FNDebitos.ValorDebito > 0 AND
					FNDebitos.DebitoEmAcordo = 0 AND
					FNDebitos.Tipo NOT IN ('Taxa', 'Matrícula', 'Renovação de Matrícula', 'Matrícula - Pós', 'Repasse Fies') AND 
					FNDebitos.Tipo NOT LIKE '%Produto%' AND
					FNDebitos.ValorPago IS NULL AND 
					FNDebitos.Abonado = 0 AND 
					FNDebitos.Ano BETWEEN 2014 AND YEAR(GETDATE()) AND
					FNDebitos.Mes <= 13 AND
					FNDebitos.DataVencimento < CONVERT(DATE, GETDATE())
GROUP BY
		Tabela.RM,
		Tabela.Turma,
		Tabela.TotalDisciplinas,
		Tabela.SomaNac1,
		Tabela.QtdNac1,
		Tabela.MediaNac1,
		Tabela.SomaAM1,
		Tabela.QtdAM1,
		Tabela.MediaAM1,
		Tabela.SomaPS1,
		Tabela.QtdPS1,
		Tabela.MediaPS1,
		Tabela.SomaFalta1,
		Tabela.SomaNac2,
		Tabela.QtdNac2,
		Tabela.MediaNac2,
		Tabela.SomaAM2,
		Tabela.QtdAM2,
		Tabela.MediaAM2,
		Tabela.SomaPS2,
		Tabela.QtdPS2,
		Tabela.MediaPS2,
		Tabela.SomaFalta2,
		Tabela.CH,
		Tabela.Ano,
		Tabela.Semestre,
		Tabela.RegraNota

```

**Dicionário de dados do modelo presencial:** 📖

- **RM:** Matrícula do estudante.
- **TotalDisciplinas:** Número total de disciplinas sendo cursadas.
- **MediaNac1:** Média de nota de NACs do primeiro semestre.
- **MediaPS1:** Média de nota de PS do primeiro semestre.
- **NotaFalta:** Percentual de faltas. Esse cálculo é composto pela soma total de faltas do estudante dividido pela carga horária.
- **Predição:** Resultado do algoritmo preditivo.

Foram coletadas apenas notas do primeiro semestre, pois o objetivo do algoritmo é capturar o comportamento do estudante logo no **início** do curso. As variáveis do 2º semestre estavam ocasionando multicolinearidade.

**Algoritmo preditivo para graduação presencial 🔮**

O algoritmo utilizado foi o **AdaBoostClassifier** que também é um tipo de algoritmo de boosting. O algoritmo utiliza boosting adaptativo, ajustando os pesos dos exemplos de treinamento durante o processo de treinamento para enfatizar os exemplos mal classificados.

O conceito básico por trás do Adaboost é definir os pesos dos classificadores e treinar a amostra de dados em cada iteração de forma que garanta previsões precisas de observações incomuns.

Qualquer algoritmo de aprendizado de máquina pode ser usado como classificador base se aceitar pesos no conjunto de treinamento. Neste caso, foi utilizado o modelo de árvore de decisão.

**Resultados do modelo preditivo:  ✅**

> Acurácia: 86%
> 
> Curva ROC: 91%
>  
> Classe propenso a evadir (F1-Score): 82%
> 
> Classe propenso a se formar (F1-Score): 89%
> 

## Conclusão 🏁

Este projeto foi uma iniciativa criada desde 2018, na qual iniciei os estudos e testes de modelos preditivos sobre o comportamento de estudantes a fim de criar um modelo preditivo efetivo para generalizar os dados. É um grande prazer poder contriuir com a educação e agradeço a FIAP pela oportunidade de poder aplicar data science com o objetivo de melhorar a educação. 💙

**Passos realizados:**

- Extração dos dados.
- Estudo dos dados.
- Limpeza e ETL dos dados.
- Feature engineering.
- Pipeline do modelo preditivo.
- Criação da aplicação do modelo.

**Possíveis melhorias:** esse modelo possúi um viés acadêmico, observando apenas o comportamento acadêmico dos estudantes. Seria interessante futuramente melhorarmos a base que alimenta o modelo preditivo incluindo variáveis de fatores socioeconômicos.

**Autora:** _Ana Raquel Fernandes Cunha Kondostanos_

## Referências 📚

[GÉRON, Aurélien. Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow, 2nd Edition. O'Reilly Media, Inc., 2019](https://www.oreilly.com/library/view/hands-on-machine-learning/9781492032632/)

[XGBoost Hyperparameters — Explained](https://amangupta16.medium.com/xgboost-hyperparameters-explained-bb6ce580501d)

[Mastering XGBoost Parameter Tuning: A Complete Guide with Python Codes](https://www.analyticsvidhya.com/blog/2016/03/complete-guide-parameter-tuning-xgboost-with-codes-python/#:~:text=The%20three%20main%20hyperparameters%20in,and%20performance%20of%20the%20model)

[XGBoost — A matemática passo a passo](https://medium.com/@aln.deaguiar/xgboost-a-matem%C3%A1tica-passo-a-passo-29d34fa561dc)

[AdaBoost Classifier Tutorial](https://www.kaggle.com/code/prashant111/adaboost-classifier-tutorial)