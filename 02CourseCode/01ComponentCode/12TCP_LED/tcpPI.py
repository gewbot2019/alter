'''
这两个库用来控制WS2812 LED灯
'''
from rpi_ws281x import *
import argparse

'''
导入TCP通信要用到的socket库
'''
import socket

'''
一些有关LED灯的设置，来自于WS281X例程
Source Code:https://github.com/rpi-ws281x/rpi-ws281x-python/
'''
LED_COUNT		= 24
LED_PIN			= 18
LED_FREQ_HZ		= 800000
LED_DMA			= 10
LED_BRIGHTNESS	= 255
LED_INVERT		= False
LED_CHANNEL		= 0

'''
Process arguments
'''
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
args = parser.parse_args()

'''
Create NeoPixel object with appropriate configuration.
'''
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

'''
Intialize the library
'''
strip.begin()

'''
接下来是与TCP通信相关的配置,其中PORT是定义端口号，你可以从0-65535之间自由选择，建议选择1023之后的数字，需要与PC中客户端定义的端口号一致
'''
HOST = ''
PORT = 10223
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpSerSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

'''
开始监听客户端连接，客户端连接成功后开始接收从客户端发来的信息
'''
tcpCliSock, addr = tcpSerSock.accept()

while True:
    data = ''
    
    '''
    接收来自客户端的信息
    '''
    '''
    如果信息内容为on则开灯
    如果信息内容为off则熄灯
    '''
    data = str(tcpCliSock.recv(BUFSIZ).decode())
    if not data:
        continue

    elif 'on' == data:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(255, 0, 255))
            strip.show()
            
    elif 'off' == data:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0, 0, 0))
            strip.show()
    
    '''
  最后打印出接收到的数据，并开始继续监听客户端发来的下一条信息
    '''
    print(data)