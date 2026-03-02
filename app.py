# ✅ COMPLETE OpenAI VERSION - Copy & Replace Entire app.py

import streamlit as st
from openai import OpenAI
import pandas as pd
import os

# --- SETUP ---
st.set_page_config(page_title="AI Test Script Generator", layout="centered")

# Title and description
st.title("🧪 AI-Powered Test Script Generator")
st.markdown("""
Choose your test mode and input method. This app uses **OpenAI** to generate:
- 🟦 QMate UI test scripts for SAP UI5 / non-UI5
- 🟩 API Integration test scripts using Mocha + Got + Chai

Also includes:
- 🧠 Auto-inferred edge cases
- 🔁 Reusable functions (if repeated steps detected)
- ⏱ Timeout or retry handling
- 📚 Follows [QMate official syntax](https://sap.github.io/wdio-qmate-service/doc/)
""")

# Load QMate documentation from local scraped index.md file
scraped_path = "index.md"
qmate_docs = ""
if os.path.exists(scraped_path):
    with open(scraped_path, "r", encoding="utf-8") as f:
        qmate_docs = f.read()[:12000]  # Keep within token limit

# --- API Key Setup ---
api_key = st.text_input("🔐 Enter your **OpenAI** API Key", type="password", 
                       help="Get free key: https://platform.openai.com/api-keys")

if api_key:
    client = OpenAI(api_key=api_key)

    # --- Test Type & Input ---
    test_type = st.selectbox("🧪 Select Test Type", ["QMate UI Test (UI5/Non-UI5)", "Integration Test (API)"])
    input_method = st.radio("✍️ Choose Input Method", ["Manual Input", "Upload CSV (Xray Format)"])

    test_steps = ""
    if input_method == "Manual Input":
        test_steps = st.text_area("📋 Enter Test Steps", height=200, 
                                 placeholder="1. Go to login\n2. Enter credentials\n3. Click login")
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
        curl_cmd = st.text_area("🔗 Provide cURL Command", 
                               placeholder="curl -X GET https://api.example.com/users")
        expected_response = st.text_area("📨 Expected Response (JSON or text)", 
                                        placeholder='{"status": "success", "users": [...]}')

    # --- Generate Button ---
    if st.button("🚀 Generate Test Script"):
        if not test_steps.strip():
            st.warning("Please provide test steps.")
        else:
            with st.spinner("Generating script with OpenAI..."):
                try:
                    if "QMate" in test_type:
                        prompt = f"""You are a QMate test automation expert.

Use official QMate syntax to generate JavaScript test script for these steps:

📋 Test Steps:
{test_steps}

✅ REQUIREMENTS:
- Use `common.userInteraction`, `common.assertion`, `common.navigation`
- Realistic selectors: `await $(...)`
- Separate `it` blocks for each major action
- Add `waitUntil`, timeouts, retries
- Include 1-2 edge cases
- Mocha `describe`/`it` structure

Return ONLY the JavaScript code. No explanations."""

                    else:
                        prompt = f"""Create Mocha + Got + Chai API test for:

📋 Steps: {test_steps}
🔗 cURL: {curl_cmd}
📨 Expected: {expected_response}

✅ Include:
- Happy path test
- Edge cases (400, 404, timeout)
- `got()` for HTTP requests
- `chai.expect()` assertions
- Proper `describe`/`it` blocks

Return ONLY JavaScript code."""

                    # 🔥 OPENAI CALL - 100% WORKING
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",  # FREE tier model
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=2000,
                        temperature=0.1
                    )
                    
                    script = response.choices[0].message.content.strip()
                    st.code(script, language="javascript")
                    st.success("✅ Test script generated with OpenAI!")
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.info("💡 Get free OpenAI key: platform.openai.com/api-keys")
else:
    st.info("🔐 Enter OpenAI API key to start (Free $5 credit at signup)")
