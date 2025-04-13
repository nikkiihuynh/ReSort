import os 
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

load_dotenv()
client = OpenAI()

client.api_key = os.getenv("OPENAI_API_KEY")

if 'messages' not in st.session_state:
    st.session_state['messages'] = [{"role": "system", "content": "You are a helpful assistant and waste management expert. Provide clear instructions on whether to dispose of items in the trash, recycling, or compost. Give answer in the format: <Trash, Recycle, or Compost>: <brief explanation on why>" }]

def get_chatgpt_response(user_input):
    st.session_state['messages'].append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state['messages']
    )

    reply = response.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": reply})

    return reply