import tkinter as tk
import random
import webbrowser as wb

root = tk.Tk()
label = tk.Label(root)
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

img_names = ["idle.png", "move_left.png", "move_right.png", "sleeping.png", "idle_to_sleeping.png", "sleeping_to_idle.png"]
images = [tk.PhotoImage(file=img_names[i]) for i in range(len(img_names))]
def image_choice(event_num): #dobiera sprite'a do eventu
    img = images[event_num]
    prev_event = event_num
    root.geometry("100x100+500+300")
    label.config(image=img)
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
    image_choice(event_num[0])

root.after(1, event_choice, 0)
tk.mainloop()
    