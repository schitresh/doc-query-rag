import typing as t

import streamlit as st


def render_chat_workspace(messages: list[dict[str, t.Any]]) -> str | None:
    st.header("Chat")

    for message in messages:
        with st.chat_message(message["type"]):
            response = message["response"]

            if message["type"] == "question":
                st.markdown(response["query"])
            else:
                st.markdown(response.get("answer"))

                if response.get("sources"):
                    with st.expander("Sources"):
                        for src in response["sources"]:
                            st.write(src.get("document_name"))
                            st.caption(src.get("snippet"))

    return st.chat_input("Ask a question...")
