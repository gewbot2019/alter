from mpu6050 import mpu6050
import time

sensor = mpu6050(0x68)


while 1:
	xyzGet = sensor.get_accel_data()	#从传感器获取XYZ的读数信息

	xGet = xyzGet['x'] # 获取x轴读数
	yGet = xyzGet['y'] # 获取y轴读数
	zGet = xyzGet['z'] # 获取z轴读数

	print(xGet, yGet, zGet)
	time.sleep(0.5)