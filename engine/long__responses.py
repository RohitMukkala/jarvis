# long_responses.py

import random

import requests




R_EATING = "I don't like eating anything because I'm a Bot obviously!"
C_DO = "I'm here to assist you with tasks, answer questions, and keep you entertained!"

def unknown():
    responses = [
        "Could you please re-phrase that?",
        "Sounds about right.",
        "What does that mean?"
    ]
    return random.choice(responses)


JOKES = [
    "Why don’t scientists trust atoms? Because they make up everything!",
    "Why did the bicycle fall over? Because it was two-tired!",
    "How does a computer tell you a joke? With a bit of byte!"
]

def random_joke():
    return random.choice(JOKES)


API_KEY = "Your API_KEY"  

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        weather_desc = data["weather"][0]["description"]
        return f"The current temperature in {city} is {temp}°C with {weather_desc}."
    else:
        return "I'm sorry, I couldn't retrieve the weather for that location."
    


NEWS_API_KEY = "Your API_KEY"  

def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        headlines = [article["title"] for article in articles[:5]]  # Get top 5 headlines
        return "Here are the top news headlines:\n" + "\n".join(headlines)
    else:
        return "I'm sorry, I couldn't fetch the news at the moment."
    
