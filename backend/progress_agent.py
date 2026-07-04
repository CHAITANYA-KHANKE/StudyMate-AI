import datetime

class ProgressAgent:
    @staticmethod
    def calculate_metrics(user_data: dict) -> dict:
        profile = user_data.get("profile")
        study_plan = user_data.get("study_plan")
        progress = user_data.get("progress", {})
        
        if not profile or not study_plan:
            return {
                "completed_count": 0,
                "pending_count": 0,
                "percentage": 0,
                "streak": 0,
                "hours_completed": 0.0,
                "weekly_data": {"Mon": 0, "Tue": 0, "Wed": 0, "Thu": 0, "Fri": 0, "Sat": 0, "Sun": 0},
                "subject_completion": {}
            }

        completed_task_ids = set(progress.get("completed_tasks", []))
        
        all_tasks = []
        for day in study_plan.get("days", []):
            for task in day.get("tasks", []):
                all_tasks.append(task)
        
        total_tasks_count = len(all_tasks)
        completed_count = sum(1 for t in all_tasks if t.get("id") in completed_task_ids)
        pending_count = total_tasks_count - completed_count
        percentage = round((completed_count / total_tasks_count * 100), 1) if total_tasks_count > 0 else 0

        # Calculate completed study hours
        hours_completed = sum(t.get("estimated_hours", 0) for t in all_tasks if t.get("id") in completed_task_ids)
        hours_completed = round(hours_completed, 1)

        # Subject completion percentage
        subject_stats = {}
        for t in all_tasks:
            subject = t.get("subject")
            if subject not in subject_stats:
                subject_stats[subject] = {"total": 0, "completed": 0}
            subject_stats[subject]["total"] += 1
            if t.get("id") in completed_task_ids:
                subject_stats[subject]["completed"] += 1
        
        subject_completion = {}
        for sub, stats in subject_stats.items():
            sub_pct = round((stats["completed"] / stats["total"] * 100), 1) if stats["total"] > 0 else 0
            subject_completion[sub] = sub_pct

        # Weekly Progress: Tasks completed grouped by the day-of-week of the task's date
        weekly_data = {"Mon": 0, "Tue": 0, "Wed": 0, "Thu": 0, "Fri": 0, "Sat": 0, "Sun": 0}
        for day in study_plan.get("days", []):
            date_str = day.get("date")
            try:
                dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                day_name = dt.strftime("%a")
            except Exception:
                day_name = "Mon"
            
            day_tasks = day.get("tasks", [])
            completed_in_day = sum(1 for t in day_tasks if t.get("id") in completed_task_ids)
            if day_name in weekly_data:
                weekly_data[day_name] += completed_in_day

        streak = progress.get("streak", 0)

        # Calculate consistency status
        total_days = len(study_plan.get("days", []))
        completed_days_count = 0
        for day in study_plan.get("days", []):
            day_tasks = day.get("tasks", [])
            if len(day_tasks) > 0 and all(t.get("id") in completed_task_ids for t in day_tasks):
                completed_days_count += 1
        
        consistency_level = "Beginner"
        if streak >= 3:
            consistency_level = "Consistent Studier"
        if streak >= 7:
            consistency_level = "Ultimate Academic Warrior"

        return {
            "completed_count": completed_count,
            "pending_count": pending_count,
            "percentage": percentage,
            "streak": streak,
            "hours_completed": hours_completed,
            "weekly_data": weekly_data,
            "subject_completion": subject_completion,
            "consistency_level": consistency_level,
            "completed_days": completed_days_count,
            "total_days": total_days
        }

    @staticmethod
    def update_streak(progress: dict, completed_task_ids: list, study_plan: dict) -> int:
        today = datetime.date.today()
        today_str = today.strftime("%Y-%m-%d")
        yesterday_str = (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

        completed_set = set(completed_task_ids)
        
        # Check if tasks were completed today
        tasks_completed_today = 0
        for day in study_plan.get("days", []):
            if day.get("date") == today_str:
                tasks_completed_today += sum(1 for t in day.get("tasks", []) if t.get("id") in completed_set)

        current_streak = progress.get("streak", 0)
        last_active = progress.get("last_active_date")

        if tasks_completed_today > 0:
            if last_active != today_str:
                # If last active was yesterday, increment streak
                if last_active == yesterday_str:
                    current_streak += 1
                elif current_streak == 0:
                    current_streak = 1
                else:
                    # Broke streak in between, reset to 1
                    current_streak = 1
                progress["last_active_date"] = today_str
        else:
            # Check if we broke streak (last active is older than yesterday)
            if last_active and last_active != today_str and last_active != yesterday_str:
                current_streak = 0
        
        progress["streak"] = current_streak
        return current_streak
