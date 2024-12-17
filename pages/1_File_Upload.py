import streamlit as st
import pandas as pd

st.title("File Upload")

if "prompt_saved" not in st.session_state:
    st.write("Please set your system prompt first.")
    exit()

if not st.session_state["prompt_saved"]:
    st.write("Please set your system prompt first.")
    exit()

if "file_uploaded" not in st.session_state:
    st.session_state["file_uploaded"] = False

if st.session_state["file_uploaded"]:
    st.write("Please proceed to the Codebook window.")
    exit()

### FILE UPLOAD LOGIC ###
st.write("""Upload your data here. Ensure data is in .csv format. Upload your file and press 'Done' to process them.""")

# Streamlit file uploader
uploaded_file = st.file_uploader("Upload a file", type=["csv"], accept_multiple_files=False)

def file_uploaded():

    if uploaded_file is not None:
        survey_data = pd.read_csv(uploaded_file).to_json()

        if "survey_data" not in st.session_state:
            st.session_state["survey_data"] = survey_data
        
    
        st.session_state["file_uploaded"] = True


if uploaded_file:
    st.button("Done", on_click=file_uploaded)
    


