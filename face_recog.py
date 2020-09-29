#coding:utf-8
import cv2
import numpy as np
import dlib
import face_recognition
import time
import os
from chineseText import cv2ImgAddText


class FACE_RECOG:
    def __init__(self,std_faces):
        self.std_faces = std_faces
        self.detector = self.dlib_detect_init()
        self.faceCascade = self.opencv_detect_init()
        # self.std_encodings,self.total_image_name = self.face_recog_init()
        
    #初始化前脸检测器 _dlib
    def dlib_detect_init(self):
        detector=dlib.get_frontal_face_detector()
        return detector


    #初始化opencv检测器
    def opencv_detect_init(self):
        cascadePath = "haarcascade_frontalface_alt.xml"      # 下载人脸检测器
        print('load completed')
        faceCascade = cv2.CascadeClassifier(cascadePath)
        return faceCascade

    #opencv的人脸检测
    def detect_byOpencv(self,img,radio = 2):
        img = cv2.resize(img,(img.shape[1]//radio,img.shape[0]//radio))#缩放增加帧率
        if img.ndim == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        elif img.ndim == 2:#只有长宽。灰度
            gray = img.copy()
        else:
            print('异常图片')
            return False
        faces = self.faceCascade.detectMultiScale(gray, 1.3, 5)
        loctions = []
        #  rect to css
        for (x,y,w,h) in faces:
            top = y
            right = x + w
            bottom = y + h
            left = x
            loctions.append((top*radio, right*radio, bottom*radio, left*radio))   
        return loctions

    #dlib 人脸检测
    def detect_byDlib(self,img,radio = 2):#缩放增加帧率
        img = cv2.resize(img,(img.shape[1]//radio,img.shape[0]//radio))
        if img.ndim == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        elif img.ndim == 2:#只有长宽。灰度
            gray = img.copy()
        else:
            print('异常图片')
            return False
        faces=self.detector(gray,1)
        loctions = []
        for idx,face in enumerate(faces):
            left=face.left()
            right=face.right()
            top=face.top()
            bottom=face.bottom()
            loctions.append((top*radio, right*radio, bottom*radio, left*radio))   
        return loctions

    #人脸识别 初始化；初始化比对的样本
    def face_recog_init(self):
        path = self.std_faces # 模型数据图片目录  face_recognition face_test
        total_image_name = []
        total_face_encoding = []
        for fn in os.listdir(path):  #fn 表示的是文件名q
            print(path + "/" + fn)
            img = cv2.imread(path + "/" + fn)
            location_face = [[0,img.shape[1],img.shape[0],0]]
            total_face_encoding.append(
                face_recognition.face_encodings(
                    face_recognition.load_image_file(path + "/" + fn),location_face)[0])
            fn = fn[:(len(fn) - 4)]  #截取图片名（这里应该把images文件中的图片名命名为为人物名）
            total_image_name.append(fn)  #图片名字列表
        return total_face_encoding,total_image_name
        # img = face_recognition.load_image_file('std_img.jpg')
        # encoding_face = face_recognition.face_encodings(img)[0]
        # return encoding_face


    ''' 
    人脸识别函数
        输入：
            img 输入图像
            loctions 输入脸部位置 类型list
            std_encoding 需要比对的特征集
            start_flag=0 不开启  
        返回：
            绘制后的图像
            识别到的名字
            识别到的人脸
            比对成功的置信度（相似度）
    '''
    def face_recog_run(self,img,loctions,start_flag = 1):
        if len(loctions) == 0:
            print("没有检测到面部！")
            return img,[],[],[]
        
        #start_flag不开启识别
        if start_flag == 0:
            for (top, right, bottom, left) in loctions:
                cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)
            return img,-2

        result_name = []
        result_face = []
        confidences = []
        face_encodings = face_recognition.face_encodings(img, loctions)#这步比较耗时，对图像中人脸进行特在提取
        # 在这个视频帧中循环遍历每个人脸
        for (top, right, bottom, left), face_encoding in zip(loctions, face_encodings):
            cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)
            for i,std_encoding in enumerate(self.std_encodings):
                conf = face_recognition.face_distance([std_encoding], face_encoding)
                # match = face_recognition.compare_faces([std_encoding], face_encoding, tolerance=0.5)#0.5
                # if match[0]:
                if conf < 0.4:
                    # print(conf)
                    name = self.total_image_name[i]
                    result_name.append(name)
                    result_face.append(img[top:bottom,left:right])
                    confidences.append("%.3f"%(1 - conf))
                    # cv2.putText(img, name, (left, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.9,(255, 255, 255), 2)
                    
                    img = cv2ImgAddText(img, name, left, top, textColor=(0, 255, 0), textSize=20)
                    break
                else:
                    pass

        return img,result_name,result_face,confidences
    
    #人脸编码函数    
    def faceEncode(self,img,faces):
        face_encodings = face_recognition.face_encodings(img,faces)
        return face_encodings
    
    #人脸编码评价函数
    def faceEncode_distance(self,encoding1,encoding2):
        conf = face_recognition.face_distance([encoding1],encoding2)
        return 1-conf
