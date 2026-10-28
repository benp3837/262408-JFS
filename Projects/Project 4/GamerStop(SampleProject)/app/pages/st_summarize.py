from io import StringIO

import streamlit as st

from services.langchain_service import get_basic_chain

# Grab basic chain from service
basic_chain = get_basic_chain()

st.header("Summarize Text Demo")

uploaded_file = st.file_uploader("Choose a TXT file:")

if uploaded_file is not None:

    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

    # Prompt to tell the LLM to summarize the text:
    prompt = f"Summarize this text, neutral on perspective: {stringio.read()}"

    # Invoke the chain with the prompt and display the response
    with st.spinner("Summarizing..."):
        response = basic_chain.invoke(input=prompt)
    st.subheader("Summary:")
    st.write(response.content)
