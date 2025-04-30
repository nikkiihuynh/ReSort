import os 
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def get_gemini_response(user_input):
    model = genai.GenerativeModel('gemini-1.5-pro')
    prompt = """
    You are a helpful assistant and waste management expert. 
    Provide clear instructions on whether to dispose of items in the trash, recycling, or compost. 
    Give answer in the format: <Trash, Recycle, or Compost>: <brief explanation on why> Only give one option 
    """

    response = model.generate_content(prompt + user_input)
    reply = response.text

    return reply

def get_targeted_tips(history):
    model = genai.GenerativeModel('gemini-1.5-pro')
    history_text = '\n'.join([f"{h['item']}: {h['disposal_method']}" for h in history])
    prompt = (
        f"You are a waste management expert. Based on the following waste sorting history:\n"
        f"{history_text}\n"
        "Provide 3 targeted tips to help the user improve their sorting habits."
    )
    response = model.generate_content(prompt)
    return response.text