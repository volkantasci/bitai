import streamlit as st
import requests

API_URL = "http://localhost:3000/api/v1/prediction/cb680c86-db57-4efc-b367-75f9d531c624"


def handle_user_input(prompt):
    def query(payload):
        response = requests.post(API_URL, json=payload)
        return response.json()

    with st.spinner("Generating topics for your video..."):
        output = query({
            "question": prompt,
        })

        st.write(output)
        st.session_state.video_subject = prompt
        st.session_state.video_topics = output


def main():
    st.session_state.video_subject = None
    st.session_state.video_topics = None

    #  Add title and subtitle
    st.title(":orange[bit AI] 🤖")
    st.caption("ℹ️ We are powered by AI tools like OpenAI GPT-3.5-Turbo 🤖, HuggingFace 🤗, CodeLLaMa and Streamlit 🎈")

    st.subheader("Create Topics and Titles")

    prompt = st.chat_input("✏️ Enter video subject here you want to create topics for: ")
    if prompt:
        handle_user_input(prompt)

    with st.sidebar:
        logo_html = open('logo.html')
        st.write(logo_html.read(), unsafe_allow_html=True)
        logo_html.close()


if __name__ == "__main__":
    main()
