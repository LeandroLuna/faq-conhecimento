
# Implementando padrão UnitOfWork em um sistema DotNet

O padrão **UnitOfWork** é uma forma de **agrupar** em uma transaction **requisições SQL** que são 
realizadas em sequência, possibilitando a **reversão** de 
todas as alterações realizadas na transação **caso algum erro ocorra**.

## Exemplo de cenário que o padrão **UnitOfWork** se aplica: 

Imagine que determinado sistema bancário possua um método de transferir dinheiro 
entre 2 contas. 

**João** deseja **enviar** R$ 100,00 para sua amiga **Maria**, e para que isso 
seja possível, este método precisa realizar o **débito** do valor na 
**conta do João** e em seguida o **depósito** deste mesmo valor na 
**conta da Maria**.

Porém, por conta de algum erro, o **depósito** do valor na conta da Maria 
**não foi bem sucedido**. Desta forma, o valor **teria saído** da conta do João e 
**não teria entrado** na conta da Maria.

Podemos utilizar o padrão **UnitOfWork** para que, caso ocorra algum problema na 
segunda alteração, seja possível **reverter** toda a **transação**, 
**retornando o valor** para a conta do João.

## Passo a passo para implementar o padrão **UnitOfWork**:

- Implementar padrão de **Injeção de Dependência** nas camadas **BLL** e 
**DAL**;
- Adicionar as libs **SqlHelpers** e **Dapper** na camada **DAL**;
- Criar interface **IDbSession** na pasta de Interfaces da camada **DAL**;
    
    ```csharp
    public interface IDbSession
    {
    	IDbConnection Connection { get; set; }
    	IDbTransaction Transaction { get; set; }
    
    	Task<IDbConnection> GetConnectionAsync(string banco);
    	Task<IDbTransaction> GetTransactionAsync();
    }
    ```
    
- Criar classe **DbSession** em uma pasta **DatabaseConnection** na camada 
**DAL**;
    
    ```csharp
    public class DbSession : IDisposable, IDbSession
    {
    	public IDbConnection Connection { get; set; }
    	public IDbTransaction Transaction { get; set; }
    
    	public DbSession(string banco = "master")
    	{
    		Task.Run(() => GenerateSessionDB(banco)).Wait();
    	}
    
    	public async Task<bool> GenerateSessionDB(string banco)
    	{
    		Connection = await ConnectionFactorySqlServer.ConexaoAsync(banco);
    
    		if (Connection.State != ConnectionState.Open)
    			Connection.Open();
    
    		return Connection != null;
    	}
    
    	public async Task<IDbConnection> GetConnectionAsync(string banco)
    	{
    		if (Connection == null)
    		{
    			await GenerateSessionDB(banco);
    		}
    
    		Connection.ChangeDatabase(banco);
    
    		return Connection;
    	}
    
    	public async Task<IDbTransaction> GetTransactionAsync() => Transaction;
    
    	public void Dispose() => Connection?.Dispose();
    }
    ```
    
- Criar interface **IUnitOfWork** na pasta de Interfaces da camada **BLL**;
    
    ```csharp
    public interface IUnitOfWork : IDisposable
    {
    	void BeginTransaction();
    	void Commit();
    	void Rollback();
    }
    ```
    
- Criar classe **UnitOfWork** na raiz da camada **BLL**;
    
    ```csharp
    public class UnitOfWork : IUnitOfWork
    {
    	private readonly IDbSession _session;
    
    	public UnitOfWork(IDbSession session)
    	{
    		_session = session;
    	}
    
    	public void BeginTransaction()
    	{
    		_session.Transaction = _session.Connection.BeginTransaction();
    	}
    
    	public void Commit()
    	{
    		_session.Transaction.Commit();
    		Dispose();
    	}
    
    	public void Rollback()
    	{
    		_session.Transaction.Rollback();
    		Dispose();
    	}
    
    	public void Dispose() => _session.Connection?.Dispose();
    }
    ```
    
- Adicionar relação entre as classes **DbSession** e **UnitOfWork** e suas 
respectivas interfaces;
    
    ```csharp
    // Projeto .NET Framework
    container.RegisterType<IDbSession, DbSession>(TypeLifetime.Scoped);
    container.RegisterType<IUnitOfWork, UnitOfWork>();
    
    // Projeto .NET Core
    services.AddScoped<IDbSession, DbSession>();
    services.AddTransient<IUnitOfWork, UnitOfWork>();
    ```
    
- Adicionar a **Injeção de Dependência** para a **IUnitOfWork**, na 
**Controller** (Camada **Web**);
    
    ```csharp
    private readonly IDependenciaExemplo1 _dependenciaExemplo1;
    private readonly IDependenciaExemplo2 _dependenciaExemplo2;
    private readonly IUnitOfWork _unitOfWork;
    
    public ExemploController(
    		IDependenciaExemplo1 dependenciaExemplo1, 
    		IDependenciaExemplo2 dependenciaExemplo2, 
    		IUnitOfWork unitOfWork)
    {
    	_dependenciaExemplo1 = dependenciaExemplo1;
    	_dependenciaExemplo2 = dependenciaExemplo2;
    	_unitOfWork = unitOfWork;
    }
    ```
    
- Ainda na **Controller**, envolver as requisições que deseja manter em 
**transação**, certificando-se sempre de que será executado um **Commit** ou um 
**Rollback** no final da execução do método;
    
    ```csharp
    try
    {
    	// Iniciando transação
    	_unitOfWork.BeginTransaction();
    
    	bool sucesso = await _dependenciaExemplo1.RequisicaoExemplo();
    
    	if (sucesso)
    	{
    		// Efetivando alterações e finalizando transação
    		_unitOfWork.Commit();
    	}
    	else
    	{
    		// Cancelando alterações e finalizando transação
    		_unitOfWork.Rollback();
    	}
    
    	return ...
    }
    catch (Exception ex)
    {
    	// Cancelando alterações e finalizando transação
    	_unitOfWork.Rollback();
    
    	return ...
    }
    ```
    
- Adicionar a **Injeção de Dependência** para a **IDbSession**, nas classes da 
camada **DAL** que deseja implementar o padrão **UnitOfWork**;
    
    ```csharp
    private readonly IDbSession _dbSession;
    
    public ExemploDAL(IDbSession dbSession)
    {
    	_dbSession = dbSession;
    }
    ```
    
- Ainda nas classes da camada **DAL**, **todas as requisições** de banco 
realizadas dentro de uma **transação** do padrão **UnitOfWork** devem estar no 
seguinte modelo:
    
    ```csharp
    public async Task<int> RequisicaoExemplo(ObjetoMOD mod)
    {
    	IDbConnection conn = await _dbSession.GetConnectionAsync("Banco");
    	string query = @"
    			-- Query a ser executada
    			";
    
    	return await conn.QueryFirstOrDefaultAsync<int>(
			query, 
			mod, 
			transaction: _dbSession.Transaction);
    }
    ```
    
### Observação

!!! warning "Atenção"
	**NÃO UTILIZAR** o modelo de requisição SQL com um bloco **using**, 
	conforme exemplo abaixo, pois ao finalizar este bloco a transação será 
	finalizada, impedindo que o padrão **UnitOfWork** funcione corretamente.

```csharp
public async Task<int> RequisicaoExemplo(ObjetoMOD mod)
{
	// NÃO UTILIZAR ESTE MODELO !!!
	using (var connection = ConnectionFactorySqlServer.Conexao("Banco"))
	{
		string query = @"
				-- Query a ser executada
			";

		return await connection.QueryFirstOrDefaultAsync<int>(
			query, 
			mod, 
			transaction: _dbSession.Transaction);
	}
}
```

Qualquer dúvida, acessar o **exemplo de implementação** do sistema 
[Intranet.AcessoAlura](https://gitlab.fiap.com.br/dotnet/Intranet.AcessoAlura), 
ou se preferir, é possível acessar o 
[tutorial de implementação](https://www.devmedia.com.br/unit-of-work-o-padrao-de-unidade-de-trabalho-net/25811) 
que tivemos como **base** para desenvolver nossa própria versão do padrão 
**UnitOfWork**.