import typing as t

import streamlit as sl


def init_state() -> None:
    if "active_folder" not in sl.session_state:
        sl.session_state["active_folder"] = {}


def get_active_folder() -> int | None:
    return sl.session_state.get("active_folder")


def set_active_folder(folder: dict[str, t.Any]) -> None:
    sl.session_state["active_folder"] = folder
