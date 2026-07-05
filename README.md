# StudyMate AI – Smart Study Planner Agent

> **An AI-powered study planning assistant that helps students prepare smarter, stay consistent, and achieve their academic goals through personalized study plans powered by Google Gemini.**

---

# 🔗 Project Links

## 🌐 Live Demo

https://studymate-ai-zi3r.onrender.com

## 💻 GitHub Repository

https://github.com/CHAITANYA-KHANKE/StudyMate-AI

---

# 📖 Project Overview

StudyMate AI is an AI-powered study planning assistant built to help students prepare effectively for examinations. Instead of following a fixed timetable, the application generates personalized study schedules based on each student's subjects, available study hours, exam date, and study preferences.

Using Google's Gemini models through the **google-genai SDK**, StudyMate AI creates intelligent daily study plans, schedules revision sessions, tracks learning progress, maintains study streaks, and provides context-aware study guidance through an AI-powered chatbot.

The application follows a modern **Neo-Brutalist UI** design philosophy featuring bold typography, thick outlines, playful colors, and a clean, interactive interface that delivers an engaging user experience.

---

# 🎯 Problem Statement

Many students struggle with creating realistic study schedules and maintaining consistency throughout their exam preparation. Traditional planners are static and cannot adapt to each student's learning pace, available time, or subject priorities.

StudyMate AI solves this problem by using AI to generate dynamic, personalized study plans while continuously helping students stay organized, motivated, and focused.

---

# 💡 Solution

StudyMate AI acts as a personal AI study companion.

The application analyzes a student's academic information and automatically creates a personalized study schedule. It continuously tracks completed tasks, suggests revision sessions, answers study-related questions, and provides progress insights to help students prepare efficiently for their examinations.

---

# ✨ Key Features

## 🧠 AI Smart Study Planner

* Personalized AI-generated study timetable
* Automatic subject distribution
* Intelligent revision scheduling
* Daily workload optimization
* Practice question recommendations

---

## 📊 Student Dashboard

* Exam Countdown
* Today's Tasks
* Tomorrow's Tasks
* Study Progress Overview
* Daily Study Streak
* Pomodoro Focus Timer
* Smart Notifications

---

## 📅 Interactive Study Planner

* Daily study timetable
* Revision schedule
* Task completion tracking
* Print timetable
* Export timetable as PDF

---

## 📈 Progress Analytics

* Weekly Progress Chart
* Subject Completion Statistics
* Learning Consistency Index
* Completion Percentage
* Study Streak Monitoring

---

## 🤖 AI Study Coach

The AI assistant can answer questions like:

* What should I study today?
* Help me prepare for Mathematics.
* Give me revision tips.
* How should I prepare before my exam?

The chatbot uses the student's current study plan and progress to generate personalized responses.

---

## 🔒 Personal Learning Experience

StudyMate AI is designed for individual students. The application focuses entirely on helping a single user manage their studies without social features, leaderboards, subscriptions, advertisements, referrals, or unnecessary distractions.

---

# 📸 Application Screenshots

> Replace the placeholders below with actual screenshots from your project.

---

## 🏠 Home Page

<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/e7e8fe21-0ae0-47d4-a8fc-cc50bbe0e61e" />
<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/9d19cc2c-e7ad-48cf-872c-f47ef024d131" />
Description:

Landing page introducing StudyMate AI with its Neo-Brutalist design and project overview.

---

## 👤 Student Setup

📷 **Insert Screenshot Here**

Description:

Student profile form where users enter subjects, exam date, daily study hours, and study preferences.

---

## 📊 Dashboard

📷 **Insert Screenshot Here**

Description:

Displays today's study tasks, exam countdown, study streak, Pomodoro timer, and progress summary.

---

## 📅 AI Study Planner

📷 **Insert Screenshot Here**

Description:

AI-generated personalized study timetable including revision sessions and task completion tracking.

---

## 📈 Progress Analytics

📷 **Insert Screenshot Here**

Description:

Interactive charts displaying weekly study progress, completion percentage, and subject mastery.

---

## 🤖 AI Study Coach

📷 **Insert Screenshot Here**

Description:

Gemini-powered chatbot providing personalized academic guidance and study assistance.

---

## ⚙️ Settings

📷 **Insert Screenshot Here**

Description:

Allows students to update their study profile and preferences.

---

## 🏗️ System Architecture

📷 **Insert Architecture Diagram Screenshot Here**

Description:

Overall architecture showing the interaction between the frontend, backend, AI agents, Gemini API, and database.

---

# 🏗️ System Architecture

StudyMate AI follows a modular architecture where the frontend communicates with a FastAPI backend. The backend coordinates multiple AI agents to generate personalized study plans, answer student queries, track learning progress, and manage study data using Google Gemini and a local JSON database.

```text
                         +----------------------+
                         |      Student         |
                         +----------+-----------+
                                    |
                                    |
                                    v
                    +-------------------------------+
                    |   Frontend (HTML/CSS/JS)      |
                    +---------------+---------------+
                                    |
                             HTTP API Requests
                                    |
                                    v
                    +-------------------------------+
                    |      FastAPI Backend          |
                    +---------------+---------------+
                                    |
        +---------------------------+----------------------------+
        |                           |                            |
        v                           v                            v
+------------------+      +------------------+       +----------------------+
| Planner Agent    |      | Chat Agent       |       | Progress Agent       |
| Generates Plans  |      | AI Study Coach   |       | Tracks Progress      |
+---------+--------+      +---------+--------+       +----------+-----------+
          |                         |                           |
          +------------+------------+                           |
                       |                                        |
                       v                                        v
              +--------------------+                 +----------------------+
              | Google Gemini API  |                 | users.json Database  |
              +--------------------+                 +----------------------+
```

## Workflow

1. The student enters their study details through the frontend.
2. The frontend sends the information to the FastAPI backend.
3. The Planner Agent uses Google Gemini to generate a personalized study schedule.
4. The generated timetable is stored in the local JSON database.
5. The Progress Agent continuously tracks completed tasks, study streaks, and learning consistency.
6. The Chat Agent accesses the student's study plan and progress to provide personalized study guidance.
7. The frontend displays updated schedules, analytics, reminders, and AI-generated responses in real time.

---

# 🤖 Why AI Agents?

Traditional study planners generate static schedules that cannot adapt to individual students.

StudyMate AI uses AI Agents to:

* Analyze each student's study profile.
* Generate personalized study plans.
* Recommend revision sessions.
* Answer study-related questions.
* Track learning progress.
* Encourage consistent study habits through intelligent guidance.

By combining planning, progress tracking, and conversational assistance, the application delivers a personalized and adaptive learning experience.
# 💻 Technology Stack

## Frontend

* HTML5
* CSS3
* JavaScript

## Backend

* Python
* FastAPI
* Uvicorn

## Artificial Intelligence

* Google Gemini
* google-genai SDK

## Data Visualization

* Chart.js

## Database

* JSON (`users.json`)

## Deployment

* Render

---

# 📂 Project Structure

```text
StudyMate-AI/
│
├── frontend/
│   ├── home/
│   ├── setup/
│   ├── dashboard/
│   ├── study-plan/
│   ├── progress/
│   ├── chat/
│   ├── settings/
│   ├── css/
│   └── js/
│
├── backend/
│   ├── main.py
│   ├── planner_agent.py
│   ├── chat_agent.py
│   ├── progress_agent.py
│   ├── reminder.py
│   └── notification.py
│
├── database/
│   └── users.json
│
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation Guide

## 1. Clone the Repository

```bash
git clone https://github.com/CHAITANYA-KHANKE/StudyMate-AI.git

cd StudyMate-AI
```

---

## 2. Create Virtual Environment

```bash
python -m venv .venv
```

Activate Virtual Environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Gemini API Key

### Windows CMD

```cmd
set GEMINI_API_KEY=your_api_key
```

### Windows PowerShell

```powershell
$env:GEMINI_API_KEY="your_api_key"
```

### Linux / macOS

```bash
export GEMINI_API_KEY="your_api_key"
```

---

## 5. Run the Project

```bash
uvicorn backend.main:app --reload
```

Open your browser and visit:

```text
http://localhost:8000
```

---

# 🌐 Live Deployment

The application is deployed on Render and is publicly accessible.

**Live Demo**

https://studymate-ai-zi3r.onrender.com

---

# 🤖 AI Agent Modules

## 🧠 Planner Agent

**File**

`backend/planner_agent.py`

### Responsibilities

* Analyze student profile.
* Calculate available study days.
* Generate personalized study timetable.
* Create revision schedule.
* Optimize daily study workload.
* Recommend practice sessions.

---

## 💬 Chat Agent

**File**

`backend/chat_agent.py`

### Responsibilities

* Answer study-related questions.
* Read the student's active timetable.
* Provide personalized study advice.
* Explain difficult concepts.
* Suggest revision strategies.
* Motivate students during preparation.

---

## 📈 Progress Agent

**File**

`backend/progress_agent.py`

### Responsibilities

* Monitor completed tasks.
* Calculate study streaks.
* Measure learning consistency.
* Generate progress statistics.
* Update dashboard analytics.

---

## 🔔 Reminder Module

**File**

`backend/reminder.py`

### Responsibilities

* Generate daily reminders.
* Display upcoming revision sessions.
* Notify users about unfinished tasks.

---

## 🔔 Notification Module

**File**

`backend/notification.py`

### Responsibilities

* Generate smart notifications.
* Display important study alerts.
* Inform users about upcoming deadlines.

---

# 🔄 Application Workflow

```text
Student

↓

Enter Study Details

↓

Frontend

↓

FastAPI Backend

↓

Planner Agent

↓

Google Gemini

↓

Generate Personalized Study Plan

↓

Store Data (users.json)

↓

Dashboard

↓

Progress Tracking

↓

AI Chat Assistant

↓

Exam Preparation
```

---

# 🚀 Future Improvements

Future versions of StudyMate AI may include:

* Google Calendar Integration
* Voice Commands
* Speech-to-Text Support
* Mobile Application
* Cloud Database
* Offline Study Mode
* AI Performance Prediction
* Smart Revision Forecasting
* Email Reminder Support
* Multi-language Support

---

# 🙏 Acknowledgements

This project was developed as part of the **Kaggle 5-Day AI Agents Intensive Course with Google**.

Special thanks to:

* Google
* Kaggle
* Google Gemini
* FastAPI
* Chart.js
* Render
* The Open Source Community

---

# 📄 License

This project is licensed under the **MIT License**.

---

# 👨‍💻 Developer

**Chaitanya Khanke**

GitHub:

https://github.com/CHAITANYA-KHANKE

---

# ⭐ Support

If you found this project useful, please consider giving the repository a **⭐ Star** on GitHub.

Your support helps improve the project and encourages future development.
