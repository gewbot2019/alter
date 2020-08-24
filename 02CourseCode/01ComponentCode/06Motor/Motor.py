#!/usr/bin/env python3

import time
import RPi.GPIO as GPIO


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# 对应接口 Motor A
Motor_EN    = 4
Motor_Pin1  = 26
Motor_Pin2  = 21

'''
Motor B接口对应BCM引脚号：EN 17, Pin1 27, Pin2 18
'''

GPIO.setup(Motor_EN, GPIO.OUT)
GPIO.setup(Motor_Pin1, GPIO.OUT)
GPIO.setup(Motor_Pin2, GPIO.OUT)

pwm_A = GPIO.PWM(Motor_EN, 1000)

if __name__ == '__main__':
	GPIO.output(Motor_Pin1, GPIO.HIGH)
	GPIO.output(Motor_Pin2, GPIO.LOW)
	pwm_A.start(100)

	pwm_A.ChangeDutyCycle(100)
	time.sleep(2)

	pwm_A.ChangeDutyCycle(20)
	time.sleep(2)

	#切换高低电平，让电机反向旋转
	GPIO.output(Motor_Pin1, GPIO.LOW)
	GPIO.output(Motor_Pin2, GPIO.HIGH)
	time.sleep(2)

	pwm_A.ChangeDutyCycle(100)
	time.sleep(2)

	GPIO.cleanup()
