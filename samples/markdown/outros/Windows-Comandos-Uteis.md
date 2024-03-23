#Windows

##Comandos úteis para serem usados no windows

###Comando para remover as extenções dos arquivos via PowerShell

De vez em quando o servidor de WebExterno não envia os e-mails e coloca-os na pasta "BadMail" e para tentar reenviar essas mensagem é necessário copiar os arquivos com a extensão .bad para a pasta "Puckup" e depois remover as extenções .bad dos arquivos, o comando abaixo faz isso, só roda no PowerShell do windows.

```
cd c:\inetpub\mailroot\pickup
get-childitem *.bad | foreach { rename-item $_ $_.Name.Replace(".BAD", "") }
```