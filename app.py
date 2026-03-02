import streamlit as st
import requests
import pandas as pd
import os
import json

st.set_page_config(page_title="AI Test Script Generator", layout="centered")

st.title("🧪 AI-Powered Test Script Generator")
st.markdown("""
**Hugging Face FREE Inference API** se generate hota hai:
- 🟦 QMate UI test scripts (SAP UI5/non-UI5)
- 🟩 API Integration tests (Mocha + Got + Chai)
""")

# Load QMate documentation 
scraped_path = "index.md"
qmate_docs = ""
if os.path.exists(scraped_path):
    with open(scraped_path, "r", encoding="utf-8") as f:
        qmate_docs = f.read()[:8000]

# --- HUGGING FACE API KEY ---
api_key = st.text_input(
    "🔐 Hugging Face API Key (FREE)",
    type="password",
    help="https://huggingface.co/settings/tokens → New token → Read access"
)

HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

# ✅ FIX: test_steps GLOBAL scope mein initialize
test_steps = ""

if api_key:
    # Test Type & Input
    test_type = st.selectbox("🧪 Select Test Type", ["QMate UI Test (UI5/Non-UI5)", "Integration Test (API)"])
    input_method = st.radio("✍️ Choose Input Method", ["Manual Input", "Upload CSV (Xray Format)"])

    # ✅ FIXED: test_steps ab yahan update hota hai
    if input_method == "Manual Input":
        test_steps = st.text_area(
            "📋 Enter Test Steps",
            height=200,
            placeholder="1. Go to login\n2. Enter credentials\n3. Click login"
        )
    else:
        uploaded_file = st.file_uploader("📂 Upload CSV (Action, Data, Expected Result)", type=["csv"])
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            test_steps = "\n".join(
                f"{row.get('Action', '')} - {row.get('Data', '')} - {row.get('Expected Result', '')}"
                for _, row in df.iterrows()
            )

    # API specific inputs
    curl_cmd = ""
    expected_response = ""
    if "Integration" in test_type:
        curl_cmd = st.text_area("🔗 Provide cURL Command", placeholder="curl -X GET https://api.example.com/users")
        expected_response = st.text_area("📨 Expected Response (JSON)", placeholder='{"status": "success"}')

    # ✅ FIXED: test_steps ab globally available hai
    if st.button("🚀 Generate Test Script", type="primary"):
        if not test_steps.strip():  # ✅ No more NameError!
            st.warning("Please provide test steps.")
        else:
            with st.spinner("Generating with Hugging Face FREE API..."):
                try:
                    if "QMate" in test_type:
                        prompt = f"""You are expert QMate test automation engineer for SAP UI5.
Generate COMPLETE JavaScript test script ONLY for these steps:
{test_steps}
Use: common.userInteraction.click(), await $(selector).waitForDisplayed()
CODE ONLY - No explanations."""
                    else:
                        prompt = f"""Create Mocha + Got + Chai API test for: {test_steps}
cURL: {curl_cmd}
Expected: {expected_response}
CODE ONLY."""

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
                        st.success("✅ Perfect test script generated!")
                    else:
                        st.error(f"HF Error: {response.text}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

else:
    st.info("🔐 FREE Hugging Face API Key → https://huggingface.co/settings/tokens")
