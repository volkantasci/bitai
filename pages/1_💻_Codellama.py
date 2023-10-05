import streamlit as st
import requests
from langchain.schema.messages import AIMessage, HumanMessage
from langchain.memory import ConversationBufferMemory
from respond_beauty import make_it_beautiful

API_HOST = "http://localhost:3000"

#  List of models we can use
MODELS = [
    "Meta AI - Codellama 34b Instruct",
    "Meta AI - Codellama 34b Python",
    "Meta AI - Codellama 13b Instruct",
    "Meta AI - Codellama 13b Python",
    "Meta AI - Codellama 7b Instruct"
    "Meta AI - Codellama 7b Python"
]

#  List of API URLs for each model
API_URLS = {
    "Meta AI - Codellama 34b Instruct": API_HOST + "/api/v1/prediction/2c13186c-affc-4837-9dee-0295f27d6cff",
    "Meta AI - Codellama 34b Python": API_HOST + "/api/v1/prediction/75f3c668-1261-4216-aaa8-2176ccb2ff6a",
    "Meta AI - Codellama 13b Instruct": API_HOST + "/api/v1/prediction/8bd8c170-9baf-4769-9fb2-2a748749b2b2",
    "Meta AI - Codellama 13b Python": API_HOST + "/api/v1/prediction/d5cb84d9-9bf0-449a-a1ba-c916877f472c",
    "Meta AI - Codellama 7b Instruct": API_HOST + "/api/v1/prediction/a5a3b276-5e13-4789-9fce-b9cc64d10401",
    "Meta AI - Codellama 7b Python": API_HOST + "/api/v1/prediction/5f50d315-1d0f-425c-8776-62bf0a06fad6"
}

#  Create a memory object and add it to the session state
if "codellama_interface_memory" not in st.session_state:
    st.session_state.codellama_interface_memory = ConversationBufferMemory(memory_key="codellama_history")

if "codellama_model" not in st.session_state:
    st.session_state.codellama_model = "Meta AI - Codellama 34b"


def handle_user_input(prompt):
    """
    Handle user input and send it to the API
    """

    #  Add user input to memory
    st.session_state.codellama_interface_memory.chat_memory.add_message(HumanMessage(content=prompt))

    def query(payload):
        selected_api_url = API_URLS[st.session_state.codellama_model]
        response = requests.post(selected_api_url, json=payload)
        return response.json()

    with st.spinner("Chatting with AI..."):
        output = query({
            "question": prompt,
        })

        st.session_state.codellama_interface_memory.chat_memory.add_message(AIMessage(content=output))


def main():
    # set page config
    st.set_page_config(
        page_title="Codellama Models Fine Tuned for Python 🤖",
        page_icon="🤖",
        initial_sidebar_state="expanded",
    )

    #  Add title and subtitle
    st.title(":orange[bit AI] 🤖")
    st.caption("ℹ️ We are powered by AI tools like OpenAI GPT-3.5-Turbo 🤖, HuggingFace 🤗, CodeLLaMa and Streamlit 🎈")

    st.subheader("Write a Code with CodeLLaMa")

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            #  List models we can use
            st.session_state.codellama_model = st.selectbox("Select a model to use Codellama:", MODELS, )

        with col2:
            st.write('<div style="height: 27px"></div>', unsafe_allow_html=True)
            clear_button = st.button("🗑️ Clear chat history")
            if clear_button:
                st.session_state.codellama_interface_memory.clear()

    #  Set initial variables
    if "codellama_model" not in st.session_state:
        st.session_state.codellama_model = "Meta AI - Codellama 34b Instruct"

    prompt = st.chat_input("✏️ Enter your message here: ")
    if prompt:
        st.session_state.user_input = prompt
        handle_user_input(prompt)

    #  Display chat history
    for message in st.session_state.codellama_interface_memory.buffer_as_messages:
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

    st.sidebar.image("bitpython-logo.png")


if __name__ == "__main__":
    main()
