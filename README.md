# FAQ - Conhecimento

Este é um projeto que propõe o desenvolvimento de um indexador para documentações internas, inspirado no serviço Kendra da AWS. A motivação por trás desse projeto é fornecer uma alternativa mais acessível ao Kendra, que muitas vezes pode ter custos elevados. Em vez de utilizar diretamente o Kendra, a ideia é criar manualmente um indexador utilizando ferramentas de _Large Language Model_ (LLM) e _Natural Language Processing_ (NLP). Dessa forma, será possível acessar informações de documentos de maneira mais direcionada e eficiente.

## Tecnologias

- **Python:** linguagem de programação amplamente utilizada, conhecida por sua simplicidade e versatilidade.
- **Streamlit:** uma biblioteca de código aberto para criação de aplicativos da web interativos com Python.
- **Langchain:** framework projetado para simplificar a criação de aplicativos usando LLM.
- **OpenAI:** uma plataforma de IA que fornece acesso a modelos de linguagem poderosos e ferramentas de processamento de linguagem natural.

## Como utilizar

Existem duas maneiras de utilizar a aplicação. A abordagem convencional envolve a instalação dos módulos diretamente na máquina, enquanto a segunda opção é isolar um ambiente de desenvolvimento usando o VENV. Esta última é recomendada para evitar conflitos com os módulos previamente instalados em sua máquina.

### Método 1: Convencional

1. **Instalação das Dependências:** Antes de executar o código, é necessário instalar as dependências do projeto. Você pode fazer isso executando o seguinte comando:
    ```python
    pip install -r requirements.txt
    ```

2. **Configuração da Chave da API:** É necessário configurar a chave da API do OpenAI. Certifique-se de ter a chave da API e substitua-a no arquivo `config.py` - é necessário criá-lo manualmente.

3. **Execução do Código:** Execute o código Python fornecido.
    ```
    streamlit run index.py
    ```

4. **Interagindo com o Chatbot:** Se o treinamento for bem-sucedido, você poderá iniciar uma conversa com o arquivo MARKDOWN carregado.

### Método 2: Ambiente Virtual (VENV)

1. **Instalação do virtualenv**: 
    ```bash
    pip install virtualenv
    ````

2. **Criação do ambiente virtual**:
    ```bash
    python<versao> -m venv <nome-do-ambiente-virtual>
    ```

    Exemplo:
    ```bash
    python3 -m venv env
    ```

4. **Ativação do ambiente virtual**:
    - CMD:
    ```bash
    env\Scripts\activate.bat
    ```

    - PowerShell:
    ```powershell
    env\Scripts\Activate.ps1
    ```

5. Agora é possivel utilizar os passos 1 ao 5 do método anterior.

6. **Desativação do ambiente virtual**:
    ```bash
    deactivate
    ```

## Contribuindo

Se você encontrar algum problema ou tiver sugestões de melhorias, sinta-se à vontade para contribuir com o projeto. Basta enviar um pull request com suas alterações.