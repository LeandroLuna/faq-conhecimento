import streamlit as st
import extra_streamlit_components as stx
import os
import time 

from config import OPENAI_KEY
from datetime import datetime, timedelta
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain.chains import RetrievalQA

# Set the app configuration
@st.cache_data(show_spinner=False) # Cache the app configuration to avoid loading it multiple times
def app_config():
    PERSIST_DIRECTORY='./data'
    MARKDOWN_DIRECTORY='./docs'

    return OPENAI_KEY, PERSIST_DIRECTORY, MARKDOWN_DIRECTORY

# Load the app configuration
os.environ['OPENAI_API_KEY'], PERSIST_DIRECTORY, MARKDOWN_DIRECTORY = app_config()
st.set_page_config(page_title="FIAP - FAQ Conhecimento")

# Load the model
@st.cache_resource(show_spinner="Loading model..")  # Cache the model to avoid loading it multiple times
def load_model():
    if 'vectordb' not in st.session_state or st.session_state.vectordb is None:
        vectordb = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=OpenAIEmbeddings())
        CURRENT_INDEXED_DOCUMENTS = len(vectordb.get()['documents'])

        if(CURRENT_INDEXED_DOCUMENTS == 0):
            md_loader = DirectoryLoader(MARKDOWN_DIRECTORY, glob="**/*.md")
            documents = md_loader.load()
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            documents = text_splitter.split_documents(documents)
            vectordb = Chroma.from_documents(
                documents,
                embedding=OpenAIEmbeddings(),
                persist_directory=PERSIST_DIRECTORY
            )
            vectordb.persist()
            print('Model created successfully!')
            return vectordb
        else:
            print('Model loaded successfully!')
            return vectordb
        

# Initialize the model
st.session_state.vectordb = load_model()

# Initialize the cookies
@st.cache_resource(experimental_allow_widgets=True)
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()
cookies = cookie_manager.get_all()

if 'previous_api_key_input' not in st.session_state: # Initialize the key to store the previous input API key
    st.session_state.previous_api_key_input = ''

if "st-api-key" in cookies and cookies["st-api-key"] != st.session_state.previous_api_key_input:
    st.session_state.previous_api_key_input = cookies["st-api-key"]

# Set the sidebar options
options = [
        'Set API Key',
        'Chat with my file(s)'
    ]

select_options = st.sidebar.selectbox(
    'What would you like to do?',
    options
)

# Clear chat history button
def clear_button():
    if st.button('Clear chat history'):
        if len(st.session_state.history) > 0:
            st.session_state.history = []
            success_clear = st.success('Session history cleared!')
            time.sleep(2)
            success_clear.empty()
        else:
            warning_clear = st.warning('There is no history to clear.')
            time.sleep(2)
            warning_clear.empty()

# Menu options
# Set the API key
if select_options == options[0]:
    st.session_state.input_api_key = st.text_input('Enter your API key to chat with the model. Press \'Enter\' to ensure it was saved correctly! ', value=st.session_state.previous_api_key_input, type='password', help='Get it from official OpenAI platform: https://platform.openai.com/api-keys')
    if st.session_state.input_api_key != st.session_state.previous_api_key_input:
        cookie_manager.set("st-api-key", st.session_state.input_api_key, expires_at=datetime.now() + timedelta(days=365))
        success = st.success('API key successfully set!')
        time.sleep(2)
        success.empty()
    elif st.session_state.input_api_key == '':    
        st.error('Please, inform your API key.')
    else:
        st.info('You did not change the API key.')

# Chat with the model
elif select_options == options[1]:
    if st.session_state.input_api_key != '':
        if 'vectordb' not in st.session_state or st.session_state.vectordb is None:
            st.error('An error ocurred while loading the model. Please, refresh this page and try again.')
        else:
            clear_button()

            if 'history' not in st.session_state or st.session_state.history is None:
                st.session_state.history = []

            for msg in st.session_state.history:
                mh = st.chat_message(msg[0])
                mh.write(msg[1])

            prompt = st.chat_input("Chat with your files.")

            if prompt:    
                user_message = st.chat_message('User')
                user_message.write(prompt)
                st.session_state.history.append(('User', prompt))

                with st.spinner('Please wait...'):
                    qa_chain = RetrievalQA.from_chain_type(
                        llm=OpenAI(api_key=st.session_state.input_api_key),
                        return_source_documents=True,
                        retriever=st.session_state.vectordb.as_retriever(search_kwargs={'k': 3})
                    )
                    result = qa_chain({'query': prompt})

                    chatbot_message = st.chat_message('Chat')

                    # Append metadata information to the response.
                    answer = result['result'] + "\n\n --- \n\n"
                    metadata_info = ""
                    for doc in result['source_documents']:
                        source_path = doc.metadata.get('source')
                        formatted_source = source_path.replace('\\', '/').replace('docs/', '')[:-3] # Replace backslashes and remove 'docs/' and '.md' from the path
                        metadata_str = f"{formatted_source}:\n\nGitlab: https://gitlab.fiap.com.br/fiap/base-de-conhecimento/-/blob/master/docs/{formatted_source}.md\n\nDeploy: http://conhecimento.fiap.com.br/{formatted_source}\n\n --- \n\n"
                        if metadata_str not in metadata_info:
                            metadata_info += metadata_str
                    metadata_info = metadata_info.rsplit('--- \n\n', 1)[0] # Remove last separator
                    answer += "\n" + metadata_info

                    chatbot_message.write(answer)
                    st.session_state.history.append(('Chat', answer))
    else:
        st.warning('Please, inform your API key.')