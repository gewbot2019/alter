import Adafruit_PCA9685	#导入控制舵机的库

pwm = Adafruit_PCA9685.PCA9685()	# 实例化舵机控制对象
pwm.set_pwm_freq(50)	# 设置舵机的PWM频率（频率不是占空比）
'''
先随便定义一个初始的PWM数值，ctrl+c退出运行后会将对应接口的PWM值设置回这个初始值
'''
initPWM  = 320
setPWM   = initPWM	# 这个变量是在程序执行过程中需要改变的
ctrlPort = 8	#舵机连接的是哪个PWM口，就填哪个数字，这里填8就要将舵机连接到8号PWM口

# 定义一个主函数，用来执行具体操作
def main():
	'''
	由于这个数值在函数外部被定义，属于全局变量，在函数中改变全局变量前需要将其声明为全局变量
	'''
	global setPWM
	while 1:
		commandInput = input()
		if commandInput == 'w':	# 获得键盘输入的指令
			setPWM += 1		# PWM值加1
		elif commandInput == 's':	# 如果输入的是‘s’
			setPWM -= 1		 # PWM值减1

		pwm.set_pwm(ctrlPort, 0, setPWM)	# 将ctrl这个舵机口的PWM值设置为新的PWM值
		print(setPWM)	# 终端中打印出新设置的PWM值

'''
如果ctrl+c退出运行，舵机口被设置为initPWM
'''
try:
	main()
except KeyboardInterrupt:
	pwm.set_pwm(ctrlPort, 0, initPWM)