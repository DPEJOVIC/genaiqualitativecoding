import streamlit as st
import pandas as pd
import json
from openai import OpenAI
from pydantic import BaseModel

st.title("Discussion")


if "prompt_saved" not in st.session_state:
    st.write("Please set your system prompt first.")
    exit()

if not st.session_state["prompt_saved"]:
    st.write("Please set your system prompt first.")
    exit()

if "file_uploaded" not in st.session_state:
    st.write("Please upload your data first.")
    exit()

if not st.session_state["file_uploaded"]:
    st.write("Please upload your data first.")
    exit()

if "codebook" not in st.session_state:
    st.write("Please visit the 'Codebook' tab first.")
    exit()


def setup():

    # Select OpenAI model
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o-mini"

    # Initialise chat history
    if "chat_history_discussion" not in st.session_state:
        st.session_state["chat_history_discussion"] = []
    
    if "system_prompt_discussion" not in st.session_state:
        st.session_state["system_prompt_discussion"] = "Use the context of the conversation provided to discuss and answer the user's questions. Try to be brief."

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    return client

client = setup()


# JSON schema for the chatbot's response to adhere to
class Codebook(BaseModel):
    themes: list[str]
    codes: list[str]
    code_definitions: list[str]
    example_responses: list[str]


# Write chat history
for message in st.session_state["chat_history_discussion"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat logic
if prompt := st.chat_input("Discuss the codebook here"):
    st.session_state["chat_history_discussion"].append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        messages = [{"role": "system", "content": st.session_state["system_prompt_discussion"]}] + st.session_state["chat_history"] + st.session_state["chat_history_discussion"]

        stream = client.chat.completions.create(
            model = st.session_state["openai_model"],
            messages = messages,
            stream = True,
        )
        response = st.write_stream(stream)

    st.session_state["chat_history_discussion"].append({"role": "assistant", "content": response})


def change_codebook():
    completion = client.beta.chat.completions.parse(
        model = st.session_state["openai_model"], 
        messages = [{"role": "system", "content": st.session_state["system_prompt"]}] + st.session_state["chat_history"] + st.session_state["chat_history_discussion"],
        response_format = Codebook)

    response = completion.choices[0].message.parsed

    st.session_state["codebook"] = response

    st.session_state["chat_history"].append({"role": "assistant", "content": f"{response}"})


if st.session_state["chat_history_discussion"]:
    st.button("Update Codebook according to this conversation", on_click=change_codebook, use_container_width=True)