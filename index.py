import streamlit as st
import os
import shutil

from config import OPENAI_KEY
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI

os.environ['OPENAI_API_KEY'] = OPENAI_KEY

# Clearing the data and tmp directories
# shutil.rmtree('./data')
# shutil.rmtree('./tmp')
# os.makedirs('./data')
# os.makedirs('./tmp')    

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
    st.text('Select the PDF(s) class(es) to train your chatbot:')
    files = st.file_uploader('File:', accept_multiple_files=True, type=['pdf'])
    if files:
        if st.button('Train'): 
            for file in files:
                with open('./tmp/' + file.name, "wb") as f:
                    f.write(file.getbuffer())
                    pdf_loader = PyPDFLoader('./tmp/' + file.name)
            documents = pdf_loader.load()
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

        prompt = st.chat_input("Chat with your file:")

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
                message2.write(result['result'])

                # Append metadata information to the response. Must comment line before this one to work.
                # message2.write(result['result'] + "\n\n --- \n\n")
                # metadata_info = "References List:\n\n"
                # reference_count = 1
                # for doc in result['source_documents']:
                #     metadata = doc.metadata
                #     metadata_str = f"Reference {reference_count}: Page = {metadata.get('page')} | Source = {metadata.get('source')}\n\n"
                #     metadata_info += metadata_str
                #     reference_count += 1
                # message2.write("\n" + metadata_info)

                st.session_state.history.append(('Chat', result['result']))

if select_options == options[2]:
    st.session_state.history = []
    st.success('Session history restarted!')