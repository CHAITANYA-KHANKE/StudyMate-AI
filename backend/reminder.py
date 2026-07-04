import datetime

class ReminderService:
    @staticmethod
    def generate_reminders(user_data: dict) -> list:
        profile = user_data.get("profile")
        study_plan = user_data.get("study_plan")
        progress = user_data.get("progress", {})

        if not profile or not study_plan:
            return []

        today_str = datetime.date.today().strftime("%Y-%m-%d")
        completed_set = set(progress.get("completed_tasks", []))
        reminders = []

        # Find today's tasks
        today_plan = None
        for day in study_plan.get("days", []):
            if day.get("date") == today_str:
                today_plan = day
                break

        if today_plan:
            for task in today_plan.get("tasks", []):
                if task.get("id") not in completed_set:
                    reminders.append({
                        "id": f"rem_{task.get('id')}",
                        "subject": task.get("subject"),
                        "topic": task.get("topic"),
                        "message": f"Don't forget to study {task.get('subject')} ({task.get('topic')}) today!",
                        "preferred_time": profile.get("preferred_time", "Afternoon"),
                        "estimated_hours": task.get("estimated_hours", 1)
                    })
        
        return reminders
