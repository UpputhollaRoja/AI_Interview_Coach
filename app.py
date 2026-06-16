import re
import streamlit as st
import google.generativeai as genai

# ------------------------------------------------------------
# Page Config
# ------------------------------------------------------------
st.set_page_config(page_title="AI Interview Prep Coach", page_icon="🎯", layout="wide")

# ------------------------------------------------------------
# Custom Styling
# ------------------------------------------------------------
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #6C63FF 0%, #4834d4 100%);
        padding: 1.8rem 1.5rem;
        border-radius: 14px;
        color: white;
        text-align: center;
        margin-bottom: 1.2rem;
    }
    .main-header h1 { margin: 0; font-size: 2rem; }
    .main-header p { margin: 0.4rem 0 0 0; opacity: 0.9; font-size: 0.95rem; }
    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
        border: none;
    }l
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6C63FF 0%, #4834d4 100%);
        color: white;
    }
    .stTabs [data-basweb="tab-list"] { gap: 6px; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 8px 16px;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# API Key Setup
# ------------------------------------------------------------
def get_api_key():
    # Try Streamlit secrets first (used when deployed)
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return st.session_state.get("api_key", "")

st.sidebar.title("🎯 AI Interview Coach")

api_key_input = st.sidebar.text_input(
    "Gemini API Key",
    type="password",
    help="Get a free key from https://aistudio.google.com/app/apikey"
)
if api_key_input:
    st.session_state["api_key"] = api_key_input

api_key = get_api_key()

model = None
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

st.sidebar.markdown("---")
job_role = st.sidebar.text_input("Job Role", value="Software Engineer")
experience = st.sidebar.selectbox(
    "Experience Level",
    ["Fresher", "1-3 years", "3-5 years", "5+ years"]
)
num_questions = st.sidebar.slider("Number of Questions", 3, 10, 5)

# ------------------------------------------------------------
# Header
# ------------------------------------------------------------
st.markdown("""
<div class="main-header">
    <h1>🎯 AI Interview Preparation Coach</h1>
    <p>Practice smarter, get instant AI feedback, and walk into your next interview with confidence.</p>
</div>
""", unsafe_allow_html=True)

if not api_key:
    st.info("👈 Enter your free Gemini API key in the sidebar to get started.")

tab1, tab2, tab3 = st.tabs(["📝 Question Generator", "🎤 Mock Interview", "💡 Tips & Resources"])

# ------------------------------------------------------------
# Helper: call the AI
# ------------------------------------------------------------
def ask_ai(prompt):
    if not model:
        return "⚠️ Please enter your Gemini API key in the sidebar first."
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {e}"


def extract_score(feedback_text):
    """Pull the X/10 score out of the AI's feedback for a visual progress bar."""
    match = re.search(r"Score:?\s*\*{0,2}\s*(\d+)\s*/\s*10", feedback_text)
    if match:
        return int(match.group(1))
    return None

# ------------------------------------------------------------
# Tab 1: Question Generator
# ------------------------------------------------------------
with tab1:
    st.header("Generate Interview Questions")
    st.write(f"Role: **{job_role}**  |  Experience: **{experience}**")

    if st.button("Generate Questions", key="gen_questions", type="primary"):
        with st.spinner("Generating questions..."):
            prompt = (
                f"Generate {num_questions} interview questions for a {experience} "
                f"candidate applying for the role of {job_role}. "
                f"Include a mix of technical and behavioral (HR) questions. "
                f"Format as a numbered list with clear, concise questions only."
            )
            st.session_state["generated_questions"] = ask_ai(prompt)

    if "generated_questions" in st.session_state:
        with st.container(border=True):
            st.markdown(st.session_state["generated_questions"])

# ------------------------------------------------------------
# Tab 2: Mock Interview
# ------------------------------------------------------------
with tab2:
    st.header("Mock Interview Practice")
    st.write("AI will ask you a question. Type your answer below and get instant feedback with a score!")

    if "current_question" not in st.session_state:
        st.session_state["current_question"] = ""
    if "feedback_history" not in st.session_state:
        st.session_state["feedback_history"] = []

    if st.button("🎲 Get New Question"):
        with st.spinner("Thinking of a question..."):
            prompt = (
                f"Ask ONE interview question for a {experience} candidate "
                f"applying for {job_role}. Randomly mix technical and behavioral "
                f"questions. Return ONLY the question text, nothing else."
            )
            st.session_state["current_question"] = ask_ai(prompt)

    if st.session_state["current_question"]:
        with st.container(border=True):
            st.markdown("**🗣️ Question**")
            st.markdown(st.session_state["current_question"])

        user_answer = st.text_area("Your Answer", height=150, key="user_answer")

        if st.button("Submit Answer", type="primary"):
            if user_answer.strip():
                with st.spinner("Evaluating your answer..."):
                    prompt = (
                        f"You are a friendly interview coach. The candidate is applying "
                        f"for {job_role} ({experience}).\n\n"
                        f"Question: {st.session_state['current_question']}\n"
                        f"Candidate's Answer: {user_answer}\n\n"
                        f"Give feedback in this exact format:\n"
                        f"**Score:** X/10\n"
                        f"**Strengths:** ...\n"
                        f"**Areas to Improve:** ...\n"
                        f"**Sample Better Answer:** ..."
                    )
                    feedback = ask_ai(prompt)
                    st.session_state["feedback_history"].insert(0, {
                        "question": st.session_state["current_question"],
                        "answer": user_answer,
                        "feedback": feedback
                    })
            else:
                st.warning("Please type an answer first.")

    if st.session_state["feedback_history"]:
        st.markdown("---")
        st.subheader("📋 Feedback History")
        for i, item in enumerate(st.session_state["feedback_history"]):
            label = item["question"][:60] + ("..." if len(item["question"]) > 60 else "")
            with st.expander(f"Q: {label}", expanded=(i == 0)):
                score = extract_score(item["feedback"])
                if score is not None:
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.metric("Score", f"{score}/10")
                    with col2:
                        st.progress(score / 10)
                st.write(f"**Your Answer:** {item['answer']}")
                st.markdown(item["feedback"])

# ------------------------------------------------------------
# Tab 3: Tips & Resources
# ------------------------------------------------------------
with tab3:
    st.header("Interview Tips & Resources")

    if st.button("Get Personalized Tips", type="primary"):
        with st.spinner("Generating tips..."):
            prompt = (
                f"Give 5 practical interview preparation tips for a {experience} "
                f"candidate applying for {job_role}. Keep each tip to 1-2 sentences "
                f"and format as a numbered list."
            )
            st.session_state["tips"] = ask_ai(prompt)

    if "tips" in st.session_state:
        with st.container(border=True):
            st.markdown(st.session_state["tips"])

    st.markdown("---")
    st.subheader("General Tips")
    with st.container(border=True):
        st.markdown(
            """
- **Research the company** before the interview.
- **Use the STAR method** for behavioral questions (Situation, Task, Action, Result).
- **Prepare 2-3 questions** to ask the interviewer.
- **Test your tech setup** in advance for virtual interviews.
- **Send a thank-you note** after the interview.
            """
  )
