#GitHub test
import tkinter as tk
import random
import webbrowser as wb

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



#arrays of names of frames
event_names = ["im_idle", "im_left" ,"im_right" , "im_sleeping", "im_idle_sleeping", "im_sleeping_idle"]


idle_names = ["idle"+ str(i) + ".png" for i in range(1,5)]
left_names = ["move_left"+ str(i) + ".png" for i in range(1,5)]
right_names = ["move_right"+ str(i) + ".png" for i in range(1,5)]
sleeping_names = ["sleeping"+ str(i) + ".png" for i in range(1,5)]
idle_sleeping_names = ["idle_to_sleeping"+ str(i) + ".png" for i in range(1,5)]
sleeping_idle_names = ["sleeping_to_idle"+ str(i) + ".png" for i in range(1,5)]

im_idle = [tk.PhotoImage(file=idle_names[i]) for i in range(len(idle_names))]
im_left = [tk.PhotoImage(file=left_names[i]) for i in range(len(left_names))]
im_right = [tk.PhotoImage(file=right_names[i]) for i in range(len(right_names))]
im_sleeping = [tk.PhotoImage(file=sleeping_names[i]) for i in range(len(sleeping_names))]
im_idle_sleeping = [tk.PhotoImage(file=idle_sleeping_names[i]) for i in range(len(idle_sleeping_names))]
im_sleeping_idle = [tk.PhotoImage(file=sleeping_idle_names[i]) for i in range(len(sleeping_idle_names))]




def f_idle(it):
    img = im_idle[it]
    root.geometry("100x100+500+300")
    label.config(image=img)
    if it+1 < 4:
        it+=1
        root.after(100,f_idle,it)

def f_left(it):
    img = im_left[it]
    root.geometry("100x100+500+300")
    label.config(image=img)
    if it+1 < 4:
        it+=1
        root.after(100,f_left,it)
  

def f_right(it):
    img = im_right[it]
    root.geometry("100x100+500+300")
    label.config(image=img)
    if it+1 < 4:
        it+=1
        root.after(100,f_right,it)
    
def f_sleeping(it):
    img = im_sleeping[it]
    root.geometry("100x100+500+300")
    label.config(image=img)
    if it+1 < 4:
        it+=1
        root.after(100,f_sleeping,it)

def f_idle_sleeping(it):
    img = im_idle_sleeping[it]
    root.geometry("100x100+500+300")
    label.config(image=img)
    if it+1 < 4:
        it+=1
        root.after(100,f_idle_sleeping,it)

def f_sleeping_idle(it):
    img = im_sleeping_idle[it]
    root.geometry("100x100+500+300")
    label.config(image=img)
    if it+1 < 4:
        it+=1
        root.after(100,f_sleeping_idle,it)

def action(event_num):
    prev_event = event_num

    if event_num == 0:
        f_idle(0)
        root.after(100000000, event_choice, prev_event)

    if event_num == 1:
        f_left(0)
        root.after(1000, event_choice, prev_event)

    if event_num == 2:
        f_right(0)
        root.after(1000, event_choice, prev_event)

    if event_num == 3:
        f_sleeping
        root.after(100000000, event_choice, prev_event)

    if event_num == 4:
        f_idle_sleeping
        root.after(1000, event_choice, prev_event)
        

    if event_num == 5:
        f_sleeping_idle
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
    