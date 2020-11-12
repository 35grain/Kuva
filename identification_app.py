from datetime import *
import easygui
import speech_recognition as sr
import pyttsx3
from google_calendar import kuva_kalender

r = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices') 
engine.setProperty('voice', voices[3].id)

nimed = ('Uku','Richard')
päeva_osad = ('hommikust','päevast','õhtust')

def isikusta(sisend, nimed):
    try:
        for variant in sisend['alternative']:
            for nimi in nimed:
                if nimi.lower() in variant['transcript'].lower():
                    isik = nimi
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

#Display selection of names if unable to identify
if isik == None:
    engine.say("Ma ei saanud aru. Palun vali oma nimi ekraanilt.")
    engine.runAndWait()
    vajutati = easygui.choicebox("Valige oma nimi ekraanilt", choices = nimed)
    if vajutati == None:
        easygui.msgbox("Sa ei valinud midagi!")
    else:
        isik = vajutati
        kuva_kalender(isik)
else:
    #Greet based on time of the day
    osa_päevast = ""
    tund = int(datetime.now().strftime("%H"))
    if tund < 3 or tund > 16:
        osa_päevast = päeva_osad[2]
    elif tund > 3 and tund < 12:
        osa_päevast = päeva_osad[0]
    else:
        osa_päevast = päeva_osad[1]
    engine.say("Tere " + osa_päevast + " , " + isik + " !")
    engine.runAndWait()
    kuva_kalender(isik)




