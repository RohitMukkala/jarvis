# import threading
# import time
# from datetime import datetime, timedelta

# reminders = []

# def set_reminder(message, reminder_time):
#     # Calculate time delay in seconds
#     delay = (reminder_time - datetime.now()).total_seconds()
#     if delay > 0:
#         # Schedule reminder
#         reminder = threading.Timer(delay, show_reminder, [message])
#         reminders.append(reminder)
#         reminder.start()
#         return f"Reminder set for {reminder_time.strftime('%H:%M:%S')}."
#     else:
#         return "The specified time has already passed. Please choose a future time."

# def show_reminder(message):
#     print(f"Reminder: {message}")

# # Clear all reminders (useful for testing)
# def clear_reminders():
#     for reminder in reminders:
#         reminder.cancel()
#     reminders.clear()
