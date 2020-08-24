#!/usr/bin/env/python3
# File name   : server.py
# Description : for OLED functions
# Website	 : www.gewbot.com
# Author	  : William(Based on Adrian Rosebrock's OpenCV code on pyimagesearch.com)
# Date		: 2019/08/28

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
import time
import threading

try:
	serial = i2c(port=1, address=0x3C)
	device = ssd1306(serial, rotate=0)
except:
	print('OLED disconnected\n')


'''
设置每一行的初始内容
'''
text_1 = 'HELLO WORLD'
text_2 = 'IP:CONNECTING'
text_3 = '<ARM> OR <PT> MODE'
text_4 = 'MPU6050 DETECTING'
text_5 = 'FUNCTION OFF'
text_6 = 'Message:None'

class OLED_ctrl(threading.Thread):
	def __init__(self, *args, **kwargs):
		super(OLED_ctrl, self).__init__(*args, **kwargs)
		self.__flag = threading.Event()	 # 用于暂停线程的标识
		self.__flag.set()	   # 设置为True
		self.__running = threading.Event()	  # 用于停止线程的标识
		self.__running.set()	  # 将running设置为True

	def run(self):
		while self.__running.isSet():
			self.__flag.wait()	  # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
			try:
				with canvas(device) as draw:
					draw.text((0, 0), text_1, fill="white")
					draw.text((0, 10), text_2, fill="white")
					draw.text((0, 20), text_3, fill="white")
					draw.text((0, 30), text_4, fill="white")
					draw.text((0, 40), text_5, fill="white")
					draw.text((0, 50), text_6, fill="white")
			except:
				pass
			print('loop')
			self.pause()

	def pause(self):
		self.__flag.clear()	 # 设置为False, 让线程阻塞

	def resume(self):
		self.__flag.set()	# 设置为True, 让线程停止阻塞

	def stop(self):
		self.__flag.set()	   # 将线程从暂停状态恢复, 如何已经暂停的话
		self.__running.clear()		# 设置为False  

	def screen_show(self, position, text):
		'''
		调用这个函数来控制OLED屏幕，其中position是想要改变内容的所在行编号，可以为1-6， text为内容
		'''
		global text_1, text_2, text_3, text_4, text_5, text_6
		if position == 1:
			text_1 = text
		elif position == 2:
			text_2 = text
		elif position == 3:
			text_3 = text
		elif position == 4:
			text_4 = text
		elif position == 5:
			text_5 = text
		elif position == 6:
			text_6 = text
		self.resume()

if __name__ == '__main__':
	'''
	实例化OLED屏幕对象
	'''
	screen = OLED_ctrl()

	'''
	开启这个线程
	'''
	screen.start()

	'''
	设置第一行的内容为12345678
	'''
	screen.screen_show(1, '123345678')

	'''
	由于上面的操作不会阻塞线程，所以这里要做循环避免执行完成后程序退出
	'''
	while 1:
		time.sleep(10)
		pass