import streamlit as st

from frontend import state
from frontend.chat import components, service


def display_chat():
    active_folder = state.get_active_folder()
    if active_folder.get("id") is None:
        return

    messages = state.get_chat_messages()
    user_query = components.render_chat_workspace(messages)

    if user_query:
        state.add_chat_message("question", {"query": user_query})
        st.markdown(user_query)

        with st.spinner("Searching documents..."):
            try:
                response = service.submit_query(question=user_query, folder_id=active_folder["id"])
                state.add_chat_message("answer", response)
            except Exception as err:
                st.error(f"Some error occurred: {err}")

        st.rerun()
