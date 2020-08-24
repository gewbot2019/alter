import Adafruit_PCA9685   # 导入用来与PCA9685进行通信的库
import time
  
pwm = Adafruit_PCA9685.PCA9685()    # 实例化用来控制PWM的对象
pwm.set_pwm_freq(50)    # 设置PWM信号的频率
  
while 1:
      for i in range(0,100):    # 使舵机从300缓慢运动到400
          pwm.set_pwm(3, 0, (300+i))
          time.sleep(0.05)
      for i in range(0,100):    # 使舵机从400缓慢运动到300
          pwm.set_pwm(3, 0, (400-i))
          time.sleep(0.05)