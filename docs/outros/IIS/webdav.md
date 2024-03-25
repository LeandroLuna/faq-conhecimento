# Desativar o WebDav de um projeto

Caso a API seja RESTFul e esteja usando os verbos PUT, PATCH, DELETE, etc... pode acontecer de não funcionar se o WebDav estiver habilitado no projeto dentro do IIS.

Para desativar, basta colocar a seguinte tag **modules** dentro de **<system.webServer>**:

```
<system.webServer>    
    <modules runAllManagedModulesForAllRequests="true">
		<remove name="WebDAVModule" />
	  </modules>
</system.webServer>
```