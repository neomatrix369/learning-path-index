#!/usr/bin/env python3
import argparse
import os
import time
from datetime import datetime

import torch
from constants import CHROMA_SETTINGS
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma

OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')


def build_model():
    IS_GPU_AVAILABLE = torch.cuda.is_available()
    (
        print(
            f'~~~ GPU is available (CUDA-DNN Enabled: {torch.backends.cudnn.enabled}) ~~~'
        )
        if IS_GPU_AVAILABLE
        else print('~~~ GPU is NOT available, falling back to CPU ~~~')
    )

    # https://smith.langchain.com/hub/rlm/rag-prompt-mistral
    #                          or
    # https://smith.langchain.com/hub/rlm/rag-prompt-llama
    prompt_template = """
        [INST]
        <<SYS>> You are an assistant for question-answering tasks using the Learning Path Index.
        Show the results in a table or tabular form, and the results must contain a link for each line of the courses, modules or sub-modules returned.
        <</SYS>>
        Context: {context}
        Question: {question}
        Answer: [/INST]
    """
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=['context', 'question']
    )
    chain_type_kwargs = {'prompt': PROMPT}

    start = time.time()

    # Parse the command line arguments
    args = parse_arguments()
    embeddings = HuggingFaceEmbeddings(model_name=args.embeddings_model_name)
    vector_db = Chroma(
        persist_directory=args.persist_directory,
        embedding_function=embeddings,
        client_settings=CHROMA_SETTINGS,
    )
    retriever = vector_db.as_retriever(search_kwargs={'k': args.target_source_chunks})

    # activate/deactivate the streaming StdOut callback for LLMs
    callbacks = [] if args.mute_stream else [StreamingStdOutCallbackHandler()]

    llm = Ollama(model=args.chat_model, callbacks=callbacks, base_url=OLLAMA_HOST)

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=retriever,
        return_source_documents=not args.hide_source,
        chain_type_kwargs=chain_type_kwargs,
    )

    end = time.time()

    print(f'Models took about {end - start} seconds to load.')
    return qa, llm


def main():
    args = parse_arguments()
    qa, _ = build_model()
    # Interactive questions and answers
    while True:
        query = input('\nEnter a query: ')
        if query == 'exit':
            break
        if query.strip() == '':
            continue

        # Get the answer from the chain
        start = time.time()
        print(
            f"\nStart time: {datetime.utcfromtimestamp(start).strftime('%Y-%m-%d %H:%M:%S')}"
        )
        answer = qa({'query': query})
        answer, _docs = (
            answer['result'],
            ([] if args.hide_source else answer['source_documents']),
        )
        end = time.time()

        # Print the result
        print('\n\n> Question:')
        print(query)
        print(
            f"\nEnd time: {datetime.utcfromtimestamp(end).strftime('%Y-%m-%d %H:%M:%S')}"
        )
        print(f'\nAnswer (took about {end - start} seconds):')
        print(answer)

        # # Print the relevant sources used for the answer
        # for document in docs:
        #     print("\n> " + document.metadata["source"] + ":")
        #     print(document.page_content)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='lpiGPT: Ask questions to your documents without an internet connection, '
        'using the power of LLMs (the InstructGPT or Chat model).'
    )
    # https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard or https://ollama.ai/library
    parser.add_argument(
        '--chat-model',
        '-CM',
        action='store',
        default='llama2-uncensored',
        help='Use this flag to set the InstructGPT or Chat model name, see https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard or https://ollama.ai/library for more names.',
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
        help='Use this flag to set the Embeddings model name, see https://www.sbert.net/docs/pretrained_models.html for examples of names. Use the same model as used for ingesting the documents (ingest.py)',
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
        '--hide-source',
        '-S',
        action='store_true',
        help='Use this flag to disable printing of source documents used for answers.',
    )

    parser.add_argument(
        '--mute-stream',
        '-M',
        action='store_true',
        help='Use this flag to disable the streaming StdOut callback for LLMs.',
    )

    return parser.parse_args()


if __name__ == '__main__':
    main()
