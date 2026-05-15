'''Lan_Class_Chat - A lightweight LAN messaging tool for classrooms
Copyright (C) 2024 lizhaohaoxuan
 
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
'''
import tkinter as tk
import socket as skt
from threading import Thread
from tkinter import messagebox as msgbox
from tkinter import scrolledtext as scrtext
def get_info():
    host_name = skt.gethostname()
    host_ip_address = skt.gethostbyname(host_name)
    return (host_name,host_ip_address)
server_list = []
ip_range = 1
mode = 'client'
class LanChat:
    def __init__(self):
        self.host_name, self.host_ip_address = get_info()
    def Chatname(self,Chatname):
        self.chatname = Chatname
    def Addserver(self,Serveraddress):
        global server_list        
        if Serveraddress not in server_list:
            server_list.append(Serveraddress)
    def set_range(self, Networkrange):
        global ip_range
        ip_range = Networkrange
        Thread(target=scan_ip, daemon=True).start()
        fill_server_list(online_servers)

LanChat = LanChat()

def server_launch():
    print('starting server...')
    socket = skt.socket()
    socket.bind(('0.0.0.0',8000))
    socket.listen(1)
    print('waiting for connection...')
    conn , addr = socket.accept()
    print(f'connected to {addr}')

def client_launch(ip_addr=None, mode='launch'):
    print('starting client...')
    socket = skt.socket()
    if ip_addr == None:
        return False
    elif mode == 'close':
        socket.close()
    elif ip_addr:
        try:
            socket.connect((ip_addr, 8000))
            print(f'connected to {ip_addr}')
        except:
            raise

def send_message(addr , message):
    global mode
    if mode == 'client':
        while True:
            socket.send(message.encode('UTF-8')) # type: ignore
            msg_text.insert(tk.END, f'Me: {message}\n') # type: ignore
            data = socket.recv(1024).decode('UTF-8') # type: ignore
            msg_text.insert(tk.END, f'Other: {data}\n') # type: ignore
    if mode == 'server':
        while True:
            conn.send(message.encode('UTF-8')) # type: ignore
            msg_text.insert(tk.END, f'Me: {message}\n') # type: ignore
            data = conn.recv(1024).decode('UTF-8') # type: ignore
            msg_text.insert(tk.END, f'Other: {data}\n') # type: ignore

def check_network(addr):
    try:
        socket = skt.socket()
        socket.settimeout(0.2)
        result = socket.connect_ex((addr, 8000))
        socket.close()
        LanChat.Addserver(addr)
        return addr
    except:
        return False

def scan_ip():
    global ip_range
    print('start scan')
    for i in range(0,255):
        check_network(f'192.168.{ip_range}.{i}')
        print(f'scanning 192.168.{ip_range}.{i}')

def fill_server_list(master):
    for server in server_list:
        master.insert(tk.END, server)

def sub_window():
    sub_win = tk.Toplevel()
    sub_win.geometry('200x200')
    sub_win.title('Settings')
    set_label = tk.Label(sub_win, text='Network Range')
    set_label.pack(side='top')
    set_entry = tk.Entry(sub_win)
    set_entry.pack(side='top')
    ok_button = tk.Button(sub_win, text='OK', command=lambda: LanChat.set_range(set_entry.get()))
    ok_button.pack(side='bottom')

def on_server_select(event):
    sel = event.widget.curselection()
    if not sel:
        return
    index = sel[0]
    ip = event.widget.get(index)
    # 在后台线程连接，避免阻塞 UI
    Thread(target=client_launch, args=(ip,), daemon=True).start()

root = tk.Tk()
root.geometry('700x400')
root.minsize(400,300)
root.title('Lan_Class_Chat')

deck = tk.Frame(root)
deck.pack(side='top')
set_button = tk.Button(deck, text='settings', command=sub_window)
set_button.pack(side='left')

chat_area = tk.Frame(root)
chat_area.pack(side='right')

entry_area = tk.Frame(chat_area)
entry_area.pack(side='bottom')

msg_entry = tk.Entry(entry_area)
msg_entry.pack(side='left')

send_button = tk.Button(entry_area, text='GO!', command=lambda: send_message(None, msg_entry.get()))
send_button.pack(side='right')

msg_text = scrtext.ScrolledText(chat_area, wrap='word')
msg_text.pack(expand=True, fill='both',side='top')

list_area = tk.Frame(root)
list_area.pack(side='left')

online_servers = tk.Listbox(list_area,height=18,selectmode=tk.SINGLE)
online_servers.pack(side='top', fill='both', expand=True)
online_servers.bind('<<ListboxSelect>>', on_server_select)

create_button = tk.Button(list_area, text='Create a chat', command=lambda: Thread(target=server_launch, daemon=True).start())
create_button.pack(side='bottom', fill='x', pady=5)

root.mainloop()

while True:
    if online_servers.curselection() is not None:
        client_launch(mode='close')
        get_line = online_servers.get(online_servers.curselection())
        client_launch(server_list[get_line])