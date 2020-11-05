import speech_recognition as sr
import pyttsx3
from google_calendar import display_calendar
r = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices') 
engine.setProperty('voice', voices[3].id)

nimed = ('Uku','Richard')

def isikusta(sisend, nimed):
    try:
        for variant in sisend['alternative']:
            for nimi in nimed:
                if nimi.lower() in variant['transcript'].lower():
                    isik = nimi
                    engine.say("Tere hommikust "+ isik +" !")
                    engine.runAndWait()
                    return isik
                else:
                    isik = None
    except:
        isik = None
        
    return isik

# Listen for ambient noise
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    
engine.say("Tere! Kes sa oled?")
engine.runAndWait()

# Listen for input
with sr.Microphone() as source:
    data = r.record(source, duration=5)
    sisend = r.recognize_google(data,show_all=True,language="fi")

isik = isikusta(sisend,nimed)
    
if isik == None:
    engine.say("Ma ei saanud aru. Palun vali oma nimi ekraanilt.")
    engine.runAndWait()
else:
    display_calendar(isik)