#GitHub test
import tkinter as tk
import random
from tkinter.constants import BOTTOM, TOP
import webbrowser as wb
from collections import defaultdict as dd

#path to sprites
im_path = "temp_sprites/"

root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()


root.config(highlightbackground='black')
label = tk.Label(root, bd=0,bg='black')
label.place(relwidth=1, relheight=1, relx=0, rely=0)

dialogue_box = tk.Label(root, bd=0, bg='black', fg='white', height=10)
dialogue_box.place(anchor='s', relheight=0.2, relwidth=1, relx=0.5, rely=1)

m = tk.Menu(root, tearoff=0)


#dropdown menu options
def menu_nuta():
    wb.open("https://open.spotify.com/track/3VIJBrMpvimHEw5wtPh2wB?si=633932ef19b842e7")
m.add_command(label='Dobra nuta', command=menu_nuta)

dialogue_box_visible = True
def toggle_dialogue_box():
    global dialogue_box_visible
    if dialogue_box_visible:
        dialogue_box.place_forget()
        dialogue_box_visible = False
    else:
        dialogue_box.place(anchor='s', relheight=0.2, relwidth=1, relx=0.5, rely=1)
        dialogue_box_visible = True
m.add_command(label='Toggle dialogue box', command=toggle_dialogue_box)

def dad_joke():
    f = open('jokes.txt', 'r', encoding='Utf-8')
    jokes = f.readlines()
    x = random.randint(0, len(jokes))
    print(jokes[x].strip())
    f.close()
m.add_command(label='Dad joke', command=dad_joke)

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
    root.geometry("100x100+"+str(x)+"+300")
    label.config(image=img)
    dialogue_box.config(text=event)
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
    

root.after(1, event_choice, 0)
tk.mainloop()
    