import streamlit as st
import requests
from langchain.schema.messages import AIMessage, HumanMessage
from langchain.memory import ConversationBufferMemory
from streamlit_extras.app_logo import add_logo

API_HOST = "http://localhost:3000"

#  List of models we can use
MODELS = [
    "OpenAI GPT-4",
    "OpenAI GPT-3.5-Turbo",
    "Meta AI LLaMa-2 70B"
]

#  List of API URLs for each model
API_URLS = {
    "OpenAI GPT-4": API_HOST + "/api/v1/prediction/4fb38d2e-1341-4e79-81f6-5d20f7f36a6a",
    "OpenAI GPT-3.5-Turbo": API_HOST + "/api/v1/prediction/5668868a-b59a-4aaf-98eb-bf31e0058d81",
    "Meta AI LLaMa-2 70B": API_HOST + "/api/v1/prediction/c16c790d-227c-4919-9925-06988c2115a7"
}

#  Create a memory object and add it to the session state
if "chat_interface_memory" not in st.session_state:
    st.session_state.chat_interface_memory = ConversationBufferMemory(memory_key="chat_history")

if "chat_model" not in st.session_state:
    st.session_state.chat_model = "OpenAI GPT-3.5-Turbo"


def handle_user_input(prompt):
    """
    Handle user input and send it to the API
    Add the user input to the memory
    Add the AI response to the memory
    """
    with st.sidebar:
        add_logo("./bitpython-logo.png", 200)

    #  Add user input to memory
    st.session_state.chat_interface_memory.chat_memory.add_user_message(prompt)
    selected_api_url = API_URLS[st.session_state.chat_model]

    def query(payload):
        response = requests.post(selected_api_url, json=payload)
        return response.json()

    with st.spinner("Chatting with AI..."):
        output = query({
            "question": st.session_state.chat_interface_memory.buffer_as_str,
        })

        st.session_state.chat_interface_memory.chat_memory.add_message(AIMessage(content=output))


def main():
    if "user_input" not in st.session_state:
        st.session_state.user_input = None

    # set page config
    st.set_page_config(
        page_title="PisiMan 😼 - The Powwer of AI 🤖",
        page_icon="🤖",
        initial_sidebar_state="expanded",
    )

    #  Add title and subtitle
    st.title("PisiMan 😼 - The Powwer of AI 🤖")
    st.caption("ℹ️ We are powered by AI tools like OpenAI GPT-3.5-Turbo 🤖, HuggingFace 🤗, Replicate and Streamlit 🎈")

    #  List models we can use
    st.session_state.chat_model = st.selectbox("Select a model to use Chat:", MODELS)

    #  Set initial variables
    if "chat_model" not in st.session_state:
        st.session_state.chat_model = "GPT-3.5-Turbo"

    prompt = st.chat_input("✏️ Enter your message here: ")
    if prompt:
        st.session_state.user_input = prompt
        handle_user_input(prompt)

    with st.sidebar:
        clear_button = st.button("Clear chat history")
        if clear_button:
            st.session_state.chat_interface_memory.clear()

    #  Display chat history
    for message in st.session_state.chat_interface_memory.buffer_as_messages:
        if isinstance(message, HumanMessage):
            st.write(f"👤 {message.content}")
        elif isinstance(message, AIMessage):
            st.write(f"🤖 {message.content}")


if __name__ == "__main__":
    main()
