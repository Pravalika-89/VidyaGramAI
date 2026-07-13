import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel("gemini-2.5-flash")

def ask_ai(question):

    prompt = f"""
You are VidyaGram AI, an intelligent AI Career Assistant.

Your job is to help students with:
- Career Guidance
- AI
- Data Science
- Software Development
- Web Development
- Python
- Machine Learning
- Interview Preparation
- Resume Tips
- English Communication
- Study Plans
- Project Ideas

Student Question:
{question}
"""

    response = model.generate_content(prompt)
    return response.text