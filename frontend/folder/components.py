import streamlit as st

from frontend.folder import actions


def render_folder_list(folders: dict[str, int], active_folder: int):
    st.header("Folders")
    selected_folder = None

    for folder in folders:
        is_active = folder["id"] == active_folder.get("id")
        if st.button(
            folder["name"],
            key=f"folder_btn_{folder['id']}",
            type="primary" if is_active else "secondary",
            use_container_width=True,
        ):
            selected_folder = folder

    st.divider()
    if st.button("New Folder", use_container_width=True):
        render_create_folder_dialog()

    return selected_folder


@st.dialog("Create New Folder")
def render_create_folder_dialog() -> str | None:
    folder_name = None

    with st.form("dialog_folder_form", clear_on_submit=True):
        input_name = st.text_input("Folder Name", placeholder="e.g., Marketing")

        col1, col2 = st.columns([1, 1])
        with col1:
            submitted = st.form_submit_button("Create", use_container_width=True, type="primary")
        with col2:
            canceled = st.form_submit_button("Cancel", use_container_width=True)

        if submitted and input_name.strip():
            folder_name = input_name.strip()
            actions.create_folder(folder_name)
        elif canceled:
            st.rerun()

    return folder_name
