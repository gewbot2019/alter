import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)		# 当GPIO重复定义时会有警告，忽略掉警告
GPIO.setmode(GPIO.BCM)		# 设置为BCM编码编码方式
GPIO.setup(5, GPIO.OUT)		# Port1接口对应的GPIO引脚的BCM编号是5
GPIO.setup(6, GPIO.OUT)		# Port1接口对应的GPIO引脚的BCM编号是6
GPIO.setup(13, GPIO.OUT)	# Port1接口对应的GPIO引脚的BCM编号是13

GPIO.output(5, GPIO.HIGH)	#开启Port1接口
GPIO.output(6, GPIO.HIGH)	#开启Port2接口
GPIO.output(13, GPIO.HIGH)	#开启Port3接口

time.sleep(3)	#延时3s

GPIO.output(5,GPIO.LOW)	#关闭Port1接口
GPIO.output(6,GPIO.LOW)	#关闭Port2接口
GPIO.output(13,GPIO.LOW)	#关闭Port3接口