import streamlit as st

from frontend import state
from frontend.document import components, service


def display_documents():
    active_folder = state.get_active_folder()
    if not active_folder.get("id"):
        return

    documents = service.fetch_documents(active_folder["id"])
    file_to_upload = components.render_document_list(active_folder, documents)

    if file_to_upload is not None:
        with st.spinner("Uploading..."):
            try:
                service.upload_document(
                    file_bytes=file_to_upload.getvalue(),
                    filename=file_to_upload.name,
                    folder_id=active_folder["id"],
                )
                st.success(f"Uploaded `{file_to_upload.name}`")
                st.rerun()
            except Exception as err:
                st.error(f"Upload failed: {err}")
