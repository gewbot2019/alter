import os
import cv2
from base_camera import BaseCamera
import numpy as np
import datetime
import time
import threading
import imutils

class CVThread(threading.Thread):
    '''
    这个类用来在后台处理OpenCV分析视频帧的任务，关于多线程类的更基本使用原理可以参考14.2
    '''
    def __init__(self, *args, **kwargs):
        self.CVThreading = 0

        super(CVThread, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()
        self.__flag.clear()

        
    def mode(self, imgInput):
        '''
        这个方法用于传入需要处理的视频帧
        '''
        self.imgCV = imgInput
        self.resume()

        
    def elementDraw(self,imgInput):
        '''
        在画面中绘制元素
        '''
        return imgInput

    
    def doOpenCV(self, frame_image):
        '''
        这里添加OpenCV要处理的内容
        '''
        self.pause()


    def pause(self):
        '''
        将线程阻塞，等待处理下一帧
        '''
        self.__flag.clear()
        self.CVThreading = 0

    def resume(self):
        '''
        将线程恢复
        '''
        self.__flag.set()

    def run(self):
        '''
        在后台线程处理视频帧
        '''
        while 1:
            self.__flag.wait()
            self.CVThreading = 1
            self.doOpenCV(self.imgCV)


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
        '''
        实例化CVThread()
        '''
        cvt = CVThread()
        cvt.start()

        while True:
            # read current frame
            _, img = camera.read()

            if cvt.CVThreading:
                '''
                如果OpenCV正在处理视频帧，跳过
                '''
                pass
            else:
                '''
                如果OpenCV没有在处理视频帧，则给处理视频帧的线程新的视频帧并恢复处理线程
                '''
                cvt.mode(img)
                cvt.resume()
            '''
            在画面上绘制元素
            '''
            img = cvt.elementDraw(img)

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()