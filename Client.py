import socket
import os 
from tkinter import *
import time
import threading


background = "steelblue2"
WIDTH = 400
HEIGHT = 300

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 8080
s.connect((host, port))

print("[ + ] Erfolgreich mit dem Server {} verbunden".format(host))


root = Tk()
root.title("Chat")
root.configure(bg=background)
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(0, 0)

titel = Label(root, text="Chatprogramm", bg=background, fg="white", font="Arial 15 bold")
titel.place(relx=0.5, rely=0.1, anchor=CENTER)

messages = Text(background="black", fg="green", height=WIDTH / 40, width=31)
messages.place(relx=0.5, rely=0.5, anchor=CENTER)
messages.configure(state=DISABLED)

entry = Entry(root, background="black", fg="green", width=31, font="Times 10 ")
entry.insert(0, "Nachricht...")
entry.place(relx=0.43, rely=0.9, anchor=CENTER)



def send():

    text = entry.get()
    s.send(text.encode())



def empfangen():

    while True:
        try:
            text = s.recv(52).decode()
            messages.configure(state=NORMAL)
            messages.insert(END, f"\n{text}")
            messages.configure(state=DISABLED)
            if text == "[ i ] Server: Sie wurden vom Admin gekickt.":
                time.sleep(3.5)
                root.destroy()
                quit()
            root.update()
        except:
            break

t = threading.Thread(target = empfangen)
t.start()

send_button = Button(root, fg="green", text="Send", font="Times 12 bold", command=send)
send_button.place(relx=0.75, rely=0.9, anchor=CENTER)

try:
    root.mainloop()
except:
    quit()





