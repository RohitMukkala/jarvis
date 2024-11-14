# chatbot.py

import re
import engine.long_responses as long  # Ensure long_responses.py is in the same directory
from datetime import datetime

# from engine.reminders import set_reminder

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    percentage = float(message_certainty) / float(len(recognised_words))

    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    return int(percentage * 100) if has_required_words or single_response else 0

def check_all_messages(message):
    highest_prob_list = {}

    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    response("Hey there! How can I assist you today?", ['hey', 'hello', 'hi', 'greetings'], single_response=True)
    response("Goodbye! Have a great day!", ['bye', 'goodbye', 'see', 'later'], single_response=True)
    response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('Thank You', ['i', 'love', 'code', 'palace'], required_words=['code', 'palace'])
    response(long.R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])
    response("You're very welcome!", ['thanks', 'thank', 'appreciate'], single_response=True)
    response("Thank you! I'm here to help!", ['you', 'are', 'great', 'awesome', 'helpful'], required_words=['great'])
    response(long.C_DO, ['what', 'can', 'you', 'do'], required_words=['can', 'do'])
    response(f"The current time is {datetime.now().strftime('%H:%M:%S')}.", ['time', 'current', 'now'], required_words=['time'])
    response(f"Today's date is {datetime.now().strftime('%Y-%m-%d')}.", ['date', 'today'], required_words=['date', 'today'])
    response("I'm glad to hear that!", ['i', 'am', 'good', 'great', 'well', 'happy'], required_words=['good'])
    response("I'm here if you need to talk.", ['i', 'am', 'sad', 'unhappy', 'not', 'well'], required_words=['sad'])
    response(long.random_joke(), ['tell', 'me', 'a', 'joke'], required_words=['joke'])
    response("Of course! Let me know what you need help with.", ['help', 'assist', 'support'], required_words=['help'])
    response("I enjoy learning new things and helping people—24/7!", ['what', 'your', 'hobby'], required_words=['hobby'])
    # if "remind" in message or "reminder" in message:
    #     reminder_response = handle_reminder(message)
    #     return reminder_response if reminder_response else "Please specify a valid time for the reminder."

    response(long.get_news(), ['news', 'headlines', 'today'], required_words=['news'])


    if "weather" in message:
        city = " ".join(word for word in message if word not in ['what', 'is', 'the', 'weather', 'in'])
        if city:
            response(long.get_weather(city), ['weather', 'in'], required_words=['weather', 'in'])



# def handle_reminder(message):
#     # Extract time and message for the reminder
#     time_match = re.search(r'(\d{1,2}:\d{2})', message)
#     reminder_message = message.replace("remind me to", "").strip() if time_match else None

#     if time_match and reminder_message:
#         reminder_time_str = time_match.group(0)
#         reminder_time = datetime.strptime(reminder_time_str, "%H:%M").replace(
#             year=datetime.now().year, month=datetime.now().month, day=datetime.now().day
#         )
#         # Set the reminder
#         return set_reminder(reminder_message, reminder_time)
#     else:
#         return None


    best_match = max(highest_prob_list, key=highest_prob_list.get)
    return long.unknown() if highest_prob_list[best_match] < 1 else best_match

def get_response(user_input):
    split_message = re.split(r'\s|[,;:?.!-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response
