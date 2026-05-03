import streamlit as st
import google.generativeai as genai
import os

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Election Education Hub", page_icon="🗳️", layout="wide")

# Hide Streamlit Default Menu for a cleaner UI
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- INITIALIZE GEMINI API ---
# Try to get the API key from environment variables first, then Streamlit secrets
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

if not api_key:
    st.warning("⚠️ Please provide a Gemini API Key to use the application. You can set it in Streamlit `.streamlit/secrets.toml` or as a `GEMINI_API_KEY` environment variable.")
    st.stop()

genai.configure(api_key=api_key)

# Configure the model to use the latest Gemini Pro
model = genai.GenerativeModel('gemini-pro-latest')

# --- SIDEBAR: USER DEMOGRAPHICS ---
st.sidebar.title("👤 Voter Profile")
st.sidebar.write("Enter your details to get a customized voting experience.")

age = st.sidebar.number_input("Age", min_value=18, max_value=120, value=18)

states = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", 
    "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", 
    "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", 
    "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", 
    "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", 
    "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", 
    "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
]
state = st.sidebar.selectbox("State", states)

st.sidebar.markdown("---")
st.sidebar.info("🤖 This app is powered by the latest Gemini Pro to provide tailored election information and answer your questions.")

# --- MAIN PAGE CONTENT ---
st.title("🗳️ Election Education Process")
st.write(f"Welcome! Explore your personalized election guide and resources for **{state}**.")

# Create tabs for the different features
tab1, tab2 = st.tabs(["📋 Step-by-Step Voting Guide", "💬 Election FAQ Chatbot"])

# --- TAB 1: VOTING GUIDE ---
with tab1:
    st.header("Your Personalized Voting Guide")
    st.write(f"Get a customized step-by-step voting guide based on your profile ({age} years old, resident of {state}).")
    
    if st.button("Generate Voting Guide", type="primary"):
        with st.spinner("Generating your customized guide using the latest Gemini Pro..."):
            prompt = f"""
            You are an expert, non-partisan civic education assistant. 
            Please provide a step-by-step voting guide for a {age}-year-old resident of {state}.
            
            The guide should clearly include:
            1. Registration requirements and standard deadlines in {state}.
            2. How to check voter registration status.
            3. Methods of voting available in {state} (e.g., mail-in, early voting, Election Day).
            4. ID requirements for voting.
            5. Key general advice for first-time or returning voters.
            
            Format the response nicely with markdown headers and bullet points. Make the guide clear, encouraging, and easy to understand.
            """
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"An error occurred while generating the guide: {e}")

# --- TAB 2: FAQ CHATBOT ---
with tab2:
    st.header("Election FAQ Chatbot")
    st.write("Ask any questions you have about the election process, voter registration, or voting mechanics.")
    
    # Initialize chat session in Streamlit session state
    if "chat_session" not in st.session_state:
        # Start a chat session with an initial system-level instruction (provided as context)
        st.session_state.chat_session = model.start_chat(history=[
            {"role": "user", "parts": ["You are a helpful, non-partisan election education assistant. Answer questions objectively and clearly."]},
            {"role": "model", "parts": ["I understand. I am ready to provide objective and clear election education assistance."]}
        ])
    
    # Display chat history (excluding the initial setup messages)
    for message in st.session_state.chat_session.history[2:]:
        role = "assistant" if message.role == "model" else "user"
        with st.chat_message(role):
            st.markdown(message.parts[0].text)

    # Chat input box
    if prompt := st.chat_input("Ask a question (e.g., 'What is an absentee ballot?')..."):
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get and display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            try:
                # Send the message to the Gemini chat session
                response = st.session_state.chat_session.send_message(prompt)
                message_placeholder.markdown(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")
