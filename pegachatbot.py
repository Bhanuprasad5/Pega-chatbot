import google.generativeai as genai
import streamlit as st
from PIL import Image

# Set up Streamlit page configuration
st.set_page_config(page_title="Pega Tutor", page_icon="🎓", layout="wide")

# Load and display logo/image
image = Image.open("pega.jpeg")

# Session state initialization for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Define the function to generate responses and maintain chat history
def generate_response():
    user_prompt = st.session_state.user_prompt
    if user_prompt:
        with st.spinner("Generating answer..."):
            response = model.generate_content(user_prompt)
            # Save conversation history
            st.session_state.chat_history.append((user_prompt, response.text))
            st.session_state.user_prompt = ""  # Clear the input box

# Configure API key
genai.configure(api_key="AIzaSyDhzLev5d_V46XA7KQrmg4u90M_g2Xq8Kc")

# System prompt for the generative model
sys_prompt = """
You are an experienced Tutor with 20 years of professional expertise in the Pega Customer decision hub and pega systems expert.
Your role is to help students by answering their questions related to Pega in a very clear, simple, 
and easy-to-understand manner. Provide detailed explanations and use relatable examples to help 
illustrate your points effectively. If a student asks a question outside the scope of Pega, politely 
decline and remind them to ask questions only related to Pega platform.
"""

# Initialize the generative model
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash", system_instruction=sys_prompt)

# Layout setup: sidebar for chat history and main area for question/response
with st.sidebar:
    st.image(image, width=120)
    st.title("Pega Tutor Application")
    st.write("An expert AI-powered tutor to help with your Pega-related questions.")
    st.markdown("### Chat History")
    for user_question, ai_response in st.session_state.chat_history:
        with st.expander(user_question):
            st.write(f"🧑‍🏫: {ai_response}")

# Main content layout
st.subheader("Ask your Pega-related question:")
st.write("---")

# Display chat history in main window for a larger view
for user_question, ai_response in st.session_state.chat_history:
    st.markdown(f"**You:** {user_question}")
    st.write(f"🧑‍🏫: {ai_response}")
    st.write("---")

# Bottom input area fixed with `st.text_input` for user prompt
st.text_input(
    "Enter your question below:", 
    placeholder="E.g., How does Pega manage workflows?", 
    key="user_prompt", 
    on_change=generate_response,
    label_visibility="collapsed",
)
