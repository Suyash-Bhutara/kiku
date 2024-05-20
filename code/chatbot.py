# Load environment variables
from dotenv import load_dotenv

load_dotenv()
import os
import streamlit as st
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from utils import *
from session_state import initialize_session_state

# App configuration
st.set_page_config(page_title="Kiku", page_icon="🤖")
st.title("Japanese Tutor")


japanese_tutor_instructions = """
Your job is to answer the user's query and respond to them adhering to the following template:
TEMPLATE:

`
JAPANESE: Respond to the user's query according to your character in Japanese.  
TRANSLITERATION: Convert your Japanese response to its romanji transliteration.  
TRANSLATION: Finally translate your response into English.  
`
Remember the following points:
1. Your answer will be parsed as a markdown, so separate all the three language responses with a '  ' (double space) to make sure all three responses appear in a separate newline.
2. No need to mention headers like `JAPANESE`, `TRANSLITERATION`, `TRANSLATION`. Directly mention your answer.
3. DO NOT add bullet points or number points just to separate the 3 language versions."""


# Function to get the streaming response from the LLM
def get_response(llm, user_query, bot_name, bot_instructions, chat_history):
    """
    Gets a response from the LLM based on the bot instructions, user query and chat history.

    Args:
        llm (AzureChatOpenAI/ChatOpenAI/others): The LLM object to use.
        user_query (str): The user's query.
        bot_instructions (SystemMessage): The instructions for the bot.
        chat_history (list): The chat history.

    Returns:
        str: The response from the LLM.
    """
    template = """  
    {bot_instructions}


    Chat history: {chat_history}  
    User: {user}  
    """
    prompt = ChatPromptTemplate.from_template(template)

    chain = prompt | llm | StrOutputParser()
    chat_interaction_history = format_chat_history(chat_history, bot_name)
    return chain.invoke(
        {
            "bot_instructions": bot_instructions.content,
            "chat_history": chat_interaction_history,
            "user": user_query,
        }
    )


# Add a sidebar with a dropdown for various configurations
personas = load_personas("./personas.json")
persona_options = list(personas.keys())
models = ["GPT-3.5", "GPT-4"]

with st.sidebar:
    st.header("Configurations")
    st.write("Select a persona")
    selected_persona = st.selectbox(
        "Select a Persona", persona_options, label_visibility="collapsed"
    )
    st.write("Select desired LLM for the chatbot")
    selected_model = st.selectbox(
        "Select a Model", models, label_visibility="collapsed"
    )
    st.divider()
    llm = initialize_llm(model_name=selected_model)


initialize_session_state()

# Set SystemMessage and AIMessage based on selected persona
selected_system_message = personas[selected_persona]["SystemMessage"]
selected_ai_message = personas[selected_persona]["AIMessage"]

# Initialize the chat history in the session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = reset_chat_history(selected_ai_message)

if selected_persona != st.session_state.selected_persona:
    st.session_state.selected_persona = selected_persona
    st.session_state.chat_history = reset_chat_history(selected_ai_message)

if selected_model != st.session_state.selected_model:
    st.session_state.selected_model = selected_model
    st.session_state.chat_history = reset_chat_history(selected_ai_message)

# Display the chat history
chat_container = st.container()
with chat_container:
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(message.content)

# Get user input and generate response
user_query = st.chat_input("Type your message here...")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    with st.chat_message("Human"):
        st.markdown(user_query)
    with st.chat_message("AI"):
        bot_instructions = SystemMessage(
            content=selected_system_message + japanese_tutor_instructions
        )
        response = get_response(
            llm, user_query, selected_persona, bot_instructions, st.session_state.chat_history
        )
        st.markdown(response)
        update_chat_history(st.session_state.chat_history, AIMessage(content=response))
