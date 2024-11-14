import google.generativeai as genai
import streamlit as st
from PIL import Image

# Set up Streamlit page configuration
st.set_page_config(page_title="Pega Tutor", page_icon="🎓", layout="wide")

# Load and display logo/image
image = Image.open("pega.jpeg")

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'response_text' not in st.session_state:
    st.session_state.response_text = ""

# Sidebar for chat history
with st.sidebar:
    st.image(image, width=120)
    st.title("Pega Tutor Application")
    st.write("Your personal AI-powered Pega expert.")
    st.markdown("---")
    st.subheader("Chat History")
    for i, message in enumerate(st.session_state.chat_history):
        st.write(f"{i+1}. {message['role']}: {message['content']}")
    st.markdown("---")

# Main layout
st.subheader("Ask your Pega-related question:")

def generate_response():
    user_prompt = st.session_state.user_prompt
    if user_prompt:
        with st.spinner("Generating answer..."):
            # Add user prompt to chat history
            st.session_state.chat_history.append({"role": "User", "content": user_prompt})

            # Generate response using generative model
            response = model.generate_content(user_prompt)
            st.session_state.response_text = response.text
            
            # Add AI response to chat history
            st.session_state.chat_history.append({"role": "Tutor", "content": response.text})

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

# Fixed input box at the bottom
user_input = st.text_input(
    "Enter your question below:", 
    placeholder="E.g., How does Pega manage workflows?", 
    key="user_prompt", 
    on_change=generate_response
)

# Display the response in a chat format
if 'response_text' in st.session_state and st.session_state.response_text:
    st.markdown("#### Tutor's Response:")
    st.write(f"🧑‍🏫: {st.session_state.response_text}")

# Display footer or additional help text
st.write("---")
st.info("Note: This AI Tutor answers questions specifically about the Pega platform. For other topics, please use other resources.")
