import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# --- Configure Gemini API ---
genai.configure(api_key="AIzaSyDEl99LtXjbWHJjqm9X-unxzotXaL7qTU0")  # Replace with your actual API key
model = genai.GenerativeModel("gemini-2.0-flash")

# --- Streamlit UI Setup ---
st.set_page_config(page_title="Design Audit Bot", layout="wide")
st.title("🧠 Design Audit Bot – AI-Powered UX Feedback")
st.caption("Analyze UI screens and get expert UX improvement tips from an AI co-pilot.")
st.markdown("---")

# --- UI: Split layout for inputs ---
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("👤 User Context")
    persona = st.text_input("User Persona", placeholder="e.g., First-time banking user, Gen Z shopper")
    needs = st.text_area("User Needs", placeholder="e.g., Easily transfer funds, find best deals")
    goals = st.text_area("User Goals", placeholder="e.g., Buy item in 2 clicks, access quickly")
    success_metrics = st.text_input("Success Metrics (optional)", placeholder="e.g., NPS, bounce rate")

with col2:
    st.subheader("📋 UI Input")
    st.markdown("**Option 1** – Describe your UI (HTML/CSS or plain English)")
    input_text = st.text_area("✍️ Paste your UI description or code", height=200)
    st.markdown("**Option 2** – Upload a UI Screenshot")
    uploaded_image = st.file_uploader("Upload image (PNG, JPG)", type=["png", "jpg", "jpeg"])

st.markdown("---")

# --- Run UX Audit ---
run_audit = st.button("🚀 Run UX Audit")

if run_audit:
    if not input_text.strip() and uploaded_image is None:
        st.warning("⚠️ Please enter a UI description or upload a screenshot to proceed.")
    else:
        with st.spinner("🔍 Analyzing your design with Gemini..."):
            try:
                context = f"""
User Persona: {persona or 'Not specified'}
User Needs: {needs or 'Not specified'}
User Goals: {goals or 'Not specified'}
Success Metrics: {success_metrics or 'Not specified'}
"""

                if uploaded_image is not None:
                    image = Image.open(uploaded_image)
                    prompt = f"""
You are a professional UX designer.

Analyze the following UI image and provide a comprehensive UX audit. Consider the user persona, needs, goals, and metrics:

{context}

Your response should include:
1. 🧪 Usability issues
2. 🎯 UX design improvement suggestions
3. 🧩 Accessibility concerns
4. 🎨 Visual hierarchy and layout feedback
5. 🔄 Design alignment with user goals
6. 📊 Opportunities to improve success metrics
7. 🌐 Modern UX trends to consider
"""
                    response = model.generate_content([prompt, image])
                    st.success("✅ Image Audit Complete")
                    st.image(image, caption="Uploaded Screenshot", use_column_width=True)
                    st.markdown("### 💡 UX Suggestions")
                    st.write(response.text)

                elif input_text.strip():
                    prompt = f"""
You are a professional UX designer.

Review the following screen description or HTML/CSS. Incorporate user persona, needs, goals, and metrics in your feedback:

{context}

Design Input:
\"\"\"{input_text}\"\"\"

Your response should include:
1. 🧪 Usability issues
2. 🎯 UX design improvement suggestions
3. 🧩 Accessibility concerns
4. 🎨 Visual hierarchy and layout feedback
5. 🔄 Design alignment with user goals
6. 📊 Opportunities to improve success metrics
7. 🌐 Modern UX trends to consider
"""
                    response = model.generate_content(prompt)
                    st.success("✅ Text Audit Complete")
                    st.markdown("### 💡 UX Suggestions")
                    st.write(response.text)

                # --- Downloadable Report ---
                report_md = f"""
## 🧠 UX Audit Report

### 👤 User Context
- **Persona:** {persona or 'Not specified'}
- **Needs:** {needs or 'Not specified'}
- **Goals:** {goals or 'Not specified'}
- **Success Metrics:** {success_metrics or 'Not specified'}

---

### 💬 Gemini UX Feedback
{response.text}
"""

                report_bytes = io.BytesIO(report_md.encode("utf-8"))
                st.download_button(
                    label="📥 Download UX Report",
                    data=report_bytes,
                    file_name="ux_audit_report.md",
                    mime="text/markdown"
                )

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

st.markdown("---")
st.caption("Made with ❤️ using Streamlit and Gemini AI")
