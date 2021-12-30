#GitHub test
import tkinter as tk
import random
import webbrowser as wb
from collections import defaultdict as dd

im_path = "temp_sprites/"

root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()


root.config(highlightbackground='black')
label = tk.Label(root, bd=0,bg='black')
label.pack()

m = tk.Menu(root, tearoff=0)


#opcje w menu
def menu_nuta():
    wb.open("https://open.spotify.com/track/3VIJBrMpvimHEw5wtPh2wB?si=633932ef19b842e7")
m.add_command(label='Dobra nuta', command=menu_nuta)

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

x = 1000

def f_static(event, it):
    img = im_frames[event][it]
    root.geometry("100x100+"+str(x)+"+300")
    label.config(image=img)
    if it+1 < 4:
        it+=1
        root.after(100, f_static, event, it)

def f_left(it):
    img = im_frames['left'][it]
    global x
    x-=3
    root.geometry("100x100+"+str(x)+"+300")
    label.config(image=img)
    if it+1 < 4:
        it+=1
        root.after(100, f_left, it)
  
def f_right(it):
    img = im_frames['right'][it]
    global x
    x+=3
    root.geometry("100x100+"+str(x)+"+300")
    label.config(image=img)
    if it+1 < 4:
        it+=1
        root.after(100,f_right,it)

def action(event_num):
    prev_event = event_num

    if event_num in {0, 3, 4, 5}:
        f_static(event_names[event_num], 0)
        root.after(1000, event_choice, prev_event)

    if event_num == 1:
        f_left(0)
        root.after(1000, event_choice, prev_event)

    if event_num == 2:
        f_right(0)
        root.after(1000, event_choice, prev_event)

def event_choice(prev_event): #wybiera kolejny event
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
    