# Gerar .pfx a partir de arquivos .cer e .key 

O processo abaixo é necessário quando o servidor Windows não tiver a chave privada 
do certificado SSL a ser instalado.

Criando o arquivo **.pfx**, o mesmo instala a chave privada necessária para o processo.

Normalmente ao instalar o arquivo **.pfx** no servidor, o mesmo permite digitar uma 
senha para permitir depois exportá-lo para o outro servidor. **Guarde essa senha com segurança.**

Os arquivos necessários para gerar o **.pfx** geralmente são enviados pelo **"Fernando Adamo de Araujo"** <fernando@fiap.com.br>
( [Chat do Teams](https://teams.microsoft.com/l/chat/0/?users=fernando@fiap.com.br) )

**OBS:** Caso não venham arquivos **.crt**, somente .cer, basta renomear a extensão, pois são a mesma coisa!

<div style="height: 350px; overflow-x:scroll;">
  <img src="../gerar-pfx-a-partir-de-arquivo-cer-e-key.svg" style="max-width: initial;">
</div>


## Comando para executar no terminal

```
openssl pkcs12 -export -out nome-final-para-o-arquivo.pfx -inkey arquivo-da-chave-privada.key -in arquivo-do-certificado-emitido.crt -certfile arquivo-do-certificado-root.crt
```

## Quem desenhou o processo
- Douglas Cabral <douglas.cabral@fiap.com.br>
  ( [Chat do Teams](https://teams.microsoft.com/l/chat/0/?users=douglas.cabral@fiap.com.br) )


## Quem conhece?
- Douglas Cabral <douglas.cabral@fiap.com.br>
  ( [Chat do Teams](https://teams.microsoft.com/l/chat/0/?users=douglas.cabral@fiap.com.br) )