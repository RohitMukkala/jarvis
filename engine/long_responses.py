# long_responses.py

import random

R_EATING = "I don't like eating anything because I'm a Bot obviously!"

def unknown():
    responses = [
        "Could you please re-phrase that?",
        "...",
        "Sounds about right.",
        "What does that mean?"
    ]
    return random.choice(responses)
