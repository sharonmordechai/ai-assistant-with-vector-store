"""
This scripts is an example which demonstrates a simple chat interface using the OpenAI GPT models
in a Streamlit app. Users can interact with the chat interface and receive responses from the
selected GPT model.

For more information, please check examples/README.md
"""

import streamlit as st
from openai import OpenAI

# Set the title of the Streamlit app
st.title("ChatGPT-like clone")

# Create a sidebar in the Streamlit app
with st.sidebar:
    # Input field for the OpenAI API key
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    # Dropdown menu to select the GPT model version
    model_name = st.selectbox("Model", options=["gpt-4", "gpt-3.5-turbo"])

# Check if the OpenAI API key is provided
if not openai_api_key:
    # Display an error message if the API key is missing
    st.error("Please input your OpenAI API key in the sidebar.")
    st.stop()

# Initialize the OpenAI client with the provided API key
client = OpenAI(api_key=openai_api_key)

# Check if the 'messages' key exists in the session state
if "messages" not in st.session_state:
    # Initialize an empty list to store chat messages
    st.session_state.messages = []

# Display existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input and add it to the chat
if prompt := st.chat_input("Type your message here..."):
    # Append the user's message to the session state
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        # Display the user's message
        st.markdown(prompt)

    # Get the assistant's response from OpenAI
    with st.chat_message("assistant"):
        # Both PyCharm's code-inspection and pylint will complain
        # about the following lines of code, so, we disable those
        # noinspection PyTypeChecker
        # pylint: disable=invalid-name

        # Create a chat completion stream using the OpenAI API
        stream = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Write the assistant's response to the chat
        response = st.write_stream(stream)

    # Append the assistant's response to the session state
    st.session_state.messages.append({"role": "assistant", "content": response})
