# Git

Esta página tem como finalidade documentar as principais configurações necessárias e utilitários
para o uso do git.


## Endereços do gitlab: 

GitLab antigo: (Depreciado - Evitar usar para novos projetos)
> **URL**: https://gitlab.fiap.com.br
> <small> 192.168.60.77 </small>

GitLab novo:
> **URL**: https://gitlab.fiap.com.br
> <small> 172.31.44.247 </small>

## Runners do gitlab: 
Linux - 192.168.10.20 (Mesmo servidor que está o banco SQL Server de desenvolvimento)
Windows - 192.168.10.40 

### Arquivo de configuração do runner Linux - Docker

O arquivo de configuração de runners instalados no 192.168.10.20 fica em: 
**/etc/gitlab-runner/config.toml**

Neste arquivo é necessário configurar sempre o DNS e o pull_policy quando criar um novo runner
conforme o exemplo abaixo:

```
[[runners]]
  name = "Identificador do seu runner aqui"
  url = "https://gitlab.fiap.com.br/"
  token = "token de acesso aqui"
  executor = "docker"
  limit = 1
  [runners.docker]
    tls_verify = false
    image = "imagem default aqui"
    dns = ["192.168.60.95", "192.168.60.96"]
    privileged = false
    disable_cache = false
    volumes = ["/cache"]
    pull_policy = "if-not-present"
    shm_size = 0
  [runners.cache]
```

Para criar novos runners, seguir o tutorial para o SO desejado em: <https://gitlab.fiap.com.br/admin/runners> 
no botão "Register an instance runner" e na opção "Show runner installation and registration instructions".


## Atalhos

Alguns atalhos práticos para o shell que agilizam o dia a dia com o git.

```shell
alias ckout='git checkout'
alias cmt='git add .; git commit -am'
alias cmtf='cmt "First commit"'
alias lg='git log'
alias mmd='git checkout master && git merge dev'
alias pll='git pull origin'
alias psh='git push origin'
alias pull='git pull'
alias push='git push'
alias st='git status'
```

