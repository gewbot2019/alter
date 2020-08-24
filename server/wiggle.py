'''
本程序需要放在server文件夹内运行
当机器人倒地后，机器人腿部会有摆动动作
'''
import alterMove
import time

'''
导入随机函数库
'''
import random

'''
导入MPU6050库
'''
from mpu6050 import mpu6050

'''
导入卡曼滤波库
'''
import Kalman_filter

'''
实例化MPU6050对象，默认I2C地址为0x68
'''
sensor = mpu6050(0x68)
print('mpu6050 connected')

'''
实例化XY轴的卡曼滤波对象，卡曼滤波可以让从传感器读取到的数值变得更加平滑
由于只需要检测Y轴读数所以这里只需要实例化一个卡曼滤波对象
'''
kfY = Kalman_filter.Kalman_filter(0.01,0.1)

'''
当机器人站立时的高度
'''
stayHeight = 55

'''
设置机器人腿部摆动的范围
'''
wiggleRange = 10

'''
使用这里的这个变量来设置每两次循环之间的时间间隔
'''
mpuDelay = 0.1

'''
设置判断机器人是否倒下的阈值
'''
failValue = 6

'''
检测到机器人被扶正后，执行这一函数来控制机器人站稳
'''
def standStill():
	alterMove.linkageQ(1, 0, stayHeight)
	alterMove.linkageQ(2, 0, stayHeight)
	alterMove.linkageQ(3, 0, stayHeight)
	alterMove.linkageQ(4, 0, stayHeight)


'''
检测到机器人倒地后，执行这一函数来控制机器人腿部随机摆动
'''
def wiggle():
	'''
	使用randint()来生成-wiggleRange到wiggleRange之间的整数
	'''
	alterMove.linkageQ(1, 0, stayHeight + random.randint(-wiggleRange,wiggleRange))
	alterMove.linkageQ(2, 0, stayHeight + random.randint(-wiggleRange,wiggleRange))
	alterMove.linkageQ(3, 0, stayHeight + random.randint(-wiggleRange,wiggleRange))
	alterMove.linkageQ(4, 0, stayHeight + random.randint(-wiggleRange,wiggleRange))


if __name__ == '__main__':
	while True:
		'''
		如果I2C通信断开连接，重新实例化MPU6050对象
		'''
		try:
			valueGet = sensor.get_accel_data()
			print(valueGet)
		except:
			sensor = mpu6050(0x68)
			print('mpu6050 connected')

		'''
		获取MPU6050的Y轴读数，使用卡曼滤波消除MPU6050读数的噪波
		'''
		yGet = kfY.kalman(valueGet['y'])

		'''
		如果Y轴读数大于用来判断机器人是否倒下的阈值的绝对值，则摆动腿部
		否则站立不动
		'''
		if abs(yGet) > failValue:
			wiggle()
		else:
			standStill()

		'''
		延迟一段时间再进行下一次循环
		'''
		time.sleep(mpuDelay)

