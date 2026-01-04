import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from agents.pharmacist import get_pharmacist_response
from langchain_core.messages import HumanMessage

try:
    print("Testing Pharmacist Agent...")
    response = get_pharmacist_response("Hi, I'm John Doe. I need a refill for my Metformin.")
    print("Agent Response:", response)
except Exception as e:
    import traceback
    traceback.print_exc()
