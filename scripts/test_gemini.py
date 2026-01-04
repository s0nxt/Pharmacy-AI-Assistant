import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

load_dotenv(dotenv_path='backend/.env')

try:
    model = ChatGoogleGenerativeAI(model="models/gemini-flash-latest")
    response = model.invoke([HumanMessage(content="Explain 1+1")])
    print("Gemini Response:", response.content)
except Exception as e:
    print("Gemini Error:", e)
