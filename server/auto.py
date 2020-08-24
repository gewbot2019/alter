#!/usr/bin/env python3

import time
import RPi.GPIO as GPIO
import Adafruit_PCA9685
import alterMove
'''
导入用于控制Alter的对象并实例化
'''
alter = alterMove.Alter()
alter.start()


Tr = 11 		# 超声波模块输入端针脚号
Ec = 8 			# 超声波模块输出端针脚号
	
'''
本教程例子为普通的蓝色超声波模块
初始化超声波模块的GPIO
'''
GPIO.setmode(GPIO.BCM)
GPIO.setup(Tr, GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(Ec, GPIO.IN)


'''
当测距结果小于这一数值时，转向
'''
turnRange = 0.2

'''
调用此函数会获得测距的返回值
'''
def checkdist():
	GPIO.output(Tr, GPIO.HIGH) # 设置模块输入端为高电平，发出一段初始声波
	time.sleep(0.000015)
	GPIO.output(Tr, GPIO.LOW)

	while not GPIO.input(Ec): # 当模块不再接收到初始声波时
		pass
	t1 = time.time() # 记下初始声波发出时的时间
	while GPIO.input(Ec): # 当模块接收到返回声波时
		pass
	t2 = time.time() # 记下返回声波被捕获到时的时间

	return round((t2-t1)*340/2,2) # 计算距离


print('开启自动避障模式')
distDect = None

while 1:
	distDect = checkdist()
	print(distDect) # 打印出测距结果

	'''
	如果测得前方距离小于turnRang所规定的数值，则左转；否则向前走
	'''
	if distDect < turnRange:
		alter.moveAlter(100, 'no', 'left', 0.3)
	else:
		alter.moveAlter(100, 'forward', 'no', 1)