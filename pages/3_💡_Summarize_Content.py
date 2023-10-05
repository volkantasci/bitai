import streamlit as st
import requests
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage

from respond_beauty import make_it_beautiful

API_URLS = {
    "ChatGPT-4": "http://localhost:3000/api/v1/prediction/bce8e1fd-cb78-4068-9822-d386d914068a"
}

MODELS = [
    "ChatGPT-4"
]

if "summarize_interface_memory" not in st.session_state:
    st.session_state.summarize_interface_memory = ConversationBufferMemory()

if "summarize_model" not in st.session_state:
    st.session_state.summarize_model = "ChatGPT-4"


def handle_user_input(prompt):
    st.session_state.summarize_interface_memory.chat_memory.add_user_message(prompt)

    def query(payload):
        selected_api_url = API_URLS[st.session_state.summarize_model]
        response = requests.post(selected_api_url, json=payload)
        return response.json()

    with st.spinner("Summarizing your content..."):
        output = query({
            "question": prompt,
        })

        st.session_state.summarize_interface_memory.chat_memory.add_ai_message(output)


def main():
    st.session_state.user_input = None
    st.session_state.summarized_text = None

    #  Add title and subtitle
    st.title(":orange[bit AI] 🤖")
    st.caption("ℹ️ We are powered by AI tools like OpenAI GPT-3.5-Turbo 🤖, HuggingFace 🤗, CodeLLaMa and Streamlit 🎈")

    st.subheader("Summarize Your Content With AI")

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            #  List models we can use
            st.session_state.summarize_model = st.selectbox("Select a model to use Summarize:", MODELS, )

        with col2:
            st.write('<div style="height: 27px"></div>', unsafe_allow_html=True)
            clear_button = st.button("🗑️ Clear history")
            if clear_button:
                st.session_state.summarize_interface_memory.clear()

    prompt = st.chat_input("✏️ Enter your content here you want to summarize for: ")
    if prompt:
        handle_user_input(prompt)

    st.sidebar.image("bitpython-logo.png")

    #  Display chat history
    for message in st.session_state.summarize_interface_memory.buffer_as_messages:
        if isinstance(message, HumanMessage):
            with open("user_message_template.html") as user_message_template:
                new_content = make_it_beautiful(message.content)
                html = user_message_template.read()
                st.write(html.format(new_content), unsafe_allow_html=True)
        elif isinstance(message, AIMessage):
            with open("ai_message_template.html") as ai_message_template:
                new_content = make_it_beautiful(message.content)
                html = ai_message_template.read()
                st.write(html.format(new_content), unsafe_allow_html=True)


if __name__ == "__main__":
    main()
