import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# Set up Streamlit page configuration
st.set_page_config(
    page_title="Pega Tutor",
    page_icon="🎓",
    layout="wide"  # Changed to wide layout
)

# Configure API key
genai.configure(api_key="AIzaSyDhzLev5d_V46XA7KQrmg4u90M_g2Xq8Kc")

# System prompt
sys_prompt = """
You are an experienced Tutor with 20 years of professional expertise in the Pega Customer decision hub and pega systems expert. 
Your role is to help students by answering their questions related to Pega in a very clear, simple, and easy-to-understand manner. 
Provide detailed explanations and use relatable examples to help illustrate your points effectively. 
If a student asks a question outside the scope of Pega, politely decline and remind them to ask questions only related to Pega platform.
"""

# Initialize the generative model
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash", system_instruction=sys_prompt)

# Initialize session state for chat history if not exists
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Custom CSS for the interface
st.markdown("""
    <style>
        .main {
            padding: 0rem 1rem;
        }
        .stTextInput {
            position: fixed;
            bottom: 20px;
            left: 25%;
            right: 5%;
            background-color: white;
            padding: 10px;
            z-index: 1000;
        }
        .chat-message {
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
            display: flex;
            flex-direction: column;
        }
        .user-message {
            background-color: #f0f2f6;
        }
        .bot-message {
            background-color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Create two columns: one for chat history and one for main content
col1, col2 = st.columns([1, 3])

# Left sidebar with chat history
with col1:
    st.markdown("### Chat History")
    # Display all previous chats as clickable elements
    for idx, (q, a) in enumerate(st.session_state.chat_history):
        st.markdown(f"**Q: {q[:50]}...**")
        st.markdown("---")

# Main content area
with col2:
    # Header with logo
    header_col1, header_col2 = st.columns([1, 4])
    with header_col1:
        image = Image.open("pega.jpeg")
        st.image(image, width=120)
    with header_col2:
        st.title("Pega Tutor Application")
        st.write("An expert AI-powered tutor to help with your Pega-related questions.")

    # Chat display area
    chat_container = st.container()
    
    with chat_container:
        for q, a in st.session_state.chat_history:
            st.markdown(f'<div class="chat-message user-message">👤 **You**: {q}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-message bot-message">🧑‍🏫 **Tutor**: {a}</div>', unsafe_allow_html=True)

# Fixed input area at the bottom
input_container = st.container()

with input_container:
    def generate_response():
        if st.session_state.user_prompt.strip():
            with st.spinner("Generating answer..."):
                response = model.generate_content(st.session_state.user_prompt)
                # Add to chat history
                st.session_state.chat_history.append((st.session_state.user_prompt, response.text))
                # Clear input
                st.session_state.user_prompt = ""
            st.experimental_rerun()

    # Input field
    st.text_input(
        "",
        placeholder="Ask your Pega-related question...",
        key="user_prompt",
        on_change=generate_response,
        label_visibility="collapsed"
    )

    # Footer
    st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)  # Add space for fixed input
    st.write("---")
    st.info("Note: This AI Tutor answers questions specifically about the Pega platform. For other topics, please use other resources.")
