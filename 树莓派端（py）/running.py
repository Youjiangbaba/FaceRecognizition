# -*- coding: utf-8 -*-
import golbal_define as gd
from HARDWARE import HardWare
import sys, cv2, time ,os
import numpy as np


from PyQt5 import QtCore, QtGui, QtWidgets

from windows import Ui_TabWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog,QTabWidget, QMessageBox
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QImage

#import pdb  #debug


class mywindow(QTabWidget,Ui_TabWidget): #这个窗口继承了用QtDesignner 绘制的窗口
    def __init__(self):
        super(mywindow,self).__init__()
        self.setupUi(self)
        HardWare.IO_Init()
        kk = 0       				# kk = 1  auto open camera
        if kk==1:
            self.videoprocessing() 	        # 启动摄像头线程
            kk = 100



    def videoprocessing(self):
        print("open camera")				 
        th = Thread(self)			 	
        th.changePixmap.connect(self.setImage)         
        th.start()					#开启显示进程

    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))  #label显示

class Thread(QThread):#采用线程来播放视频

    global id, minH, minW, font, recognizer, faceCascade, names
    changePixmap = pyqtSignal(QtGui.QImage)
    
    #线程主函数
    def run(self):
        #HardWare.IO_Init()            
        global none_save                            
        none_save = 0
        if_dist = 1				   
   #pdb.set_trace()  # start debug
        while 1:
            #time.sleep(2)
            if_dist = HardWare.if_distance()	   
            print(if_dist)
            if if_dist == 0:			    
                flag = self.if_recognize(100,1)     #用户自己修改，100代表检测一百帧，1代表识别到就跳出
                print(flag)
		#识别失败，保存图片
                if flag == 'False':
                    none_save += 1
                    
		#识别到用户开门
                else:					
                    HardWare.openDoor()
                    time.sleep(5)
                    HardWare.closeDoor()
            else:
                HardWare.closeDoor()            #没人始终关门

            




    #封装人脸识别函数，实现功能： 输入 指定帧数 图像，凡是指定帧有 n张 识别成功 or 识别到连续的为同一个人，则返回 name；否则返回 false。
    def if_recognize(self,in_nums,ok_nums):
        cap = cv2.VideoCapture(0)
        last_id = 0
        i = 0
        ok_i = 0
        
        while 1:
            if cap.isOpened()==True:
                ret, img = cap.read()
                i += 1
                #img = cv2.resize(img, (320, 240), cv2.INTER_CUBIC)  # 缩小图像处理，增加帧率
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(  # 人脸检测
                    gray,
                    scaleFactor=1.2,
                    minNeighbors=5,
                    minSize=(int(minW), int(minH)),
                )
                if i >= in_nums:																			
					cv2.imwrite('none/'+str(none_save)+'.png',img,[int(cv2.IMWRITE_PNG_COMPRESSION),9])     
                    cap.release()																			
                    img.fill(255)																			
                    cv2.putText(img,' False !',(20,120),cv2.FONT_HERSHEY_SIMPLEX,2.0,(0,0,0),2)            	
                    rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)											
                    convertToQtFormat = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],	
                                                 QImage.Format_RGB888)
                    p = convertToQtFormat.scaled(gd.show_w, gd.show_h, Qt.KeepAspectRatio)					
                    self.changePixmap.emit(p)																
                    break

                count = 0								
                for (x, y, w, h) in faces:
                    count += 1								
                    if count>=2:							
                        break
                    # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
                    # 置信度 confidence ；  0 最完美
                    if (confidence < 80):
                        ok_i += 1
                        if (last_id == id)|(ok_i >= ok_nums):   
                            id = names[id]
                            #识别完一次之后，释放摄像头，并关闭显示
                            cap.release()
                            img.fill(255)
                            cv2.putText(img,'Success ! ',(50,150),cv2.FONT_HERSHEY_SIMPLEX,2.0,(0,0,0),2)
                            cv2.putText(img,'Welcome '+str(id)+'!',(10,250),cv2.FONT_HERSHEY_SIMPLEX,2.0,(0,0,0),2)
                            rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            convertToQtFormat = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],
                                                 QImage.Format_RGB888)  										# 在这里可以对每帧图像进行处理，
                            p = convertToQtFormat.scaled(gd.show_w, gd.show_h, Qt.KeepAspectRatio)
                            self.changePixmap.emit(p)
                            return str(id)
                        last_id = id

                    else:
                        id = "unknown"
                        continue

                rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],
                                                 QImage.Format_RGB888)  
                p = convertToQtFormat.scaled(gd.show_w, gd.show_h, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)


        return 'False'




if __name__ == '__main__':

    global kk
    print('wait for load...')
    recognizer = cv2.face.LBPHFaceRecognizer_create()        # opencv 识别api 我们用的局部二值特征 LBP
    recognizer.read('trainer/trainer.yml')                   # 下载人脸识别器
    cascadePath = "haarcascade_frontalface_default.xml"      # 下载人脸检测器
    print('load completed')
    faceCascade = cv2.CascadeClassifier(cascadePath);
    font = cv2.FONT_HERSHEY_SIMPLEX                          
    # iniciate id counter
    id = 0
    # 名字列表，分别对应 0 ，1 ，2 ，3 ...
    names = ['None', 'YJ', 'ZJN', 'CXB']

    # 定义被识别的最小窗口
    minW = 0.05 * 640
    minH = 0.05 * 480


    #启动qt窗口
    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()
    sys.exit(app.exec_())
