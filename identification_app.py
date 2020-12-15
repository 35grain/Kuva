from datetime import *
import speech_recognition as sr
import pyttsx3
from google_calendar import kuva_kalender
import PySimpleGUI as sg

r = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices') 
engine.setProperty('voice', voices[3].id)

nimed = ('Uku','Richard')
päeva_osad = ('hommikust','päevast','õhtust')

def createwindow():
    layout = [[sg.Text("Valikud:")], [sg.Button("Richard")], [sg.Button("Uku")], [sg.Button("Sulge")]] 
    return sg.Window("Avaleht", layout)
def createwindow2():
    layout2 = [[sg.Text("Ilmateade")], [sg.Button("Tagasi")], [sg.Button("Sulge")]]
    return sg.Window("Ilm", layout2)
def createwindow3(sündmused):
    layout3 = [[sg.Text(sündmused)], [sg.Button("Tagasi")], [sg.Button("Sulge")]]
    return sg.Window("Sündmused", layout3)
def createwindow4():
    layout = [[sg.Text("Valikud:")], [sg.Button("Ilmateade")], [sg.Button("Sündmused")], [sg.Button("Sulge")]] 
    return sg.Window("Avaleht", layout)

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
    while True:
        window = createwindow()
        event, values = window.read()
        if event == "Sulge" or event == sg.WIN_CLOSED:
            window.close()
            break
        elif event == "Richard":
            isik = "Richard"
            break
        elif event == "Uku":
            isik = "Uku"
            break
    window.close()
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
    
while True:
    window = createwindow4()
    event, values = window.read()
    if event == "Sulge" or event == sg.WIN_CLOSED:
        break
    elif event == "Ilmateade":
        vajutus = "Ilm"
        window.close()
        window2 = createwindow2()
        event, values = window2.read()
        if event == "Sulge" or event == sg.WIN_CLOSED:
            break
        elif event == "Tagasi":
            window2.close()
            continue
    elif event == "Sündmused":
        vajutus = "Sündmus"
        sündmused = kuva_kalender(isik)
        window.close()
        window3 = createwindow3(sündmused)
        event, values = window3.read()
        if event == "Sulge" or event == sg.WIN_CLOSED:
            break
        elif event == "Tagasi":
            window3.close()
            continue

try:
    window.close()
except:
    x = 3
try:
    window2.close()
except:
    x = 3
try:
    window3.close()
except:
    x = 3