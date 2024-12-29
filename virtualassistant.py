import speech_recognition as sr
import pyttsx3
import calendar as c
from time import strftime
import tkinter as tk
from tkinter import *
from GoogleNews import GoogleNews
import pywhatkit as pwt


pyobj = pyttsx3.init()
recognizer = sr.Recognizer()


listen_counter = 0  
def speak(message):
    pyobj.say(message)
    pyobj.runAndWait()


def listen():
    global listen_counter
    if listen_counter >= 8:  
        speak("I've reached the maximum number of listens. Goodbye!")
        return
    
    listen_counter += 1  
    with sr.Microphone() as source:
        print(f"Listening... ({listen_counter}/8)")
        speak("You can speak now, I am listening.")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)  
            text = recognizer.recognize_google(audio).lower()
            print(f"You said: {text}")
            speak(f"You said: {text}")

        
            if "hello" in text:
                
                speak("Hello! It's wonderful to hear from you. How can I assist you today?")
            elif "search" in text:
                query = text.replace("search", "").strip()
                speak(f"Searching for {query}")
                pwt.search(query)
            elif "play" in text:
                query = text.replace("play", "").strip()
                speak(f"Playing {query} on YouTube")
                pwt.playonyt(query)
            elif "calendar" in text:
                speak("Displaying the calendar for 2025.")
                print(c.calendar(2025))
            elif "time" in text:
                speak("Opening the digital clock.")
                digital_clock()
            elif "news" in text:
                speak("Fetching the latest news.")
                display_news()
            elif "exit" in text or "stop" in text:
                speak("Goodbye!")
                return  # Exit the function to stop recursion

        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand what you said.")
        except sr.RequestError:
            speak("There was an issue connecting to the recognition service.")
        except Exception as e:
            speak("An unexpected error occurred.")
            print(e)
        finally:
            # Recursive call to listen again
            listen()

# Function to display a digital clock
def digital_clock():
    dc = tk.Tk()
    dc.title("Digital Clock")
    dc.geometry("500x200")

    def time_display():
        current_time = strftime("%H:%M:%S")
        l.config(text=current_time)
        l.after(1000, time_display)

    l = Label(dc, font=('Arial', 30), bg="white", fg="blue")
    l.pack()
    time_display()
    dc.mainloop()

# Function to display the latest news in a Tkinter window
def display_news():
    news_window = Tk()
    news_window.title("Latest News")
    news_window.geometry("1000x800")

    scrollbar = Scrollbar(news_window)
    scrollbar.pack(side=RIGHT, fill=Y)

    text_area = Text(news_window, wrap="word", yscrollcommand=scrollbar.set)
    text_area.pack(expand=True, fill="both")

    googlenews = GoogleNews(period='7d')
    googlenews.search('India')
    result = googlenews.result()

    if result:
        for x in result:
            news = f"Title: {x['title']}\nDate/Time: {x['date']}\nDescription: {x['desc']}\nLink: {x['link']}\n{'-'*50}\n"
            text_area.insert(END, news)
    else:
        text_area.insert(END, "No news found for the given search term.")

    scrollbar.config(command=text_area.yview)
    news_window.mainloop()

# Start listening for commands
listen()
