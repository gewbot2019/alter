import Adafruit_PCA9685		#导入控制舵机的库
import time

pwm = Adafruit_PCA9685.PCA9685()	 # 实例化舵机控制对象
pwm.set_pwm_freq(50)	# 设置舵机的PWM频率（频率不是占空比）

ctrlPort   = 8
startMoveA = 339	# 比较大的一个
startMoveB = 314	# 上一步记下的那两个数中比较小的一个 
'''
那两个数相加除以二，取中间值当作控制舵机停止转动的PWM，int（）用于将结果转换为整型
'''
stopPWM = int((startMoveA+startMoveB)/2)


'''
参数direction导入1和-1控制转动方向，导入0为停止转动
参数speed导入速度大小，不导入的话默认值为0
'''
def ctrlServo(direction, speed=0):
	if direction == -1:
		setPWM = startMoveA - speed
	elif direction == 1:
		setPWM = startMoveB + speed
	elif direction == 0:
		setPWM = stopPWM

	pwm.set_pwm(ctrlPort, 0, setPWM)

# 按照位置导入参数，第一位是direction，第二位是speed
ctrlServo(-1, 100)
time.sleep(2)
# 按照参数名称进行导入，位置关系可随意
ctrlServo(speed = 50, direction = 1)
time.sleep(2)
# 不导入speed参数，则speed为默认值
ctrlServo(0)