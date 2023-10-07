import streamlit as st
import requests
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage
from api_config import API_HOST, API_PORT
from respond_beauty import make_it_beautiful



API_URLS = {
    "ChatGPT-4": API_HOST + f":{API_PORT}" + "/api/v1/prediction/bce8e1fd-cb78-4068-9822-d386d914068a"
}

MODELS = [
    "ChatGPT-4"
]

if "summarize_interface_memory" not in st.session_state:
    st.session_state.summarize_interface_memory = ConversationBufferMemory()

if "summarize_model" not in st.session_state:
    st.session_state.summarize_model = "ChatGPT-4"

if "summarize_interface_html" not in st.session_state:
    st.session_state.summarize_interface_html = False


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
    st.caption(
        "bitAI powered by these AI tools:"
        "OpenAI GPT-3.5-Turbo 🤖, HuggingFace 🤗, CodeLLaMa 🦙, Replicate and Streamlit of course."
    )

    st.subheader("Summarize Your Content With AI")

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            #  List models we can use
            st.session_state.summarize_model = st.selectbox("Select a model to use Summarize:", MODELS, )

        with col2:
            st.write('<div style="height: 27px"></div>', unsafe_allow_html=True)
            second_col1, second_col2 = st.columns([2, 1])
            with second_col1:
                clear_button = st.button("🗑️ Clear history", use_container_width=True)
                if clear_button:
                    st.session_state.summarize_interface_memory.clear()

            with second_col2:
                st.session_state.summarize_interface_html = st.toggle("HTML", value=False)

    prompt = st.chat_input("✏️ Enter your content here you want to summarize for: ")
    if prompt:
        handle_user_input(prompt)

    st.sidebar.caption('<p style="text-align: center;">Made by volkantasci</p>', unsafe_allow_html=True)

    #  Display chat history
    for message in st.session_state.summarize_interface_memory.buffer_as_messages:
        if isinstance(message, HumanMessage):
            if st.session_state.summarize_interface_html:
                with open("templates/user_message_template.html") as user_message_template:
                    new_content = make_it_beautiful(message.content)
                    html = user_message_template.read()
                    st.write(html.format(new_content), unsafe_allow_html=True)

            else:
                st.chat_message("Human", avatar="🤗").write(message.content)

        elif isinstance(message, AIMessage):
            if st.session_state.summarize_interface_html:
                with open("templates/ai_message_template.html") as ai_message_template:
                    new_content = make_it_beautiful(message.content)
                    html = ai_message_template.read()
                    st.write(html.format(new_content), unsafe_allow_html=True)

            else:
                st.chat_message("AI", avatar="🤖").write(message.content)


if __name__ == "__main__":
    main()
