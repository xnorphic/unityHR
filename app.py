import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state for data storage (simulating a database)
if "users" not in st.session_state:
    st.session_state.users = {
        "applicant1@example.com": {
            "role": "Applicant",
            "password": "pass123",
            "profile": {
                "name": "John Doe",
                "contact": "john.doe@example.com | (123) 456-7890",
                "resume": "Software Engineer with 5 years of experience in Python, JavaScript, and cloud computing. Worked at TechCorp (2018-2023) as Senior Developer. B.S. in Computer Science from State University (2014-2018). Skills: Python, AWS, React.",
                "cover_letter": "Dear Hiring Manager, I am excited to apply for the Software Engineer position. My experience in software development and passion for innovation make me a strong candidate."
            }
        },
        "applicant2@example.com": {
            "role": "Applicant",
            "password": "pass123",
            "profile": {
                "name": "Jane Smith",
                "contact": "jane.smith@example.com | (234) 567-8901",
                "resume": "Marketing Specialist with 3 years of experience in digital campaigns and content creation. Worked at MarketTrend (2020-2023) as Marketing Associate. B.A. in Marketing from City College (2016-2020). Skills: SEO, Content Writing, Google Analytics.",
                "cover_letter": "Dear Hiring Manager, I am eager to contribute my marketing expertise to your team. My background in digital strategies aligns with your needs."
            }
        },
        "company1@example.com": {
            "role": "Company",
            "password": "pass123",
            "profile": {
                "company_name": "Tech Innovators",
                "primary_color": "#1E90FF"
            }
        },
        "company2@example.com": {
            "role": "Company",
            "password": "pass123",
            "profile": {
                "company_name": "Market Solutions",
                "primary_color": "#FF4500"
            }
        }
    }

if "companies" not in st.session_state:
    st.session_state.companies = {
        "Tech Innovators": st.session_state.users["company1@example.com"]["profile"],
        "Market Solutions": st.session_state.users["company2@example.com"]["profile"]
    }

if "jobs" not in st.session_state:
    st.session_state.jobs = {
        0: {
            "title": "Software Engineer",
            "description": "Develop and maintain web applications using Python and React. Collaborate with cross-functional teams.",
            "requirements": "5+ years experience in Python, React, AWS. B.S. in Computer Science.",
            "company": "Tech Innovators",
            "posted_by": "company1@example.com"
        },
        1: {
            "title": "Marketing Manager",
            "description": "Lead digital marketing campaigns and content strategy. Analyze performance metrics.",
            "requirements": "3+ years in digital marketing, SEO, Google Analytics. B.A. in Marketing.",
            "company": "Market Solutions",
            "posted_by": "company2@example.com"
        },
        2: {
            "title": "Data Analyst",
            "description": "Analyze business data and provide insights using SQL and Python. Create dashboards.",
            "requirements": "2+ years in data analysis, SQL, Python. Degree in Statistics or related field.",
            "company": "Tech Innovators",
            "posted_by": "company1@example.com"
        }
    }

if "applications" not in st.session_state:
    st.session_state.applications = {
        0: {
            "candidate": "applicant1@example.com",
            "job_id": 0,
            "company": "Tech Innovators",
            "stage": "First Round",
            "docs": st.session_state.users["applicant1@example.com"]["profile"],
            "feedback": {
                "liked": True,
                "comments": ["Great technical skills, very confident in Python.", "Good cultural fit for the team."]
            }
        },
        1: {
            "candidate": "applicant1@example.com",
            "job_id": 1,
            "company": "Market Solutions",
            "stage": "Second Round",
            "docs": st.session_state.users["applicant1@example.com"]["profile"],
            "feedback": {
                "liked": False,
                "comments": ["Lacks marketing experience for senior role."]
            }
        },
        2: {
            "candidate": "applicant2@example.com",
            "job_id": 1,
            "company": "Market Solutions",
            "stage": "Final Round",
            "docs": st.session_state.users["applicant2@example.com"]["profile"],
            "feedback": {
                "liked": True,
                "comments": ["Strong marketing background, impressive portfolio.", "Excellent communication skills."]
            }
        },
        3: {
            "candidate": "applicant2@example.com",
            "job_id": 2,
            "company": "Tech Innovators",
            "stage": "First Round",
            "docs": st.session_state.users["applicant2@example.com"]["profile"],
            "feedback": {
                "liked": False,
                "comments": ["Limited data analysis experience."]
            }
        }
    }

if "app_counter" not in st.session_state:
    st.session_state.app_counter = 4

# Helper functions
def simple_resume_bucketing(resume_text, job_description):
    """Basic keyword matching for bucketing resumes."""
    resume_text = resume_text.lower()
    job_description = job_description.lower()
    keywords = job_description.split()
    match_count = sum(1 for kw in keywords if kw in resume_text)
    match_ratio = match_count / len(keywords) if keywords else 0
    if match_ratio > 0.8:
        return "Highly Suitable"
    elif match_ratio > 0.5:
        return "Suitable"
    elif match_ratio > 0.2:
        return "Moderately Suitable"
    else:
        return "Not Suitable"

# App layout
st.title("HR & Applicant Tracking System MVP")

# User Authentication (Simplified with Debug Logging)
auth_option = st.radio("Login as", ["Applicant", "Company"])
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login / Sign Up"):
    if email and password:
        st.write(f"Attempting login with email: {email}")
        if email not in st.session_state.users:
            st.session_state.users[email] = {
                "role": auth_option,
                "password": password,
                "profile": {} if auth_option == "Applicant" else {"company_name": email.split("@")[0]}
            }
            st.success(f"Signed up as {auth_option} with email {email}")
            st.session_state.current_user = email
        else:
            stored_password = st.session_state.users[email].get("password", "")
            st.write(f"Stored password for {email}: {'Found' if stored_password else 'Not Found'}")
            if stored_password == password:
                st.success(f"Logged in as {auth_option}")
                st.session_state.current_user = email
            else:
                st.error(f"Invalid login credentials. Password does not match for {email}.")
    else:
        st.error("Please enter both email and password")

# Main App Logic based on User Role
if "current_user" in st.session_state:
    user_role = st.session_state.users[st.session_state.current_user]["role"]
    st.sidebar.title(f"Welcome, {st.session_state.current_user}")
    st.sidebar.write(f"Role: {user_role}")

    if user_role == "Applicant":
        menu = st.sidebar.radio("Menu", ["Profile", "Browse Jobs", "My Applications"])
        
        if menu == "Profile":
            st.header("Applicant Profile")
            with st.form("profile_form"):
                name = st.text_input("Name", value=st.session_state.users[email].get("profile", {}).get("name", ""))
                contact = st.text_input("Contact", value=st.session_state.users[email].get("profile", {}).get("contact", ""))
                resume = st.text_area("Resume Content (placeholder for file upload)", value=st.session_state.users[email].get("profile", {}).get("resume", ""))
                cover_letter = st.text_area("Cover Letter", value=st.session_state.users[email].get("profile", {}).get("cover_letter", ""))
                if st.form_submit_button("Save Profile"):
                    st.session_state.users[email]["profile"] = {
                        "name": name,
                        "contact": contact,
                        "resume": resume,
                        "cover_letter": cover_letter
                    }
                    st.success("Profile saved!")

        elif menu == "Browse Jobs":
            st.header("Browse Jobs")
            for job_id, job in st.session_state.jobs.items():
                st.subheader(job["title"])
                st.write(f"Company: {job['company']}")
                st.write(f"Description: {job['description']}")
                if st.button(f"Apply to {job['title']}", key=f"apply_{job_id}"):
                    app_id = st.session_state.app_counter
                    st.session_state.app_counter += 1
                    st.session_state.applications[app_id] = {
                        "candidate": email,
                        "job_id": job_id,
                        "company": job["company"],
                        "stage": "First Round",
                        "docs": st.session_state.users[email].get("profile", {}),
                        "feedback": {"liked": False, "comments": []}
                    }
                    st.success("Application submitted!")

        elif menu == "My Applications":
            st.header("My Applications")
            for app_id, app in st.session_state.applications.items():
                if app["candidate"] == email:
                    job = st.session_state.jobs.get(app["job_id"], {})
                    st.write(f"Job: {job.get('title', 'N/A')}")
                    st.write(f"Company: {app['company']}")
                    st.write(f"Stage: {app['stage']}")
                    st.write("---")

    elif user_role == "Company":
        menu = st.sidebar.radio("Menu", ["Company Settings", "Post Job", "Manage Jobs", "View Applicants", "Kanban Board"])
        
        if menu == "Company Settings":
            st.header("Company Settings")
            with st.form("company_settings"):
                company_name = st.text_input("Company Name", value=st.session_state.users[email].get("profile", {}).get("company_name", ""))
                primary_color = st.color_picker("Primary Color", value=st.session_state.users[email].get("profile", {}).get("primary_color", "#000000"))
                if st.form_submit_button("Save Settings"):
                    st.session_state.users[email]["profile"]["company_name"] = company_name
                    st.session_state.users[email]["profile"]["primary_color"] = primary_color
                    st.session_state.companies[company_name] = st.session_state.users[email]["profile"]
                    st.success("Settings saved!")

        elif menu == "Post Job":
            st.header("Post a New Job")
            with st.form("job_posting"):
                title = st.text_input("Job Title")
                description = st.text_area("Job Description")
                requirements = st.text_area("Requirements")
                if st.form_submit_button("Post Job"):
                    job_id = len(st.session_state.jobs)
                    company_name = st.session_state.users[email]["profile"].get("company_name", "Unknown")
                    st.session_state.jobs[job_id] = {
                        "title": title,
                        "description": description,
                        "requirements": requirements,
                        "company": company_name,
                        "posted_by": email
                    }
                    st.success("Job posted!")

        elif menu == "Manage Jobs":
            st.header("Manage Jobs")
            company_name = st.session_state.users[email]["profile"].get("company_name", "")
            for job_id, job in st.session_state.jobs.items():
                if job["company"] == company_name:
                    st.subheader(job["title"])
                    st.write(f"Description: {job['description']}")
                    st.write("---")

        elif menu == "View Applicants":
            st.header("View Applicants")
            company_name = st.session_state.users[email]["profile"].get("company_name", "")
            for app_id, app in st.session_state.applications.items():
                if app["company"] == company_name:
                    st.subheader(f"Applicant: {app['candidate']}")
                    job = st.session_state.jobs.get(app['job_id'], {})
                    st.write(f"Job: {job.get('title', 'N/A')}")
                    st.write(f"Current Stage: {app['stage']}")
                    resume_text = app.get("docs", {}).get("resume", "")
                    job_desc = job.get("description", "")
                    bucket = simple_resume_bucketing(resume_text, job_desc)
                    st.write(f"Bucket: {bucket}")
                    stages = ["First Round", "Second Round", "Final Round", "Rejected", "Hired"]
                    new_stage = st.selectbox("Update Stage", stages, index=stages.index(app["stage"]) if app["stage"] in stages else 0, key=f"stage_{app_id}")
                    if st.button("Update", key=f"update_{app_id}"):
                        st.session_state.applications[app_id]["stage"] = new_stage
                        st.success("Stage updated!")
                    st.write("---")

        elif menu == "Kanban Board":
            st.header("Kanban Board for Job Roles")
            company_name = st.session_state.users[email]["profile"].get("company_name", "")
            company_jobs = {job_id: job for job_id, job in st.session_state.jobs.items() if job["company"] == company_name}
            
            if not company_jobs:
                st.write("No jobs posted by your company.")
            else:
                for job_id, job in company_jobs.items():
                    st.subheader(f"Kanban Board for {job['title']}")
                    col1, col2, col3 = st.columns(3)
                    
                    stages = {"First Round": col1, "Second Round": col2, "Final Round": col3}
                    job_applications = {app_id: app for app_id, app in st.session_state.applications.items() if app["job_id"] == job_id and app["company"] == company_name}
                    
                    # Organize applications by stage for display
                    for stage, col in stages.items():
                        with col:
                            st.subheader(stage)
                            for app_id, app in job_applications.items():
                                if app["stage"] == stage:
                                    with st.container():
                                        st.markdown("---")
                                        st.write(f"**Name:** {app['docs'].get('name', 'N/A')}")
                                        st.write(f"**Contact:** {app['docs'].get('contact', 'N/A')}")
                                        # Heart icon for liked status
                                        heart = "❤️" if app["feedback"]["liked"] else "🖤"
                                        st.write(f"Previous Interviewer Rating: {heart}")
                                        # Comment icon with dummy number
                                        comment_count = len(app["feedback"]["comments"])
                                        if st.button(f"💬 Comments ({comment_count})", key=f"comments_{app_id}_{stage}"):
                                            if comment_count > 0:
                                                st.write("**Comments from Previous Interviewers:**")
                                                for comment in app["feedback"]["comments"]:
                                                    st.write(f"- {comment}")
                                            else:
                                                st.write("No comments available.")
                                        # Buttons to move between stages
                                        all_stages = ["First Round", "Second Round", "Final Round", "Rejected", "Hired"]
                                        if app["stage"] != "Rejected" and app["stage"] != "Hired":
                                            new_stage = st.selectbox("Move to Stage", [s for s in all_stages if s != app["stage"]], key=f"move_{app_id}_{stage}")
                                            if st.button("Move", key=f"move_btn_{app_id}_{stage}"):
                                                st.session_state.applications[app_id]["stage"] = new_stage
                                                st.experimental_rerun()
                                        st.markdown("---")

if st.button("Logout"):
    if "current_user" in st.session_state:
        del st.session_state.current_user
    st.experimental_rerun()
