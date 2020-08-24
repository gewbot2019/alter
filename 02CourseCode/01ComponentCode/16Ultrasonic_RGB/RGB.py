'''
导入用来控制GPIO的库和时间相关的库
'''
import RPi.GPIO as GPIO
import time

'''
定义与RGB超声波相关的GPIO引脚号
'''
Tx = 11
Rx = 8

'''
调用这个函数可以返回距离信息
'''
def checkdist():
    '''
    GPIO引脚初始化，由于超声波测距和控制RGB灯颜色时的GPIO引脚的功能不同
    所以使用相关功能前需要将其根据具体的功能初始化
    '''
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Tx, GPIO.OUT)
    GPIO.setup(Rx, GPIO.OUT)
    
    '''
    控制RGB超声波进入测距模式
    '''
    GPIO.output(Tx, GPIO.LOW)
    GPIO.output(Rx, GPIO.HIGH)
    
    '''
    检测当Rx引脚电平变低后，说明超声波已经发出，获得时间t1
    '''
    GPIO.setup(Rx, GPIO.IN)
    while  GPIO.input(Rx):
        pass
    t1 = time.time()

    '''
    检测Rx引脚低电平的持续时间，当Rx引脚变为高电平后，获得时间t2
    '''
    while not GPIO.input(Rx):
        pass
    t2 = time.time()

    '''
    控制RGB超声波模块退出测距模式
    '''
    GPIO.setup(Tx, GPIO.OUT)
    GPIO.output(Tx, GPIO.HIGH)
    
    '''
    根据t1和t2以及声音在空气中的传播速度，计算出距离并返回数值
    '''
    return round((t2-t1)*340/2,2)


'''
调用这个函数改变RGB超声波上面的灯的颜色，分为红绿蓝三个通道，每个通道有两个状态（0和1）
R = 1, G = 0, B = 0 —— 红色
R = 0, G = 1, B = 0 —— 绿色
R = 0, G = 0, B = 1 —— 蓝色

R = 0, G = 0, B = 0 —— 熄灭
R = 1, G = 1, B = 1 —— 全亮（接近白色）
'''
def setColor(R, G, B):
    '''
    GPIO引脚初始化
    '''
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Tx, GPIO.OUT)
    GPIO.setup(Rx, GPIO.OUT)

    '''
    第一次进入改变颜色的模式，用来设置R通道状态
    '''
    GPIO.output(Rx, GPIO.LOW)
    GPIO.output(Tx, GPIO.HIGH)
    
    if R:
        GPIO.output(Rx, GPIO.HIGH)
    else:
        GPIO.output(Rx, GPIO.LOW)

    '''
    第二次进入改变颜色的模式，用来设置G通道状态
    '''
    GPIO.output(Tx, GPIO.LOW)
    GPIO.output(Tx, GPIO.HIGH)

    if G:
        GPIO.output(Rx, GPIO.HIGH)
    else:
        GPIO.output(Rx, GPIO.LOW)

    '''
    第三次进入改变颜色的模式，用来设置B通道状态
    '''
    GPIO.output(Tx, GPIO.LOW)
    GPIO.output(Tx, GPIO.HIGH)

    if B:
        GPIO.output(Rx, GPIO.HIGH)
    else:
        GPIO.output(Rx, GPIO.LOW)

    '''
    退出改变颜色
    '''
    GPIO.output(Tx, GPIO.LOW)
    GPIO.output(Tx, GPIO.HIGH)
    
    GPIO.output(Tx, GPIO.HIGH)
    GPIO.output(Rx, GPIO.HIGH)


if __name__ == '__main__':
    while 1:
        setColor(1,0,0)
        time.sleep(1)
        setColor(0,1,0)
        time.sleep(1)
        setColor(0,0,1)
        time.sleep(1)

        a = checkdist()
        print(a)

        time.sleep(0.1)