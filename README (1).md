# 🎯 AI Interview Preparation Coach

An AI-powered web application designed to help job seekers and students prepare confidently for technical and behavioral interviews — combining question generation, mock interview practice, resume analysis, and personalized study planning into a single platform.

---

## 📖 Overview

Most candidates struggle to find realistic, personalized interview practice in one place. The **AI Interview Preparation Coach** solves this by using a large language model to generate tailored content based on a user's job role, experience level, and target industry — making interview preparation more focused, interactive, and effective.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📝 **Question Generator** | Generates custom interview questions filtered by type (technical, behavioral, situational) and difficulty. |
| 🎤 **Mock Interview** | Simulates a real interview, evaluates typed answers, and provides a score out of 10 with detailed feedback. |
| 📄 **Resume Review** | Analyzes pasted resume text and provides ATS-friendly, role-specific improvement suggestions. |
| 🏢 **Company Prep** | Produces company-specific interview questions and culture insights. |
| 🃏 **Flashcards** | Generates quick-revision flashcards on technical topics such as Data Structures, SQL, and System Design. |
| 💡 **Tips & Study Plan** | Provides personalized interview tips and a structured 30-day preparation plan. |

---

## 🤖 AI Model

This application uses **Meta's Llama 3.3 70B** model, served through **Groq's API**. Llama 3.3 was selected for its strong contextual reasoning and response quality, while Groq provides free, low-latency inference — making real-time interview feedback fast and accessible without licensing costs.

---

## 🛠️ Tech Stack

- **Language & Framework:** Python, Streamlit
- **AI Model:** Llama 3.3 70B (via Groq API)
- **Deployment:** Streamlit Community Cloud
- **Version Control:** Git & GitHub

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- A free Groq API key — available at [console.groq.com](https://console.groq.com/keys)

### Installation

```bash
git clone https://github.com/UpputhollaRoja/AI_Interview_Coach.git
cd AI_Interview_Coach
pip install -r requirements.txt
streamlit run app.py
```

Once the app launches in your browser, enter your Groq API key in the sidebar to begin.

---

## 📂 Project Structure

```
AI_Interview_Coach/
├── app.py              # Main application logic
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

---

## 👤 Author

**Upputholla Roja**
B.Tech CSE (Artificial Intelligence), MITS Madanapalle (2024–2028)

---

## 📄 License

This project is open-source and available for educational use.
