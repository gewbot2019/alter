from mpu6050 import mpu6050
import time

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

sensor = mpu6050(0x68)

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, rotate=0)


while 1:
	xyzGet = sensor.get_accel_data()	#从传感器获取XYZ的读数信息

	xGet = xyzGet['x'] # 获取x轴读数
	yGet = xyzGet['y'] # 获取y轴读数
	zGet = xyzGet['z'] # 获取z轴读数

	#在OLED上显示出XYZ三轴数值
	with canvas(device) as draw:
		draw.text((0, 0), str(xGet), fill="white")
		draw.text((0, 20), str(yGet), fill="white")
		draw.text((0, 40), str(zGet), fill="white")

	time.sleep(0.1)