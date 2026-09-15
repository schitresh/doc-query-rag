import typing as t

import streamlit as st


def init_state() -> None:
    if "active_folder" not in st.session_state:
        st.session_state["active_folder"] = {}
    if "chat_messages" not in st.session_state:
        st.session_state["chat_messages"] = {}


def get_active_folder() -> int | None:
    return st.session_state.get("active_folder")


def set_active_folder(folder: dict[str, t.Any]) -> None:
    st.session_state["active_folder"] = folder


def get_chat_messages(folder_id: int):
    return st.session_state.get("chat_messages").get(folder_id, [])


def add_chat_message(folder_id: int, type: str, response: dict[str, t.Any]):
    messages = st.session_state["chat_messages"].get(folder_id)
    if not messages:
        st.session_state["chat_messages"][folder_id] = []
        messages = st.session_state["chat_messages"][folder_id]

    messages.append({"type": type, "response": response})
