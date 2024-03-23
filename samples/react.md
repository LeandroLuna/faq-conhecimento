# Deploy no IIS

## Passo 01
Hospedar a aplicação dentro de /React/<nome da aplicação> no servidor 10.10


## Passo 02
No IIS, criar uma nova aplicação na raiz do Portal do Aluno, mapeado para o diretório
da aplicação dentro de /React/<nome da aplicação>.


## Passo 03

Usar o seguinte web.config:

```
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <system.webServer>
    <rewrite>
      <rules>
        <rule name="ReactRouter Routes" enabled="true" stopProcessing="true">
          <match url=".*" />
          <conditions logicalGrouping="MatchAll">
            <add input="{REQUEST_FILENAME}" matchType="IsFile" negate="true" />
            <add input="{REQUEST_FILENAME}" matchType="IsDirectory" negate="true" />
            <add input="{REQUEST_URI}" pattern="^/(static)" negate="true" />
          </conditions>
          <action type="Rewrite" url="index.html" />
        </rule>
      </rules>
    </rewrite>
  </system.webServer>
</configuration>
```