# StudyMate AI – Smart Study Planner Agent

**StudyMate AI** is an AI-powered study planning assistant designed to help students prepare for exams. By leveraging Google's Gemini models (via the `google-genai` SDK) and a FastAPI backend, the application dynamically generates highly personalized study schedules, schedules revision sessions, tracks completed tasks, and manages study streaks and consistency records.

The user interface features a custom **Neo-Brutalist** design style (inspired by high-contrast flat layout elements, warm cream background `#FFF8E7`, thick black outlines, and playful colors), providing an interactive, accessible, and premium client experience.

---

## 🚀 Key Features

1. **Smart Planner Agent (AI Timetable Generation)**:
   * Analyzes student profiles (name, subjects, exam date, daily available study hours, difficulty level, and study preferences).
   * Intelligently schedules daily topics, dedicated revision sessions, and custom practice questions.
   * Ensures the scheduled load never exceeds the user's daily study hours budget.

2. **Student Dashboard (Study Control Room)**:
   * Displays an active exam countdown clock.
   * Tracks a **Daily Study Streak** (increases automatically when tasks are completed day-after-day).
   * Displays today's/tomorrow's task lists and upcoming revision sessions.
   * Features an integrated, beautifully styled **Pomodoro Focus Timer** with Start, Pause, and Reset controls.
   * Displays dynamic alerts and notifications based on task deadlines.

3. **Timetable & PDF Export**:
   * Interactive study calendar allowing students to toggle checkboxes to mark tasks as completed.
   * Features a clean `Export / Print PDF` configuration that formats the timetable beautifully for printing or saving.

4. **Progress Analytics (Chart.js)**:
   * Visualizes weekly completions (bar chart) and subject-wise mastery rates (horizontal bar chart).
   * Displays a **Learning Consistency Index** to show student tiers (e.g. *Beginner, Consistent Studier, Ultimate Academic Warrior*).

5. **AI Study Coach Chatbot**:
   * A conversational assistant capable of answering student queries (e.g. *"What should I study today?"* or *"Help me with Mathematics"*).
   * Automatically accesses the active student's plan and progress logs to provide context-aware, practical advice.

6. **Session-based Multi-user Isolation**:
   * Utilizes a browser `localStorage` user ID and custom `X-User-ID` request headers.
   * The backend registers and saves profile records independently in `database/users.json` based on the user ID, ensuring different browsers or sessions load a fresh setup screen by default and do not overwrite each other's data.

---

## 📂 Project Directory Structure

```
StudyMate-AI/
├── frontend/             # Client-side Static Interface
│   ├── home/             # Landing page
│   ├── setup/            # Student onboarding profile form
│   ├── dashboard/        # Main student hub, streaks, and timers
│   ├── study-plan/       # Study timetable (with PDF print styles)
│   ├── progress/         # Statistics and Chart.js analytics graphs
│   ├── chat/             # AI study coach chat window
│   ├── settings/         # Configuration updates and database resets
│   ├── css/style.css     # Core Neo-Brutalist stylesheets
│   └── js/app.js         # Sidebar renderer & global fetch interceptor
├── backend/              # FastAPI Application
│   ├── main.py           # Core routes, data management, and file mounting
│   ├── planner_agent.py  # Gemini-powered study planner
│   ├── chat_agent.py     # Gemini-powered coaching chatbot
│   ├── progress_agent.py # Progress metrics and streak tracker
│   ├── reminder.py       # Active daily task reminder compiler
│   └── notification.py   # Dynamic notification log manager
├── database/
│   └── users.json        # Unified multi-user state files database
└── requirements.txt      # Python libraries dependencies
```

---

## ⚙️ Setup and Installation

Follow these steps to set up and launch the application locally:

### 1. Prerequisites
Ensure you have **Python 3.10+** and a package manager (like `pip` or `uv`) installed. Set your Gemini API key in your environment variables:

**On Windows (Command Prompt):**
```cmd
set GEMINI_API_KEY=your_actual_api_key_here
```

**On Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your_actual_api_key_here"
```

**On Linux/macOS:**
```bash
export GEMINI_API_KEY="your_actual_api_key_here"
```

### 2. Environment Setup & Dependency Installation
Create a local Python virtual environment and install the required libraries:

```bash
# Initialize virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

*(Alternatively, if you use **`uv`**, simply run `uv sync` to set up the environment)*

### 3. Launching the Application
Start the FastAPI development server:

```bash
python -m uvicorn backend.main:app --reload
```

The application will start, serving the static pages and API endpoints at:
👉 **[http://localhost:8000](http://localhost:8000)**

---

## 🤖 AI Agent Details

*   **Planner Agent (`backend/planner_agent.py`)**: Uses the new `google-genai` library with Gemini models. Employs Structured Outputs (`response_mime_type="application/json"` with Pydantic schema validation) to guarantee a strictly formatted list of day tasks.
*   **Chat Agent (`backend/chat_agent.py`)**: Gathers active profile settings, progress indicators, and today's task schedules as prompt context before query execution, enabling context-aware coaching answers.
*   **Progress Agent (`backend/progress_agent.py`)**: Computes consistency ratios, perfect study days, and study streaks (checking if tasks were completed today and yesterday).
