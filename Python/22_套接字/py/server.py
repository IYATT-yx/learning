#!/usr/bin/env python3
"""
@file server.py
@brief TCP通信 - 服务端
@author IYATT-yx
@copyright Copyright (C) 2021 IYATT-yx
            2514374431@qq.com
            基于 AGPL-3.0 许可
"""
from tkinter import *
from socket import *
from threading import *

serverSocket = -1
clientSocket = socket(AF_INET, SOCK_STREAM)
clientAddr = -1
addr = None

class Server(Thread):
    """服务器线程
    1.监听端口，接入连接后循环接收消息
    2.发送消息
    """

    def __init__(self, op, port=None, obj=None, data=None):
        """构造
        @param op 1 监听并接收消息（TCP）; 2 发送消息（TCP）; 3 监听并接收消息（UDP）; 4 发送消息（UDP）
        @param port op选1、3时，要监听的端口
        @param obj Text对象，op选1、3时，将收到消息向该对象插入
        @param data op选2、4时，要发送的数据
        """

        super().__init__()
        self.__op = op
        self.__port = port
        self.__obj = obj
        self.__data = data

    def run(self):
        global serverSocket
        global clientSocket
        global clientAddr
        
        # 监听 - TCP
        if self.__op == 1:
            serverSocket = socket(AF_INET, SOCK_STREAM)
            serverSocket.bind(('', self.__port))
            serverSocket.listen(1)
            clientSocket.close()
            clientSocket, clientAddr = serverSocket.accept()

            # 接收消息并显示 - TCP
            while True:
                data = clientSocket.recv(1024)
                if not data:
                    break
                self.__obj.insert(END, str(clientAddr[0]) + ':' + str(clientAddr[1]) + '    ' + data.decode('utf-8'))
            
        # 发送 - TCP
        elif self.__op == 2:
            clientSocket.sendall(self.__data.encode('utf-8'))

        # 监听 - UDP
        elif self.__op == 3:
            serverSocket = socket(AF_INET, SOCK_DGRAM)
            serverSocket.bind(('', self.__port))

            # 接收消息并显示 - UDP
            global addr
            while True:
                data, addr = serverSocket.recvfrom(1024)
                if not data:
                    break
                self.__obj.insert(END, str(addr[0]) + ':' + str(addr[1]) + '    ' + data.decode('utf-8'))
                serverSocket.sendto(('对方已收到： ' + data.decode('utf-8')).encode('utf-8'), addr)
                



class Interface(Frame):
    """软件界面设计"""

    def __init__(self, master=None):
        super().__init__(master)
        self.__master = master
        self.pack()

        # 关闭程序事件
        self.__master.protocol("WM_DELETE_WINDOW", self.__onClosing)

    def createWidgets(self):
        """TCP/UDP 协议选择
        1 - 选中
        0 - 未选中
        默认 TCP 选中
        """
        self.__protocol = StringVar()
        self.__protocol.set('tcp')

        self.__radiobutton1 = Radiobutton(self, text='TCP', value='tcp', variable=self.__protocol)
        self.__radiobutton1.grid(column=0, row=0)
        self.__radiobutton2 = Radiobutton(self, text='UDP', value='udp', variable=self.__protocol)
        self.__radiobutton2.grid(column=1, row=0)

        # 端口
        Label(self, text='端口:').grid(column=0, row=1)

        self.__port = IntVar()
        self.__port.set(9999)

        Entry(self, textvariable=self.__port, width=6).grid(column=1, row=1)

        # 服务器启停
        self.__switchStatus = 0
        self.__switch = Button(self, text='启动', command=self.__switchCall)
        self.__switch.grid(column=2, row=0, rowspan=2)

        # 消息窗口
        Label(self, text='消息').grid(column=0, row=3)
        self.__message = Text(self, width=50, height=7)
        self.__message.grid(column=1, row=3, columnspan=3)

        # 发送消息框
        Label(self, text='发送').grid(column=0, row=4)
        self.__send = Text(self, width=50, height=4)
        self.__send.grid(column=1, row=4, columnspan=3)

        # 发送按钮
        self.__sendButton = Button(self, text='发送', command=self.__sendCall)
        self.__sendButton.grid(column=0, row=5, columnspan=4)

    def __switchCall(self):
        """服务器启停执行"""

        if self.__switchStatus == 1:
            self.__switch['text'] = '启动'
            self.__switchStatus = 0

            # 停止服务器后，切换协议恢复正常
            self.__radiobutton1['state'] = NORMAL
            self.__radiobutton2['state'] = NORMAL

            # 停止服务器
            serverSocket.close()
            clientSocket.close()

        elif self.__switchStatus == 0:
            self.__switch['text'] = '停止'
            self.__switchStatus = 1

            # 启动服务器后禁止切换协议 
            self.__radiobutton1['state'] = DISABLED
            self.__radiobutton2['state'] = DISABLED

            if self.__protocol.get() == 'tcp':
                Server(1, self.__port.get(), self.__message).start()

                # 恢复发送框和发送按钮
                self.__send['state'] = NORMAL
                self.__sendButton['state'] = NORMAL

            elif self.__protocol.get() == 'udp':
                Server(3, self.__port.get(), self.__message).start()

                # 禁用发送框和发送按钮
                self.__send['state'] = DISABLED
                self.__sendButton['state'] = DISABLED

    def __sendCall(self):
        """发送消息"""
        if self.__protocol.get() == 'tcp':
            Server(2, data=self.__send.get(1.0, END)).start()

        # 发送后清空
        self.__send.delete(1.0, END)

    def __onClosing(self):
        serverSocket.close()
        clientSocket.close()
        self.__master.destroy()


if __name__ == '__main__':
    root = Tk()
    root.geometry('500x300+500+500')
    root.title('服务器')
    app = Interface(master=root)
    app.createWidgets()
    root.mainloop()
