from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
import os
import streamlit as st

from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-pro")

def get_gemini_response(input_prompt, image, image_prompt):
    if image_prompt.strip() != "":
        response = model.generate_content([input_prompt, image, image_prompt])
        return response.text
    else:
        response = model.generate_content([input_prompt, image])
        return response.text


## Streamlit - FE

st.set_page_config("Invoice Extractor")
st.header("AI Invoice Extractor")


image_prompt = st.text_input("Ask Question From Image", key="input")
submit = st.button("Ask Question", key="ques-btn")

## 1. UPLOAD FILE
uploaded_file = st.file_uploader("Upload Your Invoice", type=['jpg', 'jpeg', 'png'])



## 2. DISPLAY THE UPLOADED FILE

image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image)


## 3. GENERATE CONTENT

input_prompt = """
You are an expert in understanding invoices. I will upload an invoice
image and you will have to answer questions based on the uploaded
invoice image
"""

if submit:
    response = get_gemini_response(input_prompt, image, image_prompt)
    st.write(response)