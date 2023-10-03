import streamlit as st
import requests
from langchain.schema.messages import AIMessage, HumanMessage
from langchain.memory import ConversationBufferMemory

API_HOST = "http://localhost:3000"

#  List of models we can use
MODELS = [
    "Meta AI - Codellama 34b",
    "Meta AI - Codellama 13b",
    "Meta AI - Codellama 7b"
]

#  List of API URLs for each model
API_URLS = {
    "Meta AI - Codellama 34b": API_HOST + "/api/v1/prediction/2c13186c-affc-4837-9dee-0295f27d6cff",
    "Meta AI - Codellama 13b": API_HOST + "/api/v1/prediction/8bd8c170-9baf-4769-9fb2-2a748749b2b2",
    "Meta AI - Codellama 7b": API_HOST + "/api/v1/prediction/a5a3b276-5e13-4789-9fce-b9cc64d10401"
}

#  Create a memory object and add it to the session state
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory()


def handle_user_input(prompt):
    """
    Handle user input and send it to the API
    """

    #  Add user input to memory
    st.session_state.memory.chat_memory.add_user_message(prompt)
    selected_api_url = API_URLS[st.session_state.model]

    def query(payload):
        response = requests.post(selected_api_url, json=payload)
        return response.json()

    with st.spinner("Chatting with AI..."):
        output = query({
            "question": prompt,
        })

        st.session_state.memory.chat_memory.add_message(AIMessage(content=output))


def main():
    #  Set initial variables
    if "model" not in st.session_state:
        st.session_state.model = "GPT-3.5-Turbo"

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
    st.session_state.model = st.selectbox("Select a model to use Chat:", MODELS)
    prompt = st.chat_input("✏️ Enter your message here: ")
    if prompt:
        st.session_state.user_input = prompt
        handle_user_input(prompt)

    with st.sidebar:
        clear_button = st.button("Clear chat history")
        if clear_button:
            st.session_state.memory.clear()

    #  Display chat history
    for message in st.session_state.memory.buffer_as_messages:
        if isinstance(message, HumanMessage):
            st.write(f"👤 {message.content}")
        elif isinstance(message, AIMessage):
            st.write(f"🤖 {message.content}")


if __name__ == "__main__":
    main()
