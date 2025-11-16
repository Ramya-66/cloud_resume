def calculate_fit_score(skills):
    required = ["Python", "ML", "Deep Learning"]
    score = len([s for s in skills if s.lower() in " ".join(required).lower()])
    return score * 10

def calculate_upskill_score(job_role, user_skills):
    roadmap = {
        "Data Scientist": ["Python", "ML", "Statistics", "Deep Learning", "NLP"],
        "Web Developer": ["HTML", "CSS", "JS", "React", "Node"],
        "Cloud Engineer": ["AWS", "Linux", "Docker", "Terraform"]
    }

    required = roadmap.get(job_role, [])
    missing = [skill for skill in required if skill not in user_skills]

    return {
        "job_role": job_role,
        "current_skills": user_skills,
        "missing_skills": missing,
        "upskill_recommendation": [f"Learn {m} using Coursera/Udemy" for m in missing]
    }
