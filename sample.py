import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# --- Setup Gemini API ---
genai.configure(api_key="AIzaSyBTPDAVY2fKwg5zvipyIDkzqwybsoMO5qA")
model = genai.GenerativeModel('gemini-2.0-flash')

# --- Helper function to generate email ---
def generate_email(prompt, format_type, tone):
    prompt_text = f"""
    Generate a professional email using the following details:
    
    Context: {prompt}
    Format: {format_type}
    Tone: {tone}

    Ensure it's clear, concise, and grammatically correct.
    """
    response = model.generate_content(prompt_text)
    return response.text.strip()

# --- Helper function to create downloadable PDF ---
def create_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in content.split('\n'):
        pdf.multi_cell(0, 10, line)
    return pdf

# --- Streamlit UI ---
st.set_page_config(page_title="AI Email Generator", layout="centered")
st.title("✉️ AI Email Generator using Gemini")

with st.expander("ℹ️ Instructions", expanded=False):
    st.markdown("""
    1. Enter your message or context.
    2. Choose the format and tone.
    3. Click 'Generate Email' to create a draft.
    4. You can regenerate or download as PDF.
    """)

# --- User Input ---
user_input = st.text_area("Enter the base message or context:", height=150)

format_type = st.selectbox("Choose Email Format", ["Formal", "Semi-formal", "Informal", "Apology", "Request", "Follow-up"])
tone = st.radio("Select Tone", ["Professional", "Friendly", "Urgent", "Appreciative", "Persuasive"])

if "generated_email" not in st.session_state:
    st.session_state.generated_email = ""

# --- Buttons ---
col1, col2 = st.columns(2)

with col1:
    if st.button("Generate Email"):
        if user_input.strip() == "":
            st.warning("Please enter the email context.")
        else:
            email_output = generate_email(user_input, format_type, tone)
            st.session_state.generated_email = email_output

with col2:
    if st.button("Regenerate"):
        if user_input.strip() == "":
            st.warning("Please enter the email context.")
        else:
            regenerated_email = generate_email(user_input, format_type, tone)
            st.session_state.generated_email = regenerated_email

# --- Display Generated Email ---
if st.session_state.generated_email:
    st.subheader("📩 Generated Email")
    st.text_area(label="", value=st.session_state.generated_email, height=300)

    # --- Download as PDF ---
    pdf = create_pdf(st.session_state.generated_email)
    pdf_output = pdf.output(dest='S').encode('latin1')
    st.download_button(label="📥 Download Email as PDF", data=pdf_output, file_name="generated_email.pdf", mime='application/pdf')

