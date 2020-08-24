import alterMove
import time

'''
直接调用alterMove.linkageQ(leg, x, y)函数即可
其中leg可以为1、2、3、4分别对应四条腿

具体来说：

1-forward-3
|		  |
|		  |
|		  |
|		  |
2—————————4

x,y参数为着地点的坐标，x正值越大，着地点越偏向前进方向
y正值越大，着地点越偏向地面方向

当你控制每条腿的着地点位置时，不需要实例化Alter对象
因为实例化Alter对象主要目的是进行多线程控制

你可以通过编写着地点位置和设置恰当的延迟时间，为机器人编舞或者编辑其它动作

以下例程分别控制机器人的1、2、3、4号腿摆动，可以直观了解改函数地调用方法
'''
while 1:
	alterMove.linkageQ(1, 15, 50)
	time.sleep(1)

	alterMove.linkageQ(2, 15, 50)
	time.sleep(1)

	alterMove.linkageQ(3, 15, 50)
	time.sleep(1)

	alterMove.linkageQ(4, 15, 50)
	time.sleep(1)

	alterMove.linkageQ(1, -15, 50)
	time.sleep(1)

	alterMove.linkageQ(2, -15, 50)
	time.sleep(1)

	alterMove.linkageQ(3, -15, 50)
	time.sleep(1)

	alterMove.linkageQ(4, -15, 50)
	time.sleep(1)