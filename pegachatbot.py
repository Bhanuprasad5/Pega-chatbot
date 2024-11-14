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

# Function to generate responses and maintain chat history
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

# Sidebar for chat history
with st.sidebar:
    st.image(image, width=120)
    st.title("Pega Tutor Application")
    st.write("An expert AI-powered tutor to help with your Pega-related questions.")
    st.markdown("### Chat History")
    for user_question, ai_response in st.session_state.chat_history:
        with st.expander(user_question):
            st.write(f"🧑‍🏫: {ai_response}")

# Display chat history in main area for a larger view
for user_question, ai_response in st.session_state.chat_history:
    st.markdown(f"**You:** {user_question}")
    st.write(f"🧑‍🏫: {ai_response}")
    st.write("---")

# CSS for the fixed search bar at the bottom and styling
st.markdown("""
    <style>
        /* Fixed position for the input area at the bottom */
        .fixed-bottom {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #333;
            padding: 10px;
            display: flex;
            align-items: center;
            z-index: 9999;
        }
        /* Styling the input box */
        .fixed-bottom input[type="text"] {
            flex: 1;
            padding: 10px;
            border-radius: 20px;
            border: none;
            outline: none;
            margin-right: 10px;
            background-color: #444;
            color: #fff;
        }
        /* Styling the button */
        .fixed-bottom button {
            background-color: #5c5f8a;
            border: none;
            padding: 10px 15px;
            border-radius: 50%;
            cursor: pointer;
            color: white;
            font-size: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# JavaScript to capture button click and trigger response
st.markdown("""
    <script>
        function onButtonClick() {
            window.parent.document.getElementById("user_prompt").value = "";
        }
    </script>
""", unsafe_allow_html=True)

# Bottom input area fixed with the CSS class
st.markdown(
    f"""
    <div class="fixed-bottom">
        <input type="text" placeholder="Type your question..." id="user_prompt" 
            onkeydown="if(event.key === 'Enter'){{window.parent.document.getElementById('user_prompt').value = '';}}"
            value="{st.session_state.get('user_prompt', '')}"/>
        <button onclick="onButtonClick()">⬆️</button>
    </div>
    """,
    unsafe_allow_html=True
)

# Ensure that the function runs when Enter or the button is clicked
if st.session_state.get("user_prompt"):
    generate_response()
