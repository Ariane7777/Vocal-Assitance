import customtkinter as ctk 
import speech_recognition as sr 
import pyttsx3
from youtube_search import YoutubeSearch 
import webbrowser
import urllib.parse
import pyaudio
import os
import subprocess
import platform
from datetime import datetime



VLC_PATH = r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"
MUSIC_PATH = r"C:\Users\Andrea\Documents\songs"

#initialising the vocal recognition et la synthése vocal
recognizer = sr.Recognizer() 
engine = pyttsx3.init()
#function to talk
def speak(text):
    engine.say(text)
    engine.runAndWait() #is use to ensure the speech will execute before the code
#function to listen and recognize the voice
def recognize_speech():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source) # eliminate noise from source
        print("Speak now")
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio, language="en-EN")
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("I haven't listen to what you just said")
            return ""
        except sr.RequestError:
            speak("Connection Error")
            return ""

def search_google(query):
    query = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak(f"here are the search results for {query}")

#function to read the date and time
def tell_time():
    current_time=datetime.now().strftime("%H:%M")
    speak(f"The time is {current_time}")
def tell_date():
    current_date=datetime.now().strftime("%A %d %B %Y")
    speak(f"Today is {current_date}")

    
#function to open files or folders
def open_folder(path):
    if os.path.exists(path):
        os.startfile(path)
        speak("Opening folder")
    else:
        speak("Folder not found")

#function to open vlc
def play_vlc(media_path):
    if os.path.exists(media_path):
        subprocess.Popen([VLC_PATH,media_path])
        speak("Playing media in VLC")
    else:
        speak("VLC not found")

#function to open applications
def open_app(app):
    apps={
        "vlc":VLC_PATH,
        "notepad":"notepad",
        "chrome":r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "xampp":r"C:\xampp\xampp-control.exe",
        "github":r"C:\Users\Andrea\AppData\Local\GitHubDesktop\GitHubDesktop.exe"
    }
    if app in apps:
        subprocess.Popen(apps[app])
        speak(f"Opening {app}")
    else:
        speak("Application not found")

#function to execute the  vocal commands
def execute_command():
    command = recognize_speech()
    # print("COMMAND RECEIVED:",command)
    if not command:
        return
        
    if "play local music" in command or "play music offline" in command:
        play_vlc(MUSIC_PATH)

    elif "open vlc" in command:
        open_app("vlc")
    
    elif "open notepad" in command:
        open_app("notepad")

    elif "open chrome" in command:
        open_app("chrome")

    elif "open panel" in command:
        open_app("xampp")
    
    elif "open github" in command:
        open_app("github")

    elif any(word in command for word in ["time","clock","hour"]):
        tell_time()

    elif any(word in command for word in ["date","day","today"]):
        tell_date()
    
    elif "open music folder" in command or "open songs" in command:
        open_folder(r"C:\Users\Andrea\Documents\songs")
    
    elif "open mydocuments" in command or "open year 2" in command:
        open_folder(r"C:\Users\Andrea\Documents\Year 2")

    elif "search for" in command:
        search_query=command.replace("search for","").strip()
        if search_query:
            search_google(search_query)
        else:
                speak("What do you want me to search for?")

    elif"play" in command:
        song_name = command.replace("play","").strip()
        speak(f"Searching for {song_name} on Youtube.")

        #youtube research
        results = YoutubeSearch(song_name,max_results=1).to_dict() 
        if results:
            video_url = f"https://www.youtube.com/watch?v={results[0]['id']}"
            speak(f"lecture of {results[0]['title']}.")
            webbrowser.open(video_url)
        else:
            speak(f"Video not found.")
    elif "open youtube" in command:
            speak("opening youtube.")
            webbrowser.open("https://www.youtube.com/")
    elif"close" in command:
            speak("closing application")
            app.quit()
    else:
            speak("command not recognise")


#initialisation of the interface
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

#creation of an object app
app = ctk.CTk()
app.title("Ari Vocal Assistance")
app.geometry("500x400")

# lable instruction(what is inside the window)
label = ctk.CTkLabel(app, text="Click on the button to listen to a command", font=("Helvetica",16))
label.pack(pady=30)

#button to activate the vocal assistance
act_button = ctk.CTkButton(app,text = "Listen", command=execute_command, font=("Helvetica",14),height=50,width=200)
act_button.pack(pady=20)

close_button= ctk.CTkButton(app, text ="Close app", command= app.quit(), font=("Helvetica",14),height=50,width=200,fg_color="green")
close_button.pack(pady=20)
app.mainloop()