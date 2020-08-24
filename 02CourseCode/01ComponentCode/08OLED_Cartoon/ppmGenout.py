import os
from PIL import Image
import time

jpgPath = 'jpg/' # 导入就jpg图像的位置
ppmPath = 'ppm/' # 导出ppm图像的位置

jpgNames = os.listdir(jpgPath) # 获取jpg文件夹内所有jpe图像的文件名


for frameName in jpgNames: # 一个一个转换
	image = Image.open(jpgPath+frameName) # 打开一个jpg图形
	newName = frameName[:-4]+'.ppm'		# 新的名字要把原名字中的.jpg删掉，加上.ppm
	image.save((ppmPath+newName), 'ppm') # 保存为ppm格式的文件，保存在ppm文件夹内