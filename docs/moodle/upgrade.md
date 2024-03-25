# Upgrade

Esta página tem as considerações básicas de como atualizar a versão do Moodle da FIAP sem dores de cabeça.

## Atualização dos arquivos

### Download
Antes de baixar o arquivo zip com a versão mais recente do Moodle, verificar se a versão atual instalada
pode ser migrada diretamente para a nova versão.

Para realizar o download da versão mais recente acessa [este link](https://download.moodle.org/).

Para realizar o download de outras versões suportadas [clique aqui](https://download.moodle.org/releases/supported/).

Para o download de versão legadas [clique aqui](https://download.moodle.org/releases/legacy/).

### Descompactação dos arquivos
Antes de descompactar, **todos** os arquivos atuais devem ser removidos do diretório 
(considerar mover para um outra pasta como backup), deixando apenas o **config.php** ([Recomendação do próprio Moodle](https://docs.moodle.org/33/en/Upgrading)).

O processo de apenas jogar por cima faz com que aconteça alguns erros durante a atualização.

Após isto, voltar os arquivos e plugins personalizados para a FIAP para dentro desta nova instalação.

```
/ajax-cursos.php
/clearcaches.php
/config.php
/fiapautoload.php
/troca-curso.php
/troca-turma.php
/auth/fiapldap/
/fiap/
/fiaplogin/
/lib/dompdf/
/lib/fiap/
/lib/kalendorius/
/local/
/mod/conteudosaudio/
/mod/conteudosexternos/
/mod/conteudoshtml/
/mod/conteudospdf/
/mod/conteudosvideo/
/report/acessos/
/report/acessosfasegradead/
/report/acessosfasembaead/
/report/acessosgradead/
/report/acessosmbaead/
/report/atividades/
/report/atividades_sem_disciplinas/
/report/coletadados/
/report/conteudos/
/report/conteudos_pdf/
/theme/fiap/
```

## Arquivos do core alterados

```
/index.php

/auth/manual/auth.php

/calendar/event.php
/calendar/export.php
/calendar/index.php
/calendar/managesubscriptions.php
/calendar/view.php

/course/edit.php
/course/edit_form.php
/course/index.php
/course/lib.php
/course/loginas.php
/course/modedit.php
/course/search.php
/course/view.php

/comment/comment_ajax.php
/comment/lib.php

/enrol/index.php

/group/assign.php
/group/autogroup.php
/group/delete.php
/group/duplicar.php
/group/group.php
/group/groupings.php
/group/index.php
/group/members.php
/group/overview.php
/group/tabs.php

/lib/moodlelib.php
/lib/myprofilelib.php
/lib/outputrenderers.php
/lib/tablelib.php

/login/index.php
/login/change_password.php
/login/change_password_form.php
/login/confirm.php
/login/forgot_password.php
/login/forgot_password_form.php
/login/set_password_form.php
/login/signup.php
/login/signup_form.php
/login/unlock_account.php

/message/edit.php

/mod/assign/locallib.php
/mod/assign/gradingtable.php
/mod/assign/mod_form.php
/mod/assign/renderer.php
/mod/assign/view.php

/mod/forum/classes/observer.php
/mod/forum/classes/post_form.php
/mod/forum/output/selecao_page.php
/mod/forum/templates/selecao_page.mustache
/mod/forum/discuss.php
/mod/forum/index.php
/mod/forum/lib.php
/mod/forum/mod_form.php
/mod/forum/post.php
/mod/forum/renderer.php
/mod/forum/selecao.php
/mod/forum/view.php

/mod/quiz/edit.php
/mod/quiz/lib.php
/mod/quiz/mod_form.php
/mod/quiz/renderer.php

/mod/wiki/styles.css

/my/index.php

/report/log/classes/renderable.php
/repository/filepicker.js
/repository/repository_ajax.php
/repository/upload/lib.php

/user/action_redir.php
/user/calendar.php
/user/course.php
/user/classes/output/myprofile/tree.php
/user/edit.php
/user/edit_form.php
/user/editadvanced.php
/user/editlib.php
/user/editor.php
/user/files.php
/user/forum.php
/user/language.php
/user/managetoken.php
/user/portfolio.php
/user/portfoliologs.php
/user/preferences.php
/user/profile.php
/user/profilesys.php
/user/repository.php
/user/view.php
```

## TODO para o momento da atualização/migração do Moodle ou dos Servidores

Alguns passos e cuidados devem ser tomados no momento da atualização do Moodle ou da migração de servidores.

Estes passos estão documentados abaixo e devem ser seguidos em ordem para que não haja problemas:

---------------------------------

**Passo 01** - Criação da(s) máquina(s) e configuração (Apache/NGINX, PHP/PHP-FPM, PHP Extensions, MySQL Client, Redis, LDAP) 
aonde será realizado a instalação. Obs: verificar permissão do usuário na pasta do projeto. Caso servidor web não consiga
executar o index.php, verificar no error.log do servidor;

**Passo 02** - Ajustar os timezones para GMT -3 ou America/Sao_Paulo nos servidores Web e no banco de dados. 

**Passo 03** - Habilitar o acesso da(s) máquina(s) criada(s) ao servidor do GIT da FIAP;

**Passo 04** - Montagem e migração do arquivos do Moodle (conteúdos, upload, atividades, imagens dos usuários, etc) 
para o EFS mapeado na máquina utilizando o RSYNC;

**Passo 05** - Habilitar o aviso de "Em manutenção" pelo LoadBalance;

**Passo 06** - Desativar acessos dos servidores atuais;

**Passo 07** - Desativar builds automáticos no servidor via Jenkins

**Passo 08** - Desativar o banco de dados;

**Passo 09** - Criar snapshot do banco de dados atual;

**Passo 10** - Criar novo banco de dados a partir do snapshot atual;

**Passo 11** - Alterar o Engine do banco de dados e a configuração de memória, processamento, etc (se necessário); 

**Passo 12** - Atualizar as últimas modificações dos arquivos do "Passo 04" com RSYNC;

**Passo 13** - Alterar o arquivo de configuração do Moodle para acessar a nova base de dados, novo domínio (se nessário)
e se utiliza SSL ou não. (No caso do NGINX, se utilizar SSL, verificar "if" de redirecionamento no arquivo de configuração
default (/etc/nginx/sites-available/default);

**Passo 14** - Alterar no hosts para acessar através do domínio da plataforma apenas uma das máquinas 
(Neste momento, não pode ser acessado via LoadBalance);

**Passo 15** - Realizar o update do banco de dados através do terminal (para evitar timeout do servidor Apache/NGINX) 
acessando o seguinte arquivo no diretório do projeto com php: **php /admin/cli/upgrade.php**;

**Passo 16** - Configuração do cache via Redis via plataforma: (Administração do site > Plugins > Caching > Configuração);

**Passo 17** - Configuração do pacote de linguagem do Moodle via plataforma: (Administração do site > Language > Language Settings);

**Passo 18** - Repetir os passos 14, 16 e 17 para cada servidor que existir;

**Passo 19** - Acessar o admin do Moodle (admin nativo ==> /admin), para verificar atualizações de informações e 
configurações necessárias caso hajam.

**Passo 20** - Desativar registro do Moodle da FIAP no Moodle.org via admin;

**Passo 21** - Testes de segurança: Acessar a pasta .git pelo navegador;

**Passo 22** - Testes de login manual;

**Passo 23** - Testes de login via LDAP;

**Passo 24** - Testes de navegação nos conteúdos;

**Passo 25** - Testes de navegação no admin;

**Passo 26** - Habilitar LoadBalance removendo o registro do arquivos Hosts;

**Passo 27** - Remover o aviso de em manutenção para os alunos;

**Passo 28** - Testes de balanceamento;

**Passo 29** - Atualizar acesso aos servidores via SSH a partir do Jenkins

**Passo 30** - Ativar builds automáticos do Jenkins

**Passo 31** - Cadastrar monitoramento no Nagios

**Passo 32** - Fixar o IP

**Passo 33** - Habilitar acesso ao servidor do GIT para os novos IPs

**Tempo estimado para migração/atualização para liberar para o aluno:** 03 horas

**Tempo estimado para migração/atualização total:** 05 horas