import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel("gemini-1.5-flash")

def generate_career_guidance(maths, programming, communication, problem_solving, career):

    prompt = f"""
You are VidyaGram AI Career Assistant.

Student Scores:
Maths: {maths}
Programming: {programming}
Communication: {communication}
Problem Solving: {problem_solving}

Predicted Career:
{career}

Provide:

1. Why this career suits the student.
2. Required skills.
3. 6-month learning roadmap.
4. Best free courses.
5. 3 project ideas.
6. Interview preparation tips.
7. Future scope.
8. Motivation in 2 lines.

Keep it simple and well formatted.
"""

    response = model.generate_content(prompt)
    return response.text