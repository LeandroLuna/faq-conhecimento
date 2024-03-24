import streamlit as st
import os
import time 

from config import OPENAI_KEY
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI

os.environ['OPENAI_API_KEY'] = OPENAI_KEY
PERSIST_DIRECTORY='./data'
MARKDOWN_DIRECTORY='./samples/markdown'

st.set_page_config(page_title="FIAP - FAQ Conhecimento")

# Initialize the model
if 'vectordb' not in st.session_state or st.session_state.vectordb is None:
    try:
        vectordb = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=OpenAIEmbeddings())
        st.session_state.vectordb = vectordb
    except:
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
        st.session_state.vectordb = vectordb

options = [
    'Set API Key',
    'Chat with my file(s)',
    'Restart chatbot history'
]

select_options = st.sidebar.selectbox(
    'What would you like to do?',
    options
)

st.session_state.previous_api_key_input = ''

if select_options == options[0]:
    st.session_state.input_api_key = st.text_input('Enter your API key to chat with the model. Get it from official OpenAI platform: https://platform.openai.com/api-keys', value=st.session_state['previous_api_key_input'])
    if st.session_state['input_api_key'] != st.session_state['previous_api_key_input']:
        os.environ['OPENAI_API_KEY'] = input_api_key
        success = st.success('API key successfully set!')
        time.sleep(2)
        success.empty()
        st.session_state['previous_api_key_input'] = st.session_state['input_api_key']
    elif st.session_state['input_api_key'] == '':    
        st.error('Please, inform your API key.')
    else:
        st.warning('You did not change the API key.')

if select_options == options[1]:
    if st.session_state['input_api_key'] != '':
        if 'vectordb' not in st.session_state or st.session_state.vectordb is None:
            st.error('An error ocurred while loading the model. Please, refresh this page and try again.')
        else:
            if 'history' not in st.session_state or st.session_state.history is None:
                st.session_state.history = []

            for msg in st.session_state.history:
                mh = st.chat_message(msg[0])
                mh.write(msg[1])

            prompt = st.chat_input("Chat with your files.")

            if prompt:    
                message = st.chat_message('User')
                message.write(prompt)
                st.session_state.history.append(('User', prompt))

                with st.spinner('Please wait...'):
                    qa_chain = RetrievalQA.from_chain_type(
                        llm=OpenAI(api_key=os.environ['OPENAI_API_KEY']),
                        return_source_documents=True,
                        retriever=st.session_state.vectordb.as_retriever(search_kwargs={'k': 3})
                    )
                    result = qa_chain({'query': prompt})

                    message2 = st.chat_message('Chat')

                    # Append metadata information to the response.
                    answer = result['result'] + "\n\n --- \n\n"
                    metadata_info = ""
                    for doc in result['source_documents']:
                        source_path = doc.metadata.get('source')
                        formatted_source = source_path.replace('\\', '/').replace('samples/markdown/', '')[:-3]
                        metadata_str = f"{formatted_source}:\n\nGitlab: https://gitlab.fiap.com.br/fiap/base-de-conhecimento/-/blob/master/docs/{formatted_source}.md\n\nDeploy: http://conhecimento.fiap.com.br/{formatted_source}\n\n --- \n\n"
                        if metadata_str not in metadata_info:
                            metadata_info += metadata_str
                    metadata_info = metadata_info.rsplit('--- \n\n', 1)[0] # Remove last separator
                    answer += "\n" + metadata_info

                    message2.write(answer)
                    st.session_state.history.append(('Chat', answer))
    else:
        st.warning('Please, inform your API key.')

if select_options == options[2]:
    st.session_state.history = []
    st.success('Session history restarted!')