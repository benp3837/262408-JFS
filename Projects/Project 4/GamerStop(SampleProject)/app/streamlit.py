import streamlit as st

from services.langchain_service import get_basic_chain

# Import basic chain (no memory, but faster for this demo)
basic_chain = get_basic_chain()

# Now the actual UI ------------------------------------------

# Basic Header
st.header("*sigh...* GamerStopGPT")

# Storing chat history so we can display it
if "messages" not in st.session_state:
    st.session_state.messages = [] # Empty list for now

# The actual storage/display of messages in the session
# (saves the messages to get rendered below)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Sidebar with an "About" section and a button to clear the UI
with st.sidebar:

    # Button that switches to the st_summarize.py file
    if st.button("Summarize Text Demo"):
        st.switch_page("pages/st_summarize.py")

    st.header("About GamerStopGPT")
    st.write("This is a quick StreamLit chatbot demo with real LangChain integration for responses"
             "StreamLit is great for making quick and easy UIs for LLMs and other stuff like dashboard.")

    # Button that wipes chat transcript
    if st.button("Clear Chat"): # "If this button is clicked, run this functionality"
        st.session_state.messages = []
        st.rerun()

# User Input Box (btw prompt is a built-in variable from Streamlit)
if prompt := st.chat_input("Ask me a question if you must..."):

    # Save and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt) # write() is what actually displays the message

    # Invoke basic chain to respond to the user
    # Notice the "thinking..." animation while we wait
    with st.spinner("Thinking..."):
        response = basic_chain.invoke(input=prompt)

    # Save and display the LLM response
    response_text = response.content

    st.session_state.messages.append({"role":"assistant", "content":response_text})
    with st.chat_message("assistant"):
        st.write(response_text)
