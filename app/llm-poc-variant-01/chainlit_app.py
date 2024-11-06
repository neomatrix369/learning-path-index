import chainlit as cl
from chainlit.input_widget import Select, Slider
from constants import PERSIST_DIRECTORY
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.runnable.config import RunnableConfig
from lpiGPT import build_model, build_retriever


def build_runnable_from_settings(settings: dict):
    retriever = build_retriever(
        model_embeddings=settings['ModelEmbeddings'],
        persist_directory=PERSIST_DIRECTORY,
    )
    _qa, llm = build_model(retriever, model_name=settings['ModelName'])
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                'system',
                """
            You are an assistant for question-answering tasks using the Learning Path Index.
            Show the results in a table or tabular form, and the results must contain a link for each line of the courses, modules or sub-modules returned.
            """,
            ),
            ('human', '{question}'),
        ]
    )

    runnable = (
        {'context': retriever | format_docs, 'question': RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return runnable


@cl.on_settings_update
async def setup_agent(settings):
    await cl.Message(
        content='Updating settings',
    ).send()
    runnable = build_runnable_from_settings(settings)
    cl.user_session.set('settings', settings)
    cl.user_session.set('runnable', runnable)


def format_docs(docs):
    return '\n\n'.join(doc.page_content for doc in docs)


@cl.on_chat_start
async def on_chat_start():
    settings = await cl.ChatSettings(
        [
            Select(
                id='ModelName',
                label='Chat Model',
                values=['gemma:2b', 'llama2-uncensored'],
                initial_index=0,
            ),
            Select(
                id='ModelEmbeddings',
                label='Model Embeddings',
                values=['all-MiniLM-L6-v2'],
                initial_index=0,
            ),
            Slider(
                id='TargetSourceChunks',
                label='Target Source Chunks',
                initial=500,
                min=250,
                max=2000,
                step=50,
            ),
        ]
    ).send()
    runnable = build_runnable_from_settings(settings)

    cl.user_session.set('settings', settings)
    cl.user_session.set('runnable', runnable)


@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get('runnable')

    msg = cl.Message(content='')

    for chunk in await cl.make_async(runnable.stream)(
        message.content,
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)

    await msg.send()
