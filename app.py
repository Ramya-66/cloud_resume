from flask import Flask, request, jsonify
from utils.textract_utils import extract_text_textract
from utils.nlp_utils import analyze_skills, analyze_experience
from utils.scoring_utils import calculate_fit_score, calculate_upskill_score
from utils.resume_creator import generate_resume
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Resume AI Backend Running Successfully"})


# -------------------- 1️⃣ Resume Analyzer --------------------
@app.route("/analyze", methods=["POST"])
def analyze_resume():
    if "file" not in request.files:
        return jsonify({"error": "No resume uploaded"}), 400
    
    resume_file = request.files["file"]

    text = extract_text_textract(resume_file)
    skills = analyze_skills(text)
    experience = analyze_experience(text)
    fit_score = calculate_fit_score(skills)

    return jsonify({
        "text": text,
        "skills": skills,
        "experience": experience,
        "fit_score": fit_score
    })


# -------------------- 2️⃣ Resume Creator --------------------
@app.route("/create-resume", methods=["POST"])
def create_resume_api():
    data = request.json

    name = data.get("name")
    job_role = data.get("job_role")
    skills = data.get("skills")
    projects = data.get("projects")
    experience = data.get("experience")

    resume_text = generate_resume(name, job_role, skills, projects, experience)

    return jsonify({"resume": resume_text})


# -------------------- 3️⃣ Upskill Recommendation --------------------
@app.route("/upskill", methods=["POST"])
def upskill_api():
    data = request.json
    job_role = data.get("job_role")
    skills = data.get("skills")

    result = calculate_upskill_score(job_role, skills)

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
