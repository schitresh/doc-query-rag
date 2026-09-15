import streamlit as st

from frontend import state
from frontend.folder import components, service


def display_folder_list():
    folders = service.fetch_folders()
    active_folder = state.get_active_folder()
    selected_folder = components.render_folder_list(folders, active_folder)

    if selected_folder is not None:
        state.set_active_folder(selected_folder)
        st.rerun()


def create_folder(folder_name: str):
    try:
        service.create_folder(folder_name)
        st.success(f"Folder '{folder_name}' created!")
        st.rerun()
    except Exception as err:
        st.error(f"Could not create folder: {err}")
