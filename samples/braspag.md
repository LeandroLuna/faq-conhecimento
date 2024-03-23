# Braspag

## API

A API da Braspag oferece, além do ambiente de produção, um sandbox para
que seja possível realizar testes e verificar as respostas da API para
casos específicos sem a necessidade de um cartão de crédito real. Cada
ambiente possui duas URLs: uma para consulta e outra para realizar as
transações, sendo elas:

**Homologação**  
Transações: <https://apisandbox.braspag.com.br/v2/sales/>  
Consultas: <https://apiquerysandbox.braspag.com.br/v2/sales/>  

**Produção**  
Transações: <https://api.braspag.com.br/v2/sales/>  
Consultas: <https://apiquery.braspag.com.br/v2/sales/>  

A documentação oficial da API está disponível em:
<http://apidocs.braspag.com.br/>

## Chaves

Para utilizar a API deve-se passar dois campos no header para
identificar e autorizar as requisições, sendo eles o **MerchantId** e
**MerchantKey**.

A FIAP possui uma combinação de MerchantId e
MerchantKey diferente para cada unidade de negócio, sendo que cada uma
está atrelada a uma conta bancária diferente.

### Chaves por unidade de negócio

| Unidade de Negócio | MerchantId                           | MerchantKey                              | Provider |
| ------------------ | ------------------------------------ | ---------------------------------------- | -------- |
| MBA                | 83F401F3-9A4D-4058-A676-0D6B5138F895 | bBHaw0xRLsbsNhnEyBMfBwa2tgYXzJhnzR9vRC6b | Rede2    |
| COPI               | F8196EFD-5512-4DA7-B9AC-343E714F1606 | mHHGEuskRKMXYmonDSUYJ2qoeFWXlSDQj0yoXAWL | Rede2    |
| FIAP               | 50ACF166-F0EA-42BB-870D-B3C22D5D14E3 | 42on6cxjC4MCLajsEKDfwYkXbgwN2OnWvHQl7ZAs | Rede2    |
| Colégio Módulo     | A5C61604-CB1A-43E2-88AD-F0375AE8ED1E | npOchQdEBrOfd0JhbyfZCxrBYRVQlc1qfua4pCwA | Rede2    |
| Shift              | 948C3297-4B41-49BA-8B9E-B61FDA878B67 | R5reqmcrq2NoK7sudJI3LVpy78XEnpMZqVitwQon | Rede2    |

### Chaves especiais

Além as chaves de cada unidade, possuímos outras chaves para casos
especiais. Verifique as considerações abaixo antes de
utilizá-las.

| Descrição        | MerchantId                           | MerchantKey                              | Provider |
| ---------------- | ------------------------------------ | ---------------------------------------- | -------- |
| Homologação<sup>1</sup>    | 1750fb75-3568-42ba-af22-fff178b3d51f | dwCJERoivH1hL4pSMAAjc3SAueznp9vERamAPhV7 | Simulado |
| Genérica<sup>2</sup>| 95C8BF32-7AA4-7D9E-094A-AF5FDDEEE09B | LbtJscW3r9FllUXHPSVoc3lfWaGnM0DFWqKeOou3 | Rede2    |
| FIAP Store<sup>3</sup> | DE500A32-CFA8-455A-A07D-BD968B7D70FA | hZrAHvtNKKbI5shwTRIBsddAUYEFhJ1FCzUx8qHC | Rede2     |



!!! warning "Atenção"

    1. **Homologação**: Usada em ambiente de desenvolvimento e homologação. 
      Deve ser usada junto com as URLs de homologação, caso contrário não funciona.
    2. **Genérica**: Chave que era usada antes de termos uma loja na Braspag para cada unidade de negócio
    3. **FIAP Store**:  Só deve ser em transações que não são relacionadas a educação, como por exemplo 
      venda de produtos (camisetas do São Paulo, blusas, canecas, etc.)