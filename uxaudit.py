import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- Configure Gemini API ---
genai.configure(api_key="AIzaSyDEl99LtXjbWHJjqm9X-unxzotXaL7qTU0")  # Replace with your actual API key
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Streamlit UI Setup ---
st.set_page_config(page_title="Design Audit Bot", layout="wide")
st.title("🧠 Design Audit Bot – AI-Powered UX Feedback")

# --- Input Section ---
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
                # --- Image-based Analysis ---
                if uploaded_image is not None:
                    image = Image.open(uploaded_image)  # ✅ Use PIL.Image
                    response = model.generate_content(
                        [
                            "You are a professional UX designer. Analyze the UI in this image and provide:\n"
                            "1. Key usability issues\n"
                            "2. UX design improvement suggestions\n"
                            "3. Accessibility concerns\n"
                            "4. Visual hierarchy tips\n"
                            "5. Modern design recommendations",
                            image
                        ]
                    )
                    st.success("✅ Image Audit Complete")
                    st.image(image, caption="Uploaded UI Screenshot", use_column_width=True)
                    st.markdown("### 💡 UX Suggestions")
                    st.write(response.text)

                # --- Text-based Analysis ---
                elif input_text.strip():
                    prompt = f"""
You are a professional UX designer. Review the following screen description or HTML/CSS and provide:
1. Key usability issues.
2. Suggestions for improvement (based on UX principles).
3. Accessibility tips.
4. Visual and layout recommendations.

Design Input:
\"\"\"
{input_text}
\"\"\"
"""
                    response = model.generate_content(prompt)
                    st.success("✅ Text Audit Complete")
                    st.markdown("### 💡 UX Suggestions")
                    st.write(response.text)

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
