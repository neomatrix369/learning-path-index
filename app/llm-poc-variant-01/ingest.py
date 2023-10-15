#!/usr/bin/env python3
import os
import glob
from typing import List
from multiprocessing import Pool
from tqdm import tqdm
import argparse

from langchain.document_loaders import (
    CSVLoader
)

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from constants import CHROMA_SETTINGS


# Map file extensions to document loaders and their arguments
LOADER_MAPPING = {
    ".csv": (CSVLoader, {}),
    # Add more mappings for other file extensions and loaders as needed
}


def load_single_document(file_path: str) -> List[Document]:
    ext = "." + file_path.rsplit(".", 1)[-1]
    if ext in LOADER_MAPPING:
        loader_class, loader_args = LOADER_MAPPING[ext]
        loader = loader_class(file_path, **loader_args)
        return loader.load()

    raise ValueError(f"Unsupported file extension '{ext}'")

def load_documents(source_dir: str, ignored_files: List[str] = []) -> List[Document]:
    """
    Loads all documents from the source documents directory, ignoring specified files
    """
    all_files = []
    for ext in LOADER_MAPPING:
        all_files.extend(
            glob.glob(os.path.join(source_dir, f"**/*{ext}"), recursive=True)
        )
    filtered_files = [file_path for file_path in all_files if file_path not in ignored_files]

    with Pool(processes=os.cpu_count()) as pool:
        results = []
        with tqdm(total=len(filtered_files), desc='Loading new documents', ncols=80) as pbar:
            for i, docs in enumerate(pool.imap_unordered(load_single_document, filtered_files)):
                results.extend(docs)
                pbar.update()

    return results

def process_documents(source_directory: str,
                      chunk_size: int,
                      chunks_overlap: int,
                      ignored_files: List[str] = []) -> List[Document]:
    """
    Load documents and split in chunks
    """
    print(f"Loading documents from {source_directory}")
    documents = load_documents(source_directory, ignored_files)
    if not documents:
        print("No new documents to load")
        exit(0)
    print(f"Loaded {len(documents)} new documents from {source_directory}")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunks_overlap=chunks_overlap)
    texts = text_splitter.split_documents(documents)
    print(f"Split into {len(texts)} chunks of text (max. {chunk_size} tokens each)")
    return texts

def does_vectorstore_exist(persist_directory: str) -> bool:
    """
    Checks if vectorstore exists
    """
    if os.path.exists(os.path.join(persist_directory, 'index')):
        if os.path.exists(os.path.join(persist_directory, 'chroma-collections.parquet')) and os.path.exists(os.path.join(persist_directory, 'chroma-embeddings.parquet')):
            list_index_files = glob.glob(os.path.join(persist_directory, 'index/*.bin'))
            list_index_files += glob.glob(os.path.join(persist_directory, 'index/*.pkl'))
            # At least 3 documents are needed in a working vectorstore
            if len(list_index_files) > 3:
                return True
    return False


def parse_arguments():
    parser = argparse.ArgumentParser(description='ingest: process one or more documents (text) in order to create embeddings '
                                                 'from them, and make them ready to be used with LLMs.')
    # For embeddings model, the example uses a sentence-transformers model
    # https://www.sbert.net/docs/pretrained_models.html 
    # "The all-mpnet-base-v2 model provides the best quality, while all-MiniLM-L6-v2 is 5 times faster 
    # and still offers good quality."
    parser.add_argument("--embeddings-model-name", "-EM", action='store', default="all-MiniLM-L6-v2",
                        help='Use this flag to set the Embeddings model name, see https://www.sbert.net/docs/pretrained_models.html for examples of names. Use the same model when running the lpiGPT.py app.')

    parser.add_argument("--source-directory", "-S", action='store', default="source_directory",
                        help='Use this flag to specify the name of the source folder where all the documents are stored (for ingestion purposes) on the local machine.')

    parser.add_argument("--persist-directory", "-P", action='store', default="vector_db",
                        help='Use this flag to specify the name of the vector database i.e. vector_db - this will be a folder on the local machine.')

    parser.add_argument("--target-source-chunks", "-C", action='store', default=500,
                        help='Use this flag to specify the name chunk size to use to chunk source data.')
    
    parser.add_argument("--chunks-overlap", "-O", action='store', default=50,
                        help='Use this flag to specify the name chunk overlap value to use to chunk source data.')

    return parser.parse_args()


def main():
    args = parse_arguments()

    # Create embeddings
    embeddings = HuggingFaceEmbeddings(model_name=args.embeddings_model_name)

    if does_vectorstore_exist(args.persist_directory):
        # Update and store locally vectorstore
        print(f"Appending to existing vectorstore at {args.persist_directory}")
        vector_db = Chroma(
            persist_directory=args.persist_directory, 
            embedding_function=embeddings, 
            client_settings=CHROMA_SETTINGS
        )
        collection = vector_db.get()
        texts = process_documents(
            args.source_directory,
            args.target_source_chunks,
            args.chunks_overlap,
            [metadata['source'] for metadata in collection['metadatas']]
        )
        print(f"Creating embeddings. May take some minutes...")
        vector_db.add_documents(texts)
    else:
        # Create and store locally vectorstore
        print("Creating new vectorstore")
        texts = process_documents(args.source_directory, 
                                  args.target_source_chunks,
                                  args.chunks_overlap)
        print(f"Creating embeddings. May take some minutes...")
        vector_db = Chroma.from_documents(texts, embeddings, 
                                          persist_directory=args.persist_directory, 
                                          client_settings=CHROMA_SETTINGS)
    vector_db.persist()
    vector_db = None

    print(f"Ingestion complete! You can now run lpiGPT.py to query your documents")


if __name__ == "__main__":
    main()
