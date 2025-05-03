import random
import datetime
import time

# ------------------ Settings ------------------
USE_TYPING_EFFECT = True
THEME = "dark"  # options: 'light', 'dark'

# ------------------ Responses & Keywords ------------------

intents = {
    "greeting": {
        "keywords": ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"],
        "responses": ["Hello! 😊", "Hey there! 👋", "Hi, how can I help you today? 🤖"]
    },
    "how_are_you": {
        "keywords": ["how are you", "how's it going", "what's up"],
        "responses": ["I'm good, thanks for asking! 😄", "Doing great! What about you? 💪"]
    },
    "name_query": {
        "keywords": ["your name", "who are you"],
        "responses": ["I'm RuleBot 3.5 – your friendly chatbot assistant. 🤖", "RuleBot here! Always ready to chat. 🧠"]
    },
    "capabilities": {
        "keywords": ["what can you do", "help", "features"],
        "responses": ["I can chat with you, tell the time, remember your name, cheer you up, and more! ✨"]
    },
    "time": {
        "keywords": ["time", "current time", "tell me the time"],
        "responses": [f"The current time is {datetime.datetime.now().strftime('%I:%M %p')} 🕒"]
    },
    "thanks": {
        "keywords": ["thanks", "thank you", "thx"],
        "responses": ["You're welcome! 😊", "Anytime! 🙌", "Glad to help! 👍"]
    },
    "bye": {
        "keywords": ["bye", "goodbye", "see you"],
        "responses": ["Goodbye! Talk to you soon. 👋", "Take care! 💖", "See you later! 😄"]
    },
    "jokes": {
        "keywords": ["joke", "make me laugh", "funny"],
        "responses": [
            "Why did the computer go to the doctor? Because it had a virus! 😂",
            "I would tell you a UDP joke... but you might not get it. 😅",
            "Why don't robots panic? Because they have nerves of steel! 🤖"
        ]
    },
    "mood_sad": {
        "keywords": ["sad", "depressed", "unhappy", "upset"],
        "responses": [
            "I'm here for you. Everything will be okay. 💖",
            "Sending you virtual hugs 🤗",
            "Tough times don’t last, but tough people do 💪"
        ]
    },
    "mood_happy": {
        "keywords": ["happy", "excited", "joyful", "glad"],
        "responses": ["Yay! I’m happy to hear that! 😄", "That’s awesome! Let’s keep the good vibes going 🎉"]
    }
}

# ------------------ Time Greeting ------------------

def time_greeting():
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "Good morning! 🌅"
    elif hour < 18:
        return "Good afternoon! ☀️"
    else:
        return "Good evening! 🌙"

# ------------------ Response Matching ------------------

def get_intent(user_input):
    user_input = user_input.lower()
    for intent, data in intents.items():
        for keyword in data["keywords"]:
            if keyword in user_input:
                return intent
    return None

def reply(text):
    if USE_TYPING_EFFECT:
        for char in text:
            print(char, end='', flush=True)
            time.sleep(0.02)
        print()
    else:
        print(text)

# ------------------ Main Chat Loop ------------------

print("RuleBot 3.5:", time_greeting())
reply("Ask me anything! Type 'bye' to exit.\n")

user_name = None

while True:
    user_input = input("You: ").strip().lower()

    if "my name is" in user_input:
        user_name = user_input.split("my name is")[-1].strip().capitalize()
        reply(f"Nice to meet you, {user_name}! 😄")
        continue

    if "what's my name" in user_input or "do you remember me" in user_input:
        if user_name:
            reply(f"Of course! You're {user_name} 😎")
        else:
            reply("I don't know your name yet! Tell me by saying 'my name is ...'")
        continue

    intent = get_intent(user_input)

    if intent == "bye":
        reply(random.choice(intents[intent]["responses"]))
        break
    elif intent:
        reply(random.choice(intents[intent]["responses"]))
    else:
        reply("Hmm... I didn't catch that. Try asking me something else. 🤔")