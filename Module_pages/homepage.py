import streamlit as st
from Modules.sort import get_targeted_tips
from Modules.database import get_user_id, get_sorting_history
from streamlit import session_state as ss

def show():
    st.markdown(
        """
        <div style='padding: 20px; background-color: #f0fff4; border-radius: 12px;'>
            <p style='font-size: 18px; line-height: 1.6; color: #2E7D32;'>
                Welcome to <strong>ReSort</strong> — your eco-friendly companion for smarter waste sorting.
                Our goal is to help you easily classify your waste as Trash, Recycle, or Compost.
            </p>
            <ul style='color: #2E7D32; font-size: 16px;'>
                <li>📦 Sort any item with text or image input</li>
                <li>📈 View yout personalized sorting history</li>
                <li>💡 Get targeted tips to improve your sustainability habits</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

