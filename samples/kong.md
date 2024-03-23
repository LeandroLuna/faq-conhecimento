# Kong

> **URL**: https://apis.fiap.com.br
> <small> 192.168.60.78 </small>

## O que é?

É o API Gateway usado na FIAP para centralizar todas as nossas APIs (.NET, Node.js, etc) em um único gateway.

Usamos o [KongDash](https://ajaysreedhar.github.io/kongdash) para monitorar e gerenciar as APIs cadastradas no gateway.


!!! info ""

    1. **HTTPS**: As APIs são acessadas via HTTPS em [apis.fiap.com.br](https://apis.fiap.com.br)
      A porta 80 por padrão não responde
      location. This is the recommended way.
    2. **Admin**: A porta de administração do kong é 8001, seguindo a URL: http://apis.fiap.com.br:8001/