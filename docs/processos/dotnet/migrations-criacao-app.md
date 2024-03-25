# Migrations - Criação de aplicação .NET (Não Pronto)

<div  style="height: 600px; overflow-x:scroll;">
    <img  src="../migrations-criacao-app.svg"  style="max-width: initial;">
</div>

## Criado por:
- Henrique Lopes <henrique.mendonca@fiap.com.br> 
([Chat do Teams](https://teams.microsoft.com/l/chat/0/?users=henrique.mendonca@fiap.com.br))
- Marcos Lima <marcos.lima@fiap.com.br> 
([Chat do Teams](https://teams.microsoft.com/l/chat/0/?users=marcos.lima@fiap.com.br))

## Informações Adicionais

- O **versionamento de migrations** será gerado com a data atual + código do 
sistema que foi cadastrado na tabela **SistemasMigracao**.
- Todos os Migrations rodados estarão contidos na tabela de versionamento 
**VersionInfo**, que é gerada automaticamente.
- O **Método Up** será responsável por **efetuar a alteração no banco**, 
enquanto que o **Método Down** terá o papel de **reverter a alteração** feita no 
**Método Up**, caso ocorra algum problema.

## Detalhes de Criação do Projeto

No item 4, devem ser **adicionados** os seguintes **pacotes**:

- Dapper
- FluentMigrator
- FluentMigrator.Runner
- Microsoft.AspNetCore.Http.Abstractions
- Microsoft.Extensions.Hosting
- SqlHelpers.Standard
- System.Data.SqlClient

No item 5, **adicionar** o seguinte código abaixo na classe **Program.cs** e 
alterar **string de conexão** para o banco que deseja rodar o migration.

```c#
using FluentMigrator.Runner;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Migracoes.Shift.Migrations;
using SqlHelpers.Standard;

using IHost host = Host.CreateDefaultBuilder(args).ConfigureServices((_, services) =>
          services
                .AddFluentMigratorCore()
                .ConfigureRunner(rb => rb
                .AddSqlServer2016()
                .WithGlobalConnectionString(ConnectionFactory.Conexao("NomeBanco").ConnectionString)
                .ScanIn(typeof(ProjetoMigration).Assembly).For.Migrations())
                .AddLogging(lb => lb.AddFluentMigratorConsole())
                .BuildServiceProvider(false)
                ).Build();

using var scope = host.Services.CreateScope();
var runner = scope.ServiceProvider.GetService<IMigrationRunner>();

if (!(runner is null))
{
    runner.ListMigrations();
    runner.MigrateUp();
}

host.Run();

```

No item 7, adicionar classe de **CustomAttribute** para gerar a **número long** 
da versão do migration.

```c#
using Dapper;
using SqlHelpers.Standard;

public class CustomAttribute : FluentMigrator.MigrationAttribute
{
    public CustomAttribute(string Sistema)
       : base(CalculateValue(Sistema)) { }

    private static long CalculateValue(string Sistema)
    {
        int codigo;

        using (var connection = ConnectionFactory.Conexao("BaseEducacional"))
        {
            codigo = connection.QueryFirstOrDefault<int>("SELECT Codigo FROM SistemasFiap WHERE NomeSistema = @Sistema", new { Sistema });
        }

        return codigo * 1000000000000L 
            + DateTime.Now.Year * 100000000L 
            + DateTime.Now.Month * 1000000L 
            + DateTime.Now.Day * 10000L 
            + DateTime.Now.Hour * 100L 
            + DateTime.Now.Minute;
    }
}
```

No item 8, inserir registro na tabela de **SistemasMigracao** para que os 
**números de versão** dos migrations sejam feitos **automaticamente**.

Inserindo registro na Tabela **SistemasMigracao**:

```sql
INSERT INTO site_fiap..SistemasMigracao
    (Sistema, 
    DataCadastro, 
    Ativo)
VALUES
    (@NomeSistema, 
    CONVERT(DATE, GETDATE()),
    1);
```

| Codigo    | sistema               | DataCadastro              | Ativo |
| ----------|-----------------------|---------------------------|-------|
| 1         | Shift                 |2022-04-05 00:00:00.000    | 1     |
| 2         | DiplomaDigital        |2022-04-05 00:00:00.000    | 1     |
| 3         | MatriculaVestibular   |2022-04-05 00:00:00.000    | 1     |

No item 9, deve-se implementar a seguinte **estrutura de código** na classe 
abstrata do migration e o **Attribute** para versão do Migration com o nome do 
banco que foi inserido na tabela **SistemasMigracao**.

```c#
using FluentMigrator;
using FluentMigrator.SqlServer;

namespace Migracoes.Sistema.Migrations
{
    //Versionamento de Migration
    [Migration("NomeBanco")]         
    public class ProjetoMigration : Migration
    {
	    //Método de execução de alterações no banco
        public override void Up()    
        {

        }

	    //Método de reversão das alterações do método "Up"
        public override void Down()         
        {       

        }
    }
}

```

## Detalhes da Execução dos Migrations

No item 3, deve **adicionar** qual **classe** de migration sera **executada**, 
dentro da Program.cs.

<div  style="height: 500px; overflow-x:scroll;">

<img  src="../Imagens/AondeAdicionarClasseMigration.jpg"  style="max-width: initial;">

</div>

Para executar o passo do item 4, 
(**acesse aqui a documentação do pacote**)[https://fluentmigrator.github.io/] 
com todos os **comandos necessários**. 


```c#
public override void Down()
{
	Delete.Table("Tabela");
}
public override void Up()
{
         Create.Table("Tabela").WithColumn("ColunaA").AsString(12)
                                  .WithColumn("ColunaB").AsBoolean()
                                  .WithColumn("ColunaC").AsDate();
}
```
	
## Estrutura da Tabela **VersionInfo**

| Version       | AppliedOn                 | Description           |
| --------------|---------------------------|-----------------------|
| 202203160747  | 2022-03-16 08:34:04.000   | Projeto_202203160747  |
| 202203170906  | 2022-03-17 10:03:01.000   | Projeto_202203170906  |

