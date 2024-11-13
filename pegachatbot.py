import google.generativeai as genai
import streamlit as st
from PIL import Image

# Set up Streamlit page configuration with an engaging title
st.set_page_config(page_title="AI-Powered Pega Tutor", page_icon="🎓", layout="centered")

# Add a background image or color gradient (CSS hack)
st.markdown(
    """
    <style>
        .main {
            background: linear-gradient(to right, #ece9e6, #ffffff);
            padding: 20px;
            border-radius: 8px;
        }
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            width: 100%;
            padding: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stTextInput {
            border-radius: 8px;
        }
    </style>
    """, unsafe_allow_html=True
)

# Logo and Hero Section
image = Image.open("pega.jpeg")
col1, col2 = st.columns([1, 3])
with col1:
    st.image(image, width=120)
with col2:
    st.title("AI-Powered Pega Tutor")
    st.write("🌐 **Your Personal Pega Guide**")
    st.write("Get expert answers to all your Pega-related queries, directly from an AI tutor with 20 years of experience!")

# Configure API key
genai.configure(api_key="AIzaSyDhzLev5d_V46XA7KQrmg4u90M_g2Xq8Kc")

# System prompt for the generative model
sys_prompt = """
You are an experienced AI Tutor with 20 years of professional expertise in the Pega platform.
Your role is to help students by answering their questions related to Pega in a very clear, simple, 
and easy-to-understand manner. Provide detailed explanations and use relatable examples to help 
illustrate your points effectively. If a student asks a question outside the scope of Pega, politely 
decline and remind them to ask questions only related to Pega platform.
"""

# Initialize the generative model
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash", system_instruction=sys_prompt)

# Function to generate response
def generate_response():
    user_prompt = st.session_state.user_prompt
    if user_prompt:
        with st.spinner("Generating an answer for you..."):
            response = model.generate_content(user_prompt)
            st.session_state.response_text = response.text
    else:
        st.session_state.response_text = "Please enter a query before pressing Enter."

# User input section with chat-like style
st.subheader("Ask Your Pega-Related Question Below:")
st.text_input(
    "Type your question here:", 
    placeholder="E.g., How does Pega manage workflows?", 
    key="user_prompt", 
    on_change=generate_response,
)

# Button with improved styling
btn_click = st.button("Get Answer 🎓")

if btn_click:
    generate_response()

# Display the response with a chat bubble-like format
if 'response_text' in st.session_state:
    st.markdown("#### Tutor's Response:")
    st.write(f"💬: {st.session_state.response_text}")

# Footer note
st.write("---")
st.info("This AI Tutor is dedicated to answering questions specifically about the Pega platform. For other topics, please use additional resources.")

