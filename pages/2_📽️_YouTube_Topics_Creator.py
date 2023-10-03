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

    if st.session_state.video_subject and st.session_state.video_topics:
        st.title(f"Topics for {st.session_state.video_subject}")
        st.write(st.session_state.video_topics)

    st.title("📽️ YouTube Video Topics Creator 🤖")
    st.caption("ℹ️ We are powered by AI tools like OpenAI GPT-3.5-Turbo 🤖, HuggingFace 🤗, Replicate and Streamlit 🎈")
    st.caption("You can create topics for your YouTube videos using this tool.")

    prompt = st.chat_input("✏️ Enter video subject here you want to create topics for: ")
    if prompt:
        handle_user_input(prompt)


if __name__ == "__main__":
    main()
