# CDDocumentoDigital

Tabela onde é armazenada a referência dos **documentos assinados digitalmente** a partir dos nossos sistemas. É utilizada no sistema <a href="http://www2.fiap.com.br/consultadocumento" target="_blank">ConsultaDocumento</a>, onde o usuário informa a **chave de acesso** e o sistema retorna o documento, a situação e o link para download.

## Colunas

- **Codigo**: **Identificador** do registro;
- **Chave**:  Valor utilizado para **acessar o documento** a partir do sistema <a href="http://www2.fiap.com.br/consultadocumento" target="_blank">ConsultaDocumento</a>;
- **Arquivo**: **Nome** do documento;
- **DataCadastro**: Data de **inserção** do registro;
- **NomeDocumento**: Especifica o **tipo de documento** que está armazenado (Contrato, Aditivo, etc);
- **SistemaOrigem**: Nome do sistema responsável pelas **alterações** do registro;
- **NomeSolicitante**: **Nome do aluno** a qual o documento está vinculado;
- **CodigoStatus**: Valor que define o **status do documento**, de acordo com a relação abaixo:

```
CodigoStatus:
1 --> Aguardando;
2 --> Assinado;
3 --> Cancelado.
```