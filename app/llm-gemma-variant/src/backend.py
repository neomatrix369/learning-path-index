import os 
from dotenv import load_dotenv
from llama_index.core import Settings
from loguru import logger
from llama_index.llms.ollama import Ollama
from model import Gemma
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from vector_db import VectorDB
from pathlib import Path

def main():
    # Load and verify API key
    load_dotenv('credentials.env')

    # Initialize the model
    gemma2_2b = Ollama(model="gemma2:2b", request_timeout=30.0)
    llm_model = Gemma(gemma2_2b, 2000)
    Settings.llm = llm_model

    # Initialize embedding model
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

    current_directory = os.getcwd()
    data_path = current_directory + "//LPI_folder//Learning_Pathway_Index.csv"
    folder_path = current_directory + "//LPI_folder"
    logger.info(f"Current directory: {current_directory}")

    # Initialize the VectorDB class
    weaviate_vector_db = VectorDB(
        folder_path=folder_path,
        data_path=data_path,
        index_name="Learning_path_index"
    )
    
    # Create the vector database
    index = weaviate_vector_db.vector_db_creation()

    # Initialize RAG
    naive_rag_query_engine = index.as_query_engine()

    # Run your naive RAG query
    response = naive_rag_query_engine.query("What courses should I take if i want to learn about finetuning?")

    logger.info(response.response)

if __name__ == "__main__":
    main()

