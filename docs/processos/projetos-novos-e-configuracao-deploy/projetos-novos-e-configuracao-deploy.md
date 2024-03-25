# Projetos Novos e Configuração de Deploy via CI/CD (Backend - DotNet)

## Projetos Novos

Criar sempre os projetos na versão **DotNet mais recente** (atualmente 
**Core 7**) e sempre rodar no **IIS Express**, evitando a que seja necessária a 
**configuração** do projeto no **IIS** da máquina dos **Desenvolvedores**, de 
**Homologação** e de **Produção**.

## Configuração de Deploy via CI/CD

Concentrar as configurações de **deploy** no **Henrique Mendonça**, pois será 
necessário analisar o **Web.config de produção** e o projeto como um todo para 
identificar se possuem algum **apontamento fixo** para o 
**ambiente de produção**.

Buscar no projeto os seguintes **termos**, e caso encontrar, mover para o 
**Web.config**.

- on.fiap.com.br
- on1.fiap.com.br
- apis.fiap.com.br
- www2.fiap.com.br
- intranet.fiap.com.br
- intranet3.fiap.com.br
- vestibular.fiap.com.br