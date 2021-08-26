#!/usr/bin/env python3
"""
@file client.py
@brief TCP通信 - 客户端
@author IYATT-yx
@copyright Copyright (C) 2021 IYATT-yx
            2514374431@qq.com
            基于 AGPL-3.0 许可
"""
from tkinter import *
from socket import *
from threading import *

clientSocket = socket(AF_INET, SOCK_STREAM)

class Client(Thread):
    """客户端进程"""

    def __init__(self, op, ip=None, port=None, obj=None, data=None):
        super().__init__()
        self.__op = op
        self.__ip = ip
        self.__port = port
        self.__obj = obj
        self.__data = data

    def run(self):
        global clientSocket

        # 建立连接 - TCP
        if self.__op == 1:
            clientSocket.close()
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.connect((self.__ip, self.__port))

            # 接收消息 - TCP
            while True:
                data = clientSocket.recv(1024)
                if not data:
                    break
                self.__obj.insert(END, data.decode('utf-8'))

        # 发送 - TCP
        elif self.__op == 2:
            clientSocket.sendall(self.__data.encode('utf-8'))

        # 创建UDP
        elif self.__op == 3:
            clientSocket.close()
            clientSocket = socket(AF_INET, SOCK_DGRAM)

            while True:
                data, addr = clientSocket.recvfrom(1024)
                self.__obj.insert(END, data.decode('utf-8'))



class Interface(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.__master = master
        self.pack()

    def createWidgets(self):

        # 协议选择
        self.__protocol = StringVar()
        self.__protocol.set('tcp')
 
        self.__radiobutton1 = Radiobutton(self, text='TCP', value='tcp', variable=self.__protocol, command=self.__enable)
        self.__radiobutton1.grid(column=0, row=0)
        self.__radiobutton2 = Radiobutton(self, text="UDP", value='udp', variable=self.__protocol, command=self.__disable)
        self.__radiobutton2.grid(column=1, row=0)

        # IP 和端口输入
        self.__ip = StringVar()
        self.__ip.set('localhost')

        self.__port = IntVar()
        self.__port.set(9999)

        Label(self, text='IP: ').grid(column=0, row=1)
        Entry(self, textvariable=self.__ip, width=32).grid(column=1, row=1)

        Label(self, text='端口：').grid(column=2, row=1)
        Entry(self, textvariable=self.__port, width=6).grid(column=3, row=1)

        # 连接/断开按钮
        self.__status = 0
        self.__switch = Button(self, text='连接', command=self.__switchCall)
        self.__switch.grid(column=2, row=0)

        # 消息框
        Label(self, text='消息').grid(column=0, row=2)
        self.__message = Text(self, width=50, height=7)
        self.__message.grid(column=1, row=2, columnspan=3)

        # 发送消息
        Label(self, text='发送').grid(column=0, row=3)
        self.__send = Text(self, width=50, height=4)
        self.__send.grid(column=1, row=3, columnspan=3)

        Button(self, text='发送', command=self.__sendCall).grid(column=0, row=4, columnspan=4)

    def __switchCall(self):
        if self.__status == 0:
            self.__switch['text'] = '断开'
            self.__status = 1

            # 建立连接后进制切换协议
            self.__radiobutton1['state'] = DISABLED
            self.__radiobutton2['state'] = DISABLED

            Client(1, self.__ip.get(), self.__port.get(), self.__message).start()
                

        elif self.__status == 1:
            self.__switch['text'] = '连接'
            self.__status = 0

            # 断开连接后，切换协议恢复正常
            self.__radiobutton1['state'] = NORMAL
            self.__radiobutton2['state'] = NORMAL

            # 断开连接
            clientSocket.close()

    def __disable(self):
        """禁用连接按钮"""

        self.__switch['state'] = DISABLED

        Client(3, obj=self.__message).start()

    def __enable(self):
        """启用连接按钮"""

        self.__switch['state'] = NORMAL

        # 关闭 UDP
        clientSocket.close()


    def __sendCall(self):
        if self.__protocol.get() == 'tcp':
            Client(2, data=self.__send.get(1.0, END)).start()

        elif self.__protocol.get() == 'udp':
            clientSocket.sendto(self.__send.get(1.0, END).encode('utf-8'), (self.__ip.get(), self.__port.get()))


        self.__send.delete(1.0, END)

if __name__ == '__main__':
    root = Tk()
    root.geometry('500x300+500+500')
    root.title('客户端')
    app = Interface(root)
    app.createWidgets()
    root.mainloop()