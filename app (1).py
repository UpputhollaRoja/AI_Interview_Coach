import streamlit as st
from groq import Groq
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
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem; border-radius: 16px; color: white;
        margin-bottom: 2rem; text-align: center;
    }
    .main-header h1 { font-size: 2.2rem; font-weight: 700; margin: 0; }
    .main-header p { font-size: 1rem; opacity: 0.85; margin-top: 0.5rem; }
    .stat-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 12px; padding: 1.2rem; text-align: center;
        border-left: 4px solid #667eea;
    }
    .stat-number { font-size: 2rem; font-weight: 700; color: #667eea; }
    .stat-label { font-size: 0.85rem; color: #555; margin-top: 0.2rem; }
    .question-card {
        background: #f8f9ff; border: 1px solid #e0e4ff;
        border-radius: 12px; padding: 1.5rem; margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    .tip-card {
        background: #fff9f0; border: 1px solid #ffe4b0;
        border-radius: 10px; padding: 1rem 1.2rem; margin: 0.5rem 0;
        border-left: 4px solid #f6a623;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; border: none; border-radius: 8px;
        padding: 0.5rem 1.5rem; font-weight: 600;
    }
    .stButton > button:hover { opacity: 0.9; color: white; }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Session State Init
# ------------------------------------------------------------
defaults = {
    "api_key": "", "generated_questions": "", "current_question": "",
    "feedback_history": [], "tips": "", "scores": [],
    "resume_feedback": "", "company_questions": "",
    "flashcards": [], "flashcard_index": 0, "show_flashcard_answer": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🎯 Interview Coach")

    # Auto-load from Streamlit Secrets if available
    if not st.session_state["api_key"]:
        try:
            st.session_state["api_key"] = st.secrets["GROQ_API_KEY"]
        except Exception:
            pass

    api_key_input = st.text_input("🔑 Groq API Key", type="password",
        value=st.session_state["api_key"],
        help="Get free key at https://console.groq.com/keys")
    if api_key_input:
        st.session_state["api_key"] = api_key_input
    if st.session_state["api_key"]:
        st.success("✅ API Key set!")
    else:
        st.warning("⚠️ Enter your API key above")

    st.markdown("---")
    st.markdown("### ⚙️ Job Settings")
    job_role = st.text_input("💼 Job Role", value="Software Engineer")
    experience = st.selectbox("📊 Experience Level",
        ["Fresher", "1-3 years", "3-5 years", "5+ years"])
    industry = st.selectbox("🏢 Industry",
        ["Technology", "Finance", "Healthcare", "Marketing", "Education", "Data Science", "Other"])
    num_questions = st.slider("❓ Number of Questions", 3, 15, 5)

    st.markdown("---")
    st.markdown("### 📊 Your Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div class="stat-card">
            <div class="stat-number">{len(st.session_state['feedback_history'])}</div>
            <div class="stat-label">Answered</div></div>""", unsafe_allow_html=True)
    with col2:
        avg = round(sum(st.session_state['scores'])/len(st.session_state['scores']),1) if st.session_state['scores'] else 0
        st.markdown(f"""<div class="stat-card">
            <div class="stat-number">{avg}</div>
            <div class="stat-label">Avg Score</div></div>""", unsafe_allow_html=True)

    if st.button("🗑️ Clear History"):
        st.session_state["feedback_history"] = []
        st.session_state["scores"] = []
        st.rerun()

# ------------------------------------------------------------
# Header
# ------------------------------------------------------------
st.markdown(f"""<div class="main-header">
    <h1>🎯 AI Interview Preparation Coach</h1>
    <p>Powered by Claude AI • Role: <b>{job_role}</b> • Level: <b>{experience}</b> • Industry: <b>{industry}</b></p>
</div>""", unsafe_allow_html=True)

if not st.session_state["api_key"]:
    st.error("👈 Please enter your Groq API key in the sidebar to get started.")
    st.stop()

# ------------------------------------------------------------
# Helper
# ------------------------------------------------------------
def ask_ai(prompt, system_prompt="You are an expert interview coach.", max_tokens=1500):
    try:
        client = Groq(api_key=st.session_state["api_key"])
        message = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return message.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {e}"

def extract_score(text):
    import re
    match = re.search(r'\*\*Score:\*\*\s*(\d+(?:\.\d+)?)/10', text)
    return float(match.group(1)) if match else None

# ------------------------------------------------------------
# Tabs
# ------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📝 Questions", "🎤 Mock Interview", "📄 Resume Review",
    "🏢 Company Prep", "🃏 Flashcards", "💡 Tips"
])

# ============================================================
# TAB 1: Question Generator
# ============================================================
with tab1:
    st.header("📝 Interview Question Generator")
    col1, col2 = st.columns([2, 1])
    with col1:
        question_type = st.multiselect("Question Types",
            ["Technical", "Behavioral (HR)", "Situational", "Problem Solving", "Culture Fit"],
            default=["Technical", "Behavioral (HR)"])
        difficulty = st.select_slider("Difficulty", options=["Easy", "Medium", "Hard", "Mixed"], value="Mixed")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        include_answers = st.checkbox("Include Sample Answers")
        include_tips = st.checkbox("Include Tips per Question")

    if st.button("🚀 Generate Questions", key="gen_questions"):
        with st.spinner("Generating personalized questions..."):
            types_str = ", ".join(question_type) if question_type else "mixed"
            ans = "After each question, provide a brief sample answer." if include_answers else ""
            tips = "After each question, add a 1-line tip." if include_tips else ""
            prompt = f"""Generate {num_questions} interview questions for a {experience} candidate applying for {job_role} in {industry}.
Types: {types_str} | Difficulty: {difficulty}
{ans} {tips}
Format as a numbered list. Be specific and realistic."""
            st.session_state["generated_questions"] = ask_ai(prompt)

    if st.session_state["generated_questions"]:
        st.markdown("---")
        st.markdown(st.session_state["generated_questions"])
        st.download_button("⬇️ Download Questions",
            data=st.session_state["generated_questions"],
            file_name=f"questions_{job_role.replace(' ','_')}.txt", mime="text/plain")

# ============================================================
# TAB 2: Mock Interview
# ============================================================
with tab2:
    st.header("🎤 Mock Interview Practice")
    st.write("Get a question → Type your answer → Get instant AI feedback with score!")

    col1, col2 = st.columns(2)
    with col1:
        mock_type = st.selectbox("Question Category",
            ["Random Mix", "Technical Only", "Behavioral Only", "Situational", "Stress Questions"])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        timer_enabled = st.checkbox("⏱️ Enable 2-min Answer Timer")

    if st.button("🎲 Get New Question"):
        with st.spinner("Preparing question..."):
            prompt = f"Generate ONE {mock_type} interview question for a {experience} {job_role} in {industry}. Return ONLY the question text."
            st.session_state["current_question"] = ask_ai(prompt, max_tokens=200)
            st.session_state["show_flashcard_answer"] = False

    if st.session_state["current_question"]:
        st.markdown(f"""<div class="question-card">
            <b>🎯 Your Question:</b><br><br>{st.session_state["current_question"]}
        </div>""", unsafe_allow_html=True)

        if timer_enabled:
            st.info("⏱️ You have 2 minutes to answer!")

        user_answer = st.text_area("✍️ Your Answer", height=180,
            placeholder="Type your answer here. Use the STAR method for behavioral questions...",
            key="mock_answer")

        col1, col2 = st.columns(2)
        with col1:
            submit = st.button("✅ Submit & Get Feedback")
        with col2:
            hint_btn = st.button("💡 Get a Hint")

        if hint_btn:
            with st.spinner("Getting hint..."):
                h = ask_ai(f"Give a 2-sentence hint for answering: {st.session_state['current_question']}", max_tokens=150)
                st.info(f"💡 **Hint:** {h}")

        if submit:
            if user_answer.strip():
                with st.spinner("Evaluating your answer..."):
                    prompt = f"""You are a strict but encouraging interview coach for a {experience} {job_role} candidate.

Question: {st.session_state['current_question']}
Candidate's Answer: {user_answer}

Give feedback in EXACTLY this format:
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
                        "answer": user_answer, "feedback": feedback,
                        "score": score, "time": datetime.now().strftime("%b %d, %H:%M")
                    })
                st.success("✅ Feedback ready!")
                st.markdown(feedback)
            else:
                st.warning("Please type your answer before submitting.")

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
    st.write("Paste your resume and get AI feedback tailored to your target role.")

    resume_text = st.text_area("📋 Paste Your Resume Here", height=300,
        placeholder="Paste your resume content here (education, experience, skills, projects...)")

    focus_areas = st.multiselect("Focus Areas",
        ["Overall Impression", "Skills Match", "Experience Relevance",
         "Keywords & ATS", "Achievements", "Gaps & Red Flags", "Formatting Suggestions"],
        default=["Overall Impression", "Skills Match", "Keywords & ATS"])

    if st.button("🔍 Analyze Resume"):
        if resume_text.strip():
            with st.spinner("Analyzing your resume..."):
                prompt = f"""You are an expert HR consultant and ATS specialist. Analyze this resume for a {experience} {job_role} in {industry}.

Resume:
{resume_text}

Focus on: {', '.join(focus_areas)}

Give detailed, actionable feedback with an overall score out of 10."""
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

    col1, col2 = st.columns(2)
    with col1:
        company_name = st.text_input("🏢 Company Name", placeholder="e.g., Google, TCS, Infosys, Wipro")
    with col2:
        interview_round = st.selectbox("Interview Round",
            ["All Rounds", "HR / Screening", "Technical Round 1",
             "Technical Round 2", "Managerial Round", "Final Round"])

    prep_type = st.multiselect("What to Prepare",
        ["Likely Interview Questions", "Company Culture Tips",
         "Technical Topics to Study", "Questions to Ask Interviewer"],
        default=["Likely Interview Questions", "Technical Topics to Study"])

    if st.button("🔎 Generate Company Prep"):
        if company_name.strip():
            with st.spinner(f"Researching {company_name} interview patterns..."):
                prompt = f"""Act as an interview prep expert with knowledge of {company_name}'s hiring process.

Prepare a {experience} {job_role} candidate for {interview_round} at {company_name} in {industry}.
Cover: {', '.join(prep_type)}

Be specific to {company_name}'s known interview style, culture, and common questions."""
                st.session_state["company_questions"] = ask_ai(prompt, max_tokens=1500)
        else:
            st.warning("Please enter a company name.")

    if st.session_state["company_questions"]:
        st.markdown("---")
        st.markdown(st.session_state["company_questions"])
        if company_name:
            st.download_button("⬇️ Download Prep Guide",
                data=st.session_state["company_questions"],
                file_name=f"{company_name}_prep_guide.txt", mime="text/plain")

# ============================================================
# TAB 5: Flashcards
# ============================================================
with tab5:
    st.header("🃏 Interview Flashcards")
    st.write("Quick-fire Q&A cards to sharpen your knowledge before the interview.")

    flashcard_topic = st.selectbox("Topic", [
        "Data Structures & Algorithms", "System Design", "OOP Concepts",
        "SQL & Databases", "Python Basics", "JavaScript Basics",
        "HR / Behavioral Questions", "Problem Solving Frameworks", f"{job_role} Specific"
    ])
    num_cards = st.slider("Number of Flashcards", 5, 20, 10)

    if st.button("🎴 Generate Flashcards"):
        with st.spinner("Creating flashcards..."):
            prompt = f"""Create {num_cards} interview flashcards on: {flashcard_topic} for a {experience} {job_role}.

Return ONLY a valid JSON array, no other text:
[{{"question": "...", "answer": "..."}}, ...]"""
            raw = ask_ai(prompt, max_tokens=2000)
            try:
                raw = raw.strip()
                if "```" in raw:
                    raw = raw.split("```")[1]
                    if raw.startswith("json"):
                        raw = raw[4:]
                cards = json.loads(raw)
                st.session_state["flashcards"] = cards
                st.session_state["flashcard_index"] = 0
                st.session_state["show_flashcard_answer"] = False
                st.success(f"✅ {len(cards)} flashcards created!")
            except:
                st.error("Could not parse flashcards. Please try again.")

    if st.session_state["flashcards"]:
        cards = st.session_state["flashcards"]
        idx = st.session_state["flashcard_index"]
        card = cards[idx]

        st.markdown(f"**Card {idx+1} of {len(cards)}**")
        st.progress((idx+1)/len(cards))

        st.markdown(f"""<div class="question-card">
            <b>❓ Question:</b><br><br>{card['question']}
        </div>""", unsafe_allow_html=True)

        if st.session_state["show_flashcard_answer"]:
            st.markdown(f"""<div class="tip-card">
                <b>✅ Answer:</b><br><br>{card['answer']}
            </div>""", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("👁️ Show Answer"):
                st.session_state["show_flashcard_answer"] = True
                st.rerun()
        with col2:
            if st.button("⬅️ Previous") and idx > 0:
                st.session_state["flashcard_index"] -= 1
                st.session_state["show_flashcard_answer"] = False
                st.rerun()
        with col3:
            if st.button("➡️ Next") and idx < len(cards)-1:
                st.session_state["flashcard_index"] += 1
                st.session_state["show_flashcard_answer"] = False
                st.rerun()
        with col4:
            if st.button("🔀 Random"):
                import random
                st.session_state["flashcard_index"] = random.randint(0, len(cards)-1)
                st.session_state["show_flashcard_answer"] = False
                st.rerun()

# ============================================================
# TAB 6: Tips & Resources
# ============================================================
with tab6:
    st.header("💡 Tips & Resources")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎯 Get Personalized Tips"):
            with st.spinner("Generating tips..."):
                prompt = f"Give 7 practical interview tips for a {experience} {job_role} in {industry}. Numbered list, 2-3 sentences each. Be specific."
                st.session_state["tips"] = ask_ai(prompt, max_tokens=1000)
    with col2:
        if st.button("📅 30-Day Study Plan"):
            with st.spinner("Creating your study plan..."):
                prompt = f"Create a 30-day interview preparation plan for a {experience} {job_role} in {industry}. 4 weekly themes with daily tasks. Be specific."
                st.session_state["tips"] = ask_ai(prompt, max_tokens=1500)

    if st.session_state["tips"]:
        st.markdown("---")
        st.markdown(st.session_state["tips"])

    st.markdown("---")
    st.subheader("📚 General Interview Tips")
    for title, tip in [
        ("🔍 Research the Company", "Study mission, products, recent news, and culture before the interview."),
        ("⭐ STAR Method", "Situation → Task → Action → Result. Always quantify your results with numbers."),
        ("❓ Ask Smart Questions", "Prepare 3-4 thoughtful questions to ask the interviewer."),
        ("💻 Test Your Tech", "Test camera, mic, and internet 30 mins before virtual interviews."),
        ("📧 Follow Up", "Send a thank-you email within 24 hours after the interview."),
        ("🧠 Practice Aloud", "Record yourself answering — it exposes filler words and awkward pauses."),
        ("📊 Quantify Impact", "Say Improved performance by 30 percent instead of just improved performance."),
    ]:
        st.markdown(f"""<div class="tip-card"><b>{title}</b><br>{tip}</div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🔗 Useful Resources")
    for name, url in {
        "LeetCode (Coding Practice)": "https://leetcode.com",
        "GeeksForGeeks": "https://geeksforgeeks.org",
        "Glassdoor (Company Reviews & Questions)": "https://glassdoor.com",
        "System Design Primer (GitHub)": "https://github.com/donnemartin/system-design-primer",
        "Groq Console (Your Free API)": "https://console.groq.com",
    }.items():
        st.markdown(f"• [{name}]({url})")
