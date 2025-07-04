import streamlit as st
import google.generativeai as genai
import pandas as pd
import os

# --- SETUP ---
# Set page config first
st.set_page_config(page_title="AI Test Script Generator", layout="centered")

# Title and description
st.title("🧪 AI-Powered Test Script Generator")
st.markdown("""
Choose your test mode and input method. This app uses Gemini to generate:
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
api_key = st.text_input("🔐 Enter your Gemini API Key", type="password")

if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key
    genai.configure(api_key=api_key)

    # --- Test Type & Input ---
    test_type = st.selectbox("🧪 Select Test Type", ["QMate UI Test (UI5/Non-UI5)", "Integration Test (API)"])
    input_method = st.radio("✍️ Choose Input Method", ["Manual Input", "Upload CSV (Xray Format)"])

    test_steps = ""
    if input_method == "Manual Input":
        test_steps = st.text_area("📋 Enter Test Steps", height=200, placeholder="1. Go to login\n2. Enter credentials\n3. Click login")
    else:
        uploaded_file = st.file_uploader("📂 Upload CSV (Action, Data, Expected Result)", type=["csv"])
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            test_steps = "\n".join(
                f"{row['Action']} - {row['Data']} - {row['Expected Result']}" for _, row in df.iterrows()
            )

    # --- API specific inputs ---
    curl_cmd = ""
    expected_response = ""
    if "Integration" in test_type:
        curl_cmd = st.text_area("🔗 Provide cURL Command", placeholder="curl -X GET https://api.example.com/users")
        expected_response = st.text_area("📨 Expected Response (JSON or text)", placeholder='{"status": "success", "users": [...]}')

    # --- Generate Button ---
    if st.button("🚀 Generate Test Script"):
        if not test_steps.strip():
            st.warning("Please provide test steps.")
        else:
            with st.spinner("Generating script with Gemini..."):
                try:
                    model = genai.GenerativeModel("gemini-1.5-flash")

                    if "QMate" in test_type:
                        prompt = f"""
You are a QMate test automation expert.

Use the official QMate documentation provided below to generate an accurate test automation script using  QMate.


📋 Manual Steps:
{test_steps}

✅ STRICT RULES:
- Use `common.userInteraction`, `common.assertion`, `common.navigation`, etc. wherever applicable
- Avoid using `fillActive()` unless no selector is available
- Use realistic selectors with `await $(...)`
- Separate `it` blocks for login, actions, and validations
- Add `waitUntil`, retry, and timeout handling where needed
- If action patterns repeat, refactor into reusable helper functions
- Cover at least 1-2 edge case scenarios (missing data, invalid login, etc.)

Return ONLY the JavaScript test script.
"""
                    else:
                        prompt = f"""
You are an API test automation expert.

Create a JavaScript test suite using Mocha + Got + Chai based on the following:
- Manual test steps
- Given cURL command and expected response

📋 Manual Steps:
{test_steps}

🔗 API Request:
{curl_cmd}

📨 Expected Response:
{expected_response}

✅ Include:
- Happy path test
- 1-2 edge cases (400, 404, bad auth, etc.)
- Proper `describe` and `it` blocks with assertions
- Use try-catch for timeout and error handling
- Use `got` for HTTP and `chai.expect()` for assertions

Return ONLY the code.
"""

                    response = model.generate_content(prompt)
                    st.code(response.text.strip(), language="javascript")
                    st.success("Test script generated!")
                except Exception as e:
                    st.error(f"Error generating script: {str(e)}")
else:
    st.info("🔐 Please enter your Gemini API key to begin.")
