'''Lan_Class_Chat - A lightweight LAN messaging tool for classrooms
Copyright (C) 2024 lizhaohaoxuan
 
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
'''
#依赖库引入
import tkinter as tk
import socket as sc
from threading import Thread
from tkinter import messagebox as mb
'''
函数实现
'''
#获取本机信息
def get_info():
    host_name = sc.gethostname()
    host_ip_address = sc.gethostbyname(host_name)
    return (host_name,host_ip_address)
#服务端启动
def sever_start_communication():
    print('启动服务端')
    socket_sever = sc.socket()
    socket_sever.bind(('0.0.0.0',8000))
    socket_sever.listen(1)
    print('开始监听，等待连接')
    conn , address = socket_sever.accept()
    print(f'已连接，客户端信息：{address}')
    while True :
        data:str =conn.recv(1024).decode('UTF-8')
        print(data)
        msg = input('回复：')
        if msg == 'exit':
            conn.close()
            socket_sever.close()
            break
        conn.send(msg.encode('UTF-8'))
#遍历IP
def scan_ip(ip,mode='normal'):
    try:
        socket_scan = sc.socket()
        socket_scan.settimeout(0.2)
        result = socket_scan.connect_ex((ip,8000))
        socket_scan.close()
        if mode =='output':
            return ip
        elif mode =='normal':
            return result == 0
    except:
        return False
#启动客户端
def client_start_communication(ip):
    print('启动客户端')
    socket_client = sc.socket()
    socket_client.connect((ip , 8000))
    print('已连接')
    while True:
        send_msg = input('发送：')
        if send_msg == 'exit':
            socket_client.close()
            break
        socket_client.send(send_msg.encode('UTF-8'))
        recv_data = socket_client.recv(1024).decode('UTF-8')
        print(recv_data)
#询问是否创建会话，用于扫描无果情况
def ask_creat_server():    
    creat = mb.askyesno('消息','局域网内无会话，是否创建？')
    if creat == True:
        Thread(target=sever_start_communication, daemon=True).start()
#询问是否加入会话，用于已扫描情况
def ask_join_sever():
    creat = mb.askyesno('消息','寻找到会话，是否加入？')
    if creat == True:
        Thread(terget=client_start_communication, deamon=True,args=(connect_sever_ip,)).start()
#搭配上文 scan_ip() 函数，扫描局域网会话
def start_scan():
    global connect_sever_ip , connect_sever_ip_true , count
    count = 0
    connect_sever_ip_true = False
    print('开始扫描：')
    for i in range(0,255):
        count += 1
        ip = f'192.168.3.{i}'
        print(f'第{count}次扫描')
        if scan_ip(ip):
            sever_ip = scan_ip(ip,'output')
            print(f'发现服务端！IP:{sever_ip}')
            connect_sever_ip_true = True
            connect_sever_ip = sever_ip
            return ''
    if connect_sever_ip_true == True:
        main_window.after(0, lambda: ask_join_sever())
    if count == 255 and connect_sever_ip_true == False:
        main_window.after(0, lambda: ask_creat_server())
#设置聊天名称
def set_chat_name(name):
    global chat_name
    chat_name = name
#设置界面
def creat_sub_window():
    global sub_window
    sub_window = tk.Toplevel(main_window)
    sub_window.geometry('200x200')
    chat_name = tk.Label(sub_window,text='设置聊天名')
    chat_name_entry = tk.Entry(sub_window)
    chat_name_button = tk.Button(sub_window,text='确定',command=lambda:set_chat_name(chat_name_entry.get()))
    chat_name.pack()
    chat_name_entry.pack()
    chat_name_button.pack()
    sub_window.protocol("WM_DELETE_WINDOW", sub_window.destroy)
'''
---GUI部分---
'''
main_window = tk.Tk()
main_window.geometry('400x200')
main_window.minsize(300,200)

scan_button = tk.Button(main_window,text='扫描会话',command = lambda:Thread(target=start_scan, daemon=True).start())
sever_button = tk.Button(main_window,text='创建会话',command = lambda:Thread(target=sever_start_communication,daemon=True).start())

ip_label = tk.Label(main_window,text='或者加入已知会话：')
ip_entry = tk.Entry(main_window)
join_button = tk.Button(main_window,text='加入！',command= lambda:Thread(target=client_start_communication,daemon=True,args=(ip_entry.get(),)).start())

host_name , host_ip = get_info()
info_label = tk.Label(main_window,text=f'本机名称:{host_name}\n本机IP:{host_ip}')

setting_button = tk.Button(main_window,text='设置',command = lambda:creat_sub_window())

info_label.pack()
scan_button.pack()
sever_button.pack()
ip_label.pack()
ip_entry.pack()
join_button.pack()
setting_button.pack()
main_window.mainloop()