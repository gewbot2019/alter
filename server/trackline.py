import RPi.GPIO as GPIO
import time
import alterMove
'''
导入用于控制Alter的对象并实例化
'''
alter = alterMove.Alter()
alter.start()

'''
设置三路循迹模块的GPIO引脚号
'''
line_pin_right = 19
line_pin_middle = 16
line_pin_left = 20

'''
设置巡线时的速度
'''
moveSpeed = 100


'''
初始化GPIO
'''
def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(line_pin_right,GPIO.IN)
    GPIO.setup(line_pin_middle,GPIO.IN)
    GPIO.setup(line_pin_left,GPIO.IN)


'''
主函数
'''
def run():
    while 1:
        '''
        获取循迹模块的三个传感器的数值
        '''
        status_left = GPIO.input(line_pin_right)
        status_middle = GPIO.input(line_pin_middle)
        status_right = GPIO.input(line_pin_left)

        '''
        关掉ws2812的三个灯
        '''
        alterMove.setSome2812(0, 0, 0, [0, 1, 2])

        '''
        根据循迹模块的传感器数值决定WS2812的哪个灯亮，如果需要灯保持熄灭状态则让第4个灯亮（Alter不存在第四个灯，所以就是熄灭状态）
        '''
        '''
        使用灯的状态来观察机器人能否正确检测到线，如果不能正确检测到线，需要用螺丝刀调节循迹模块上面的电位器
        '''
        if status_left:
            leftStu = 0
        else:
            leftStu = 3

        if status_middle:
            middleStu = 1
        else:
            middleStu = 3

        if status_right:
            rightStu = 2
        else:
            rightStu = 3
        
        '''
        根据循迹模块的传感器数值亮起对应的灯，如果左右反了则调换leftStu和rightStu的位置
        '''
        alterMove.setSome2812(255, 64, 128, [rightStu, middleStu, leftStu])

        
        '''
        如果循迹模块的三个传感器都检测到了黑线一段时间或者机器人被拿起来一段时间，则停止运动
        '''
        if status_middle == 1 and status_left == 1 and status_right == 1:
            timeCut = 0
            while  GPIO.input(line_pin_right) and GPIO.input(line_pin_middle) and GPIO.input(line_pin_left):
                timeCut += 1
                time.sleep(0.01)
                if timeCut >= 50:
                    alter.moveStop()
                pass

        elif status_middle == 1:
            alter.moveAlter(moveSpeed, 'forward', 'no', 1)
        elif status_left == 1:
            alter.moveAlter(moveSpeed, 'no', 'left', 0.3)
        elif status_right == 1:
            alter.moveAlter(moveSpeed, 'no', 'right', 0.3)
        elif status_middle == 0 and status_left == 0 and status_right == 0:
            alter.moveAlter(moveSpeed, 'backward', 'no', 1)



if __name__ == '__main__':
    try:
        setup()
        while 1:
            run()
        pass
    except KeyboardInterrupt:
        alter.moveStop()