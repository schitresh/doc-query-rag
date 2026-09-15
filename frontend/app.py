import streamlit as st

from frontend import state
from frontend.chat.actions import display_chat
from frontend.document.actions import display_documents
from frontend.folder.actions import display_folder_list

st.set_page_config(page_title="Doc Query Rag", layout="wide")
state.init_state()

with st.sidebar:
    display_folder_list()

# Split the area into 2 columns for documents & chat
doc_col, chat_col = st.columns([1, 2], gap="large")

with doc_col:
    display_documents()

with chat_col:
    display_chat()
