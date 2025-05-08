import tkinter as tk               #for creating gui window
from tkinter import scrolledtext   #for scrollable text area in the chat
import random                      #to randomly pick a bot response
import datetime                    

# ------------------ Chatbot Logic ------------------
#this dictionary defines different topics the chatbot will understand, keywords are the words the chatbot will look for in the user's input
intents = {
    "greeting": {
        "keywords": ["hi", "hello", "hey", "good morning", "good evening"],
        "responses": ["Hello! 😊", "Hey there! 👋", "Hi, how can I help you today? 🤖"]
    },
    "how_are_you": {
        "keywords": ["how are you", "how's it going", "what's up"],
        "responses": ["I'm good, thanks for asking! 😄", "Doing great! What about you? 💪"]
    },
    "name_query": {
        "keywords": ["your name", "who are you"],
        "responses": ["I'm RuleBot 3.5 – your chatbot friend. 🤖"]
    },
    "time": {
        "keywords": ["time", "current time", "tell me the time"],
        "responses": [f"The time is {datetime.datetime.now().strftime('%I:%M %p')} 🕒"]
    },
    "thanks": {
        "keywords": ["thanks", "thank you", "thx"],
        "responses": ["You're welcome! 😊", "Anytime! 🙌", "Glad to help! 👍"]
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
    },
    "bye": {
        "keywords": ["bye", "goodbye", "see you"],
        "responses": ["Goodbye! 👋", "Take care! 💖", "See you later! 😄"]
    }
}

def get_intent(user_input):
    user_input = user_input.lower()    #converts to lowercase for case-sensitive matching
    for intent, data in intents.items():   #looping through chatbot logic
        for keyword in data["keywords"]:
            if keyword in user_input:
                return intent
    return None

def get_bot_response(user_input):
    intent = get_intent(user_input)
    if intent:
        return random.choice(intents[intent]["responses"])   #randomly selecting matching response
    else:
        return "I'm not sure I understand that 🤔"

# ------------------ GUI Setup ------------------

def send_message():
    user_input = user_entry.get()       #to get text from entry field
    if user_input.strip() == "":        #strip() is for white spaces or empty
        return

    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, "You: " + user_input + "\n")   #display user message
    bot_response = get_bot_response(user_input)
    chat_area.insert(tk.END, "RuleBot: " + bot_response + "\n\n")   #display bot response
    chat_area.config(state=tk.DISABLED)          #to make chat area read-only

    user_entry.delete(0, tk.END)       #clearing input field

# ------------------ Main Window ------------------

window = tk.Tk()
window.title("RuleBot Chat")
window.geometry("400x500")           #window size
window.config(bg="#f0f0f0")          #bg color

chat_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=50, height=20, font=("Arial", 11))
chat_area.config(state=tk.DISABLED)
chat_area.pack(pady=10)

user_entry = tk.Entry(window, width=40, font=("Arial", 12))
user_entry.pack(padx=10, pady=5)

send_button = tk.Button(window, text="Send", command=send_message, font=("Arial", 12), bg="#4CAF50", fg="white")
send_button.pack(pady=5)

window.mainloop()        #starts tkinter loop