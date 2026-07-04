import json
import datetime
from google import genai
from google.genai import types

class ChatAgent:
    def __init__(self):
        self.client = genai.Client()
        self.model_name = "gemini-2.5-flash"

    def get_response(self, user_message: str, user_data: dict) -> str:
        profile = user_data.get("profile", {})
        study_plan = user_data.get("study_plan", {})
        progress = user_data.get("progress", {})

        system_instruction = """
        You are StudyMate AI, a supportive, practical, and highly motivating AI study coach.
        You assist students in exam preparation, planning, revision tips, and staying focused.
        Keep your replies short (2-4 sentences), encouraging, and actionable.
        Avoid verbose paragraphs. Give direct answers with bullet points if helpful.
        """

        # Compile current student progress context
        context_parts = []
        if profile:
            context_parts.append(f"Student: {profile.get('name')}")
            context_parts.append(f"Subjects: {', '.join(profile.get('subjects', []))}")
            context_parts.append(f"Exam Date: {profile.get('exam_date')}")
            context_parts.append(f"Daily study budget: {profile.get('daily_hours')} hours")
        
        if progress:
            completed_tasks = progress.get("completed_tasks", [])
            streak = progress.get("streak", 0)
            context_parts.append(f"Tasks completed so far: {len(completed_tasks)}")
            context_parts.append(f"Current study streak: {streak} days")

        # Find today's tasks to answer queries like "what should I study today?"
        today_str = datetime.date.today().strftime("%Y-%m-%d")
        if study_plan and "days" in study_plan:
            today_plan = None
            for day in study_plan.get("days", []):
                if day.get("date") == today_str:
                    today_plan = day
                    break
            
            if today_plan:
                today_tasks_desc = []
                for t in today_plan.get("tasks", []):
                    status = "Done" if t.get("id") in progress.get("completed_tasks", []) else "Pending"
                    today_tasks_desc.append(f"- {t.get('subject')}: {t.get('topic')} ({t.get('estimated_hours')}h) [{status}]")
                context_parts.append(f"Today's Study Plan ({today_str}):\n" + "\n".join(today_tasks_desc))
            else:
                context_parts.append("No specific study plan scheduled for today.")

        context_string = "\n".join(context_parts)
        
        prompt = f"""
        {system_instruction}

        STUDENT CURRENT STATUS:
        {context_string}

        QUESTION: "{user_message}"

        Provide your direct, encouraging response:
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=350,
                ),
            )
            return response.text.strip()
        except Exception as e:
            print(f"Error in ChatAgent Gemini call: {e}")
            return "I ran into a small issue connecting to the AI agent. Let's try again in a moment! In the meantime, remember to take short breaks to keep your focus sharp."
