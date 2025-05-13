import streamlit as st
from Modules.sort import get_targeted_tips
from Modules.database import get_user_id, get_sorting_history
from streamlit import session_state as ss

def show():
    st.subheader("Get tips to help manage your waste disposal now")

    tab1, tab2 = st.tabs(["General Tips", "Generate Tips"])

    with tab1:
        st.markdown('### General Waste Disposal Tips')
        tips = [
            'Clean and dry recyclables before placing them in the bin to avoid contamination.',
            'Flatten cardboard boxes to save space in recycling bins.',
            'Check your local guidelines for accepted materials, as they vary by location.',
            'Avoid bagging recyclables in plastic bags; most facilities cannot process them.',
            'Keep a small compost bin in your kitchen for food scraps to reduce landfill waste.',
        ]
    
        for tip in tips:
            st.markdown(f'- {tip}')

    with tab2:
        # Button to fetch personalized tips based on user history
        if st.button('Get personalized tips'):
            user_id = get_user_id(ss["username"])
            if user_id:
                history = get_sorting_history(user_id)
                if history:
                    tips_text = get_targeted_tips(history)
                    st.subheader('Your Personalized Tips')
                    st.write(tips_text)
                else:
                    st.info('No sorting history available to generate personalized tips.')
