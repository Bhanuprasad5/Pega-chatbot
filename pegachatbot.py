import google.generativeai as genai
import streamlit as st
from PIL import Image

# Set up Streamlit page configuration
st.set_page_config(page_title="AI Pega Tutor", page_icon="📘", layout="wide")

# Load and display logo/image
image = Image.open("pega.jpeg")
st.markdown("<h1 style='text-align: center; color: #4a90e2;'>AI Pega Tutor</h1>", unsafe_allow_html=True)
st.image(image, width=100, use_column_width='auto')

# Subtitle and introduction text for users
st.markdown(
    "<p style='text-align: center; color: #5c5c5c; font-size: 1.1em;'>"
    "Your expert AI-powered tutor for everything Pega! Ask questions and get instant, clear answers.</p>",
    unsafe_allow_html=True,
)

# Configure API key
genai.configure(api_key="AIzaSyDhzLev5d_V46XA7KQrmg4u90M_g2Xq8Kc")

# System prompt for the generative model
sys_prompt = """
You are an experienced AI Tutor with 20 years of professional expertise in the Pega platform.
Your role is to help students by answering their questions related to Pega in a very clear, simple, 
and easy-to-understand manner. Provide detailed explanations and use relatable examples to help 
illustrate your points effectively. If a student asks a question outside the scope of Pega, politely 
decline and remind them to ask questions only related to Pega systems and tools.
"""

# Initialize the generative model
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash", system_instruction=sys_prompt)

# Function to generate response
def generate_response():
    user_prompt = st.session_state.user_prompt
    if user_prompt:
        with st.spinner("Generating answer..."):
            response = model.generate_content(user_prompt)
            st.session_state.response_text = response.text
    else:
        st.session_state.response_text = "Please enter a query before pressing Enter."

# Input Section with Modern Styling
st.markdown("<hr style='border-top: 1px solid #e0e0e0;'>", unsafe_allow_html=True)
st.subheader("Ask a Pega-related Question:")

st.text_input(
    "Type your question below:", 
    placeholder="E.g., What are the key benefits of using Pega for workflow automation?", 
    key="user_prompt", 
    on_change=generate_response,
)

# Button for generating a response
btn_click = st.button("Get Expert Answer")

if btn_click:
    generate_response()

# Display the response in a more prominent, chat-style format
if 'response_text' in st.session_state:
    st.markdown("<h3 style='color: #4a90e2;'>AI Tutor's Response:</h3>", unsafe_allow_html=True)
    st.markdown(f"<div style='padding: 10px; border: 1px solid #e0e0e0; background-color: #f9f9f9; border-radius: 5px;'>{st.session_state.response_text}</div>", unsafe_allow_html=True)

# Footer note or guidance for users
st.markdown("<hr style='border-top: 1px solid #e0e0e0;'>", unsafe_allow_html=True)
st.info("Note: This AI Tutor is designed to answer questions about the Pega platform. For other topics, please use other resources.")
