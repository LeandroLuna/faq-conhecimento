# faq-conhecimento

Este é um projeto que propõe o desenvolvimento de um indexador para a base de conhecimento, inspirado no serviço Kendra da AWS. A motivação por trás desse projeto é fornecer uma alternativa mais acessível ao Kendra, que muitas vezes pode ter custos elevados. Em vez de utilizar diretamente o Kendra, a ideia é criar manualmente um indexador utilizando ferramentas de _Large Language Model_ (LLM) e _Natural Language Processing_ (NLP). Dessa forma, será possível acessar informações de documentos de maneira mais direcionada e eficiente.

## Tecnologias

- **Streamlit:** Uma biblioteca de código aberto para criação de aplicativos da web interativos com Python.
- **Python:** Linguagem de programação amplamente utilizada, conhecida por sua simplicidade e versatilidade.
- **OpenAI:** Uma plataforma de IA que fornece acesso a modelos de linguagem poderosos e ferramentas de processamento de linguagem natural.

## Funcionalidades

### 1. Treinamento

A primeira funcionalidade permite treinar o chatbot arquivos MARKDOWN. Você pode seguir os passos abaixo para treinar seu chatbot:

- Selecione a opção "Train" no menu lateral.
- Informe a pasta com os arquivos MARKDOWN que deseja utilizar para treinar o chatbot.
- Clique no botão "Train" para iniciar o processo de treinamento. Os arquivos serão indexados recursivamente.  

Após o treinamento ser concluído com sucesso, você poderá usar o chatbot para interagir com o conteúdo dos arquivos MARKDOWN.

### 2. Chat com o Arquivo

A segunda funcionalidade permite interagir com o chatbot treinado à partir dos arquivos MARKDOWN. Para utilizar essa funcionalidade:

- Selecione a opção "Chat with my files" no menu lateral.
- Caso o chatbot ainda não tenha sido treinado, será exibida uma mensagem de aviso.
- Caso o chatbot tenha sido treinado com sucesso, você poderá iniciar uma conversa com os arquivos MARKDOWN.

## Como Usar

1. **Instalação das Dependências:** Antes de executar o código, é necessário instalar as dependências do projeto. Você pode fazer isso executando o seguinte comando:
    ```python
    pip install -r requirements.txt
    ```

2. **Configuração da Chave da API:** É necessário configurar a chave da API do OpenAI. Certifique-se de ter a chave da API e substitua-a no arquivo `config.py` - é necessário criá-lo manualmente.

3. **Execução do Código:** Execute o código Python fornecido.
    ```
    streamlit run index.py
    ```

4. **Treinamento do Chatbot:** Informe o diretório dos arquivos MARKDOWN e clique no botão "Train" para treinar o chatbot.

5. **Interagindo com o Chatbot:** Se o treinamento for bem-sucedido, você poderá iniciar uma conversa com o arquivo MARKDOWN carregado.

## Contribuindo

Se você encontrar algum problema ou tiver sugestões de melhorias, sinta-se à vontade para contribuir com o projeto. Basta enviar um pull request com suas alterações.