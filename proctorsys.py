from tkinter import *
from functools import partial
import cv2
import winsound
import sounddevice as sd
from scipy.io.wavfile import write

def validateLogin(username, password):
   print("username entered :", username.get())
   print("password entered :", password.get())
   return
tkWindow = Tk()
tkWindow.geometry('400x150')
tkWindow.title('Tkinter Login Form - pythonexamples.org')

usernameLabel = Label(tkWindow, text="User Name").grid(row=0, column=0)
username = StringVar()
usernameEntry = Entry(tkWindow, textvariable=username).grid(row=0, column=1)


passwordLabel = Label(tkWindow,text="Password").grid(row=1, column=0)
password = StringVar()
passwordEntry = Entry(tkWindow, textvariable=password, show='*').grid(row=1, column=1)

validateLogin = partial(validateLogin, username, password)

loginButton = Button(tkWindow, text="Login", command=validateLogin).grid(row=4, column=0)

tkWindow.mainloop()
fs = 44100  # Sample rate
seconds = 30  # Duration of recording
cam = cv2.VideoCapture(0)
count=0
while cam.isOpened():
    ret, frame1 = cam.read()
    ret, frame2 = cam.read()
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(frame1, contours, -1,(0, 255, 0), 2)
    for c in contours:
        if cv2.contourArea(c) < 3000:
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        winsound.Beep(500, 200)
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished
        write('output.mp3', fs, myrecording)  # Save as WAV file
        if(winsound.Beep):
            count =count+1
        if count>10:
            cv2.waitkey('q')
    if cv2.waitKey(10) == ord('q'):
        break
    cv2.imshow('Camera', frame1)
