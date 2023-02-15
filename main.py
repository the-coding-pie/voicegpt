import speech_recognition as sr
import pyttsx3
import openai
from time import sleep

# our confgs
name = "Arvind"

# open ai configs
openai.api_key = "" # your openai api key here
model_engine = "text-davinci-003"

# instance of sr Recognizer
r = sr.Recognizer()

# pyttsx3 configs
engine = pyttsx3.init()
# RATE
# engine.setProperty('rate', 125)
# VOICE
voices = engine.getProperty('voices') # get current voices
# engine.setProperty('voice', voices[1].id)

# text to speech
def speak(text):
    print("Jarvis: " + text)
    engine.say(text)
    engine.runAndWait()

def prompt(text):
    print("You: " + text)

# speech to text
def recognize_voice():
    text = ''

    with sr.Microphone() as source:
        # adjust for ambient noise, its good to do this - listen for 1 second to calibrate the energy threshold for ambient noise level
        r.adjust_for_ambient_noise(source, duration=0.5)
        # capture the voice
        audio = r.listen(source)

        # recognize it
        try:
            text = r.recognize_google(audio, language="ml")
            prompt(text)
            reply(text)
        except sr.RequestError:
            prompt("??????????????????")
            speak("Could not request results from Google Speech Recognition service")
        except sr.UnknownValueError:
            prompt("??????????????????")
            speak("Sorry, Unable to recognize your speech...")

# fn to ask chat gpt and give reply
def reply(text):
    if text == "":
        speak("Speak something")
        return

    if "bye" in text:
        speak(f"Good bye {name}")
        exit()
    
    # ask chat gpt
    print('Thinking...')

    try:
        completion = openai.Completion.create(
        engine=model_engine,
        prompt=text,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
        )
        response = completion.choices[0].text
        speak(response.strip())
    except:
        speak("Something went wrong, try again...")
    

# beginning
speak(f"Hi {name}, you can start now!")

if __name__ == "__main__":
    while True:
        print("Listening...")
        recognize_voice()