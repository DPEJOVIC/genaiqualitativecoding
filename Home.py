import streamlit as st
import pandas as pd


st.title("GPT Qualitative Coding")
st.write("Give the chatbot instructions detailing how it should generate a codebook here.")


# If the user has submitted their prompt, then do not execute the rest of the Python file.
if "prompt_saved" not in st.session_state:
    st.session_state["prompt_saved"] = False


if st.session_state["prompt_saved"]:
    st.write("Instructions saved.")
    st.write("\nIf you wish to start again, please reload this webpage.")
    exit()


st.write("Click 'Submit' when ready. Once submitted, the system prompt cannot be changed. To start again, please reload the webpage.")


# Read default system prompt
with open("systemprompt.txt", "r") as file:
    systemprompt = file.read()


# Edit system prompt
sysprompt = st.text_area(
    "Change the system prompt below:",
    systemprompt,
    height = 200,
    key = "sysprompt",
)

st.session_state["system_prompt"] = sysprompt


# Activates once the user submits their edited prompt
def submit_sys_prompt():
    if "system_prompt" not in st.session_state:
        st.session_state["system_prompt"] = ""

    # Save the updated system prompt to the session state
    st.session_state["system_prompt"] = sysprompt

    # Change the prompt_saved variable in the session state to stop execution of this file on rerun
    st.session_state["prompt_saved"] = True


st.button("Submit", on_click=submit_sys_prompt)