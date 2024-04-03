import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") # ChatGoogleGenerativeAI will search for GOOGLE_API_KEY

model = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=True)

def gemini_response(input_text):
    system = SystemMessage(content="you are my personal trading assistant. you are integrated to a telegram group that recommend option trades.\
                              your duty is to intrepret the messages in the group and give suitable response.\
                              your output should always follow this pattern -> 'buy/exit:nifty/banknifty:ce/pe:strike'.\
                              if you are unsure of the response or if the message only give insight and not direct trade recommendation,\
                              you should respond with 'none'. make sure that you only respond if all four information are in the message.")
    human = HumanMessage(content=input_text)
    result = model.invoke([system, human])
    return result.content

def gemini_chat(input_text):
    result = model.invoke(input_text)
    return result.content