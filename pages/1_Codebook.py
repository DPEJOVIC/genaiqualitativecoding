import streamlit as st
import pandas as pd
import json
from openai import OpenAI
from pydantic import BaseModel


st.title("Codebook")


if not st.session_state["prompt_saved"]:
    st.write("Please set your system prompt first.")
    exit()


def setup():

    # Select OpenAI model
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o-mini"

    # Initialise chat history
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    
    if "system_prompt" not in st.session_state:
        st.session_state["system_prompt"] = ""

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    return client

client = setup()


# Read the survey data and convert to json
survey_data = pd.read_csv("sample_data_csv.csv").to_json()


# JSON schema for the chatbot's response to adhere to
class Codebook(BaseModel):
    themes: list[str]
    theme_definitions: list[str]
    example_responses: list[str]


def get_initial_codebook():
    prompt_and_data = [
        {"role": "system", "content": st.session_state["system_prompt"]},
        {"role": "user", "content": survey_data},
    ]

    st.session_state["chat_history"].append({"role": "user", "content": survey_data})
    
    completion = client.beta.chat.completions.parse(
        model = st.session_state["openai_model"], 
        messages = prompt_and_data,
        response_format = Codebook)
    
    response = completion.choices[0].message.parsed

    if "codebook" not in st.session_state:
        st.session_state["codebook"] = response

    st.session_state["chat_history"].append({"role": "assistant", "content": f"{response}"})

    return response


if "codebook" not in st.session_state:
    codebook = get_initial_codebook()


def display_codebook(codebook):
    themes = codebook.themes
    theme_definitions = codebook.theme_definitions
    example_responses = codebook.example_responses

    codebook_df = pd.DataFrame({
        "Themes": themes,
        "Theme Definitions": theme_definitions,
        "Example Responses": example_responses,
    })

    st.table(codebook_df)

display_codebook(st.session_state["codebook"]) # THIS IS THE ONLY CODEBOOK DISPLAY FUNCTION CALL NECESSARY


def get_codebook():
    completion = client.beta.chat.completions.parse(
        model = st.session_state["openai_model"], 
        messages = [{"role": "system", "content": st.session_state["system_prompt"]}] + st.session_state["chat_history"],
        response_format = Codebook)

    response = completion.choices[0].message.parsed

    st.session_state["codebook"] = response

    st.session_state["chat_history"].append({"role": "assistant", "content": f"{response}"})


if prompt := st.chat_input("Suggest changes to the codebook here"):
    st.session_state["chat_history"].append({"role": "user", "content": prompt})

    get_codebook()
    st.rerun()