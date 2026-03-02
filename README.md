AIScriptGenerator
Project Overview

AI-Powered Test Script Generator – Generates QUnit UI5 tests, Mocha + Chai API tests, and reusable automation functions using Hugging Face Router API powered by Groq (Meta Llama 3 8B Instruct).

🌐 Live App: https://aiscriptgenerator.streamlit.app/

🧠 AI Model & Provider

The application now uses:

Hugging Face Router API

Groq (Inference Provider)

Model: meta-llama/Meta-Llama-3-8B-Instruct

Why This Upgrade?

⚡ Ultra-fast inference (Groq acceleration)

🧠 Strong structured code generation

🆓 Free-tier friendly

🔄 Provider abstraction (easy future model switching)

🚀 More reliable than previous Gemini free-tier setup

✨ Key Features

🟦 QUnit UI5 tests (SAP UI5 / non-UI5)

🟩 Mocha + Chai API integration tests

🟨 Reusable test functions with edge cases (Mocha + got)

⏰ Timeout & retry handling included

📋 Follows official Mocha syntax standards

🔄 CSV (Xray format) upload support

⚡ Dynamic prompt engineering for structured output

🏗 Architecture Overview
Streamlit Frontend
        ↓
Prompt Engineering Layer
        ↓
Hugging Face Router API
        ↓
Groq Inference Provider
        ↓
Meta-Llama-3-8B-Instruct
        ↓
Generated JavaScript Test Script
🚀 Live Demo

✅ Try it now:
https://aiscriptgenerator.streamlit.app/

🚀 Already Live – No Setup Required

Production deployed on Streamlit Cloud with Hugging Face API key input box in UI.

🔐 How to Generate Hugging Face API Key (For AIScriptGenerator)
Step-by-Step Guide
1️⃣ Create Hugging Face Account

Go to:
https://huggingface.co/

Sign up / Log in.

2️⃣ Generate API Token

Go to:
https://huggingface.co/settings/tokens

Click New token

Select:

Role → Read

Click Generate

Token format:

hf_xxxxxxxxxxxxxxxxx

Copy immediately.

3️⃣ Enable Groq Provider

Go to:

https://huggingface.co/settings/inference-providers

Enable:

✅ Groq

(This is required for Meta Llama 3 model support.)

4️⃣ Use in App

Open: https://aiscriptgenerator.streamlit.app/

Paste your Hugging Face API key

Select test type

Paste test scenario

Click Generate Test Script

🧪 Usage (3 Clicks)

1️⃣ Visit live app
2️⃣ Enter Hugging Face API key
3️⃣ Paste test steps → Generate → Copy script
