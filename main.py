import streamlit as st
from polymarket_prompt import get_polymarket_prompt

st.set_page_config(page_title="Polymarket Prompt Generator", layout="centered")

st.title("📋 Polymarket Prompt Generator")

event_url = st.text_input("Enter the Polymarket event URL:")

if event_url:
    with st.spinner("Generating prompt..."):
        prompt = get_polymarket_prompt(event_url)
        st.code(prompt, language="text")
