from datetime import *
import speech_recognition as sr
import pyttsx3
from google_calendar import kuva_kalender
import PySimpleGUI as sg
from win32api import GetSystemMetrics
from uudis import hangi_uudis
import webbrowser

# Set up voice recognition and text to speech
r = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[3].id)

# Get display height
width = GetSystemMetrics(0)
height = GetSystemMetrics(1)

nimed = ('Uku','Richard')
päeva_osad = ('hommikust','päevast','õhtust')


# Set up GUI elements
def createwindow():
    layout = [[sg.Text("Valikud:")], [sg.Button("Richard")], [sg.Button("Uku")], [sg.Button("Sulge rakendus")]] 
    return sg.Window("Avaleht", layout, element_justification='c', alpha_channel=0.9, margins=(100, 50), icon=r'icon.ico').Finalize()
def createwindow2():
    layout = [[sg.Text("Ilmateade")], [sg.Button("Tagasi"), sg.Button("Sulge rakendus")]]
    return sg.Window("Ilm", layout, element_justification='c', alpha_channel=0.9, margins=(100, 50), icon=r'icon.ico').Finalize()
def createwindow3(sündmused):
    layout = [[sg.Text(sündmused)], [sg.Button("Tagasi"), sg.Button("Sulge rakendus")]]
    return sg.Window("Sündmused", layout, element_justification='c', alpha_channel=0.9, margins=(100, 50), icon=r'icon.ico').Finalize()
def createwindow4():
    layout = [[sg.Text("Valikud:")], [sg.Button("Ilmateade")], [sg.Button("Sündmused")], [sg.Button("Uudis")], [sg.Button("Sulge rakendus")]] 
    return sg.Window("Avaleht", layout, element_justification='c', alpha_channel=0.9, margins=(100, 50), icon=r'icon.ico').Finalize()
def createwindow5(uudis):
    layout = [[sg.Text(uudis['title'], font=("Helvetica", 25))], [sg.Text(uudis['lead'])], [sg.Button("Loe edasi")], [sg.Button("Tagasi"), sg.Button("Sulge rakendus")]]
    return sg.Window("Uudis", layout, element_justification='c', alpha_channel=0.9, margins=(100, 50), icon=r'icon.ico').Finalize()

# Function for identifying users
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
        window.Maximize()
        event, values = window.read()
        if event == "Sulge rakendus" or event == sg.WIN_CLOSED:
            window.close()
            break
        else:
            isik = event
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
    
while isik != None:
    window = createwindow4()
    window.Maximize()
    event, values = window.read()
    if event == "Sulge rakendus" or event == sg.WIN_CLOSED:
        break
    elif event == "Ilmateade":
        window.close()
        window2 = createwindow2()
        window2.Maximize()
        event, values = window2.read()
        if event == "Sulge rakendus" or event == sg.WIN_CLOSED:
            break
        elif event == "Tagasi":
            window2.close()
            continue
    elif event == "Sündmused":
        sündmused = kuva_kalender(isik)
        window.close()
        window3 = createwindow3(sündmused)
        window3.Maximize()
        event, values = window3.read()
        if event == "Sulge rakendus" or event == sg.WIN_CLOSED:
            break
        elif event == "Tagasi":
            window3.close()
            continue
    elif event == "Uudis":
        uudis = hangi_uudis()
        window.close()
        window5 = createwindow5(uudis)
        window5.Maximize()
        event, values = window5.read()
        if event == "Sulge rakendus" or event == sg.WIN_CLOSED:
            break
        elif event == "Tagasi":
            window5.close()
            continue
        elif event == "Loe edasi":
            window5.close()
            webbrowser.open(uudis['link'])
            
try:
    window.close()
except:
    nevermind_me = False
try:
    window2.close()
except:
    nevermind_me = False
try:
    window3.close()
except:
    nevermind_me = False
try:
    window4.close()
except:
    nevermind_me = False
try:
    window5.close()
except:
    nevermind_me = False