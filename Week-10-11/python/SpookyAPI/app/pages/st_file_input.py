import streamlit as st

from services.langchain_service import get_general_chain

# Getting the basic chain again
chain  = get_general_chain()

st.header("Drop in a file for summary and judgement")

uploaded_file = st.file_uploader("Upload a file")

if uploaded_file is not None:
    # Read the file content
    file_content = uploaded_file.read().decode("utf-8")

    # Display the content of the uploaded file
    st.subheader("File Content:")
    st.text_area("Content", file_content, height=200)

    # Get the LLM's response and attach a spinner while it thinks
    with st.spinner("Analyzing..."):
        response = chain.invoke({"input": f"Please summarize and snarkily judge "
                                          f" the following content:\n{file_content}"})

    # Display the LLM's response
    st.subheader("LLM Response:")
    st.text_area("Response", response.content, height=200)
