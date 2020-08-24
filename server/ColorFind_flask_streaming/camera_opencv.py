import os
import cv2
from base_camera import BaseCamera
import numpy as np

'''
设置目标颜色，HSV色彩空间
'''
colorUpper = np.array([44, 255, 255])
colorLower = np.array([24, 100, 100])

font = cv2.FONT_HERSHEY_SIMPLEX

class Camera(BaseCamera):
	video_source = 0

	def __init__(self):
		if os.environ.get('OPENCV_CAMERA_SOURCE'):
			Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
		super(Camera, self).__init__()

	@staticmethod
	def set_video_source(source):
		Camera.video_source = source

	@staticmethod
	def frames():
		camera = cv2.VideoCapture(Camera.video_source)
		if not camera.isOpened():
			raise RuntimeError('Could not start camera.')

		while True:
			# read current frame
			_, img = camera.read() #获取摄像头采集的画面

			hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)	#将采集的画面转换为HSV色彩空间
			mask = cv2.inRange(hsv, colorLower, colorUpper)	#在HSV色彩空间的画面中遍历在目标色彩范围内的色彩，并将这些色彩块变为遮罩
			mask = cv2.erode(mask, None, iterations=2)	#将画面中的小块遮罩（噪点）腐蚀变小（小块色彩或噪点消失）
			mask = cv2.dilate(mask, None, iterations=2)	#膨胀，将上一步被缩小的大块遮罩重新变为原来的大小
			cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
				cv2.CHAIN_APPROX_SIMPLE)[-2]			#查找画面中有几块遮罩
			center = None  		
			if len(cnts) > 0:	#如果画面中整块遮罩的数量大于一
				'''
				在画面中找到目标颜色的物体的中心点坐标和物体的大小
				'''
				c = max(cnts, key=cv2.contourArea)
				((box_x, box_y), radius) = cv2.minEnclosingCircle(c)
				M = cv2.moments(c)
				center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
				X = int(box_x)
				Y = int(box_y)
				'''
				获取目标颜色物体的中心点坐标并输出
				'''
				print('检测到目标颜色物体')
				print('X:%d'%X)
				print('Y:%d'%Y)
				print('-------')

				'''
				在画面中写文字：Target Detected
				'''
				cv2.putText(img,'Target Detected',(40,60), font, 0.5,(255,255,255),1,cv2.LINE_AA)
				'''
				在目标颜色物体周围画一个框
				'''
				cv2.rectangle(img,(int(box_x-radius),int(box_y+radius)),(int(box_x+radius),int(box_y-radius)),(255,255,255),1)
			else:
				cv2.putText(img,'Target Detecting',(40,60), font, 0.5,(255,255,255),1,cv2.LINE_AA)
				print('没有检测到目标颜色物体')
			
			# encode as a jpeg image and return it
			yield cv2.imencode('.jpg', img)[1].tobytes()