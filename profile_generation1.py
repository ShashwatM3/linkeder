import random
import pandas as pd

# Sample data for generation
first_names = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Sam", "Jamie", "Avery", "Cameron"]
last_names = ["Smith", "Johnson", "Lee", "Brown", "Williams", "Garcia", "Martinez", "Davis", "Miller", "Anderson"]
universities = [
    "MIT", "Stanford University", "UC Berkeley", "Carnegie Mellon University", "Harvard University",
    "Georgia Tech", "University of Michigan", "Caltech", "Cornell University", "Princeton University",
    "UCLA", "University of Illinois Urbana-Champaign", "University of Texas at Austin",
    "Purdue University", "University of Washington"
]
majors = [
    "Computer Science", "Electrical Engineering", "Data Science", "Mechanical Engineering",
    "Artificial Intelligence", "Cybersecurity", "Robotics", "Software Engineering",
    "Information Systems", "Bioinformatics"
]
skills_pool = [
    "Python", "Java", "C++", "SQL", "TensorFlow", "PyTorch", "Machine Learning", "Deep Learning",
    "Cloud Computing", "Cybersecurity", "React", "Node.js", "Data Analysis", "MATLAB", "Docker",
    "Kubernetes", "AWS", "Blockchain", "Computer Vision", "NLP"
]
achievements_pool = [
    "Dean's List", "Hackathon Winner", "Published Research Paper", "Patent Holder",
    "Open Source Contributor", "Scholarship Recipient", "Startup Founder",
    "Conference Speaker", "Internship at FAANG", "Robotics Competition Winner"
]
experience_pool = [
    "Software Engineering Intern at Google", "Data Science Intern at Amazon",
    "Research Assistant in AI Lab", "Cybersecurity Intern at Microsoft",
    "Teaching Assistant for CS courses", "Intern at Tesla (Autopilot team)",
    "Machine Learning Intern at Meta", "Robotics Research Intern",
    "Cloud Engineer Intern at IBM", "Startup Co-Founder (Tech Product)"
]

# Generate 500 profiles
profiles = []
for _ in range(500):
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    university = random.choice(universities)
    major = random.choice(majors)
    grad_year = random.randint(2025, 2030)
    skills = random.sample(skills_pool, k=random.randint(4, 7))
    achievements = random.sample(achievements_pool, k=random.randint(1, 3))
    experience = random.sample(experience_pool, k=random.randint(1, 2))

    profiles.append({
        "Name": name,
        "University": university,
        "Major": major,
        "Graduation Year": grad_year,
        "Skills": ", ".join(skills),
        "Achievements": ", ".join(achievements),
        "Experience": ", ".join(experience)
    })

# Convert to DataFrame
df_profiles = pd.DataFrame(profiles)

# Save the generated profiles to a CSV file
file_path = "USA_Tech_Student_Profiles.csv"
df_profiles.to_csv(file_path, index=False)

# To ensure uniqueness, we'll expand the sample pools and keep track of used combinations

# Expanded first and last names
first_names_extended = first_names + ["Charlie", "Drew", "Blake", "Quinn", "Hayden", "Peyton", "Logan", "Skyler", "Kendall", "Cameron"]
last_names_extended = last_names + ["Taylor", "Moore", "Thomas", "Jackson", "White", "Harris", "Clark", "Lewis", "Walker", "Hall"]

# Expanded skills, achievements, and experiences
skills_pool_extended = skills_pool + ["JavaScript", "HTML", "CSS", "GraphQL", "Go", "Rust", "Scala", "Docker Swarm", "Ansible", "Linux"]
achievements_pool_extended = achievements_pool + ["Winner of AI Challenge", "Hackathon Finalist", "Best Thesis Award", 
                                                   "Tech Blog Contributor", "Innovation Grant Recipient", "Coding Competition Winner"]
experience_pool_extended = experience_pool + ["Intern at SpaceX", "AI Research Intern at OpenAI", 
                                               "Software Developer Intern at Adobe", "Data Analyst Intern at Oracle", 
                                               "Full Stack Intern at Shopify", "Cloud Engineer Intern at Salesforce"]

used_combinations = set((row['Name'], row['University'], row['Major'], row['Graduation Year']) for _, row in df_profiles.iterrows())

# Generate 500 new unique profiles
new_profiles = []
attempts = 0

while len(new_profiles) < 500 and attempts < 5000:
    attempts += 1
    name = f"{random.choice(first_names_extended)} {random.choice(last_names_extended)}"
    university = random.choice(universities)
    major = random.choice(majors)
    grad_year = random.randint(2025, 2030)
    
    # Ensure uniqueness of core identity
    if (name, university, major, grad_year) in used_combinations:
        continue
    
    skills = random.sample(skills_pool_extended, k=random.randint(4, 7))
    achievements = random.sample(achievements_pool_extended, k=random.randint(1, 3))
    experience = random.sample(experience_pool_extended, k=random.randint(1, 2))
    
    new_profiles.append({
        "Name": name,
        "University": university,
        "Major": major,
        "Graduation Year": grad_year,
        "Skills": ", ".join(skills),
        "Achievements": ", ".join(achievements),
        "Experience": ", ".join(experience)
    })
    
    used_combinations.add((name, university, major, grad_year))

# Convert to DataFrame
df_new_profiles = pd.DataFrame(new_profiles)
# Save the second batch to CSV
file_path_new = "USA_Tech_Student_Profiles_Batch2.csv"
df_new_profiles.to_csv(file_path_new, index=False)
file_path_new
