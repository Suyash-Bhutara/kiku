import os
import json
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import AzureChatOpenAI


def load_personas(filepath):
    """
    Loads personas from a JSON file.

    Args:
        filepath (str): The path to the JSON file containing personas.

    Returns:
        dict: A dictionary containing the personas.
    """
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)


# Function to initialize LLM
def initialize_llm(model_name):
    """
    Initializes the LLM (Language Learning Model) based on the model name.

    Args:
        model_name (str): The name of the model to initialize ('GPT-3.5' or 'GPT-4').

    Returns:
        AzureChatOpenAI: The initialized LLM object.
    """
    if model_name == "GPT-3.5":
        return ChatOpenAI(
            openai_api_key=os.environ["OPENAI_API_KEY"],
            model_name="gpt-3.5-turbo",
            temperature=0.1,
        )
    elif model_name == "GPT-4":
        return ChatOpenAI(
            openai_api_key=os.environ["OPENAI_API_KEY"],
            model_name="gpt-4",
            temperature=0.1,
        )


def reset_chat_history(ai_message):
    """
    Resets the chat history with an initial AI message.

    Args:
        ai_message (str): The initial message from the AI.

    Returns:
        list: A list containing the initial AI message.
    """
    return [AIMessage(content=ai_message)]


def update_chat_history(chat_history, message):
    """
    Updates the chat history by appending a new message.

    Args:
        chat_history (list): The current chat history.
        message (str): The new message to add to the chat history.

    Returns:
        list: The updated chat history.
    """
    chat_history.append(message)
    return chat_history


def format_chat_history(chat_history, persona_name):
    """
    Formats the chat history into a string for display.

    Args:
        chat_history (list): The chat history to format.
        persona_name (str): Name of the bot.

    Returns:
        str: The formatted chat history.
    """
    interaction_history = ""
    for ch in chat_history:
        if isinstance(ch, AIMessage):
            interaction_history += f"{persona_name}: {ch.content}\n"
        elif isinstance(ch, HumanMessage):
            interaction_history += f"User: {ch.content}\n"
    return interaction_history
