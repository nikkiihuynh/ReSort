import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
from PIL import Image

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_gemini_response(user_input):
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = """
    You are a helpful assistant and waste management expert. 
    Provide clear instructions on whether to dispose of items: Trash, Recycle, or Compost.
    Give answer in the format: <Trash, Recycle, or Compost>: <brief explanation on why> Only give one option 
    """

    response = model.generate_content(prompt + user_input)
    reply = response.text

    return reply

def get_targeted_tips(history):
    model = genai.GenerativeModel("gemini-2.0-flash")
    history_text = '\n'.join([f"{h['item']}: {h['disposal_method']}" for h in history])
    prompt = (
        f"You are a waste management expert. Based on the following waste sorting history:\n"
        f"{history_text}\n"
        "Provide 3 targeted tips to help the user improve their sorting habits."
    )
    response = model.generate_content(prompt)
    return response.text

def get_sorting_from_image(image):
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = """
    You are a helpful assistant and waste management expert. 
    Analyze the object in this image and decide how it should be disposed of: Trash, Recycle, or Compost.
    Give answer in the format: <Trash, Recycle, or Compost>:< { object } with those brackets > <brief explanation on why> Only give one option 
    """

    response = model.generate_content([prompt, image])
    return response.text
