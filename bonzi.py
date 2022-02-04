import tkinter as tk
import random
import webbrowser as wb
from collections import defaultdict as dd
import threading
import time
import json
import wikipedia as wiki

#path to sprites
im_path = "temp_sprites/"

root = tk.Tk() #Main window widget
root.title('Monke Buddy')

root.wm_attributes('-transparentcolor','black')
root.overrideredirect(True)
root.wm_attributes('-topmost', True)

label = tk.Label(root, bd=0,bg='black') #Container for the sprites
label.place(relwidth=1, relheight=1, relx=0, rely=0)

dialogue_border = tk.Frame(root, background='white')
dialogue_box = tk.Label(dialogue_border, bd=0, bg='#1a1918', fg='white', wraplength=250, font=('Helvetica', 14))

m = tk.Menu(root, tearoff=0) #Dropdown menu object

input_field = tk.Entry(dialogue_box) #Input field object

input = tk.StringVar() #Global variable for storing input
def get_input():
    global input
    input.set(input_field.get()) #Save input from input_field into a global variable
    hide_dialogue_box()
submit_button = tk.Button(dialogue_box, text="Submit", command=get_input) #Button object for submitting input

def show_dialogue_box(type):
    dialogue_box.configure(text='') #Clear dialogue box before showing it

    dialogue_border.place(anchor='s', relheight=0.3, relwidth=0.94, relx=0.5, rely=0.98)
    dialogue_box.place(relheight=0.96, relwidth=0.98, anchor='center', relx=0.5, rely=0.5)
    if type == 'input':
        input_field.place(anchor='center', relx=0.5, rely=0.3)
        submit_button.place(anchor='center', relx=0.5, rely=0.6)

def hide_dialogue_box():
    dialogue_box.config(text='') #Clear dialogue box, just in case
    input_field.delete(0, tk.END) #Clear the input field
    submit_button.place_forget() #Hide everything dialogue box related
    input_field.place_forget() 
    dialogue_box.place_forget() 
    dialogue_border.place_forget()

#dropdown menu options
def t_change_settings(setting):
    global input
    show_dialogue_box('input') #Show dialogue box in input mode

    label.unbind('<Button-3>')
    submit_button.wait_variable(input) #Wait for the submit
    label.bind('<Button-3>', do_popup)

    f = open('settings.json', 'r+') #Open settings.json to save new settings
    data = json.load(f)

    data[setting] = input.get() #Get the new setting value from input

    f.seek(0) #Update settings.json
    json.dump(data, f)
    f.truncate()

    f.close()

def t_say_hello():
    m.entryconfig('Say hello', state='disabled') #Disable 'Say Hello' option from the dropdown menu

    f = open("settings.json") #Open the settings.json file and load the data from it into a dict
    data = json.load(f)

    show_dialogue_box('text') #Show dialogue box in text mode 
    dialogue_box.config(text=data['greeting'] + ', my name is ' + data['name']) #Display greeting in dialogue box

    time.sleep(5) #Show the greeting for 5 seconds

    if len(threading.enumerate()) <= 2: #If there are no other threads running, hide the dialogue box
        hide_dialogue_box()

    m.entryconfig('Say hello', state='normal') #Enable 'Say Hello' option
    f.close()

def t_ciekawostka():
    global input
    show_dialogue_box('input')

    label.unbind('<Button-3>') #Disable the whole menu until submitting input
    submit_button.wait_variable(input) 
    label.bind('<Button-3>', do_popup)

    m.entryconfig('Ciekawostka', state='disabled')

    show_dialogue_box('text')
    dialogue_box.configure(font=('Helvetica', 9)) #Make the font smaller for a while
    query = str(input.get())
   
    try:
        results = wiki.summary(query, sentences=1, auto_suggest=False, redirect=True)  
    except wiki.exceptions.DisambiguationError:
        results="No such page found."

    dialogue_box.config(text=results)

    time.sleep(7)

    if len(threading.enumerate()) <= 2:
        hide_dialogue_box()

    m.entryconfig('Ciekawostka', state='normal')
    dialogue_box.configure(font=('Helvetica', 14)) #Make the font size normal again

def t_dad_joke():
    m.entryconfig('Dad joke', state='disabled')
    f = open('jokes.txt', 'r', encoding='Utf-8') #Open the file containing epic jokes

    show_dialogue_box('text') #Show dialogue box in text mode

    jokes = f.readlines() #Randomly select a joke to display
    x = random.randint(0, len(jokes))
    dialogue_box.config(text=jokes[x].strip())

    time.sleep(5)

    if len(threading.enumerate()) <= 2:
        hide_dialogue_box()
    
    m.entryconfig('Dad joke', state='normal')
    f.close() 

def change_name():
    x = threading.Thread(target=t_change_settings, args=('name',), daemon=True)
    x.start()
m.add_command(label='Change name', command=change_name)

m.add_separator()
def say_hello(): 
    x = threading.Thread(target=t_say_hello, daemon=True)
    x.start()
m.add_command(label='Say hello', command=say_hello)

def menu_nuta():
    wb.open("https://open.spotify.com/track/3VIJBrMpvimHEw5wtPh2wB?si=633932ef19b842e7")
m.add_command(label='Dobra nuta', command=menu_nuta)

def ciekawostka():
    x = threading.Thread(target=t_ciekawostka, args=(), daemon=True)
    x.start()
m.add_command(label='Ciekawostka', command=ciekawostka)

def dad_joke():
    x = threading.Thread(target=t_dad_joke, daemon=True)
    x.start()
m.add_command(label='Dad joke', command=dad_joke)

m.add_separator()
def exit():
    root.destroy()
m.add_command(label='Exit', command='exit')

def do_popup(event):
    try:
        m.tk_popup(event.x_root, event.y_root)
    finally:
        m.grab_release()
label.bind('<Button-3>', do_popup)

#arrays of names of events
event_names = ["idle", "left" ,"right" , "sleeping", "idle_to_sleeping", "sleeping_to_idle"]

#dictionary of animation frames for each event
im_frames = dd(lambda:[])
for event_name in event_names:
    for i in range(1, 5):
        img = im_path + event_name + str(i) + ".png"
        im_frames[event_name].append(tk.PhotoImage(file=img))

#initial position of the widget on the x axis
x = 1000

def f_animation(event, it): #working animation for events
    global x
    if event == 'left':
        x -= 3
    elif event == 'right':
        x += 3
    img = im_frames[event][it]
    root.geometry("300x300+"+str(x)+"+300")
    label.config(image=img)
    if it+1 < 4:
        it+=1
        root.after(100, f_animation, event, it)

def action(event_num): #call the animation
    prev_event = event_num
    f_animation(event_names[event_num], 0)
    root.after(1000, event_choice, prev_event)

def event_choice(prev_event): #choosing next event
    #idle, move_left, move_right, sleeping, idle_to_sleeping, sleeping_to_idle
    events = [0, 1, 2, 3, 4, 5]
    if prev_event in {0, 1, 2}:
        event_num = random.choices(events, weights=[0.4, 0.2, 0.2, 0.0, 0.1, 0.0])
    elif prev_event == 4:
        event_num = [3]
    elif prev_event == 5:
        event_num = [0]
    else:
        event_num = random.choices(events, weights=[0.0, 0.0, 0.0, 0.8, 0.0, 0.2])
    action(event_num[0])        
    
event_choice(0)
tk.mainloop()
    