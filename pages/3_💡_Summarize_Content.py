import streamlit as st
import requests

API_URL = "http://localhost:3000/api/v1/prediction/bce8e1fd-cb78-4068-9822-d386d914068a"


def handle_user_input(prompt):
    def query(payload):
        response = requests.post(API_URL, json=payload)
        return response.json()

    with st.spinner("Summarizing your content..."):
        output = query({
            "question": prompt,
        })

        st.write(output)
        st.session_state.user_input = prompt
        st.session_state.summarized_text = output


def main():
    st.session_state.user_input = None
    st.session_state.summarized_text = None

    st.title("Summarize Your Content")
    st.caption("You can summarize your content using this tool 🤖")

    prompt = st.chat_input("✏️ Enter your content here you want to summarize for: ")
    if prompt:
        handle_user_input(prompt)

    st.sidebar.image("bitpython-logo.png")


if __name__ == "__main__":
    main()
