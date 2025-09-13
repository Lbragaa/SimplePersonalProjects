import json
import datetime
import random
import os

# === Configuration ===
TASKS_FILE = "tasks.json"
GOALS_FILE = "goals.json"
DEADLINES_FILE = "deadlines.json"

# === Load JSON helper ===
def load_json(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# === Main CLI ===
def main():
    today = datetime.date.today()
    print(f"\n📆 Today is: {today.strftime('%A, %B %d')}")

    # Load tasks
    tasks = load_json(TASKS_FILE)
    today_tasks = [t for t in tasks if t.get("day") == today.strftime('%A')]
    print("📌 You have {} tasks today:".format(len(today_tasks)))
    for t in today_tasks:
        status = "[x]" if t.get("done") else "[ ]"
        print(f"   - {status} {t.get('title')}")

    # Load deadlines
    deadlines = load_json(DEADLINES_FILE)
    upcoming = []
    for d in deadlines:
        due_date = datetime.datetime.strptime(d["due"], "%Y-%m-%d").date()
        days_left = (due_date - today).days
        if 0 <= days_left <= 7:
            upcoming.append((d["title"], days_left))

    print("\n⏰ Upcoming deadlines:")
    for title, days_left in sorted(upcoming, key=lambda x: x[1]):
        print(f"   - {title}: in {days_left} day{'s' if days_left != 1 else ''}")

    # Load goals
    goals = load_json(GOALS_FILE)
    print("\n🎯 Daily Habit Reminder:")
    for g in goals:
        print(f"   - {g}")

    # Suggested task
    all_topics = [
        "Review AVL Tree insertion cases",
        "Implement linked list in C",
        "Practice SQL JOINS",
        "Do 1 Leetcode easy problem",
        "Read 1 article on Time Complexity"
    ]
    print("\n💡 Suggested task:")
    print(f"   → {random.choice(all_topics)}")

    print("\n✅ Ready to go. Make today count!")

if __name__ == "__main__":
    main()
