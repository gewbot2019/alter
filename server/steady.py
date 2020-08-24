'''
本程序需要放在server文件夹内运行
'''
import alterMove
import time

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
'''
kfX = Kalman_filter.Kalman_filter(0.01,0.1)
kfY = Kalman_filter.Kalman_filter(0.01,0.1)

'''
设置最大高度和最小高度
并通过最大高度和最小高度求出中间高度
当机器人处于水平平面上时，机器人的每条腿都是处于中间高度的状态
最大最小高度用来限制机器人腿部的活动范围
'''
maxHeight = 65.0
minHeight = 45.0
middleHeight = (maxHeight + minHeight)/2

'''
由于自动平衡模式需要不间断从MPU6050中读取信息
读取一次信息计算一次变化趋势再将新的角度应用给舵机，这一些列动作称作一次循环
所以使用这里的这个变量来设置每两次循环之间的时间间隔
'''
mpuDelay = 0.05

'''
如果机器人放在水平面时上下俯仰一定角度，则修改xMiddle
如果机器人放在水平面时左右倾斜一定角度，则修改yMiddle
这个也可以反过来用，比如你想让机器人保持某一角度时，可以调整这两个变量
'''
xMiddle  = 1.3
yMiddle  = 0

'''
简易PID控制器中的P值，比例参数，如果机器人动作缓慢则增加这一数值
如果机器人稳定不下来抖动过大，则减小这一数值
'''
valueP   = 0.7

'''
因为这个控制方法是闭环控制
所以将累积的错误（error）保存在这两个变量中
这使得机器人即使处于不断晃动的面板上，也可以随时保持水平
'''
pitchValue = 0
rollValue  = 0


'''
这个函数用于限制某一变量的大小
输入最大值和最小值，输入需要限制的变量
返回值处于最大值和最小值之间（包括最大最小值）
'''
def rangeCtrl(minIn, maxIn, val):
	if val > maxIn:
		val = maxIn
	elif val < minIn:
		val = minIn
	return val


'''
这个函数用于调整机器人的角度：
pitch是俯仰运动
roll是翻滚运动
pIn用于调整pitch轴运动，pIn数值越大机器人越仰头
rIn用于调整roll轴运动，rIn数值越大机器人越向左侧倾斜
'''
def pitchRoll(pIn, rIn):
	'''
	由于自动稳定模式时不需要腿部的前后运动
	所以每条腿末端点的X轴坐标点都为0
	'''
	xIn = 0

	'''
	通过pIn和rIn来计算出每条腿末端点坐标值Y值
	'''
	y_1 = rangeCtrl(minHeight, maxHeight, middleHeight + pIn - rIn)
	y_2 = rangeCtrl(minHeight, maxHeight, middleHeight - pIn - rIn)
	y_3 = rangeCtrl(minHeight, maxHeight, middleHeight + pIn + rIn)
	y_4 = rangeCtrl(minHeight, maxHeight, middleHeight - pIn + rIn)

	'''
	将新的坐标值应用于四条腿
	'''
	alterMove.linkageQ(1, xIn, y_1)
	alterMove.linkageQ(2, xIn, y_2)
	alterMove.linkageQ(3, xIn, y_3)
	alterMove.linkageQ(4, xIn, y_4)


'''
这个函数是自稳功能的函数
循环调用它即可实现自稳功能
'''
def steadyProcessing():
	'''
	声明为全局变量
	'''
	global pitchValue, rollValue, sensor

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
	获取MPU6050的X轴和Y轴读数，使用卡曼滤波消除MPU6050读数的噪波
	'''
	xGet = kfX.kalman(valueGet['x'])
	yGet = kfY.kalman(valueGet['y'])

	'''
	计算出每个轴的偏差值
	'''
	xDebug = xGet - xMiddle
	yDebug = yGet - yMiddle

	'''
	根据偏差值计算出pitchValue和rollValue，并将结果应用于pitchRoll()
	'''
	pitchValue = rangeCtrl((minHeight - middleHeight), (maxHeight - middleHeight), pitchValue + xDebug*valueP)
	rollValue  = rangeCtrl((minHeight - middleHeight), (maxHeight - middleHeight), rollValue - yDebug*valueP)
	pitchRoll(pitchValue, rollValue)

	'''
	延迟一段时间再进行下一次循环
	'''
	time.sleep(mpuDelay)


if __name__ == '__main__':
	while True:
		steadyProcessing()