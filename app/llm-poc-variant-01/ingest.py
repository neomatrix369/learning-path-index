#!/usr/bin/env python3
import argparse
import glob
import os
import time
from multiprocessing import Pool
from typing import List

from constants import CHROMA_SETTINGS
from langchain.docstore.document import Document
from langchain.document_loaders import CSVLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from tqdm import tqdm

# Map file extensions to document loaders and their arguments
LOADER_MAPPING = {
    '.csv': (CSVLoader, {}),
    # Add more mappings for other file extensions and loaders as needed
}


def load_single_document(file_path: str) -> List[Document]:
    ext = '.' + file_path.rsplit('.', 1)[-1]
    if ext in LOADER_MAPPING:
        loader_class, loader_args = LOADER_MAPPING[ext]
        loader = loader_class(file_path, **loader_args)
        return loader.load()

    raise ValueError(f"Unsupported file extension '{ext}'")


def load_documents(source_dir: str, ignored_files: List[str] = None) -> List[Document]:
    """
    Loads all documents from the source documents directory, ignoring specified files
    """
    if not ignored_files:
        ignored_files = []
    all_files = []
    for ext in LOADER_MAPPING:
        all_files.extend(
            glob.glob(os.path.join(source_dir, f'**/*{ext}'), recursive=True)
        )
    filtered_files = [
        file_path for file_path in all_files if file_path not in ignored_files
    ]

    with Pool(processes=os.cpu_count()) as pool:
        results = []
        with tqdm(
            total=len(filtered_files), desc='Loading new documents', ncols=80
        ) as pbar:
            for _, docs in enumerate(
                pool.imap_unordered(load_single_document, filtered_files)
            ):
                results.extend(docs)
                pbar.update()

    return results


def process_documents(
    source_documents: str,
    chunk_size: int,
    chunk_overlap: int,
    ignored_files: List[str] = None,
) -> List[Document]:
    """
    Load documents and split in chunks
    """
    if not ignored_files:
        ignored_files = []
    start_time = time.time()
    print(f'Loading documents from {source_documents}')
    documents = load_documents(source_documents, ignored_files)
    if not documents:
        print('No new documents to load')
        exit(0)
    print(f'Loaded {len(documents)} new documents from {source_documents}')
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    texts = text_splitter.split_documents(documents)
    print(f'Split into {len(texts)} chunks of text (max. {chunk_size} tokens each)')
    end_time = time.time()
    print(f'Loading documents took about {end_time - start_time} seconds to complete.')
    return texts


def does_vectorstore_exist(persist_directory: str) -> bool:
    """
    Checks if vectorstore exists
    """
    if os.path.exists(os.path.join(persist_directory, 'index')):
        if os.path.exists(
            os.path.join(persist_directory, 'chroma-collections.parquet')
        ) and os.path.exists(
            os.path.join(persist_directory, 'chroma-embeddings.parquet')
        ):
            list_index_files = glob.glob(os.path.join(persist_directory, 'index/*.bin'))
            list_index_files += glob.glob(
                os.path.join(persist_directory, 'index/*.pkl')
            )
            # At least 3 documents are needed in a working vectorstore
            if len(list_index_files) > 3:
                return True
    return False


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='ingest: process one or more documents (text) in order to create embeddings (using the Embeddings models)'
        'from them, and make them ready to be used with LLMs when a question is asked to the InstructGPT or Chat Model.'
    )
    # For embeddings model, the example uses a sentence-transformers model
    # https://www.sbert.net/docs/pretrained_models.html
    # "The all-mpnet-base-v2 model provides the best quality, while all-MiniLM-L6-v2 is 5 times faster
    # and still offers good quality."
    parser.add_argument(
        '--embeddings-model-name',
        '-EM',
        action='store',
        default='all-MiniLM-L6-v2',
        help='Use this flag to set the Embeddings model name, see https://www.sbert.net/docs/pretrained_models.html for examples of names. Use the same model when running the lpiGPT.py app.',
    )

    parser.add_argument(
        '--source-documents',
        '-S',
        action='store',
        default='source_documents',
        help='Use this flag to specify the name of the folder where all the (source/input) documents are stored for ingestion purposes, on the local machine. The documents contained in them are of the type `.csv`.',
    )

    parser.add_argument(
        '--persist-directory',
        '-P',
        action='store',
        default='vector_db',
        help='Use this flag to specify the name of the vector database, this will be a folder on the local machine.',
    )

    parser.add_argument(
        '--target-source-chunks',
        '-C',
        action='store',
        default=500,
        help='Use this flag to specify the name chunk size to use to chunk source data.',
    )

    parser.add_argument(
        '--chunk-overlap',
        '-O',
        action='store',
        default=50,
        help='Use this flag to specify the name chunk overlap value to use to chunk source data.',
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    start_time = time.time()
    # Create embeddings
    print('\nCreating/downloading HF embeddings started...')
    embeddings = HuggingFaceEmbeddings(model_name=args.embeddings_model_name)
    end_time = time.time()
    print(
        f'Creating/downloading HF embeddings completed! It took about {end_time - start_time} seconds to complete.'
    )

    start_time = time.time()
    print('\nStarted with ingestion process, to create vector database...')
    if does_vectorstore_exist(args.persist_directory):
        # Update and store locally vectorstore
        print(f'-- Appending to existing vectorstore at {args.persist_directory}')
        vector_db = Chroma(
            persist_directory=args.persist_directory,
            embedding_function=embeddings,
            client_settings=CHROMA_SETTINGS,
        )
        collection = vector_db.get()
        texts = process_documents(
            args.source_documents,
            args.target_source_chunks,
            args.chunk_overlap,
            [metadata['source'] for metadata in collection['metadatas']],
        )
        print('-- Creating embeddings. May take some minutes...')
        vector_db.add_documents(texts)
    else:
        # Create and store locally vectorstore
        print('-- Creating new vectorstore')
        texts = process_documents(
            args.source_documents, args.target_source_chunks, args.chunk_overlap
        )
        print('-- Creating embeddings. May take some minutes...')
        vector_db = Chroma.from_documents(
            texts,
            embeddings,
            persist_directory=args.persist_directory,
            client_settings=CHROMA_SETTINGS,
        )
    vector_db.persist()
    vector_db = None
    end_time = time.time()

    print(
        f'Ingestion complete! It took about {end_time - start_time} seconds to complete.'
    )
    print('\nYou can now run lpiGPT.py to query your documents')


if __name__ == '__main__':
    main()
