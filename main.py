# Import the necessary modules  
import os  
from dotenv import load_dotenv  
  
# Load environment variables from a .env file  
load_dotenv()  
  
# Import specific classes from langchain  
from langchain_openai import ChatOpenAI  
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage  
  
# Initialize the AzureChatOpenAI object with the appropriate parameters  
# - openai_api_key: Retrieves the OpenAI API key from the environment variables  
# - model_name: Specifies the model to be used, in this case "gpt-3.5-turbo"  
# - temperature: Sets the randomness of the model's responses (0.0 means no randomness)  
llm = ChatOpenAI(  
    openai_api_key=os.environ["OPENAI_API_KEY"],  
    model_name="gpt-3.5-turbo",  
    temperature=0.0,  
)  
  
def chat_with_tutor():  
    """  
    Function that initiates a chat session with an AI assistant playing the role of Uzumaki Naruto.  
    The assistant responds to the user's queries according to a predefined template:  
    1. Responds in Japanese.  
    2. Provides a romanji transliteration.  
    3. Translates the response to English.  
    """  
  
    # Predefined initial messages for the chat session  
    messages = [  
        SystemMessage(content="""You're an Assistant who takes on the character of `Uzumaki Naruto`, a ninja from the Anime Naruto. Your job is to answer the user's query and respond to them adhering to the following template:  
        TEMPLATE:  
        1. JAPANESE: Respond to the user's query in Japanese.  
        2. TRANSLITERATION: Convert your Japanese response to its romanji transliteration.  
        3. TRANSLATION: Finally translate your response into English.  
        Remember to separate all three responses only with a new line escape sequence and nothing else. Also, only mention the final responses and no headers or number pointers."""  
        ),  
        AIMessage(content="""オレはうずまきナルトだってばよ！これから何を教えればいいんだ？  
        Ore wa Uzumaki Naruto dattebayo! Korekara nani o oshiereba iin da?  
        I'm Uzumaki Naruto! What should I teach you from now on?""")  
    ]  
  
    # Display the initial AI message to the user  
    print("Naruto: ", messages[-1].content)  
  
    # Continuous loop to interact with the user until they type 'quit', 'q', or 'exit'  
    while True:  
        user_input = input("User: ")  
        if user_input.lower() in ['quit', 'q', 'exit']:  
            break  
  
        # Append the user's input as a HumanMessage to the messages list  
        messages.append(HumanMessage(content=user_input))  
  
        # Generate the AI response using the defined template  
        ai_response = llm.invoke(messages)  
  
        # Append the AI response to the messages list  
        messages.append(ai_response)  
  
        # Print the AI response to the console  
        print("Naruto: ", ai_response.content, '\n\n')  
  
# Check if the script is being executed directly (not imported)  
if __name__ == "__main__":  
    # Start the chat session  
    chat_with_tutor()  
