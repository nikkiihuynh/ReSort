import os 
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_gemini_response(user_input):
    model = genai.GenerativeModel("gemini-1.5-pro")
    prompt = """
    You are a helpful assistant and waste management expert. 
    Provide clear instructions on whether to dispose of items in the trash, recycling, or compost. 
    Give answer in the format: <Trash, Recycle, or Compost>: <brief explanation on why> 
    """

    response = model.generate_content(prompt + user_input)
    reply = response.text

    return reply