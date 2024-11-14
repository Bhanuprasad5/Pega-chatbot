import google.generativeai as genai
import streamlit as st
from PIL import Image

# Set up Streamlit page configuration
st.set_page_config(page_title="Pega Tutor", page_icon="🎓", layout="wide")

# Load and display logo/image
image = Image.open("pega.jpeg")
col1, col2 = st.columns([1, 4])
with col1:
    st.image(image, width=120)
with col2:
    st.title("Pega Tutor Application")
    st.write("An expert AI-powered tutor to help with your Pega-related questions.")

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

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Function to generate response
def generate_response():
    user_prompt = st.session_state.user_prompt
    if user_prompt:
        with st.spinner("Generating answer..."):
            response = model.generate_content(user_prompt)
            # Add user question and model response to chat history
            st.session_state.chat_history.append((user_prompt, response.text))
            st.session_state.user_prompt = ""  # Clear the input after processing

# Sidebar for chat history
with st.sidebar:
    st.header("Chat History")
    for idx, (question, answer) in enumerate(st.session_state.chat_history):
        st.write(f"**Q{idx + 1}:** {question}")
        st.write(f"**A{idx + 1}:** {answer}")

# Main input section (fixed search bar)
st.subheader("Ask your Pega-related question:")
st.text_input(
    "Enter your question below:", 
    placeholder="E.g., How does Pega manage workflows?", 
    key="user_prompt", 
    on_change=generate_response,
)

# Button for generating a response
btn_click = st.button("Generate Answer")

if btn_click:
    generate_response()

# Display the current session's Q&A
if st.session_state.chat_history:
    st.write("### Session Q&A:")
    for idx, (question, answer) in enumerate(st.session_state.chat_history):
        st.write(f"**Question {idx + 1}:** {question}")
        st.write(f"**Answer {idx + 1}:** 🧑‍🏫: {answer}")

# Footer or additional help text
st.write("---")
st.info("Note: This AI Tutor answers questions specifically about the Pega platform. For other topics, please use other resources.")
