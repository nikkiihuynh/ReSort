import streamlit as st
import plotly.express as px
import pandas as pd
from Modules.database import get_user_id, get_Trash_Size, get_Recycle_Size, get_Compost_Size,  get_sorting_history
from streamlit import session_state as ss

def show():
    st.subheader("View how much waste you have sorted")
    user_id = get_user_id(ss["username"])
    tab1, tab2 = st.tabs(["Statistics", "History"])
    
    with tab1:
        st.subheader("Statistics")
        trashSize = get_Trash_Size(user_id)
        recycleSize = get_Recycle_Size(user_id)
        compostSize = get_Compost_Size(user_id)
        labels = ['Trash', 'Recycle', 'Compost']
        sizes = [trashSize, recycleSize, compostSize]

        fig = px.pie(
            values=sizes,
            names=labels,
            color=labels,  
            color_discrete_map={
                'Trash': 'orange',
                'Recycle': 'blue',
                'Compost': 'green'
            },
            title='Trash Sorted'
        )

        st.plotly_chart(fig)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total trashed items: ", trashSize)
        with col2:
            st.metric("Total recycled items: ", recycleSize)
        with col3:
            st.metric("Total composted items: ", compostSize)

    with tab2:
        st.subheader("History")
        history = get_sorting_history(user_id)
        if history:
            df = pd.DataFrame(history)
            df['sort_date'] = pd.to_datetime(df['sort_date']).dt.strftime('%m-%d-%Y %H:%M')
            df['disposal_method'] = df['disposal_method'].str.capitalize()

            df = df.rename(columns={
                'item' : 'Item',
                'disposal_method' : 'Disposal Method',
                'sort_date' : 'Date Sorted'
            })

            def color_code(val):
                colors = {
                    'Trash': '#F8D32B',
                    'Recycle': '#2154DC',
                    'Compost': '#1FAA21'
                }
                return f'background-color: {colors.get(val,"")}'

            st.dataframe(
                df.style.applymap(color_code, subset=['Disposal Method']),
                column_config ={
                    "Item": st.column_config.TextColumn("Item", width="medium"),
                    "Disposal Method": st.column_config.TextColumn("Disposal Method", width="medium"),
                    "Date Sorted": st.column_config.DatetimeColumn("Date Sorted", width="medium")
                },
                hide_index=True,
                use_container_width=True,
                height=400
            )
        else:
            st.info("No sorting history to display.")
    