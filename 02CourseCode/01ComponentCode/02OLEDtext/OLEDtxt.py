#导入用于控制OLED屏幕和延迟时间的库
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
import time

#实例化用于控制OLED的对象
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, rotate=0)

#在OLED屏幕上（0，20）的位置上写文字“ROBOT”
with canvas(device) as draw:
    draw.text((0, 20), "ROBOT", fill="white")

while True:
    time.sleep(10)