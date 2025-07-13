import streamlit as st
from polymarket_prompt import get_polymarket_prompt

st.set_page_config(page_title="Polymarket Prompt Generator", layout="centered")

st.title("📋 Polymarket Prompt Generator")

event_url = st.text_input("Enter the Polymarket event URL:")
include_volume = st.checkbox("Include market volume in prompt", value=True)

if event_url:
    with st.spinner("Generating prompt..."):
        prompt = get_polymarket_prompt(event_url, include_volume=include_volume)
        st.code(prompt, language="text")
