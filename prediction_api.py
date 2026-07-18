from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

model = joblib.load("career_model.pkl")

ROADMAPS = {
    "AI Engineer": [
        "Python",
        "Data Structures",
        "Machine Learning",
        "Deep Learning",
        "NLP",
        "Projects",
        "Internship"
    ],

    "Data Scientist": [
        "Python",
        "Statistics",
        "SQL",
        "Machine Learning",
        "Power BI",
        "Projects"
    ],

    "Data Analyst": [
        "Excel",
        "SQL",
        "Power BI",
        "Python",
        "Tableau"
    ],

    "Software Developer": [
        "C++/Java",
        "DSA",
        "Web Development",
        "React",
        "Node.js",
        "Projects"
    ]
}

@app.route("/predict", methods=["POST"])
def predict():

    data = request.json

    features = [[
        data["maths"],
        data["programming"],
        data["communication"],
        data["problem_solving"]
    ]]

    career = model.predict(features)[0]

    return jsonify({
        "career": career,
        "roadmap": ROADMAPS[career]
    })

if __name__ == "__main__":
    app.run(debug=True)