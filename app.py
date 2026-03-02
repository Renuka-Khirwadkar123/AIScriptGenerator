import streamlit as st
import requests
import pandas as pd
import os
import json

# --- SETUP ---
st.set_page_config(page_title="AI Test Script Generator", layout="centered")

# Title and description
st.title("🧪 AI-Powered Test Script Generator")
st.markdown("""
**Hugging Face FREE API** se generate hota hai:
- 🟦 QMate UI test scripts for SAP UI5 / non-UI5  
- 🟩 API Integration test scripts using Mocha + Got + Chai

Features:
- 🧠 Auto-inferred edge cases
- 🔁 Reusable functions
- ⏱ Timeout/retry handling
- 📚 QMate official syntax
""")

# Load QMate documentation 
scraped_path = "index.md"
qmate_docs = ""
if os.path.exists(scraped_path):
    with open(scraped_path, "r", encoding="utf-8") as f:
        qmate_docs = f.read()[:8000]

# --- HUGGING FACE API KEY SETUP ---
api_key = st.text_input(
    "🔐 Enter your Hugging Face API Key (FREE)",
    type="password",
    help="Get FREE key: https://huggingface.co/settings/tokens"
)

HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

if api_key:

    # --- Test Type & Input ---
    test_type = st.selectbox("🧪 Select Test Type", ["QMate UI Test (UI5/Non-UI5)", "Integration Test (API)"])
    input_method = st.radio("✍️ Choose Input Method", ["Manual Input", "Upload CSV (Xray Format)"])

    test_steps = ""
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
                f"{row['Action']} - {row['Data']} - {row['Expected Result']}"
                for _, row in df.iterrows()
            )

    # --- API specific inputs ---
    curl_cmd = ""
    expected_response = ""
    if "Integration" in test_type:
        curl_cmd = st.text_area(
            "🔗 Provide cURL Command",
            placeholder="curl -X GET https://api.example.com/users"
        )
        expected_response = st.text_area(
            "📨 Expected Response (JSON or text)",
            placeholder='{"status": "success", "users": [...]}'
        )

    # --- Generate Button ---
    if st.button("🚀 Generate Test Script", type="primary"):

        if not test_steps.strip():
            st.warning("Please provide test steps.")
        else:
            with st.spinner("Generating script with Hugging Face FREE API..."):
                try:

                    if "QMate" in test_type:
                        prompt = f"""
You are expert QMate test automation engineer for SAP UI5.

Generate COMPLETE JavaScript test script ONLY for these steps:

{test_steps}

Use:
- common.userInteraction.click()
- common.assertion.textEquals()
- await $(selector).waitForDisplayed()
- Mocha describe/it blocks
- Realistic selectors like #loginBtn, .userTable
- Add timeouts, retries, 1-2 edge cases

CODE ONLY - No explanations.
"""
                    else:
                        prompt = f"""
Create Mocha + Got + Chai API test.

Steps:
{test_steps}

cURL:
{curl_cmd}

Expected:
{expected_response}

Use:
- const got = require('got')
- chai.expect(response.statusCode).to.equal(200)
- Happy path + 2 edge cases
- Proper async/await

CODE ONLY.
"""

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

                        if isinstance(result, list):
                            script = result[0]["generated_text"].strip()
                        else:
                            script = result.get("generated_text", "").strip()

                        st.code(script, language="javascript")
                        st.balloons()
                        st.success("✅ Perfect test script generated with Hugging Face FREE API!")

                    else:
                        st.error(f"Hugging Face API Error: {response.text}")

                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.info("💡 Get FREE key: https://huggingface.co/settings/tokens")

else:
    st.info("🔐 FREE Hugging Face API Key → https://huggingface.co/settings/tokens")
    st.markdown("No credit card needed - Free tier available!")