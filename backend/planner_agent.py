import os
import json
from datetime import datetime, date
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

class StudyTask(BaseModel):
    id: str = Field(description="Unique task identifier, e.g. day1_task1")
    subject: str = Field(description="The name of the subject")
    topic: str = Field(description="The specific topic to study")
    estimated_hours: float = Field(description="Estimated study duration in hours")
    revision_session: str = Field(description="Short description of what to revise")
    practice_questions: list[str] = Field(description="List of 1-3 practice question prompts or exercises")

class DayPlan(BaseModel):
    date: str = Field(description="Date string formatted as YYYY-MM-DD")
    day_number: int = Field(description="The day index, starting from 1")
    tasks: list[StudyTask] = Field(description="List of tasks for this day")

class StudyPlanResponse(BaseModel):
    motivation_message: str = Field(description="A highly encouraging motivational message custom-made for the student's situation")
    days: list[DayPlan] = Field(description="List of daily plans leading up to the exam")

class PlannerAgent:
    def __init__(self):
        # The google-genai client automatically uses GEMINI_API_KEY from environment
        self.client = genai.Client()
        self.model_name = "gemini-2.5-flash"

    def generate_plan(self, profile: dict) -> dict:
        name = profile["name"]
        subjects = profile["subjects"]
        exam_date_str = profile["exam_date"]
        daily_hours = profile["daily_hours"]
        difficulty = profile["difficulty"]
        preferred_time = profile["preferred_time"]

        # Calculate days until exam
        today = date.today()
        exam_date = datetime.strptime(exam_date_str, "%Y-%m-%d").date()
        days_remaining = (exam_date - today).days

        if days_remaining <= 0:
            raise ValueError("Exam date must be in the future.")

        # Limit planned days to prevent API payload explosion, maximum 14 days for high detail
        days_to_plan = min(days_remaining, 14)
        
        # Calculate dates list
        from datetime import timedelta
        dates_list = [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days_to_plan)]

        prompt = f"""
        You are StudyMate AI, an expert agentic study planner.
        Generate a highly structured, day-by-day study schedule for a student preparing for exams.

        Student Details:
        - Name: {name}
        - Subjects: {', '.join(subjects)}
        - Exam Date: {exam_date_str} ({days_remaining} days left; generate plan for the next {days_to_plan} days)
        - Daily Study Budget: {daily_hours} hours
        - Preparation Pace: {difficulty} (Easy = slower pace, Medium = balanced, Hard = fast-paced with focus on mock questions)
        - Preferred Peak Study Time: {preferred_time}

        Available Dates to Fill (in order):
        {', '.join(dates_list)}

        Requirements:
        1. Distribute the study subjects intelligently across the dates.
        2. Define highly specific, actionable study topics (not vague terms).
        3. Keep the total estimated_hours per day within the budget of {daily_hours} hours.
        4. Add a specific revision session description for each day to reinforce learning.
        5. Suggest 1-3 practice exercises or sample exam questions for each topic.
        6. Create a personalized, encouraging motivation message.
        7. Assign unique, sequential string IDs to each task, e.g. "day1_task1", "day1_task2", "day2_task1", etc.
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=StudyPlanResponse,
                    temperature=0.3,
                ),
            )
            plan_data = json.loads(response.text)
            return plan_data
        except Exception as e:
            print(f"Error calling Gemini in PlannerAgent: {e}")
            return self._generate_mock_plan(subjects, dates_list, daily_hours)

    def _generate_mock_plan(self, subjects: list, dates_list: list, daily_hours: float) -> dict:
        days = []
        for i, date_str in enumerate(dates_list):
            tasks = []
            for j, subject in enumerate(subjects):
                tasks.append({
                    "id": f"day{i+1}_task{j+1}",
                    "subject": subject,
                    "topic": f"Essential Principles of {subject} (Section {i+1})",
                    "estimated_hours": round(max(0.5, daily_hours / len(subjects)), 1),
                    "revision_session": f"Briefly review yesterday's {subject} concepts.",
                    "practice_questions": [f"Explain the core definition of {subject} in your own words."]
                })
            days.append({
                "date": date_str,
                "day_number": i + 1,
                "tasks": tasks
            })
        return {
            "motivation_message": "Let's make this study session count! Keep moving forward.",
            "days": days
        }
