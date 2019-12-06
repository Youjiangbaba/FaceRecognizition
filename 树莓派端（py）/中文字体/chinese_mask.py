#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy
from PIL import Image, ImageDraw, ImageFont

class chineseShow:
	def init_font(self,size):
		global font
		font = ImageFont.truetype("./YaHei.ttf", 40)
	def show_test(self,img,position,strr):
		img_OpenCV = img.copy()
		# 图像从OpenCV格式转换成PIL格式
		img_PIL = Image.fromarray(cv2.cvtColor(img_OpenCV, cv2.COLOR_BGR2RGB))
		# 字体  字体*.ttc的存放路径一般是： /usr/share/fonts/opentype/noto/ 查找指令locate *.ttc
		
		# 字体颜色
		fillColor = (0,255,0)
		# 文字输出位置
		#position = (x,y)	 
		# 需要先把输出的中文字符转换成Unicode编码形式
		if not isinstance(strr, unicode):
			strr = strr.decode('utf8')
		draw = ImageDraw.Draw(img_PIL)
		draw.text(position, strr, font=font, fill=fillColor)
		# 转换回OpenCV格式
		img_OpenCV = cv2.cvtColor(numpy.asarray(img_PIL),cv2.COLOR_RGB2BGR)
		cv2.imshow("print chinese to image",img_OpenCV)
		return img_OpenCV


if __name__ == '__main__':
	p = chineseShow()
	image = cv2.imread("/home/jiang/图片/labartest.png")
	p.init_font(10)
	img = p.show_test(image,(10,50),"喜欢你")
	img = p.show_test(img,(1,5),"喜欢你")
	cv2.waitKey(0)
	cv2.destroyAllWindows()
