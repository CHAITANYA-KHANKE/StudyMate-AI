import datetime

class NotificationService:
    @staticmethod
    def get_notifications(user_data: dict) -> list:
        profile = user_data.get("profile")
        progress = user_data.get("progress", {})
        study_plan = user_data.get("study_plan", {})
        
        notifications = []

        if not profile:
            notifications.append({
                "id": "setup_profile",
                "title": "Setup Required",
                "message": "Welcome to StudyMate AI! Create a Student Profile to generate your personalized study plan.",
                "type": "info",
                "timestamp": datetime.datetime.now().strftime("%I:%M %p")
            })
            return notifications

        # Exam date warning
        exam_date_str = profile.get("exam_date")
        if exam_date_str:
            try:
                exam_date = datetime.datetime.strptime(exam_date_str, "%Y-%m-%d").date()
                days_left = (exam_date - datetime.date.today()).days
                if days_left > 0:
                    notifications.append({
                        "id": "exam_warning",
                        "title": "Exam Countdown",
                        "message": f"{days_left} days remaining until your exam. Plan your revision wisely!",
                        "type": "warning",
                        "timestamp": datetime.datetime.now().strftime("%I:%M %p")
                    })
                elif days_left == 0:
                    notifications.append({
                        "id": "exam_today",
                        "title": "Exam Day!",
                        "message": "Today is the exam day! Stay calm and give it your best shot!",
                        "type": "error",
                        "timestamp": datetime.datetime.now().strftime("%I:%M %p")
                    })
            except Exception:
                pass

        # Streak achievements
        streak = progress.get("streak", 0)
        if streak >= 3:
            notifications.append({
                "id": "streak_milestone",
                "title": "Streak Milestone!",
                "message": f"Amazing! You've maintained a {streak}-day study consistency.",
                "type": "success",
                "timestamp": datetime.datetime.now().strftime("%I:%M %p")
            })
        elif streak > 0:
            notifications.append({
                "id": "streak_active",
                "title": "Streak Active",
                "message": f"You are on a {streak}-day study streak. Don't break the chain!",
                "type": "success",
                "timestamp": datetime.datetime.now().strftime("%I:%M %p")
            })

        # Today's tasks alert
        today_str = datetime.date.today().strftime("%Y-%m-%d")
        if study_plan:
            today_plan = None
            for day in study_plan.get("days", []):
                if day.get("date") == today_str:
                    today_plan = day
                    break
            
            if today_plan:
                completed_tasks = progress.get("completed_tasks", [])
                pending_count = sum(1 for t in today_plan.get("tasks", []) if t.get("id") not in completed_tasks)
                if pending_count > 0:
                    notifications.append({
                        "id": "tasks_pending",
                        "title": "Study Tasks Pending",
                        "message": f"You have {pending_count} study tasks remaining for today.",
                        "type": "info",
                        "timestamp": datetime.datetime.now().strftime("%I:%M %p")
                    })
                else:
                    notifications.append({
                        "id": "tasks_completed",
                        "title": "All Tasks Completed!",
                        "message": "Outstanding work! You've finished all of today's study tasks.",
                        "type": "success",
                        "timestamp": datetime.datetime.now().strftime("%I:%M %p")
                    })

        return notifications
