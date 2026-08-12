print("================================")
print("        STUDYPULSE 🧠")
print("   Study Productivity Tracker")
print("================================")

name = input("Enter your name: ")
subject = input("Enter subject: ")

study_minutes = int(input("Study time (minutes): "))
break_minutes = int(input("Break time (minutes): "))
tasks_planned = int(input("Tasks planned: "))
tasks_completed = int(input("Tasks completed: "))

if study_minutes <= 0:
    print("❌ Study time must be greater than 0.")
    exit()

if break_minutes < 0:
    print("❌ Break time cannot be negative.")
    exit()

if tasks_planned <= 0:
    print("❌ Tasks planned must be greater than 0.")
    exit()

if tasks_completed < 0 or tasks_completed > tasks_planned:
    print("❌ Completed tasks must be between 0 and planned tasks.")
    exit()

task_completion = (tasks_completed / tasks_planned) * 100
focus_efficiency = (study_minutes / (study_minutes + break_minutes)) * 100
productivity_score = (task_completion * 0.60) + (focus_efficiency * 0.40)

print()
print("Welcome,", name)
print("Today's subject:", subject)

print()
print("--------------------------------")
print("        STUDY SUMMARY")
print("--------------------------------")
print("Subject:", subject)
print("Study time:", study_minutes, "minutes")
print("Break time:", break_minutes, "minutes")
print("Task completion:", round(task_completion, 2), "%")
print("Focus efficiency:", round(focus_efficiency, 2), "%")
print("Productivity score:", round(productivity_score, 2), "/ 100")


if productivity_score >= 90:
    print("🔥 Outstanding study session!")
elif productivity_score >= 75:
    print("🚀 Great study session!")
elif productivity_score >= 60:
    print("👍 Good session, but there is room for improvement.")
else:
    print("💪 Keep going! Try to improve your focus and task completion.")


if task_completion < focus_efficiency:
    print("💡 Tip: Try completing more of your planned tasks.")
elif focus_efficiency < task_completion:
    print("💡 Tip: Reduce your break time and improve your focus.")
else:
    print("💡 Tip: Keep maintaining this balance!")
print("--------------------------------")