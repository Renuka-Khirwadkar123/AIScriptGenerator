import streamlit as st
import requests
import pandas as pd
import os
import json

# --- SETUP ---
st.set_page_config(page_title="AI Test Script Generator", layout="centered")

# Title and description - PURE HUGGING FACE
st.title("🧪 AI-Powered Test Script Generator") 
st.markdown("""
**Hugging Face FREE Inference API** se generate hota hai:
- 🟦 QMate UI test scripts (SAP UI5/non-UI5)
- 🟩 API Integration tests (Mocha + Got + Chai)

**Free tier**: 1000+ requests/day, no credit card!
""")

# Load QMate documentation 
scraped_path = "index.md"
qmate_docs = ""
if os.path.exists(scraped_path):
    with open(scraped_path, "r", encoding="utf-8") as f:
        qmate_docs = f.read()[:8000]

# --- HUGGING FACE API KEY (FREE) ---
api_key = st.text_input(
    "🔐 Hugging Face API Key (FREE)",
    type="password",
    help="https://huggingface.co/settings/tokens → New token → Read access"
)

HF_API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"  # ✅ Fast + Free

headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

if api_key:
    # [YOUR EXISTING INPUT CODE - SAME]
    test_type = st.selectbox("🧪 Select Test Type", ["QMate UI Test (UI5/Non-UI5)", "Integration Test (API)"])
    # ... rest of input code same ...

    if st.button("🚀 Generate Test Script", type="primary"):
        if not test_steps.strip():
            st.warning("Please provide test steps.")
        else:
            with st.spinner("Generating with Hugging Face FREE API..."):
                try:
                    # YOUR PROMPT CODE - SAME
                    response = requests.post(
                        HF_API_URL,
                        headers=headers,
                        json={
                            "inputs": prompt,
                            "parameters": {
                                "temperature": 0.1,
                                "max_new_tokens": 2048,
                                "return_full_text": False
                            }
                        },
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        script = result[0]["generated_text"].strip()
                        st.code(script, language="javascript")
                        st.balloons()
                        st.success("✅ Generated with Hugging Face FREE API!")
                    else:
                        st.error(f"HF Error: {response.text}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

else:
    st.info("🔐 **FREE HF Key**: https://huggingface.co/settings/tokens")
