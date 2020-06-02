import socket
import threading
import time
import random
from tkinter import *



background = "black"
WIDTH = 800
HEIGHT = 350


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 8080

server.bind((host, port))
print("[ + ] Server has been started.")

root = Tk()
root.title("Admin")
root.configure(bg=background)
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(0, 0)

panel_titel = Label(root, text="Admin Panel", bg=background, fg="red", font="Arial 15 bold")
panel_titel.place(relx=0.25, rely=0.1, anchor=CENTER)

chat_titel = Label(root, text="Chat", bg=background, fg="green", font="Arial 15 bold")
chat_titel.place(relx=0.75, rely=0.1, anchor=CENTER)

users = Text(background="black", fg="red", height=WIDTH / 80, width=31)
users.place(relx=0.25, rely=0.5, anchor=CENTER)
users.configure(state=DISABLED)

chat = Text(background="black", fg="green", height=WIDTH / 80, width=31)
chat.place(relx=0.75, rely=0.5, anchor=CENTER)
chat.configure(state=DISABLED)

admin_entry = Entry(root, background="black", fg="red", width=31, font="Times 10 ")
admin_entry.insert(0, "User ID")
admin_entry.place(relx=0.215, rely=0.9, anchor=CENTER)

admin_msg_entry = Entry(root, background="black", fg="green", width=31, font="Times 10 ")
admin_msg_entry.insert(0, "message...")
admin_msg_entry.place(relx=0.715, rely=0.9, anchor=CENTER)


connection_threads = []

class Client(threading.Thread):

    clients = []
    index = 0

    usernames = [f"user{x}" for x in range(1,100)]


    def __init__(self, conn, addr, nn, index):

        threading.Thread.__init__(self)
        self.conn = conn
        self.nn = nn
        self.addr = addr
        self.index = index

        

    def run(self):

        while True:

            try:
                message = self.nn + " : " + self.conn.recv(52).decode()
                chat.configure(state=NORMAL)
                chat.insert(END, f"\n{message}")
                chat.configure(state=DISABLED)
                root.update()
                print(f"{self.addr} : {message}")
                for client in Client.clients:
                    client[0].sendall(message.encode())
            except: 
                print(f"[ ! ] {self.addr} disconnected from the Server.")
                if [self.conn, self.nn] in Client.clients:
                  Client.clients.remove([self.conn, self.nn])
                break


    def kick(self):

        self.conn.send("[ i ] Server: The admin has kicked you.".encode())
        self.conn.close()
        Client.clients.remove([self.conn, self.nn])
        connection_threads.remove(self)
        print(f"[ ! ] {self.addr} has been kicked from the Server.")
        users.configure(state=NORMAL)
        users.delete("1.0", END)
        for thread in connection_threads:
            users.insert(END, f"Username: {thread.nn} \nIP: {thread.addr}\nID: {connection_threads.index(thread)}\n_______________________________\n") 
        root.update()
        users.configure(state=DISABLED)
        for client in Client.clients:
                client[0].sendall(f"[ i ] Server: {self.nn} got kicked by the Admin.".encode())
        chat.configure(state=NORMAL)
        chat.insert(END,f"\n[ i ] Server: {self.nn} got kicked by the Admin.")
        chat.configure(state=DISABLED)


            

error_message = Label(root, text="User not found!", bg=background, fg="red", font="Arial 12 bold")

def deac_emsg():
    time.sleep(5)
    error_message.place_forget()


def check():
    try:
        Client.kick(connection_threads[int(admin_entry.get())])
        error_message.place_forget()
        
    except:
        error_message.place(relx=0.2125, rely=0.8, anchor=CENTER)
        threading.Thread(target=deac_emsg).start()

def send_admin_msg():

    
    message = "Admin : " + admin_msg_entry.get()
    chat.configure(state=NORMAL)
    chat.insert(END, f"\n{message}")
    chat.configure(state=DISABLED)
    root.update()
    message = message.encode()
    for client in Client.clients:
        client[0].sendall(message)
       


kick_button = Button(root, bg="black", text="KICK", fg="red", font="Arial 13 bold", command= check)
kick_button.place(relx=0.375, rely=0.9, anchor=CENTER)

send_button = Button(root, bg="black", text="Send", fg="green", font="Arial 13 bold", command= send_admin_msg)
send_button.place(relx=0.875, rely=0.9, anchor=CENTER)

def serverloop():

    while len(Client.usernames) > 0:
        server.listen(1)
        conn, addr = server.accept()
        username = random.choice(Client.usernames)
        Client.clients.append([conn, username])
        Client.usernames.remove(username)
        thread = Client(conn, addr, username, Client.index)
        thread.start()
        connection_threads.append(thread)
        users.configure(state=NORMAL)
        users.insert(END, f"Username: {username} \nIP: {addr}\nID: {connection_threads.index(thread)}\n_______________________________\n")   
        root.update()
        print(f"{addr} hat sich mit dem Server verbunden.")
        users.configure(state=DISABLED)
     
     
        
serverthread = threading.Thread(target=serverloop)
serverthread.start()

root.mainloop()




    




