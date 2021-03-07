import random
import pyttsx3
coinResult = random.randint(0,1)
if coinResult == 0 :
        pyttsx3.speak("Its a Head!")
        print("Its a Head!")
else :
        pyttsx3.speak("Its Tails!")
        print("Its Tails!")