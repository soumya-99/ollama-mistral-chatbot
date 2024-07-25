import requests
import json
import streamlit as st

url = "http://localhost:11434/api/generate"

headers = {
    'Content-Type': 'application/json',
}

conversation_history = []

def generate_response(prompt):
    conversation_history.append(prompt)

    full_prompt = "\n".join(conversation_history)

    data = {
        "model": "mistral",
        "stream": False,
        "prompt": full_prompt,
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        actual_response = data["response"]
        conversation_history.append(actual_response)
        return actual_response
    else:
        st.error(f"Error: {response.status_code} {response.text}")
        return None

st.title("AI Chatbot")
st.write("Enter your prompt below and get a response from the AI model.")

prompt = st.text_input("Enter your prompt here...")

if st.button("Generate Response"):
    if prompt:
        response = generate_response(prompt)
        if response:
            # st.text_area("Response", value=response, height=200)
            st.markdown(body=response, unsafe_allow_html=False)
    else:
        st.warning("Please enter a prompt.")
