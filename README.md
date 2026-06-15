# AI Interview Preparation Coach

## Overview

**AI Interview Preparation Coach** is a comprehensive, AI-powered web application designed to assist job seekers in preparing for technical and behavioral interviews. Built with Python, Streamlit, and Google Gemini API, the platform provides personalized question generation, real-time mock interviews with AI feedback, and role-specific preparation resources.

## Features

### 📝 Question Generator
- Generate customized interview questions based on job role and experience level
- Mixed question sets combining technical and behavioral (HR) components
- Configurable question count (3-10 questions)
- Support for multiple experience levels: Fresher, 1-3 years, 3-5 years, 5+ years

### 🎤 Mock Interview Practice
- Interactive mock interview simulation with AI-driven questioning
- Real-time answer evaluation with scoring (0-10)
- Comprehensive feedback including:
  - Performance score with visual progress indicator
  - Identified strengths
  - Areas for improvement
  - Sample responses for reference
- Persistent feedback history for performance tracking

### 💡 Interview Tips & Resources
- AI-generated, role-specific interview preparation tips
- Best practice guidance (STAR method, follow-up strategies)
- General interview preparation resources
- Actionable insights tailored to candidate profile

## Technology Stack

| Component | Technology |
|-----------|-----------|
| **Frontend Framework** | Streamlit |
| **AI Model** | Google Gemini 2.5 Flash |
| **Language** | Python 3.x |
| **API Library** | google-generativeai |
| **Deployment** | Streamlit Cloud / Self-hosted |

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Google account (for API key generation)

### Local Development

1. **Clone the Repository**
   ```bash
   git clone https://github.com/UpputhollaRoja/AI_Interview_Coach.git
   cd AI_Interview_Coach
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Obtain Gemini API Key**
   - Navigate to [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy the generated key

5. **Run Application**
   ```bash
   streamlit run app.py
   ```
   - The application will open at `http://localhost:8501`
   - Enter your Gemini API key in the sidebar to begin

## Deployment

### Streamlit Cloud Deployment

1. **Push to Public GitHub Repository**
   ```bash
   git push origin main
   ```

2. **Deploy via Streamlit Cloud**
   - Visit [Streamlit Cloud](https://share.streamlit.io)
   - Sign in with GitHub credentials
   - Click "New app"
   - Select repository and `app.py` as the main file

3. **Configure Secrets (Optional)**
   - In **App Settings → Secrets**, add:
     ```toml
     GEMINI_API_KEY = "your-api-key-here"
     ```
   - This enables deployment without requiring users to provide their own API key

4. **Deploy**
   - Click Deploy and receive a live URL

## Project Structure

```
AI_Interview_Coach/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── config-2.toml              # Streamlit theme configuration
├── secrets.toml-1.example     # Secrets template
├── -1.gitignore              # Git ignore rules
└── README.md                  # This file
```

## Configuration

### Theme Customization (`config-2.toml`)
- **Primary Color**: `#6C63FF` (Purple)
- **Background**: White (`#FFFFFF`)
- **Secondary Background**: Light Purple (`#F0F2FF`)
- **Text Color**: Dark Gray (`#262730`)
- **Font**: Sans serif

### Application Settings (Sidebar)
- **Job Role**: Customize target position (default: Software Engineer)
- **Experience Level**: Select from predefined levels
- **Question Count**: Adjust quantity (3-10 questions)

## Usage Guide

### Step 1: Configure Your Profile
1. Enter your Gemini API key in the sidebar
2. Specify your target job role
3. Select your experience level
4. Adjust the number of questions as needed

### Step 2: Generate Questions
- Navigate to "📝 Question Generator" tab
- Click "Generate Questions" button
- Review the AI-generated question set
- Use as preparation material or practice prompts

### Step 3: Practice with Mock Interview
- Go to "🎤 Mock Interview Practice" tab
- Click "🎲 Get New Question" to receive a question
- Formulate and submit your response
- Review instant AI feedback and score
- Repeat for comprehensive practice

### Step 4: Review Resources
- Access "💡 Tips & Resources" tab
- Generate personalized tips for your profile
- Reference general best practices
- Bookmark valuable insights

## API Integration

The application leverages the **Google Generative AI API** with the **Gemini 2.5 Flash** model for:
- High-performance text generation
- Context-aware question creation
- Intelligent answer evaluation
- Detailed feedback synthesis

### API Key Management
- **Local Development**: Entered via UI sidebar
- **Deployed Application**: Can be stored securely in Streamlit Secrets
- **Free Tier**: Sufficient for individual learning and practice

## Key Features

✅ **Personalization** – Tailored to job role, experience level, and learning pace  
✅ **Instant Feedback** – Real-time scoring and actionable insights  
✅ **Interview Simulation** – Realistic Q&A format for effective preparation  
✅ **Progress Tracking** – Maintain feedback history for performance analysis  
✅ **Best Practices** – Integrated resources on interview techniques (STAR method, etc.)  
✅ **User-Friendly** – Intuitive interface suitable for candidates at all levels  

## Browser Compatibility

- Chrome (Recommended)
- Firefox
- Safari
- Edge

## Limitations & Future Enhancements

### Current Limitations
- API rate limits based on Google Gemini free tier
- Single-user session management

### Planned Enhancements
- User authentication and profile persistence
- Performance analytics dashboard
- Multi-language support
- Audio/video interview simulation
- Interview question database with company-specific preparation
- Export functionality for feedback reports

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/enhancement`)
3. Commit changes (`git commit -m 'Add enhancement'`)
4. Push to branch (`git push origin feature/enhancement`)
5. Submit Pull Request

## License

This project is provided as-is for educational purposes. See LICENSE file for details.

## Acknowledgments

- Built as a capstone project for **OnlyAI Academy – Generative AI Fundamentals**
- Powered by [Google Generative AI](https://ai.google.dev/)
- Frontend framework: [Streamlit](https://streamlit.io/)

## Support & Issues

For issues, feature requests, or questions:
- Open an [Issue](https://github.com/UpputhollaRoja/AI_Interview_Coach/issues) on GitHub
- Include detailed description and steps to reproduce
- Specify your environment (Python version, OS)

## Contact

**Author**: Upputholla Roja  
**GitHub**: [@UpputhollaRoja](https://github.com/UpputhollaRoja)

---

**Last Updated**: June 2026  
**Version**: 1.0.0
