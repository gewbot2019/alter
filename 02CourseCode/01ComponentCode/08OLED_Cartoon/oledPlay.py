#!/usr/bin/python3

import time

#导入OLED屏幕相关的库
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

#导入用于图像处理的库
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import os

#获得本文件的绝对路径
curpath = os.path.realpath(__file__)
thisPath = "/" + os.path.dirname(curpath) + "/"

#OLED屏幕初始化
RST = 24
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()

#设置播放帧率
FPS = 30

#根据播放帧率算得每帧延迟时间
timeDelay = 1/FPS

#清空屏幕
disp.clear()
disp.display()

#全部图像将会被保存在这个数组内
LaughImage = []

#设置将要播放的ppm序列串来自于哪个文件夹
ppmPath = 'ppm/'

#获得这个文件夹内所有帧的名称
ppmNames = os.listdir(ppmPath)

#将这些文件以名称排序
ppmNames.sort()

#导入这些帧
for frameName in ppmNames:
	#打开PPM格式的文件并通过convert('1')将其二值化
	image = Image.open(thisPath+ppmPath+frameName).convert('1')
	#将转换完成的图像存储进LaughImage
	LaughImage.append(image)


#一帧一帧显示就相当于播放动画片了
for i in range(0, len(LaughImage)):
	disp.image(LaughImage[i])
	disp.display()
	time.sleep(timeDelay)