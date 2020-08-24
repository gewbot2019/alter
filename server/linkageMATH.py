#!/usr/bin/python3
'''
导入用于控制舵机的库
'''
import Adafruit_PCA9685
import time

'''
导入数学函数库
'''
import numpy as np 

'''
实例化用于控制舵机的库
'''
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)


'''
当舵机摇臂垂直向下时的对应舵机的PWM数值
这里只以DOG的前进方向左前方的腿作为例子
左前方腿的两个舵机对应PWM口编号分别为0和1
此处两个变量的具体值每个机器人都是不一样的
'''
init_pwm0 = 348
init_pwm1 = 215

'''
这个数组用于调整每个舵机的摆动方向
'''
sc_direction = [1,-1]

'''
LA是连杆第一个关节的长度
LB是连杆第二个关节的长度
LC是一条腿中两个舵机轴之间的距离
'''
LA = 23.0
LB = 51.336
LC = 12.5

linkageDInput = [LA, LB]

'''
舵机角度控制相关的参数
ctrlRangeMax是舵机最大有效PWM
ctrlRangeMin是舵机最小有效PWM
angleRange是舵机的实际转动范围
'''
ctrlRangeMax = 560
ctrlRangeMin = 100
angleRange = 205

'''
这个函数输入角度来返回PWM数值
'''
def anGen(ani):
	return int(round(((ctrlRangeMax-ctrlRangeMin)/angleRange*ani),0))


'''
这个函数传入腿部两个连杆的长度参数，舵机编号和坐标点
返回值为该舵机所需要摆动的角度
'''
def linkageD(linkageLen, servoNum, goalPosZ):
	'''
	此处数学原理可以参考文档中的图A
	'''
	sqrtGenOut = np.sqrt(goalPosZ[0]*goalPosZ[0]+goalPosZ[1]*goalPosZ[1])
	nGenOut = (linkageLen[0]*linkageLen[0]+goalPosZ[0]*goalPosZ[0]+goalPosZ[1]*goalPosZ[1]-linkageLen[1]*linkageLen[1])/(2*linkageLen[0]*sqrtGenOut)
	angleA = np.arccos(nGenOut)*180/np.pi

	AB = goalPosZ[1]/goalPosZ[0]

	angleB = np.arctan(AB)*180/np.pi
	angleGenA = angleB - angleA

	'''
	通过将返回的角度乘以
	'''
	return angleGenA*sc_direction[servoNum]


'''
这个函数传入坐标点，控制腿部末端的一点运动到改坐标点，同时返回两个舵机的角度
'''
def linkageQ(x, y):
	'''
	此处数学原理可以参考文档中的图B
	'''
	x = -x
	x1 = x-LC/2
	x2 = -x1-LC/2

	a = linkageD(linkageDInput, 0, [y,x1])
	b = linkageD(linkageDInput, 1, [y,x2])
	pwm.set_pwm(0,0,init_pwm0 + anGen(a))
	pwm.set_pwm(1,0,init_pwm1 + anGen(b))

	return a,b


if __name__ == '__main__':
	while True:
		linkageQ(15, 60)
		time.sleep(1)
		linkageQ(-15, 60)
		time.sleep(2)