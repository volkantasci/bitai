import streamlit as st
import requests
from langchain.schema.messages import AIMessage, HumanMessage
from langchain.memory import ConversationBufferMemory
from os import environ

from respond_beauty import make_it_beautiful

API_HOST = 'http://' + environ.get("API_HOST", "")
API_PORT = environ.get("API_PORT", "3000")

#  List of models we can use
MODELS = [
    "OpenAI GPT-4",
    "OpenAI GPT-3.5-Turbo",
    "Meta AI LLaMa 2 - 70b"
]

#  List of API URLs for each model
API_URLS = {
    "OpenAI GPT-4": API_HOST + f":{API_PORT}" + "/api/v1/prediction/4fb38d2e-1341-4e79-81f6-5d20f7f36a6a",
    "OpenAI GPT-3.5-Turbo": API_HOST + f":{API_PORT}" + "/api/v1/prediction/5668868a-b59a-4aaf-98eb-bf31e0058d81",
    "Meta AI LLaMa 2 - 70b": API_HOST + f":{API_PORT}" + "/api/v1/prediction/c16c790d-227c-4919-9925-06988c2115a7"
}

#  Create a memory object and add it to the session state
if "chat_interface_memory" not in st.session_state:
    st.session_state.chat_interface_memory = ConversationBufferMemory(memory_key="chat_history")

if "chat_model" not in st.session_state:
    st.session_state.chat_model = "OpenAI GPT-3.5-Turbo"

if "chat_interface_html" not in st.session_state:
    st.session_state.chat_interface_html = False


def handle_user_input(prompt):
    """
    Handle user input and send it to the API
    Add the user input to the memory
    Add the AI response to the memory
    """

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
        page_title="bitAI 🤖 Chat With Your Favorite Model 💬",
        page_icon="🤖",
        initial_sidebar_state="expanded",
    )

    #  Add title and subtitle
    st.title(":orange[bit AI] 🤖")
    st.caption(
        "bitAI powered by these AI tools:"
        "OpenAI GPT-3.5-Turbo 🤖, HuggingFace 🤗, CodeLLaMa 🦙, Replicate and Streamlit of course."
    )
    st.subheader("Chat with Text Generation Models")

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            #  List models we can use
            st.session_state.chat_model = st.selectbox("Select a model to use Chat:", MODELS)

        with col2:
            st.write('<div style="height: 27px"></div>', unsafe_allow_html=True)
            second_col1, second_col2 = st.columns([2, 1])
            with second_col1:
                clear_button = st.button("🗑️ Clear history", use_container_width=True)
                if clear_button:
                    st.session_state.chat_interface_memory.clear()

            with second_col2:
                beauty = st.toggle("HTML", value=False)
                if beauty:
                    st.session_state.chat_interface_html = True
                else:
                    st.session_state.chat_interface_html = False

    #  Set initial variables
    if "chat_model" not in st.session_state:
        st.session_state.chat_model = "GPT-3.5-Turbo"

    prompt = st.chat_input("✏️ Enter your message here: ")
    if prompt:
        st.session_state.user_input = prompt
        handle_user_input(prompt)

        #  Display chat history
    for message in st.session_state.chat_interface_memory.buffer_as_messages:
        if isinstance(message, HumanMessage):
            if st.session_state.chat_interface_html:
                with open("templates/user_message_template.html") as user_message_template:
                    new_content = make_it_beautiful(message.content)
                    html = user_message_template.read()
                    st.write(html.format(new_content), unsafe_allow_html=True)

            else:
                st.chat_message("Human", avatar="🤗").write(message.content)
        elif isinstance(message, AIMessage):
            if st.session_state.chat_interface_html:
                with open("templates/ai_message_template.html") as ai_message_template:
                    new_content = make_it_beautiful(message.content)
                    html = ai_message_template.read()
                    st.write(html.format(new_content), unsafe_allow_html=True)

            else:
                st.chat_message("AI", avatar="🤖").write(message.content)

    st.sidebar.caption('<p style="text-align: center;">Made by volkantasci</p>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
