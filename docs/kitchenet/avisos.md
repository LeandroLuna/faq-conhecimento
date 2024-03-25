# Avisos

Para cadastrar avisos que são exibidos quando o aluno entra no aplicativo, basta adicionar registros na tabela **Aviso** com as informações necessárias,conforme exemplo:

```sql
DECLARE @Mensagem VARCHAR(255) = 'Você já pode pedir nossas delícias pelo app.
​
E para começar sua experiência, oferecemos R$5 de crédito em qualquer produto.';
​
INSERT INTO Aviso
SELECT 'rm' + CAST(rm as varchar), -- RM do aluno ou usuário
       'Olá ' + LEFT(nome, charindex(' ', nome) - 1) + ',', -- Título da mensagem
       @Mensagem, -- Texto da mensagem
       null, -- Destaques (itens que aparecem destacados na mensagem)
       1, -- Indicar se deve exibir o saldo atual na mensagem
       0, -- Indica se foi lido ou não
       null, -- Data que foi lido
       getdate(), -- Data que foi cadastrado
       1 -- Código usuário
```
