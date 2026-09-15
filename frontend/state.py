import typing as t

import streamlit as st


def init_state() -> None:
    if "active_folder" not in st.session_state:
        st.session_state["active_folder"] = {}
    if "chat_messages" not in st.session_state:
        st.session_state["chat_messages"] = []


def get_active_folder() -> int | None:
    return st.session_state.get("active_folder")


def set_active_folder(folder: dict[str, t.Any]) -> None:
    st.session_state["active_folder"] = folder


def get_chat_messages():
    return st.session_state.get("chat_messages")


def add_chat_message(type: str, response: dict[str, t.Any]):
    st.session_state["chat_messages"].append({"type": type, "response": response})
