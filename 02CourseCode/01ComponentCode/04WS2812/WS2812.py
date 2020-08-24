import time
from rpi_ws281x import *
class LED:  
    def __init__(self):  
        self.LED_COUNT      = 16 # 设置为机器人产品上的 LED 灯总数，可以比连接在树莓派上的LED灯的总数更多
        self.LED_PIN        = 12 # 设置为 LED 灯组的输入端针脚号  
        self.LED_FREQ_HZ    = 800000   
        self.LED_DMA        = 10   
        self.LED_BRIGHTNESS = 255  
        self.LED_INVERT     = False  
        self.LED_CHANNEL    = 0  
  
        # 使用上面的配置项创建一个 strip  
        self.strip = Adafruit_NeoPixel(  
            self.LED_COUNT,  
            self.LED_PIN,  
            self.LED_FREQ_HZ,  
            self.LED_DMA,  
            self.LED_INVERT,   
            self.LED_BRIGHTNESS,   
            self.LED_CHANNEL  
            )  
        self.strip.begin()  
    def colorWipe(self, R, G, B): # 此函数用于使 LED 灯变色  
            color = Color(R, G, B)
            for i in range(self.strip.numPixels()): # 每次只能设置一个 LED灯的颜色，所以要做一个循环  
                self.strip.setPixelColor(i, color)   
                self.strip.show() # 调用 show 方法后，颜色才会真正改变
if __name__ == '__main__':  
    LED = LED()  
    try:  
        while 1:  
            LED.colorWipe(255, 0, 0)  # 所有灯变为红色
            time.sleep(1)  
            LED.colorWipe(0, 255, 0)  # 所有灯变为绿色
            time.sleep(1)  
            LED.colorWipe(0, 0, 255)  # 所有灯变为蓝色
            time.sleep(1)  
    except:  
        LED.colorWipe(Color(0,0,0))  # 熄灭所有灯
