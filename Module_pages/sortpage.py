import streamlit as st
from Modules.database import get_user_id, save_to_history
from Modules.sort import get_gemini_response, get_sorting_from_image
from streamlit import session_state as ss
from PIL import Image

def parse_ai_response(response_text):
    if ":" in response_text:
        item, method = response_text.split(":", 1)
        return item.strip(), method.strip()
    return response_text.strip(), ""

def clean_method(s):
    return s.strip().lower().replace('*', '')

def show():
    st.subheader("Sort Waste into Trash, Recycle, or Compost")    
    tab1, tab2 = st.tabs(["Text", "Image"])
    with tab1:
        user_input = st.text_input("Describe the waste you want to dispose:")

        if st.button("Sort", key="send_msg") and user_input:
            response_text = get_gemini_response(user_input)
            st.write(response_text)
            st.session_state['last_text_response'] = response_text
            st.session_state['sort_clicked'] = True  # Set flag

        if 'last_text_response' in st.session_state and st.session_state.get('sort_clicked', False):
            if st.button("Save"):
                disposal_method, explanation = parse_ai_response(st.session_state['last_text_response'])
                valid_methods = ['trash', 'recycle', 'compost']
              
                disposal_method_clean = clean_method(disposal_method)
                valid_methods_clean = [clean_method(m) for m in valid_methods]

                if (disposal_method_clean in valid_methods_clean
                    and user_input.strip()
                    and len(user_input.strip()) > 2):
                    user_id = get_user_id(ss["username"])
                    save_to_history(user_id, user_input, disposal_method_clean)
                    st.success('Saved to history!')
                else:
                    st.error('Cannot save: invalid input or disposal method')

    with tab2:
        image_file = st.file_uploader("Upload an image of an item", type=["jpg", "png", "jpeg"])
        if image_file is not None:
            img = Image.open(image_file)
            st.image(img, caption="Uploaded Image", use_container_width=True)

        if st.button("Analyze Image", key="analyze_image"):
            response_text = get_sorting_from_image(img)
            st.write(response_text)
            st.session_state['last_response'] = response_text
            st.session_state['analyze_image_clicked'] = True

        if 'last_response' in st.session_state and st.session_state.get('analyze_image_clicked', False):
            user_input = st.session_state['last_response'].split('{')[1].split('}')[0]
            if st.button("Save Image"):
                disposal_method, explanation = parse_ai_response(st.session_state['last_response'])
                valid_methods = ['trash', 'recycle', 'compost']

                disposal_method_clean = clean_method(disposal_method)
                valid_methods_clean = [clean_method(m) for m in valid_methods]

                if (disposal_method_clean in valid_methods_clean
                    and user_input.strip()
                    and len(user_input.strip()) > 2):
                    user_id = get_user_id(ss["username"])
                    save_to_history(user_id, user_input, disposal_method_clean)
                    st.success('Saved to history!')
                else:
                    st.error('Cannot save: invalid input or disposal method')
