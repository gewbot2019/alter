'''
导入TCP通信要用到的socket库
'''
from socket import *

'''
Python 使用 Tkinter 可以快速的创建 GUI 应用程序,在导入的同时实例化
'''
import tkinter as tk

def lights_on():
    '''
    调用这个方法来发送开灯命令'on'
    '''
    tcpClicSock.send(('on').encode())

def lights_off():
    '''
    调用这个方法来发送关灯命令'off'
    '''
    tcpClicSock.send(('off').encode())

'''
这里输入树莓派的IP地址
'''
SERVER_IP = '192.168.3.146'	

'''
接下来是与TCP通信相关的配置,其中PORT是定义端口号，你可以从0-65535之间自由选择，建议选择1023之后的数字，需要与树莓派中服务器定义的端口号一致
'''
SERVER_PORT = 10223
BUFSIZ = 1024
ADDR = (SERVER_IP, SERVER_PORT)
tcpClicSock = socket(AF_INET, SOCK_STREAM)

tcpClicSock.connect(ADDR)

'''
以下为GUI的部分
'''
root = tk.Tk()	# 定义一个窗口
root.title('Lights')	# 窗口的标题
root.geometry('175x55')	# 窗口的大小，中间的x是英文字母x
root.config(bg='#000000')	# 定义窗口的背景颜色

'''
使用Tkinter的Button方法定义一个按键，按键在root窗口上，按键上面的名字是‘ON’，按键的文字颜色是#E1F5FE，按键的背景颜色是#0277BD，当按键被按下后，调用lights_on()函数
'''
btn_on = tk.Button(root, width=8, text='ON', fg='#E1F5FE', bg='#0277BD', command=lights_on)

'''
选择一个位置放置这个按键
'''
btn_on.place(x=15, y=15)

'''
同样的方法定义另一个按键，区别是按键上面的文字改为'OFF'，当按键被按下后，调用lights_off()函数
'''
btn_off = tk.Button(root, width=8, text='OFF', fg='#E1F5FE', bg='#0277BD', command=lights_off)

btn_off.place(x=95, y=15)

'''
最后开启消息循环
'''
root.mainloop()