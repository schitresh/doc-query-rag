import streamlit as st

from frontend import state
from frontend.folder.actions import display_folder_list

st.set_page_config(page_title="Doc Query Rag", layout="wide")
state.init_state()

with st.sidebar:
    display_folder_list()
