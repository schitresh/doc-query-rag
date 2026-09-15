import typing as t

import streamlit as st


def render_document_list(folder: dict[str, t.Any], documents: list[dict[str, t.Any]]):
    st.header("Documents")
    file_uploaded = _render_file_uploader()
    st.divider()

    if not documents:
        st.info("No documents")
    else:
        for doc in documents:
            print(doc.items())
            st.write(doc.get("filename"))

    return file_uploaded


def _render_file_uploader():
    file_uploaded = st.file_uploader("Add Document", type=["pdf", "txt", "md"], max_upload_size=10)

    if file_uploaded is not None:
        if st.button("Upload"):
            return file_uploaded
