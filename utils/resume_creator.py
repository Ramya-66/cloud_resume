def generate_resume(name, job_role, skills, projects, experience):
    return f"""
    Name: {name}
    Job Role: {job_role}
    
    Skills:
    {', '.join(skills)}
    
    Projects:
    {projects}
    
    Experience:
    {experience}
    """
