import streamlit as st
import requests
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage

API_HOST = "http://localhost:3000"

API_URLS = {
    "OpenAI ChatGPT-4": API_HOST + "/api/v1/prediction/f69140b3-5ed6-4c6b-9f89-0968a6de70ea",
    "OpenAI GPT-3.5-Turbo Instruct": API_HOST + "/api/v1/prediction/cb680c86-db57-4efc-b367-75f9d531c624",
    "Meta AI LLaMa 2 - 70b": API_HOST + "/api/v1/prediction/a71bf91f-6250-4cc7-8c65-a783cbf2f5c3"
}

if "youtube_memory" not in st.session_state:
    st.session_state.youtube_memory = ConversationBufferMemory()


def handle_user_input(prompt):
    def query(payload):
        st.session_state.youtube_memory.chat_memory.add_user_message(prompt)
        selected_api_url = API_URLS[st.session_state.youtube_selected_model]
        response = requests.post(selected_api_url, json=payload)
        return response.json()

    with st.spinner("Generating topics for your video..."):
        output = query({
            "question": prompt,
        })

        st.session_state.youtube_memory.chat_memory.add_ai_message(output)


def main():
    if "youtube_selected_model" not in st.session_state:
        st.session_state.youtube_selected_model = "Meta AI LLaMa 2 - 70b"

    st.session_state.youtube_models = [
        "OpenAI ChatGPT-4",
        "OpenAI GPT-3.5-Turbo Instruct",
        "Meta AI LLaMa 2 - 70b"
    ]

    #  Add title and subtitle
    st.title(":orange[bit AI] 🤖")
    st.caption("ℹ️ We are powered by AI tools like OpenAI GPT-3.5-Turbo 🤖, HuggingFace 🤗, CodeLLaMa and Streamlit 🎈")

    st.subheader("Create Topics and Titles")

    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            st.session_state.youtube_selected_model = st.selectbox("Select model to use:",
                                                                   st.session_state.youtube_models)

        with col2:
            st.write('<div style="height: 27px"></div>', unsafe_allow_html=True)
            clear_button = st.button("🗑️ Clear history")
            if clear_button:
                st.session_state.youtube_memory.clear()

    prompt = st.chat_input("✏️ Enter video subject here you want to create topics for: ")
    if prompt:
        handle_user_input(prompt)

    st.sidebar.image("bitpython-logo.png")

    for message in st.session_state.youtube_memory.buffer_as_messages:
        if isinstance(message, HumanMessage):
            st.write(f"👤 Human:\n\n {message.content}")
        elif isinstance(message, AIMessage):
            st.write(f"🤖 AI:\n {message.content}")


if __name__ == "__main__":
    main()
