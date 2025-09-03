import random
import pandas as pd
import string

# Expanded pools for more variety
first_names = [
    "Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Sam", "Jamie", "Avery", "Charlie",
    "Drew", "Blake", "Quinn", "Hayden", "Peyton", "Logan", "Skyler", "Kendall", "Cameron", "Devon",
    "Hunter", "Reese", "Rowan", "Emerson", "Dakota", "Elliot", "Finley", "Harper", "Jules", "Kai"
]

last_names = [
    "Smith", "Johnson", "Lee", "Brown", "Williams", "Garcia", "Martinez", "Davis", "Miller", "Anderson",
    "Taylor", "Moore", "Thomas", "Jackson", "White", "Harris", "Clark", "Lewis", "Walker", "Hall",
    "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Adams", "Green"
]

universities = [
    "MIT", "Stanford University", "UC Berkeley", "Carnegie Mellon University", "Harvard University",
    "Georgia Tech", "University of Michigan", "Caltech", "Cornell University", "Princeton University",
    "UCLA", "University of Illinois Urbana-Champaign", "University of Texas at Austin", "Purdue University",
    "University of Washington", "Columbia University", "University of Pennsylvania", "Yale University",
    "Duke University", "University of Southern California", "University of Wisconsin-Madison",
    "University of Toronto", "McGill University", "University of British Columbia"
]

majors = [
    "Computer Science", "Electrical Engineering", "Data Science", "Mechanical Engineering",
    "Artificial Intelligence", "Cybersecurity", "Robotics", "Software Engineering",
    "Information Systems", "Bioinformatics"
]

skills_pool = [
    "Python", "Java", "C++", "SQL", "TensorFlow", "PyTorch", "Machine Learning", "Deep Learning",
    "Cloud Computing", "Cybersecurity", "React", "Node.js", "Data Analysis", "MATLAB", "Docker",
    "Kubernetes", "AWS", "Blockchain", "Computer Vision", "NLP", "JavaScript", "HTML", "CSS",
    "GraphQL", "Go", "Rust", "Scala", "Linux", "Ansible", "TypeScript", "Flask", "Django", "FastAPI",
    "Hadoop", "Spark", "Tableau", "PowerBI"
]

achievements_pool = [
    "Dean's List", "Hackathon Winner", "Published Research Paper", "Patent Holder",
    "Open Source Contributor", "Scholarship Recipient", "Startup Founder", "Conference Speaker",
    "Internship at FAANG", "Robotics Competition Winner", "Winner of AI Challenge",
    "Hackathon Finalist", "Best Thesis Award", "Tech Blog Contributor", "Innovation Grant Recipient",
    "Coding Competition Winner"
]

experience_pool = [
    "Software Engineering Intern at Google", "Data Science Intern at Amazon", "Research Assistant in AI Lab",
    "Cybersecurity Intern at Microsoft", "Teaching Assistant for CS courses", "Intern at Tesla (Autopilot team)",
    "Machine Learning Intern at Meta", "Robotics Research Intern", "Cloud Engineer Intern at IBM",
    "Startup Co-Founder (Tech Product)", "Intern at SpaceX", "AI Research Intern at OpenAI",
    "Software Developer Intern at Adobe", "Data Analyst Intern at Oracle",
    "Full Stack Intern at Shopify", "Cloud Engineer Intern at Salesforce",
    "VR/AR Intern at Unity", "Product Management Intern at LinkedIn", "AI Ethics Research Intern",
    "Quantum Computing Intern at IBM"
]

# Generate 1000 unique(ish) profiles
profiles = []
used_combinations = set()

while len(profiles) < 1000:
    first = random.choice(first_names)
    last = random.choice(last_names)
    name = f"{first} {last}"
    university = random.choice(universities)
    major = random.choice(majors)
    grad_year = random.randint(2025, 2030)

    # Ensure uniqueness of identity
    if (name, university, major, grad_year) in used_combinations:
        continue

    skills = random.sample(skills_pool, k=random.randint(5, 8))
    achievements = random.sample(achievements_pool, k=random.randint(1, 3))
    experience = random.sample(experience_pool, k=random.randint(1, 2))

    # Generate email id: firstnamelastname + 5 random alphanumerics
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    email = f"{first.lower()}{last.lower()}{random_suffix}@gmail.com"

    profiles.append({
        "Name": name,
        "University": university,
        "Major": major,
        "Graduation Year": grad_year,
        "Skills": ", ".join(skills),
        "Achievements": ", ".join(achievements),
        "Experience": ", ".join(experience),
        "Email ID": email
    })

    used_combinations.add((name, university, major, grad_year))

# Convert to DataFrame and save
df_profiles = pd.DataFrame(profiles)
file_path = "USA_Tech_Student_Profiles.csv"
df_profiles.to_csv(file_path, index=False)

print(f"Generated {len(df_profiles)} student profiles → {file_path}")
