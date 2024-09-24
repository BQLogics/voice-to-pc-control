import speech_recognition as sr
from gtts import gTTS
import winsound
from pydub import AudioSegment
import pyautogui
import webbrowser
import os
import time

# Ensure these paths are correct
ffmpeg_path = r"C:\ffmpeg\bin\ffmpeg.exe"
ffprobe_path = r"C:\ffmpeg\bin\ffprobe.exe"

# Set the environment variables for ffmpeg and ffprobe
os.environ["FFMPEG_BINARY"] = ffmpeg_path
os.environ["FFPROBE_BINARY"] = ffprobe_path

# Ensure ffmpeg and ffprobe paths are set for pydub
AudioSegment.ffmpeg = ffmpeg_path
AudioSegment.ffprobe = ffprobe_path

def listen_for_command():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening for commands...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        print("Could not understand audio. Please try again.")
        return None
    except sr.RequestError as e:
        print(f"Unable to access the Google Speech Recognition API: {e}")
        return None

def respond(response_text):
    print(response_text)
    tts = gTTS(text=response_text, lang='en')
    tts.save("response.mp3")
    sound = AudioSegment.from_mp3("response.mp3")
    sound.export("response.wav", format="wav")
    winsound.PlaySound("response.wav", winsound.SND_FILENAME)
    os.remove("response.mp3")
    os.remove("response.wav")

tasks = []
listening_to_task = False

def main():
    global tasks
    global listening_to_task

    trigger_keyword = "siri"

    while True:
        try:
            command = listen_for_command()
            if command:
                print(f"Command received: {command}")
                
                if listening_to_task:
                    print("Currently listening for a task to add.")
                    tasks.append(command)
                    listening_to_task = False
                    respond(f"Adding '{command}' to your task list. You have {len(tasks)} tasks currently in your list.")
                elif trigger_keyword in command:
                    print(f"Trigger keyword '{trigger_keyword}' detected.")
                    
                    if "add a task" in command:
                        listening_to_task = True
                        respond("Sure, what is the task?")
                    elif "list tasks" in command:
                        if tasks:
                            respond("Your tasks are:")
                            for task in tasks:
                                respond(task)
                        else:
                            respond("You have no tasks.")
                    elif "take a screenshot" in command:
                        pyautogui.screenshot("screenshot.png")
                        respond("I took a screenshot for you.")
                    elif "what is your purpose" in command:
                        # pyautogui.screenshot("screenshot.png")
                        respond("To help you ")
                    elif "open youtube" in command:
                        respond("Opening youtube")
                        webbrowser.open("http://www.youtube.com")
                    elif "open linkedin" in command:
                        respond("Opening linkedin")
                        webbrowser.open("https://www.linkedin.com/feed")
                    elif "exit" in command:
                        respond("Goodbye!")
                        break
                    else:
                        respond("Sorry, I'm not sure how to handle that command.")
                else:
                    print("Trigger keyword not detected in the command.")
            else:
                print("No valid command detected.")
        except sr.RequestError as e:
            print(f"Network error: {e}. Retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
