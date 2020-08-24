import Adafruit_PCA9685	# 导入用来与PCA9685进行通信的库
import time

pwm = Adafruit_PCA9685.PCA9685()	# 实例化用来控制PWM的对象
pwm.set_pwm_freq(50)	# 设置PWM信号的频率

# 使与RobotHAT驱动板上面三号舵机口相连的舵机进行往复摆动
while 1:
	pwm.set_pwm(3, 0, 300)
	time.sleep(1)
	pwm.set_pwm(3, 0, 400)
	time.sleep(1)