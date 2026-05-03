**Election Education AI Agent**

A Prompt War Submission | Powered by Antigravity & Google Cloud
The Election Education Agent is an autonomous AI-native application designed to guide voters through the complexities of the election process. Built using the Antigravity IDE, this agent doesn't just provide static links; it reasons through user queries to deliver personalized, state-specific voting knowledge.

🚀 Features
Mission-Driven AI: Built using Antigravity's "agent-first" architecture to automate research and coding.

Dynamic Election Logic: Real-time answers on registration, deadlines, and ballot information.

Cloud-Native Scale: Fully containerized and deployed on Google Cloud Run for high performance.

Simplified UX: A clean, intuitive interface designed for citizens of all digital skill levels.

🛠️ Technical Architecture
Development Environment: Antigravity IDE (macOS)

Core Model: Google Gemini 1.5 Pro

Backend: Python / FastAPI

Deployment: Google Cloud Run (Serverless)

Containerization: Docker & Google Artifact Registry

📦 Local Setup & Installation
If you have Antigravity installed, you can simply clone and start the "Mission."

Clone the repository:

Bash

git clone  [(https://github.com/prekshav/election-agent.git)

cd election-education-process

Setup Credentials:
Ensure your Google Cloud SDK is authenticated:

Bash

gcloud auth application-default login

Run the Application:

Bash

# In the Antigravity Terminal

streamlit run app.py

☁️ Cloud Run Deployment
This project is configured for one-command deployment to Google Cloud:

Bash

gcloud run deploy election-education-app \
  --source . \
  --region us-central1 \
  --allow-unauthenticated

  
🏆 Competition Context
Task: Election Education Process

Track: Track 2

Goal: Demonstrate the power of Antigravity in building high-utility AI agents for social impact.
