import streamlit as st
import anthropic
import json
import time
from datetime import datetime

# ------------------------------------------------------------
# Page Config
# ------------------------------------------------------------
st.set_page_config(
    page_title="AI Interview Prep Coach",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------
# Custom CSS
# ------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }

    .main-header h1 {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
    }

    .main-header p {
        font-size: 1rem;
        opacity: 0.85;
        margin-top: 0.5rem;
    }

    .stat-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        border-left: 4px solid #667eea;
    }

    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }

    .stat-label {
        font-size: 0.85rem;
        color: #555;
        margin-top: 0.2rem;
    }

    .question-card {
        background: #f8f9ff;
        border: 1px solid #e0e4ff;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }

    .score-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 1.1rem;
    }

    .tip-card {
        background: #fff9f0;
        border: 1px solid #ffe4b0;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
        border-left: 4px solid #f6a623;
    }

    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: opacity 0.2s;
    }

    .stButton > button:hover {
        opacity: 0.9;
        color: white;
    }

    .sidebar-info {
        background: #f0f2ff;
        border-radius: 10px;
        padding: 1rem;
        margin-top: 1rem;
        font-size: 0.85rem;
        color: #444;
    }

    .history-item {
        background: white;
        border: 1px solid #e8ecff;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }

    .tag {
        display: inline-block;
        background: #e8ecff;
        color: #667eea;
        padding: 0.2rem 0.7rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 500;
        margin: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Session State Init
# ------------------------------------------------------------
defaults = {
    "api_key": "",
    "generated_questions": "",
    "current_question": "",
    "feedback_history": [],
    "tips": "",
    "total_sessions": 0,
    "avg_score": 0,
    "scores": [],
    "resume_feedback": "",
    "company_questions": "",
    "flashcards": [],
    "flashcard_index": 0,
    "show_flashcard_answer": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🎯 Interview Coach")

    # API Key
    api_key_input = st.text_input(
        "🔑 Anthropic API Key",
        type="password",
        value=st.session_state["api_key"],
        help="Get your free key at https://console.anthropic.com/"
    )
    if api_key_input:
        st.session_state["api_key"] = api_key_input

    if st.session_state["api_key"]:
        st.success("✅ API Key set!")
    else:
        st.warning("⚠️ Enter your API key above")
        st.markdown("[Get free key →](https://console.anthropic.com/)", unsafe_allow_html=False)

    st.markdown("---")

    # Job Settings
    st.markdown("### ⚙️ Job Settings")
    job_role = st.text_input("💼 Job Role", value="Software Engineer")
    experience = st.selectbox(
        "📊 Experience Level",
        ["Fresher", "1-3 years", "3-5 years", "5+ years"]
    )
    industry = st.selectbox(
        "🏢 Industry",
        ["Technology", "Finance", "Healthcare", "Marketing", "Education", "Data Science", "Other"]
    )
    num_questions = st.slider("❓ Number of Questions", 3, 15, 5)

    st.markdown("---")

    # Stats
    st.markdown("### 📊 Your Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{len(st.session_state['feedback_history'])}</div>
            <div class="stat-label">Answered</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        avg = round(sum(st.session_state['scores']) / len(st.session_state['scores']), 1) if st.session_state['scores'] else 0
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{avg}</div>
            <div class="stat-label">Avg Score</div>
        </div>""", unsafe_allow_html=True)

    if st.button("🗑️ Clear History"):
        st.session_state["feedback_history"] = []
        st.session_state["scores"] = []
        st.rerun()

# ------------------------------------------------------------
# Header
# ------------------------------------------------------------
st.markdown(f"""
<div class="main-header">
    <h1>🎯 AI Interview Preparation Coach</h1>
    <p>Powered by Claude AI • Role: <b>{job_role}</b> • Level: <b>{experience}</b> • Industry: <b>{industry}</b></p>
</div>
""", unsafe_allow_html=True)

if not st.session_state["api_key"]:
    st.error("👈 Please enter your Anthropic API key in the sidebar to get started.")
    st.stop()

# ------------------------------------------------------------
# Helper: Call Claude API
# ------------------------------------------------------------
def ask_ai(prompt, system_prompt="You are an expert interview coach.", max_tokens=1500):
    try:
        client = anthropic.Anthropic(api_key=st.session_state["api_key"])
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    except Exception as e:
        return f"⚠️ Error: {e}"

def extract_score(feedback_text):
    """Extract numeric score from feedback"""
    import re
    match = re.search(r'\*\*Score:\*\*\s*(\d+(?:\.\d+)?)/10', feedback_text)
    if match:
        return float(match.group(1))
    return None

# ------------------------------------------------------------
# Tabs
# ------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📝 Questions",
    "🎤 Mock Interview",
    "📄 Resume Review",
    "🏢 Company Prep",
    "🃏 Flashcards",
    "💡 Tips"
])

# ============================================================
# TAB 1: Question Generator
# ============================================================
with tab1:
    st.header("📝 Interview Question Generator")

    col1, col2 = st.columns([2, 1])
    with col1:
        question_type = st.multiselect(
            "Question Types",
            ["Technical", "Behavioral (HR)", "Situational", "Problem Solving", "Culture Fit"],
            default=["Technical", "Behavioral (HR)"]
        )
        difficulty = st.select_slider(
            "Difficulty Level",
            options=["Easy", "Medium", "Hard", "Mixed"],
            value="Mixed"
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        include_answers = st.checkbox("Include Sample Answers", value=False)
        include_tips = st.checkbox("Include Tips per Question", value=False)

    if st.button("🚀 Generate Questions", key="gen_questions"):
        with st.spinner("Generating personalized questions..."):
            types_str = ", ".join(question_type) if question_type else "mixed"
            answers_instruction = "After each question, provide a brief sample answer." if include_answers else ""
            tips_instruction = "After each question (and answer if included), add a 1-line tip." if include_tips else ""

            prompt = f"""Generate {num_questions} interview questions for a {experience} candidate applying for {job_role} in the {industry} industry.

Question types to include: {types_str}
Difficulty: {difficulty}

{answers_instruction}
{tips_instruction}

Format as a clean numbered list. Be specific and realistic."""

            st.session_state["generated_questions"] = ask_ai(prompt)

    if st.session_state["generated_questions"]:
        st.markdown("---")
        st.markdown(st.session_state["generated_questions"])

        # Download button
        st.download_button(
            "⬇️ Download Questions",
            data=st.session_state["generated_questions"],
            file_name=f"interview_questions_{job_role.replace(' ','_')}.txt",
            mime="text/plain"
        )

# ============================================================
# TAB 2: Mock Interview
# ============================================================
with tab2:
    st.header("🎤 Mock Interview Practice")
    st.write("Get a question, type your answer, and receive instant AI feedback with a score!")

    col1, col2 = st.columns(2)
    with col1:
        mock_type = st.selectbox("Question Category", [
            "Random Mix", "Technical Only", "Behavioral Only",
            "Situational", "Stress Questions"
        ])
    with col2:
        timer_enabled = st.checkbox("⏱️ Enable 2-min Answer Timer", value=False)

    if st.button("🎲 Get New Question"):
        with st.spinner("Preparing your question..."):
            prompt = f"""Generate ONE {mock_type} interview question for a {experience} {job_role} in {industry}.
Return ONLY the question text, nothing else. Make it realistic and challenging."""
            st.session_state["current_question"] = ask_ai(prompt, max_tokens=200)
            st.session_state["show_flashcard_answer"] = False

    if st.session_state["current_question"]:
        st.markdown(f"""
        <div class="question-card">
            <b>🎯 Your Question:</b><br><br>
            {st.session_state["current_question"]}
        </div>
        """, unsafe_allow_html=True)

        if timer_enabled:
            st.info("⏱️ You have 2 minutes to answer!")

        user_answer = st.text_area(
            "✍️ Your Answer",
            height=180,
            placeholder="Type your answer here. Be specific with examples using the STAR method for behavioral questions...",
            key="mock_answer"
        )

        col1, col2 = st.columns(2)
        with col1:
            submit = st.button("✅ Submit & Get Feedback")
        with col2:
            hint = st.button("💡 Get a Hint")

        if hint:
            with st.spinner("Getting hint..."):
                h = ask_ai(
                    f"Give a 2-sentence hint for answering this interview question: {st.session_state['current_question']}",
                    max_tokens=150
                )
                st.info(f"💡 **Hint:** {h}")

        if submit:
            if user_answer.strip():
                with st.spinner("Evaluating your answer..."):
                    prompt = f"""You are a strict but encouraging interview coach evaluating a {experience} {job_role} candidate.

Question: {st.session_state['current_question']}
Candidate's Answer: {user_answer}

Provide detailed feedback in EXACTLY this format:
**Score:** X/10
**Strengths:** [what they did well]
**Areas to Improve:** [specific improvements]
**Sample Better Answer:** [a model answer]
**Key Takeaway:** [one sentence advice]"""

                    feedback = ask_ai(prompt, max_tokens=800)
                    score = extract_score(feedback)
                    if score:
                        st.session_state["scores"].append(score)

                    st.session_state["feedback_history"].insert(0, {
                        "question": st.session_state["current_question"],
                        "answer": user_answer,
                        "feedback": feedback,
                        "score": score,
                        "time": datetime.now().strftime("%b %d, %H:%M"),
                        "role": job_role,
                        "type": mock_type
                    })

                st.success("✅ Feedback ready!")
                st.markdown(feedback)
            else:
                st.warning("Please type your answer before submitting.")

    # Feedback History
    if st.session_state["feedback_history"]:
        st.markdown("---")
        st.subheader("📋 Practice History")
        for i, item in enumerate(st.session_state["feedback_history"]):
            score_display = f"⭐ {item['score']}/10" if item.get('score') else ""
            label = item["question"][:55] + "..." if len(item["question"]) > 55 else item["question"]
            with st.expander(f"{score_display} Q{len(st.session_state['feedback_history'])-i}: {label} • {item.get('time','')}"):
                st.markdown(f"**Your Answer:** {item['answer']}")
                st.markdown("---")
                st.markdown(item["feedback"])

# ============================================================
# TAB 3: Resume Review
# ============================================================
with tab3:
    st.header("📄 Resume / CV Feedback")
    st.write("Paste your resume text and get AI-powered feedback tailored to your target role.")

    resume_text = st.text_area(
        "📋 Paste Your Resume Here",
        height=300,
        placeholder="Paste your resume content here (education, experience, skills, projects...)"
    )

    focus_areas = st.multiselect(
        "Focus Areas",
        ["Overall Impression", "Skills Match", "Experience Relevance",
         "Keywords & ATS", "Achievements", "Gaps & Red Flags", "Formatting Suggestions"],
        default=["Overall Impression", "Skills Match", "Keywords & ATS"]
    )

    if st.button("🔍 Analyze Resume"):
        if resume_text.strip():
            with st.spinner("Analyzing your resume..."):
                focus_str = ", ".join(focus_areas)
                prompt = f"""You are an expert HR consultant and ATS specialist. Analyze this resume for a {experience} {job_role} position in {industry}.

Resume:
{resume_text}

Provide detailed feedback focusing on: {focus_str}

Format your response with clear sections and actionable advice. Give an overall score out of 10."""

                st.session_state["resume_feedback"] = ask_ai(prompt, max_tokens=1500)
        else:
            st.warning("Please paste your resume content first.")

    if st.session_state["resume_feedback"]:
        st.markdown("---")
        st.markdown(st.session_state["resume_feedback"])

# ============================================================
# TAB 4: Company Prep
# ============================================================
with tab4:
    st.header("🏢 Company-Specific Preparation")
    st.write("Get tailored questions and insights for a specific company.")

    col1, col2 = st.columns(2)
    with col1:
        company_name = st.text_input("🏢 Company Name", placeholder="e.g., Google, TCS, Infosys")
    with col2:
        interview_round = st.selectbox("Interview Round", [
            "All Rounds", "HR / Screening", "Technical Round 1",
            "Technical Round 2", "Managerial Round", "Final Round"
        ])

    prep_type = st.multiselect(
        "What to Prepare",
        ["Likely Interview Questions", "Company Culture Tips",
         "Technical Topics to Study", "Questions to Ask Interviewer"],
        default=["Likely Interview Questions", "Technical Topics to Study"]
    )

    if st.button("🔎 Generate Company Prep"):
        if company_name.strip():
            with st.spinner(f"Researching {company_name} interview patterns..."):
                prep_str = ", ".join(prep_type)
                prompt = f"""Act as an interview preparation expert with knowledge of {company_name}'s hiring process.

Prepare a {experience} candidate for a {job_role} role ({interview_round}) at {company_name} in {industry}.

Cover these areas: {prep_str}

Be specific to {company_name}'s known interview style, values, and common question patterns. Format clearly with sections."""

                st.session_state["company_questions"] = ask_ai(prompt, max_tokens=1500)
        else:
            st.warning("Please enter a company name.")

    if st.session_state["company_questions"]:
        st.markdown("---")
        st.markdown(st.session_state["company_questions"])

        st.download_button(
            "⬇️ Download Prep Guide",
            data=st.session_state["company_questions"],
            file_name=f"{company_name}_prep_guide.txt",
            mime="text/plain"
        )

# ============================================================
# TAB 5: Flashcards
# ============================================================
with tab5:
    st.header("🃏 Interview Flashcards")
    st.write("Quick-fire Q&A cards to sharpen your knowledge.")

    flashcard_topic = st.selectbox("Topic", [
        "Data Structures & Algorithms", "System Design", "OOP Concepts",
        "SQL & Databases", "Python Basics", "JavaScript Basics",
        "HR / Behavioral Questions", "Problem Solving Frameworks", f"{job_role} Specific"
    ])

    num_cards = st.slider("Number of Flashcards", 5, 20, 10)

    if st.button("🎴 Generate Flashcards"):
        with st.spinner("Creating flashcards..."):
            prompt = f"""Create {num_cards} interview flashcards on the topic: {flashcard_topic} for a {experience} {job_role}.

Return ONLY a valid JSON array like this:
[
  {{"question": "What is X?", "answer": "X is ..."}},
  {{"question": "Explain Y", "answer": "Y means ..."}}
]

No extra text, no markdown, just raw JSON."""

            raw = ask_ai(prompt, max_tokens=2000)
            try:
                # Clean up response
                raw = raw.strip()
                if raw.startswith("```"):
                    raw = raw.split("```")[1]
                    if raw.startswith("json"):
                        raw = raw[4:]
                cards = json.loads(raw)
                st.session_state["flashcards"] = cards
                st.session_state["flashcard_index"] = 0
                st.session_state["show_flashcard_answer"] = False
            except:
                st.error("Could not parse flashcards. Please try again.")

    if st.session_state["flashcards"]:
        cards = st.session_state["flashcards"]
        idx = st.session_state["flashcard_index"]
        card = cards[idx]

        st.markdown(f"**Card {idx+1} of {len(cards)}**")
        st.progress((idx+1)/len(cards))

        st.markdown(f"""
        <div class="question-card">
            <b>❓ Question:</b><br><br>
            {card['question']}
        </div>
        """, unsafe_allow_html=True)

        if st.session_state["show_flashcard_answer"]:
            st.markdown(f"""
            <div class="tip-card">
                <b>✅ Answer:</b><br><br>
                {card['answer']}
            </div>
            """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
      
