import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- Configure Gemini API ---
genai.configure(api_key="AIzaSyDEl99LtXjbWHJjqm9X-unxzotXaL7qTU0")  # Replace with your actual API key
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Streamlit UI Setup ---
st.set_page_config(page_title="Design Audit Bot", layout="wide")
st.title("🧠 Design Audit Bot – AI-Powered UX Feedback")

st.markdown("Use AI to review and improve your UI design based on best practices and real-world UX insights.")

# --- Input Section ---
st.markdown("### 👤 Context: Who is this design for?")
persona = st.text_input("User Persona", placeholder="e.g., First-time mobile banking user, Gen Z e-commerce shopper")

needs = st.text_area("User Needs", placeholder="e.g., Quickly check balances, easy checkout, trustworthiness")

goals = st.text_area("User Goals", placeholder="e.g., Complete purchase within 2 minutes, find top deals easily")

success_metrics = st.text_input("Success Metrics (Optional)", placeholder="e.g., Task completion rate, NPS, bounce rate")

st.markdown("### 📋 Option 1: Describe your screen (HTML/CSS or plain English)")
input_text = st.text_area("✍️ Paste HTML/CSS or describe your UI", height=250)

st.markdown("### 🖼️ Option 2: Upload a Screenshot (PNG/JPG)")
uploaded_image = st.file_uploader("Upload a UI screenshot", type=["png", "jpg", "jpeg"])

# --- Run UX Audit ---
if st.button("Run UX Audit"):
    if not input_text.strip() and uploaded_image is None:
        st.warning("⚠️ Please enter a description or upload an image.")
    else:
        with st.spinner("🔍 Analyzing with Gemini..."):
            try:
                # Format shared context
                context = f"""
User Persona: {persona or 'Not specified'}
User Needs: {needs or 'Not specified'}
User Goals: {goals or 'Not specified'}
Success Metrics: {success_metrics or 'Not specified'}
"""

                # --- Image-based Analysis ---
                if uploaded_image is not None:
                    image = Image.open(uploaded_image)
                    prompt = f"""
You are a professional UX designer.

Analyze the following UI image and provide a comprehensive UX audit. Consider the user persona, needs, goals, and metrics:

{context}

Your response should include:
1. Key usability issues
2. UX design improvement suggestions
3. Accessibility concerns
4. Visual hierarchy and layout feedback
5. Design alignment with user goals
6. Opportunities to improve success metrics
7. Modern UX trends to consider
"""
                    response = model.generate_content([prompt, image])
                    st.success("✅ Image Audit Complete")
                    st.image(image, caption="Uploaded UI Screenshot", use_column_width=True)
                    st.markdown("### 💡 UX Suggestions")
                    st.write(response.text)

                # --- Text-based Analysis ---
                elif input_text.strip():
                    prompt = f"""
You are a professional UX designer.

Review the following screen description or HTML/CSS. Incorporate user persona, needs, goals, and metrics in your feedback:

{context}

Design Input:
\"\"\"{input_text}\"\"\"

Provide:
1. Usability issues
2. UX suggestions
3. Accessibility tips
4. Layout and visual advice
5. User-goal alignment
6. Ways to improve metrics
7. Modern UX trends
"""
                    response = model.generate_content(prompt)
                    st.success("✅ Text Audit Complete")
                    st.markdown("### 💡 UX Suggestions")
                    st.write(response.text)

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
