import streamlit as st
import os

from config import OPENAI_KEY
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI

os.environ['OPENAI_API_KEY'] = OPENAI_KEY

options = [
    'Train',
    'Chat with my file(s)',
    'Restart chatbot history'
]

select_options = st.sidebar.selectbox(
    'What would you like to do?',
    options
)

if select_options == options[0]:
    st.text('Click the button below to train your AI with your files.')
    if st.button('Train'):
        md_loader = DirectoryLoader('./samples/markdown', glob="**/*.md")
        documents = md_loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        documents = text_splitter.split_documents(documents)
        vectordb = Chroma.from_documents(
            documents,
            embedding=OpenAIEmbeddings(),
            persist_directory='./data'
        )
        vectordb.persist()
        st.session_state.vectordb = vectordb
        st.success('Successfully trained your AI!')

if select_options == options[1]: 
    if 'vectordb' not in st.session_state or st.session_state.vectordb is None:
        st.warning('You need to first train your AI')
    else:
        if 'history' not in st.session_state or st.session_state.history is None:
            st.session_state.history = []

        for msg in st.session_state.history:
            mh = st.chat_message(msg[0])
            mh.write(msg[1])

        prompt = st.chat_input("Chat with your files:")

        if prompt:    
            message = st.chat_message('User')
            message.write(prompt)
            st.session_state.history.append(('User', prompt))

            with st.spinner('Please wait...'):
                qa_chain = RetrievalQA.from_chain_type(
                    llm=OpenAI(api_key=os.environ['OPENAI_API_KEY']),
                    return_source_documents=True,
                    retriever=st.session_state.vectordb.as_retriever(search_kwargs={'k': 5})
                )
                result = qa_chain({'query': prompt})

                message2 = st.chat_message('Chat')

                # Append metadata information to the response. Must comment line before this one to work.
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

if select_options == options[2]:
    st.session_state.history = []
    st.success('Session history restarted!')