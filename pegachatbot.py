import google.generativeai as genai
import streamlit as st
from PIL import Image

# Set up Streamlit page configuration
st.set_page_config(page_title="Pega Tutor", page_icon="🎓", layout="wide")

# Load and display logo/image
image = Image.open("pega.jpeg")
col1, col2 = st.columns([1, 3])
with col1:
    st.image(image, width=120)
with col2:
    st.title("Pega Tutor Application")
    st.write("An expert AI-powered tutor to help with your Pega-related questions.")

# Configure API key
genai.configure(api_key="YOUR_API_KEY_HERE")

# System prompt for the generative model
sys_prompt = """
You are an experienced Tutor with 20 years of professional expertise in the Pega Customer decision hub and Pega systems expert.
Your role is to help students by answering their questions related to Pega in a very clear, simple, 
and easy-to-understand manner. Provide detailed explanations and use relatable examples to help 
illustrate your points effectively. If a student asks a question outside the scope of Pega, politely 
decline and remind them to ask questions only related to the Pega platform.
"""

# Initialize the generative model
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash", system_instruction=sys_prompt)

# Initialize session state to store chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Function to generate response
def generate_response():
    user_prompt = st.session_state.user_prompt
    if user_prompt:
        with st.spinner("Generating answer..."):
            response = model.generate_content(user_prompt)
            # Store the query and response in chat history
            st.session_state.chat_history.append({"question": user_prompt, "answer": response.text})
            st.session_state.response_text = response.text
    else:
        st.session_state.response_text = "Please enter a query before pressing Enter."

# User input section
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

# Display chat history on the left sidebar
with st.sidebar:
    st.header("Chat History")
    for i, chat in enumerate(st.session_state.chat_history):
        st.write(f"**Q{i+1}:** {chat['question']}")
        st.write(f"**A{i+1}:** {chat['answer']}")
        st.write("---")

# Display the latest response in the main area
if 'response_text' in st.session_state:
    st.markdown("#### Tutor's Response:")
    st.write(f"🧑‍🏫: {st.session_state.response_text}")

# Display footer or additional help text
st.write("---")
st.info("Note: This AI Tutor answers questions specifically about the Pega platform. For other topics, please use other resources.")
