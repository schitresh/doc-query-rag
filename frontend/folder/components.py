import streamlit as st


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

    return selected_folder
