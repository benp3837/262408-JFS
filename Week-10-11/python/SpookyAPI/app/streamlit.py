import streamlit as st

# NOTE: don't import app.services....... streamlit doesn't like it
from services.langchain_service import get_general_chain

# Import our basic chain for LLM ops
chain = get_general_chain()

# Now actual UI stuff----------------

# NOTE: "with" is the mechanism in streamlit that renders stuff on the page

# Basic Header
st.header("Welcome to SpookyGPT 👻")

# Store the previous chats (streamlit handles internal state for you! nice)
if "messages" not in st.session_state:
    st.session_state.messages = [] # Start empty... of course

# Here's the component that displays whatever messages are saved in state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Sidebar
with st.sidebar:

    # Button that switches to our st_file_input.py
    # NOTE: any non-main file needs to be in a folder called "pages"
    if st.button("Switch to File Input"):
        st.switch_page("pages/st_file_input.py")

    st.subheader("About SpookyGPT")
    st.markdown(
        """
        Not for the faint of heart, SpookyGPT is your friendly-ish neighborhood chatbot.
        It will answer your general questions and that's about it. 
        It sounds evil but it has a heart of gold.
        """
    )

    # Button that wipes the chat transcript
    if st.button("Clear Chat"): # IF this gets clicked, clear the chat
        st.session_state.messages = []
        st.rerun() # Auto-refresh so we see the clear chat



# User input box (btw "prompt" is a built-in streamlit variable)
if prompt := st.chat_input("Ask me anything... if you dare..."):

    # Save and display user messages
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get the LLM's response and attach a spinner while it thinks
    with st.spinner("Pondering..."):
        response = chain.invoke({"input":prompt})

    # Display the LLM reponse once it's done thinking
    st.session_state.messages.append({"role": "assistant", "content": response.content})
    with st.chat_message("assistant"):
        st.markdown(response.content)