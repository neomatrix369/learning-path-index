# https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps#build-a-chatgpt-like-app
# https://github.com/AI-Yash/st-chat/blob/7c9849537a72fe891e8a4c4bfa04b71aa480e62c/streamlit_chat/__init__.py#L31

import streamlit as st
from streamlit_chat import message

from langchain.document_loaders import CSVLoader
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chains import ConversationalRetrievalChain

from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma

st.set_page_config(page_title="KaggleX AI Course Coordinator (Demo)", page_icon=":robot_face:")

#######################################################
####################### Sidebar #######################
st.sidebar.title("Introduction (Demo)")
st.sidebar.markdown("""
KaggleX AI Course Coordinator is an advanced conversational AI, expertly crafted to solve the data science learners' problems.

<ul style='text-align: left;'>
<li><strong>What is KaggleX AI Course Coordinator?</strong>: It is part of the Learning Path Index Project. One of the objectives is to consolidate a data base which collects a collection of byte-sized courses/materials for Data Science and Machine Learning so that it is 
easy for the learners to search and filter.</li>
<li><strong>Why Do We Need It?</strong>: Addresses problems like long course durations, difficulty in finding specific topics, and the absence of a centralized index.</li>

</ul>

""", unsafe_allow_html=True)

st.sidebar.markdown("<p style='text-align: right'>Developed and maintained by <a href='https://entzyeung.github.io/portfolio/index.html'>Lorentz Yeung</a></p>", unsafe_allow_html=True)

#######################################################
####################### UI ############################
# Setting page title and header

st.markdown("<h1 style='text-align: center; color: navy;'>KaggleX AI Course Coordinator</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>(Demo)</h4>", unsafe_allow_html=True)
st.markdown("<p style='text-align: right'>By <a href='https://entzyeung.github.io/portfolio/index.html'>Lorentz Yeung</a></p>", unsafe_allow_html=True)
# st.session_state['API_Key']= st.text_input("First, to get it work, put your OpenAI API Key here please, the system will enter for you automatically.",type="password")


#if 'API_Key' not in st.session_state:
#    st.session_state['API_Key'] =''
#st.session_state['API_Key']= st.text_input("First, to get it work, put your OpenAI API Key here please, the system will enter for you automatically.",type="password")
# uploaded_file = st.sidebar.file_uploader("upload", type="csv")

persist_directory = "chroma/db"


if persist_directory :
    embeddings = OpenAIEmbeddings()

    KaggleX_courses_db = Chroma(persist_directory = persist_directory, embedding_function=embeddings)
    retriever = KaggleX_courses_db.as_retriever() # search_kwargs={"k": 4}

    chain = ConversationalRetrievalChain.from_llm(llm = ChatOpenAI(temperature=0.0,model_name='gpt-3.5-turbo',
                                                                ),
                                                                retriever = retriever)

    def conversational_chat(query):

        result = chain({"question": query, "chat_history": st.session_state['history']})
        st.session_state['history'].append((query, result["answer"]))

        return result["answer"]

    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if 'ai_history' not in st.session_state:
        st.session_state['ai_history'] = ["Sure, I am here to help!"]

    if 'user_history' not in st.session_state:
        st.session_state['user_history'] = ["Hi, I would like to know more about the courses in KaggleX!"]

    #container for the chat history
    response_container = st.container()
    #container for the user's text input
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):

            user_input = st.text_input("Your question:", placeholder="I want to learn linear regressions, which module is for me?", key='input')
            submit_button = st.form_submit_button(label='Ask')

        if submit_button and user_input:
            output = conversational_chat(user_input) # if the button is clicked, then submit he query to the Chain, and take the history from session_state.

            st.session_state['user_history'].append(user_input) # store the user input to user history
            st.session_state['ai_history'].append(output) # store the AI prediction to ai history

    # the chat interface.
    if st.session_state['ai_history']:
        with response_container:
            for i in range(len(st.session_state['ai_history'])):
                # https://docs.streamlit.io/library/api-reference/chat/st.chat_message
                # https://discuss.streamlit.io/t/streamlit-chat-avatars-not-working-on-cloud/46713/2
                # thumbs, adventurer, big-smile, micah, bottts
                message(st.session_state["user_history"][i], is_user=True, key=str(i) + '_user', avatar_style="identicon")
                # message(st.session_state["ai_history"][i], key=str(i), avatar_style="KaggleX.jpg")
                message(st.session_state["ai_history"][i], key=str(i), avatar_style='bottts')
                #st.chat_message(st.session_state["user_history"][i], is_user=True, key=str(i) + '_user', AvatarStyle="adventurer")
                #st.chat_message(st.session_state["ai_history"][i], key=str(i), AvatarStyle='bottts-neutral')

