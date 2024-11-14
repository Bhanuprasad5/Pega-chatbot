import google.generativeai as genai
import streamlit as st
from PIL import Image

# Set up Streamlit page configuration
st.set_page_config(page_title="Pega Tutor", page_icon="🎓", layout="wide")

# Sidebar for chat history
st.sidebar.header("Chat History")
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

def display_chat_history():
    for i, entry in enumerate(st.session_state['chat_history']):
        if entry.get('question') and entry.get('answer'):
            with st.sidebar.expander(f"Question {i + 1}", expanded=False):
                st.write(f"**Q:** {entry['question']}")
                st.write(f"**A:** {entry['answer']}")

# Display chat history in the sidebar
display_chat_history()

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

# Function to generate response
def generate_response():
    user_prompt = st.session_state.user_prompt
    if user_prompt:
        with st.spinner("Generating answer..."):
            response = model.generate_content(user_prompt)
            response_text = response.text
            st.session_state.response_text = response_text
            # Save the interaction in chat history
            st.session_state.chat_history.append({"question": user_prompt, "answer": response_text})

# Main chat section with scrolling feature
st.subheader("Ask your Pega-related question:")
chat_container = st.container()
with chat_container:
    for entry in st.session_state['chat_history']:
        st.markdown(f"**You**: {entry['question']}")
        st.write(f"🧑‍🏫: {entry['answer']}")

# Fixed position for the input field at the bottom with CSS styling
st.markdown(
    """
    <style>
    .stTextInput {
        position: fixed;
        bottom: 10px;
        width: 90%;
        margin-left: 5%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Input field for the user's question
st.text_input(
    "Enter your question below:", 
    placeholder="E.g., How does Pega manage workflows?", 
    key="user_prompt", 
    on_change=generate_response,
    label_visibility="collapsed"
)

# Display footer or additional help text
st.write("---")
st.info("Note: This AI Tutor answers questions specifically about the Pega platform. For other topics, please use other resources.")
