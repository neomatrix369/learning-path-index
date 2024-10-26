import os
from dotenv import load_dotenv
from datetime import datetime
import time
from langchain.llms import OpenAI
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate

from interface import app
import streamlit as st
# Define GenerateLearningPathIndexEmbeddings class: 
#  - Load .csv file
#  - Chunk text
#    - Chunk size = 1000 characters
#    - Chunk overlap = 30 characters
#  - Create FAISS vector store from chunked text and OpenAI embeddings
#  - Get FAISS vector store
# This class is used to generate the FAISS vector store from the .csv file.
class GenerateLearningPathIndexEmbeddings:
    def __init__(self, csv_filename):
        load_dotenv()  # Load .env file
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        # load the csv file from the data folder above 2 folders
        # self.data_path = os.path.join('..\..\data', csv_filename)
        self.data_path = os.path.join('../../data', csv_filename)
        self.data_path = os.path.join('data', csv_filename)
        self.our_custom_data = None
        self.openai_embeddings = None
        self.faiss_vectorstore = None

        self.load_csv_data()
        self.get_openai_embeddings()
        self.create_faiss_vectorstore_with_csv_data_and_openai_embeddings()
           
    def load_csv_data(self):
        # Load your dataset (e.g., CSV, JSON, etc.)
        print(' -- Started loading .csv file for chunking purposes.')
        loader = TextLoader(self.data_path)
        document = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=30, separator="\n")
        self.our_custom_data = text_splitter.split_documents(document)
        print(f' -- Finished spitting (i.e. chunking) text (i.e. documents) from the .csv file (i.e. {self.data_path}).')
        
    def get_openai_embeddings(self):
        self.openai_embeddings = OpenAIEmbeddings(openai_api_key=self.openai_api_key, request_timeout=60)
        
    def create_faiss_vectorstore_with_csv_data_and_openai_embeddings(self):
        faiss_vectorstore_foldername = "faiss_learning_path_index"
        if not os.path.exists(faiss_vectorstore_foldername):
            print(' -- Creating a new FAISS vector store from chunked text and OpenAI embeddings.')
            vectorstore = FAISS.from_documents(self.our_custom_data, self.openai_embeddings)
            vectorstore.save_local(faiss_vectorstore_foldername)
            print(f' -- Saved the newly created FAISS vector store at "{faiss_vectorstore_foldername}".')
        else:
            print(f' -- WARNING: Found existing FAISS vector store at "{faiss_vectorstore_foldername}", loading from cache.')
            print(f' -- NOTE: Delete the FAISS vector store at "{faiss_vectorstore_foldername}", if you wish to regenerate it from scratch for the next run.')
        self.faiss_vectorstore = FAISS.load_local(
            "faiss_learning_path_index", self.openai_embeddings
        )

    def get_faiss_vector_store(self):
        return self.faiss_vectorstore


# https://discuss.streamlit.io/t/how-to-check-if-code-is-run-inside-streamlit-and-not-e-g-ipython/23439/7
def running_inside_streamlit():
    """
    Function to check whether python code is run within streamlit

    Returns
    -------
    use_streamlit : boolean
        True if code is run within streamlit, else False
    """
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if not get_script_run_ctx():
            use_streamlit = False
        else:
            use_streamlit = True
    except ModuleNotFoundError:
        use_streamlit = False
    return use_streamlit


# Define GenAI class:
#  - Create prompt template
#  - Create GenAI project
#  - Get response for query
# This class is used to get the response for a query from the GenAI project.
# The GenAI project is created from the FAISS vector store.
class GenAILearningPathIndex:
    def __init__(self, faiss_vectorstore):
        load_dotenv()  # Load .env file
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.faiss_vectorstore = faiss_vectorstore

        prompt_template = \
            """
                Use the following template to answer the question at the end, 
                from the Learning Path Index csv file,
                display top 10 results in a tablular format and it 
                should look like this:
                | Learning Pathway | duration  | link | Module
                | --- | --- | --- | --- |
                | ... | ... | ... | ... |
                it must contain a link for each line of the result in a table,
                consider the duration and Module information mentioned in the question,
                If you don't know the answer, don't make an entry in the table,
                {context}
                Question: {question}
            """
        PROMPT = PromptTemplate(template=prompt_template, input_variables=["context","question"])
        # The chain_type_kwargs are passed to the chain_type when it is created.
        self.chain_type_kwargs = {"prompt": PROMPT}
        # Create the GenAI project 
        self.llm = OpenAI(temperature=1.0, openai_api_key=self.openai_api_key)
    # Get response for query
    # The response is returned as a string.   
       
    def get_response_for(self, query: str):
        qa = RetrievalQA.from_chain_type(
            llm=self.llm, chain_type="stuff", 
            retriever=self.faiss_vectorstore.as_retriever(),
            chain_type_kwargs=self.chain_type_kwargs
        )
        return qa.run(query)

def get_formatted_time(current_time = time.time()):
    return datetime.utcfromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')

#   Load the model
@st.cache_data
def load_model():
    start_time = time.time()
    print(f"\nStarted loading custom embeddings (created from .csv file) at {get_formatted_time(start_time)}")
    learningPathIndexEmbeddings = GenerateLearningPathIndexEmbeddings("Learning_Pathway_Index.csv")
    faiss_vectorstore = learningPathIndexEmbeddings.get_faiss_vector_store()
    end_time = time.time()
    print(f"Finished loading custom embeddings (created from .csv file) at {get_formatted_time(end_time)}")
    print(f"Custom embeddings (created from .csv file) took about {end_time - start_time} seconds to load.")
    return faiss_vectorstore

#  Query the model
def query_gpt_model(query: str):
    start_time = time.time()
    print(f"\nQuery processing start time: {get_formatted_time(start_time)}")
    genAIproject = GenAILearningPathIndex(faiss_vectorstore)
    answer = genAIproject.get_response_for(query)
    end_time = time.time()
    print(f"\nQuery processing finish time: {get_formatted_time(end_time)}")
    print(f"\nAnswer (took about {end_time - start_time} seconds)")
    return answer


if __name__=='__main__':
    faiss_vectorstore = load_model()

    if running_inside_streamlit():
        print("\nStreamlit environment detected. \nTo run a CLI interactive version just run `python main.py` in the CLI.\n")
        query_from_stream_list = app()
        if query_from_stream_list:
            answer = query_gpt_model(query_from_stream_list)
            st.write(answer)
    else:
        print("\nCommand-line interactive environment detected.\n")
        while True:
            query = input("\nEnter a query: ")
            if query == "exit":
                break
            if query.strip() == "":
                continue

            if query:
                answer = query_gpt_model(query)

                print("\n\n> Question:")
                print(query)
                print(answer)
