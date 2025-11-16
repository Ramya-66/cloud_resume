from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.textract_utils import extract_text_textract
from utils.nlp_utils import analyze_skills, analyze_experience
from utils.scoring_utils import calculate_fit_score, calculate_upskill_score
from utils.resume_creator import generate_resume
import os
import requests
from io import BytesIO

# -------------------- APP SETUP --------------------
app = Flask(__name__)
CORS(app)  # allow Wix Studio frontend to access backend

# -------------------- ROOT --------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Resume AI Backend Running Successfully"})

# -------------------- 1️⃣ Resume Analyzer --------------------
@app.route("/analyze", methods=["POST"])
def analyze_resume():
    data = request.json
    file_url = data.get("file_url")
    if not file_url:
        return jsonify({"error": "No file URL provided"}), 400

    try:
        # Download PDF from Wix UploadButton URL
        response = requests.get(file_url)
        response.raise_for_status()  # raise error if download failed
        pdf_file = BytesIO(response.content)

        # Extract text using your existing function
        text = extract_text_textract(pdf_file)

        # Analyze
        skills = analyze_skills(text)
        experience = analyze_experience(text)
        fit_score = calculate_fit_score(skills)

        return jsonify({
            "text": text,
            "skills": skills,
            "experience": experience,
            "fit_score": fit_score
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
# -------------------- 2️⃣ Resume Creator --------------------
@app.route("/create-resume", methods=["POST"])
def create_resume_api():
    data = request.json or {}

    name = data.get("name", "")
    job_role = data.get("job_role", "")
    skills = data.get("skills", [])
    projects = data.get("projects", [])
    experience = data.get("experience", "")

    try:
        resume_text = generate_resume(name, job_role, skills, projects, experience)
        return jsonify({"resume": resume_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------- 3️⃣ Upskill Recommendation --------------------
@app.route("/upskill", methods=["POST"])
def upskill_api():
    data = request.json or {}
    job_role = data.get("job_role", "")
    skills = data.get("skills", [])

    try:
        result = calculate_upskill_score(job_role, skills)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------- RUN --------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render assigns port dynamically
    app.run(host="0.0.0.0", port=port)
