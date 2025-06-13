import tkinter as tk
from tkinter import Scrollbar, END
import speech_recognition as sr
import pyttsx3
import threading

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Simple chatbot logic
def get_bot_response(user_input):
    user_input = user_input.lower()
    if "hello" in user_input or "hi" in user_input:
        return "Hello! How can I help you today?"
    elif "how are you" in user_input:
        return "I'm just a bot, but I'm doing fine!"
    elif "bye" in user_input:
        return "Goodbye! Have a great day!"
    else:
        return "I'm not sure I understand. Can you rephrase?"

# Send message from user to chatbot
def send_message():
    user_input = entry_box.get()
    if user_input.strip() != "":
        chat_log.config(state=tk.NORMAL)
        chat_log.insert(END, "You: " + user_input + "\n")
        bot_response = get_bot_response(user_input)
        chat_log.insert(END, "Bot: " + bot_response + "\n\n")
        speak(bot_response)
        chat_log.config(state=tk.DISABLED)
        entry_box.delete(0, END)
        chat_log.see(END)

# Voice input function (in a thread)
def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            entry_box.delete(0, END)
            entry_box.insert(0, text)
            send_message()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
        except sr.RequestError:
            speak("Speech service is unavailable.")
        except sr.WaitTimeoutError:
            speak("No speech detected.")

def start_voice_thread():
    threading.Thread(target=voice_input).start()

# Create main window
window = tk.Tk()
window.title("Chatbot with Voice Support")
window.geometry("400x500")

# Chat log text area
chat_log = tk.Text(window, bd=1, bg="white", font=("Arial", 12), wrap=tk.WORD)
chat_log.config(state=tk.DISABLED)
chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Scrollbar
scrollbar = Scrollbar(chat_log)
chat_log['yscrollcommand'] = scrollbar.set
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Entry box to type message
entry_box = tk.Entry(window, bd=1, font=("Arial", 12))
entry_box.pack(padx=10, pady=(0,10), fill=tk.X)

# Send button
send_button = tk.Button(window, text="Send", width=10, command=send_message)
send_button.pack(pady=(0, 5))

# Voice button
voice_button = tk.Button(window, text="🎤 Voice", width=10, command=start_voice_thread)
voice_button.pack()

# Run the app
window.mainloop()
