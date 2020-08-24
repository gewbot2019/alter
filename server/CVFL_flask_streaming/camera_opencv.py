import os
import cv2
from base_camera import BaseCamera
import numpy as np
import time
import threading
import imutils

'''
设置线的颜色，255是白线，0是黑线
'''
lineColorSet = 255
'''
设置参考的横行位置，数值越大越靠下，但是不能大于视频的竖行分辨率（默认480）
'''
linePos = 380

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
			_, img = camera.read() #获取摄像头采集的画面

			'''
			将画面转换为黑白，再二值化（画面中每个像素点的取值除了0就是255）
			'''
			img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			retval, img =  cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)
			img = cv2.erode(img, None, iterations=6)	#使用腐蚀去噪
			colorPos = img[linePos]						#获取linePos这一行的像素点数值组成的数组
			try:
				lineColorCount_Pos = np.sum(colorPos == lineColorSet)	#获取线颜色的像素点数量（线宽）
				lineIndex_Pos = np.where(colorPos == lineColorSet)		#获取线的端点在linePos这一行的横行位置
				'''
				使用端点位置和线宽来计算出线中心点的位置
				'''
				left_Pos = lineIndex_Pos[0][lineColorCount_Pos-1]
				right_Pos = lineIndex_Pos[0][0]
				center_Pos = int((left_Pos+right_Pos)/2)

				print('线中心点的位置为：%d'%center_Pos)
			except:
				'''
				如果没有检测到线，上面的线宽为0做分母会导致报错，这样就知道没有线被检测到了
				'''
				center_Pos = 0
				print('没有检测到线')

			'''
			画出横行参考线
			'''
			cv2.line(img,(0,linePos),(640,linePos),(255,255,64),1)
			if center_Pos:
				'''
				如果检测到线了，画出这个线的中心点位置
				'''
				cv2.line(img,(center_Pos,linePos+300),(center_Pos,linePos-300),(255,255,64),1)

			
			# encode as a jpeg image and return it
			yield cv2.imencode('.jpg', img)[1].tobytes()