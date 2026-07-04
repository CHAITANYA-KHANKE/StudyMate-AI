import os
import json
import datetime
from fastapi import FastAPI, HTTPException, Header
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List, Optional

# Import agents and services
from backend.planner_agent import PlannerAgent
from backend.chat_agent import ChatAgent
from backend.progress_agent import ProgressAgent
from backend.notification import NotificationService
from backend.reminder import ReminderService

app = FastAPI(title="StudyMate AI Backend")

DB_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "database", "users.json"))

def load_all_data() -> dict:
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_all_data(data: dict):
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_user_data(user_id: str) -> dict:
    all_data = load_all_data()
    if user_id not in all_data:
        all_data[user_id] = {
            "profile": None,
            "study_plan": None,
            "progress": {
                "completed_tasks": [],
                "daily_study_hours": {},
                "streak": 0,
                "last_active_date": None
            },
            "notifications": [],
            "settings": {
                "theme": "light",
                "notifications_enabled": True
            }
        }
        save_all_data(all_data)
    return all_data[user_id]

def save_user_data(user_id: str, user_data: dict):
    all_data = load_all_data()
    all_data[user_id] = user_data
    save_all_data(all_data)

# Models for request validation
class SetupProfile(BaseModel):
    name: str
    college: str
    subjects: List[str]
    exam_date: str
    daily_hours: float
    difficulty: str
    preferred_time: str

class ChatMessage(BaseModel):
    message: str

class SettingsUpdate(BaseModel):
    name: str
    subjects: List[str]
    exam_date: str
    daily_hours: float
    theme: str
    notifications_enabled: bool

# Initialize agents
planner = PlannerAgent()
chat_agent = ChatAgent()

# API Endpoints

@app.post("/api/setup")
def setup_student(profile: SetupProfile, x_user_id: str = Header(default="default_user")):
    data = load_user_data(x_user_id)
    data["profile"] = profile.model_dump()
    
    try:
        # Generate plan using Gemini planner agent
        plan = planner.generate_plan(data["profile"])
        data["study_plan"] = plan
        
        # Reset progress for new setup
        data["progress"] = {
            "completed_tasks": [],
            "daily_study_hours": {},
            "streak": 0,
            "last_active_date": None
        }
        data["notifications"] = []
        save_user_data(x_user_id, data)
        return {"status": "success", "message": "Study plan generated successfully!", "plan": plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/dashboard")
def get_dashboard(x_user_id: str = Header(default="default_user")):
    data = load_user_data(x_user_id)
    profile = data.get("profile")
    study_plan = data.get("study_plan")
    progress = data.get("progress", {})
    
    if not profile or not study_plan:
        return {"setup_required": True}
    
    # Calculate days remaining
    today = datetime.date.today()
    exam_date = datetime.datetime.strptime(profile["exam_date"], "%Y-%m-%d").date()
    days_remaining = max(0, (exam_date - today).days)
    
    today_str = today.strftime("%Y-%m-%d")
    tomorrow_str = (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    
    # Extract tasks
    today_tasks = []
    tomorrow_tasks = []
    upcoming_revisions = []
    
    completed_task_ids = progress.get("completed_tasks", [])
    
    for day in study_plan.get("days", []):
        day_date = day.get("date")
        if day_date == today_str:
            today_tasks = day.get("tasks", [])
            upcoming_revisions.append({
                "subject": "General", 
                "revision": day.get("tasks", [{}])[0].get("revision_session", "Review previous concepts") if day.get("tasks") else "Review topics"
            })
        elif day_date == tomorrow_str:
            tomorrow_tasks = day.get("tasks", [])
            
    # Fallback to day indices if dates don't match exactly
    if not today_tasks and len(study_plan.get("days", [])) > 0:
        today_tasks = study_plan["days"][0].get("tasks", [])
        upcoming_revisions.append({"subject": "General", "revision": "Review basic concepts"})
    if not tomorrow_tasks and len(study_plan.get("days", [])) > 1:
        tomorrow_tasks = study_plan["days"][1].get("tasks", [])

    # Calculate metrics
    metrics = ProgressAgent.calculate_metrics(data)
    notifications = NotificationService.get_notifications(data)
    reminders = ReminderService.generate_reminders(data)

    total_subjects = len(profile.get("subjects", []))
    
    return {
        "setup_required": False,
        "student_name": profile.get("name"),
        "days_remaining": days_remaining,
        "today_tasks": today_tasks,
        "tomorrow_tasks": tomorrow_tasks,
        "upcoming_revisions": upcoming_revisions,
        "total_subjects": total_subjects,
        "metrics": metrics,
        "motivation_message": study_plan.get("motivation_message", "Keep learning!"),
        "notifications": notifications,
        "reminders": reminders
    }

@app.get("/api/study-plan")
def get_study_plan(x_user_id: str = Header(default="default_user")):
    data = load_user_data(x_user_id)
    if not data.get("study_plan"):
        return {"setup_required": True}
    return {
        "setup_required": False,
        "profile": data.get("profile"),
        "study_plan": data.get("study_plan"),
        "completed_tasks": data.get("progress", {}).get("completed_tasks", [])
    }

@app.post("/api/study-plan/toggle-task")
def toggle_task(body: dict, x_user_id: str = Header(default="default_user")):
    task_id = body.get("task_id")
    if not task_id:
        raise HTTPException(status_code=400, detail="task_id is required")
        
    data = load_user_data(x_user_id)
    progress = data.get("progress", {})
    completed_tasks = progress.get("completed_tasks", [])
    
    if task_id in completed_tasks:
        completed_tasks.remove(task_id)
    else:
        completed_tasks.append(task_id)
        
    progress["completed_tasks"] = completed_tasks
    
    # Recalculate streak
    if data.get("study_plan"):
        ProgressAgent.update_streak(progress, completed_tasks, data["study_plan"])
        
    data["progress"] = progress
    save_user_data(x_user_id, data)
    
    # Recalculate metrics for UI update
    metrics = ProgressAgent.calculate_metrics(data)
    return {"status": "success", "completed_tasks": completed_tasks, "metrics": metrics}

@app.post("/api/chat")
def chat(message: ChatMessage, x_user_id: str = Header(default="default_user")):
    data = load_user_data(x_user_id)
    response = chat_agent.get_response(message.message, data)
    return {"response": response}

@app.get("/api/progress")
def get_progress(x_user_id: str = Header(default="default_user")):
    data = load_user_data(x_user_id)
    if not data.get("profile") or not data.get("study_plan"):
        return {"setup_required": True}
    metrics = ProgressAgent.calculate_metrics(data)
    return {"setup_required": False, "metrics": metrics}

@app.get("/api/settings")
def get_settings(x_user_id: str = Header(default="default_user")):
    data = load_user_data(x_user_id)
    return {
        "profile": data.get("profile"),
        "settings": data.get("settings", {"theme": "light", "notifications_enabled": True})
    }

@app.post("/api/settings")
def update_settings(settings: SettingsUpdate, x_user_id: str = Header(default="default_user")):
    data = load_user_data(x_user_id)
    if not data.get("profile"):
        raise HTTPException(status_code=400, detail="No profile to update. Please complete setup first.")
        
    data["profile"]["name"] = settings.name
    data["profile"]["subjects"] = settings.subjects
    data["profile"]["exam_date"] = settings.exam_date
    data["profile"]["daily_hours"] = settings.daily_hours
    
    data["settings"]["theme"] = settings.theme
    data["settings"]["notifications_enabled"] = settings.notifications_enabled
    
    save_user_data(x_user_id, data)
    return {"status": "success", "message": "Settings updated successfully!"}

@app.post("/api/reset")
def reset_all(x_user_id: str = Header(default="default_user")):
    data = {
        "profile": None,
        "study_plan": None,
        "progress": {
            "completed_tasks": [],
            "daily_study_hours": {},
            "streak": 0,
            "last_active_date": None
        },
        "notifications": [],
        "settings": {
            "theme": "light",
            "notifications_enabled": True
        }
    }
    save_user_data(x_user_id, data)
    return {"status": "success", "message": "All data has been reset."}

# Mount static files and redirect routes

frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

# Redirect routes for cleaner browser URLs
@app.get("/")
def route_root():
    return RedirectResponse(url="/static/home/index.html")

@app.get("/home")
def route_home():
    return RedirectResponse(url="/static/home/index.html")

@app.get("/setup")
def route_setup():
    return RedirectResponse(url="/static/setup/index.html")

@app.get("/dashboard")
def route_dashboard():
    return RedirectResponse(url="/static/dashboard/index.html")

@app.get("/study-plan")
def route_study_plan():
    return RedirectResponse(url="/static/study-plan/index.html")

@app.get("/progress")
def route_progress():
    return RedirectResponse(url="/static/progress/index.html")

@app.get("/chat")
def route_chat():
    return RedirectResponse(url="/static/chat/index.html")

@app.get("/settings")
def route_settings():
    return RedirectResponse(url="/static/settings/index.html")
