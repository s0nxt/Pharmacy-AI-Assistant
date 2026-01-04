import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv(dotenv_path='backend/.env')

# Try WITHOUT models/ prefix first
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
try:
    print("Testing gemini-1.5-flash...")
    res = model.invoke([HumanMessage(content="Hi")])
    print("Success:", res.content)
except Exception as e:
    print("Error:", e)

# Try WITH models/ prefix
model2 = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash", temperature=0)
try:
    print("\nTesting models/gemini-1.5-flash...")
    res = model2.invoke([HumanMessage(content="Hi")])
    print("Success:", res.content)
except Exception as e:
    print("Error:", e)

# Try models/gemini-flash-latest
model3 = ChatGoogleGenerativeAI(model="models/gemini-flash-latest", temperature=0)
try:
    print("\nTesting models/gemini-flash-latest...")
    res = model3.invoke([HumanMessage(content="Hi")])
    print("Success:", res.content)
except Exception as e:
    print("Error:", e)
