# Services Windows

## Instalação de Services

Utilize o comando abaixo no Prompt para a instalação de novos serviços criados em .NET no Windows:

!!! info ""
	OBS: O caminho do InstallUtil.exe documentado abaixo pode ser diferente dependendo da versão instalada ou local em que o .NET está instalado.

```
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\InstallUtil.exe f:\PathParaOService\NomeDoService.exe
```

## Remoção de Services

Utilize o comando abaixo no Prompt para a remoção de serviços existentes criados em .NET no Windows:

!!! info ""
	OBS: O caminho do InstallUtil.exe documentado abaixo pode ser diferente dependendo da versão instalada ou local em que o .NET está instalado.	

```
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\InstallUtil.exe -u f:\PathParaOService\NomeDoService.exe
```
