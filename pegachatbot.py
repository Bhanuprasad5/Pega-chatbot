import google.generativeai as genai
import streamlit as st

# Configure API key
genai.configure(api_key="AIzaSyDhzLev5d_V46XA7KQrmg4u90M_g2Xq8Kc")

# System prompt for the generative model
sys_prompt = """You are an experienced AI Tutor with 20 years of professional expertise in Pega platform.
Your role is to help students by answering their questions related to Pega in a very clear, simple, 
and easy-to-understand manner. Provide detailed explanations and 
use relatable examples to help illustrate your points effectively.
If a student asks a question outside the scope of Pega, politely decline and 
remind them to ask questions only related to Pega systems and tools."""

# Initialize the generative model
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash", system_instruction=sys_prompt)

# Streamlit interface setup
st.title("Pega Tutor Application")

# Get user input
user_prompt = st.text_input("Enter your query:", placeholder="Type your query here...")

# Button for generating a response
btn_click = st.button("Generate Answer")

if btn_click:
    if user_prompt:
        # Generate response from the model
        response = model.generate_content(user_prompt)
        st.write(response.text)
    else:
        st.write("Please enter a query before clicking the button.")
