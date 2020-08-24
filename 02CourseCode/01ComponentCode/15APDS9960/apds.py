'''
导入apds9960相关的库
'''
import smbus2
from apds9960.const import *
from apds9960 import APDS9960

'''
apds9960的I2C通信，如果线没有连接或连接错误这一步会报错
'''
port = 1
address = 0x39
bus = smbus2.SMBus(port)

'''
对象实例化
'''
apds = APDS9960(bus)
apds.setProximityIntLowThreshold(50)

'''
开始读取手势信息
'''
print("Gesture Test")
apds.enableGestureSensor()
while 1:
	if apds.isGestureAvailable():
		motion = apds.readGesture()
		print(motion)
	'''
	apds.readGesture()的返回值有大概5种
	包括从左到右 从右到左 从上到下 从下到上 从近到远
	用数字 1 2 3 4 5代替，具体哪个数字对应哪个手势取决于你的传感器摆放位置
	'''
	pass