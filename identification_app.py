from datetime import *
import speech_recognition as sr
import pyttsx3
from google_calendar import display_schedule
import PySimpleGUI as sg
from win32api import GetSystemMetrics
from news import get_news
import webbrowser
from weather import get_weather

# Set up voice recognition and text to speech
r = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[3].id)

# Get display resolution
width = GetSystemMetrics(0)
height = GetSystemMetrics(1)

sg.theme('Dark Blue')

names = ('Uku','Richard')
parts_of_day = ('hommikust','päevast','õhtust')


# Set up GUI elements
def createwindow():
    layout = [[sg.Text("Valikud:")], [sg.Button("Richard")], [sg.Button("Uku")], [sg.Button("Sulge rakendus")]] 
    return sg.Window("Kes sa oled?", layout, element_justification='c', alpha_channel=0.9, margins=(100, 50), icon=r'icon.ico').Finalize()
def createwindow2(weather):
    layout = [[sg.Text("Praegune ilm: " + "\n" + weather)], [sg.Button("Tagasi"), sg.Button("Sulge rakendus")]]
    return sg.Window("Kuva: Ilm", layout, element_justification='c', alpha_channel=0.9, margins=(100, 50), icon=r'icon.ico').Finalize()
def createwindow3(events):
    layout = [[sg.Text(events)], [sg.Button("Tagasi"), sg.Button("Sulge rakendus")]]
    return sg.Window("Kuva: Sündmused", layout, element_justification='c', alpha_channel=0.9, margins=(100, 50), icon=r'icon.ico').Finalize()
def createwindow4():
    layout = [[sg.Text("Valikud:")], [sg.Button("Ilmateade")], [sg.Button("Sündmused")], [sg.Button("Uudised")], [sg.Button("Sulge rakendus")]] 
    return sg.Window("Kuva", layout, element_justification='c', alpha_channel=0.9, margins=(100, 50), icon=r'icon.ico').Finalize()
def createwindow5(news):
    layout = [[sg.Text(news['title'], font=("Helvetica", 25))], [sg.Text(news['lead'])], [sg.Button("Loe edasi")], [sg.Button("Tagasi"), sg.Button("Sulge rakendus")]]
    return sg.Window("Kuva: Uudised", layout, element_justification='c', alpha_channel=0.9, margins=(100, 50), icon=r'icon.ico').Finalize()

# Function for identifying users
def identify(data, names):
    try:
        for variant in data['alternative']:
            for name in names:
                if name.lower() in variant['transcript'].lower():
                    person = name
                    return person
                else:
                    person = None
    except:
        person = None
        
    return person

# Listen for ambient noise
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    
engine.say("Tere! Kes sa oled?")
engine.runAndWait()

# Listen for input
with sr.Microphone() as source:
    data = r.record(source, duration=4)
    data = r.recognize_google(data,show_all=True,language="fi")

person = identify(data,names)

#Display selection of names if unable to identify
if person == None:
    engine.say("Ma ei saanud aru. Palun vali oma name ekraanilt.")
    engine.runAndWait()
    while True:
        window = createwindow()
        window.Maximize()
        event, values = window.read()
        if event == "Sulge rakendus" or event == sg.WIN_CLOSED:
            window.close()
            break
        else:
            person = event
            break
    window.close()
else:
    #Greet based on time of the day
    part_of_day = ""
    tund = int(datetime.now().strftime("%H"))
    if tund < 3 or tund > 16:
        part_of_day = parts_of_day[2]
    elif tund > 3 and tund < 12:
        part_of_day = parts_of_day[0]
    else:
        part_of_day = parts_of_day[1]
    engine.say("Tere " + part_of_day + " , " + person + " !")
    engine.runAndWait()
    
while person != None:
    window = createwindow4()
    window.Maximize()
    event, values = window.read()
    if event == "Sulge rakendus" or event == sg.WIN_CLOSED:
        break
    elif event == "Ilmateade":
        algne_weather = get_weather()
        temperatuur = algne_weather[0]
        kirjeldus = algne_weather[1]
        tuul = algne_weather[2]
        weather = ("Temperatuur on: " + str(temperatuur) + "°C" +
               "\n" + "Tuule kiirus on: " + str(tuul) + "m/s." +
               "\n" + "ilma kirjeldus on: " + kirjeldus + ".")
        window.close()
        window2 = createwindow2(weather)
        window2.Maximize()
        event, values = window2.read()
        if event == "Sulge rakendus" or event == sg.WIN_CLOSED:
            break
        elif event == "Tagasi":
            window2.close()
            continue
    elif event == "Sündmused":
        events = display_schedule(person)
        window.close()
        window3 = createwindow3(events)
        window3.Maximize()
        event, values = window3.read()
        if event == "Sulge rakendus" or event == sg.WIN_CLOSED:
            break
        elif event == "Tagasi":
            window3.close()
            continue
    elif event == "Uudised":
        news = get_news()
        window.close()
        window5 = createwindow5(news)
        window5.Maximize()
        event, values = window5.read()
        if event == "Sulge rakendus" or event == sg.WIN_CLOSED:
            break
        elif event == "Tagasi":
            window5.close()
            continue
        elif event == "Loe edasi":
            window5.close()
            webbrowser.open(news['link'])
            
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