import google.generativeai as genai
import streamlit as st
from PIL import Image

# Set up Streamlit page configuration
st.set_page_config(page_title="Pega Tutor", page_icon="🎓", layout="centered")

# Load and display logo/image
image = Image.open("pega.jpeg")
col1, col2 = st.columns([1, 3])
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
if "history" not in st.session_state:
    st.session_state.history = []

# Function to generate response
def generate_response():
    user_prompt = st.session_state.user_prompt
    if user_prompt:
        with st.spinner("Generating answer..."):
            response = model.generate_content(user_prompt)
            # Add user prompt and AI response to history
            st.session_state.history.append({"user": user_prompt, "bot": response.text})
            # Clear the input field after submission
            st.session_state.user_prompt = ""

# Display chat history in a scrollable format
st.subheader("Chat History")
chat_container = st.container()
with chat_container:
    for chat in st.session_state.history:
        st.markdown(f"**You**: {chat['user']}")
        st.markdown(f"**Tutor**: {chat['bot']}")

# Fixed input box at the bottom for user query
st.write("---")
st.text_input(
    "Ask your Pega-related question:", 
    placeholder="E.g., How does Pega manage workflows?", 
    key="user_prompt", 
    on_change=generate_response
)

# Button for generating a response
btn_click = st.button("Generate Answer")

if btn_click:
    generate_response()

# Display footer or additional help text
st.info("Note: This AI Tutor answers questions specifically about the Pega platform. For other topics, please use other resources.")
