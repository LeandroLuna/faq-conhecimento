# Fluxo de importação AD 

<div style="height: 600px; overflow-x:scroll;">
    <img src="../ImportacaoAD/Importacao.svg" style="max-width: initial;">
</div>

## Criado por:
- Marcos Lima ([marcos.lima@fiap.com.br](mailto:marcos.lima@fiap.com.br))
- [Chat do Teams](https://teams.microsoft.com/l/chat/0/?users=marcos.lima@fiap.com.br)

## Informações de fluxo de importação AD

### Fluxo 

1. O serviço é executado a cada 30 minutos.

2. Verifica o cadastro de usuários não processados do colégio e da pós-graduação.
    - **2.1. Colégio**: Retorna o usuário importado: `vUsuariosImportarAD`.
        - 2.1.1. Atualiza os dados e define "Ação" como "D" na base ControleUsuarioAD.
        - 2.1.2. Retorna o usuário por RM.
        - 2.1.3. Se for um novo cadastro, registra com Ação = "A". Se a turma do AD for diferente da turma do usuário ou o departamento do usuário for diferente do AD, registra a Ação como "T"; caso contrário, atualiza como Ação = "M".
    - **2.2. Pós-graduação**: Retorna o usuário importado: `vUsuariosImportarPosAD`.
        - 2.2.1. Retorna o usuário por RM.
        - 2.2.2. Se for um novo cadastro, registra com Ação = "A". Desmarca a opção "Trocar Senha Primeiro LogonPos". Se a turma do usuário for diferente do AD, marca Ação = "T"; caso contrário, marca como Ação = "M".

3. Cadastra o aluno no AD.

4. Caso o usuário não tenha sido cadastrado no AD, verifique na tabela de log:
    - 4.1. `Suporte..ControleServiceImportacaoAD`.
    - 4.2. Verifique com a equipe de infraestrutura se o usuário está no AD.
    - 4.3. Verifique em `Educacional..vUsuariosPendentesImportarPosAD` para pós-graduação e `vUsuariosPendentesImportarAD` para o colégio. Se não aparecer, remova da tabela `Educacional..ControleUsuarioAD` e execute o serviço novamente.


