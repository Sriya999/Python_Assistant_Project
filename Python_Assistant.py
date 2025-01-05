import pyttsx3 #voice api
import datetime#current time to wish
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import requests
import pyjokes

engine=pyttsx3.init('sapi5')#windows api
voices=engine.getProperty('voices')#gives list avail voices
#print(voices[0].id)#david  sys voice
#print(voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
def get_weather():
    '''Fetch weather information based on city'''
    speak("Please say the city name to get the weather information.")
    city=input("Enter city:")
    api_key = "2e3b9ee086ada58b5b280a12ebc44a7c"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
   
    response = requests.get(base_url)
    data = response.json()
    
    if data["cod"] == "404":
        speak(f"Sorry, I couldn't find the weather for {city}.")
    else:
       
        main = data["main"]
        weather_description = data["weather"][0]["description"]
        temperature = main["temp"]
        print(f"The current temperature in {city} is {temperature} degrees Celsius with {weather_description}.")

def wishme():
    '''wishes user according time'''
    current_time_hour = int(datetime.datetime.now().hour)#current hour from datetime module
    if current_time_hour>=0 and current_time_hour<=12:
        speak("Good Morning Sriya!!! Have a nice day")
    elif current_time_hour>=12 and current_time_hour<=18:
        speak("Good afternoon!!!")
    else:
        speak("Good Evening!")

    speak("Iam Harry. how can i help you.!!!")
  

def recipe_search(query):
    ''' Fetch the recipe '''
    api_url = f'https://api.api-ninjas.com/v1/recipe?query={query}'
    response = requests.get(api_url, headers={'X-Api-Key': 'd5yX1T/9U0AzhaAqjWEIjA==WySmQiztyAGWqxDG'})
    
    if response.status_code == requests.codes.ok:
        data = response.json()  # Parse the JSON response
        if data:
            instructions = data[0].get('instructions', 'Instructions not available')
            print(instructions)
            speak(instructions)
        else:
            print("No recipes found.")
            speak("No recipes found.")
    else:
        print("Error:", response.status_code, response.text)

def takecommand():
    '''it takes microphone input from user and returns  string output '''
    r=sr.Recognizer()
    with sr.Microphone() as source:#this is a source microphone
        #seconds of non speaking audio before complete
        print("Listening......")
        r.pause_threshold=1
        #energy threshold=300
        audio=r.listen(source)

    try:
        print("Recognizing...")
        query=r.recognize_google(audio,language='en-in')#google engine
        print(f"user said:{query}")
    except Exception as e:
        #print(e)
        print("say that again please")
        return "None"
    
    return query

if __name__=="__main__":
   
   
   wishme()
   
   while True:
        query=takecommand().lower()
        if 'in wikipedia' in query:
            speak("searching in wikipedia")
            query=query.replace("wikipedia","")
            result=wikipedia.summary(query,sentences=2)#summarizes in 2 lines
            speak("According to wikipedia")
            print(result)
            speak(result) 
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            webbrowser.open("google.com")
        elif 'open portal' in query:
            webbrowser.open("https://sraap.in/slogin.php")
        elif 'open notepad' in query:
            #vs_dir=
            cmd = 'notepad'
            os.system(cmd)
        elif 'open chrome' in query:
            cmd = r'"C:\Program Files\Google\Chrome\Application\chrome.exe"'
            os.system(cmd)#opens chrome
        

        elif 'time' in query:
            current_time = datetime.datetime.now().strftime('%H:%M:%S')
            speak(f"The current time is {current_time}")
            print(f"The current time is {current_time}")

        elif 'joke' in query:
            this_joke=pyjokes.get_joke()
            print(this_joke)
            speak(this_joke)
        
        elif 'weather' in query:
            get_weather()
        
        elif 'my name' in query:
            print("sriya")
            speak("sriya")
        elif 'recipe' in query:
            speak("Please say the recipe name")
            print("Please say the recipe name")
            recipe_query = takecommand().lower()  # Get the recipe name from voice command
            recipe_search(recipe_query)
        elif 'exit' in query:
            speak("Good Bye!")
            print("Good Bye!")
            exit()
 