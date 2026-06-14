🎯 AI Interview Preparation Coach
An AI-powered web app built with Python + Streamlit + Google Gemini API to help job
seekers practice for interviews.
What This App Does
📝 Question Generator – Enter a job role and experience level, and the AI generates
a custom set of technical + behavioral interview questions.
🎤 Mock Interview – The AI asks you a random interview question. Type your answer
and get instant feedback: a score out of 10, strengths, areas to improve, and a sample
better answer.
💡 Tips & Resources – Get AI-generated, role-specific interview tips plus general
best-practice advice (STAR method, follow-up emails, etc.).
Which AI Is Used
This app uses Google Gemini (gemini-2.0-flash) via the google-generativeai
Python library. Gemini was chosen because Google AI Studio offers a free API key
that's easy for students to get.
How to Run It Locally
Clone the repo
Bash
Install dependencies
Bash
Get a free Gemini API key
Go to https://aistudio.google.com/app/apikey
Sign in with your Google account and click "Create API Key"
Run the app
Bash
Then enter your API key in the sidebar of the app.
How to Deploy (Streamlit Cloud)
Push this project to a public GitHub repo.
Go to https://share.streamlit.io and sign in with GitHub.
Click "New app", select your repo and app.py as the main file.
(Optional) In App Settings → Secrets, add:
Toml
This lets the app work without users entering their own key.
Click Deploy — your app will get a live URL.
Project Structure
Code
Notes
Built as a mini project for OnlyAI Academy – Generative AI Fundamentals assignment.
Designed to be simple, functional, and beginner-friendly per the assignment guidelines.
