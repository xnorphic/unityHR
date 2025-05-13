import streamlit as st
from datetime import datetime
import os

# Initialize session state for data storage (simulating a database)
if "users" not in st.session_state:
    st.session_state.users = {}

if "jobs" not in st.session_state:
    st.session_state.jobs = {}

if "applications" not in st.session_state:
    st.session_state.applications = {}

# File upload directory
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Helper functions
def save_uploaded_file(uploaded_file, subfolder):
    file_path = os.path.join(UPLOAD_DIR, subfolder, uploaded_file.name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# App layout
st.title("ATS with File Uploads")

# User Authentication
auth_tab, signup_tab = st.tabs(["Login", "Sign Up"])

with auth_tab:
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = st.session_state.users.get(email)
        if user and user["password"] == password:
            st.session_state.current_user = email
            st.success("Login successful!")
        else:
            st.error("Invalid login credentials.")

with signup_tab:
    st.subheader("Sign Up")
    new_email = st.text_input("New Email")
    new_password = st.text_input("New Password", type="password")
    role = st.selectbox("Role", ["Applicant", "Company"])
    if st.button("Sign Up"):
        if new_email in st.session_state.users:
            st.error("Email already exists!")
        else:
            st.session_state.users[new_email] = {"role": role, "password": new_password, "profile": {}}
            st.success("Sign up successful! Please log in.")

if "current_user" in st.session_state:
    user = st.session_state.users[st.session_state.current_user]
    st.sidebar.title("Navigation")
    role = user["role"]
    if role == "Applicant":
        menu = st.sidebar.radio("Menu", ["Profile", "Browse Jobs", "My Applications"])
        
        if menu == "Profile":
            st.header("Applicant Profile")
            with st.form("profile_form"):
                name = st.text_input("Name", value=user["profile"].get("name", ""))
                contact = st.text_input("Contact", value=user["profile"].get("contact", ""))
                resume_file = st.file_uploader("Upload Resume (PDF/Word)", type=["pdf", "docx"])
                cover_letter_file = st.file_uploader("Upload Cover Letter (PDF/Word)", type=["pdf", "docx"])
                if st.form_submit_button("Save Profile"):
                    if resume_file:
                        resume_path = save_uploaded_file(resume_file, subfolder=email)
                        user["profile"]["resume_file"] = resume_path
                    if cover_letter_file:
                        cover_letter_path = save_uploaded_file(cover_letter_file, subfolder=email)
                        user["profile"]["cover_letter_file"] = cover_letter_path
                    user["profile"]["name"] = name
                    user["profile"]["contact"] = contact
                    st.success("Profile saved successfully!")
        
        elif menu == "Browse Jobs":
            st.header("Browse Jobs")
            for job_id, job in st.session_state.jobs.items():
                st.subheader(job["title"])
                st.write(f"Company: {job['company']}")
                st.write(f"Description: {job['description']}")
                if st.button(f"Apply to {job['title']}", key=f"apply_{job_id}"):
                    app_id = len(st.session_state.applications)
                    st.session_state.applications[app_id] = {
                        "candidate": email,
                        "job_id": job_id,
                        "company": job["company"],
                        "stage": "First Round",
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
    
    elif role == "Company":
        menu = st.sidebar.radio("Menu", ["Post Jobs", "View Applications"])
        
        if menu == "Post Jobs":
            st.header("Post a Job")
            with st.form("job_form"):
                title = st.text_input("Job Title")
                description = st.text_area("Job Description")
                requirements = st.text_area("Requirements")
                if st.form_submit_button("Post Job"):
                    job_id = len(st.session_state.jobs)
                    st.session_state.jobs[job_id] = {
                        "title": title,
                        "description": description,
                        "requirements": requirements,
                        "company": user["profile"].get("company_name", "Unknown"),
                        "posted_by": st.session_state.current_user
                    }
                    st.success("Job posted successfully!")
        
        elif menu == "View Applications":
            st.header("View Applications")
            for app_id, app in st.session_state.applications.items():
                if app["company"] == user["profile"].get("company_name", ""):
                    st.subheader(f"Applicant: {app['candidate']}")
                    job = st.session_state.jobs.get(app["job_id"], {})
                    st.write(f"Job: {job.get('title', 'N/A')}")
                    st.write(f"Stage: {app['stage']}")
                    st.write("---")
else:
    st.warning("Please log in to access the system.")