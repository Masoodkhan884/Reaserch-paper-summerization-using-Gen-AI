import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the Gemini model
model = genai.GenerativeModel(
    "gemini-2.0-flash",
    system_instruction="You are an expert research summarization assistant."
)

# --- Streamlit Interface ---
st.set_page_config(
    page_title="AI Research Paper Summarizer",
    page_icon="📄",
    layout="centered"
)

st.title("📄 AI Research Paper Summarizer & Chat Assistant")
st.caption("Powered by Gemini 2.0 Flash – Summarize and explore academic papers intelligently.")

# Input field for paper name
paper_name = st.text_input("Enter the research paper title:", placeholder="e.g., Attention Is All You Need")

if st.button("🔍 Generate Summary"):
    if not paper_name.strip():
        st.warning("⚠️ Please enter a paper title first.")
    else:
        with st.spinner("Generating structured academic summary..."):
            prompt = f"""
            You are a research assistant specializing in summarizing academic papers.
            Summarize the research paper titled "{paper_name}" using reliable academic knowledge.

            Provide the summary in the following structured format:
            1. **Title**
            2. **Abstract Summary**
            3. **Key Contributions**
            4. **Methodology / Approach**
            5. **Results / Findings**
            6. **Limitations**
            7. **Future Work / Research Gap**
            8. **Overall Summary (3 concise sentences)**

            Ensure the summary is factual, academic, and clearly structured.
            """
            response = model.generate_content(prompt)
            summary_text = response.text

        st.success("✅ Summary Generated Successfully!")
        st.markdown(summary_text)
        st.session_state["summary_text"] = summary_text

# --- Chat Section ---
if "summary_text" in st.session_state:
    st.divider()
    st.subheader("💬 Chat About This Paper")

    # Initialize chat if not created
    if "chat" not in st.session_state:
        st.session_state["chat"] = model.start_chat(
            history=[{"role": "user", "parts": st.session_state["summary_text"]}]
        )

    user_question = st.text_input("Ask a question about the summarized paper:")

    if st.button("Send"):
        if user_question.strip():
            response = st.session_state["chat"].send_message(user_question)
            st.markdown(f"**🧠 AI:** {response.text}")
        else:
            st.warning("Please enter a question before sending.")
