#coding:utf-8
import cv2
import numpy as np
import dlib
import face_recognition
import time
import os
import shutil
import multiprocessing
from multiprocessing import Process ,Queue

from face_recog import FACE_RECOG


#返回现在时间
def nowDataTime():
    return time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))

# nowTime = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
def str2int(a):
    if a[0] == 0:
        return int(a[1])
    else:
        return 10*int(a[0]) + int(a[1])

#计算时间
def nowTime2time(nowtime):
    listT = nowtime.split('-')
    hour = str2int(listT[3])
    minute = str2int(listT[4])
    second = str2int(listT[5])
    return hour,minute,second


class GatePersonsLOG:
    '''
        9.24 功能：
                cap0 入口
                cap1 出口
                入口检测到人脸，不识别，直接放入人脸库中，以时间命名，多个增加index；
                出口检测到人脸到人脸，与已编码进行比对，成功则计算时间，并删除编码库中的人脸、名字
            
            其他：开机初始化，删除所有已存储样本
            两个进程，入口初始化、人脸检测并编码存储,存储前识别是否与之前的编码重复；出口实时识别并删除及填写停留时间。
    '''
    def __init__(self,save_dir,faces = 0):
        self.save_dir = save_dir
        self.save_faces = faces
        self.faceRcog = FACE_RECOG(self.save_dir)
        # self.everydayInit()
    '''
        每天初始化工作：
        1、情况存储文件夹
        2、
    '''
    def everydayInit(self):
        if os.path.exists(self.save_dir):
            shutil.rmtree(self.save_dir)
        os.mkdir(self.save_dir)

    #保存编码文件
    def saveEncodings(self,encodeds):
        now_time = nowDataTime()
        for root, dirs, files in os.walk(self.save_dir):
            if len(files) == 0:#不存在文件,直接存储编码
                for i,enc in  enumerate(encodeds):
                    np.save(os.path.join(root,"%s-%d.npy"%(now_time,i)),enc)
                    print('save %s!'%os.path.join(root,"%s-%d.npy"%(now_time,i)))
            else:
                savedEncodeds = []
                for f in files:
                    savedEnc = np.load(os.path.join(root,f))
                    savedEncodeds.append(savedEnc)#这里可先采用一个log进行记录，每次读取最新的---
                #与所有脸比较，都不满足就保存
                for i,enc in  enumerate(encodeds):
                    count_different = 0
                    for savedEnc in savedEncodeds:
                        conf = self.faceRcog.faceEncode_distance(savedEnc,enc)
                        if conf  < 0.4:#两个脸不相似
                            count_different += 1
                            print(conf)

                    #都不相似，保存
                    if count_different == len(savedEncodeds):
                        np.save(os.path.join(root,"%s-%d.npy"%(now_time,i)),enc)
                        print('save %s!'%os.path.join(root,"%s-%d.npy"%(now_time,i)))
    
    #识别编码文件，识别成功进行删除已存储文件、并记录停留时间
    def compareEncodings(self,encodeds):
        now_time = nowDataTime()
        for root, dirs, files in os.walk(self.save_dir):
            savedEncodeds = []
            savedNames = []
            for f in files:
                savedEnc = np.load(os.path.join(root,f))
                savedEncodeds.append(savedEnc)#这里可先采用一个log进行记录，每次读取最新的---
                savedNames.append(f)
            for enc in  encodeds:
                for savedEnc,name in  zip(savedEncodeds,savedNames):
                    conf = self.faceRcog.faceEncode_distance(savedEnc,enc) 
                    if  conf > 0.6:#两个脸相似度大于0.6,识别成功
                        print(conf)
                        #计算停留时间
                        that_time = nowTime2time(name.split('.')[0])
                        now_time = nowTime2time(now_time)
                        h = now_time[0] - that_time[0]
                        m = now_time[1] - that_time[1]
                        s = now_time[2] - that_time[2]
                        #删除已存储的编码样本
                        os.remove(os.path.join(root,name))
                        log =  "%s 停留时间 %d 小时 %d 分钟 %d 秒!"%(name.split('.')[0],h,m,s)
                        print('删除'+log)
                        
    '''
        读取rtsp流，抓取5次都失败则失败；
        若读取过程中，中断，继续尝试抓取5次；
        #入口cap 操作
    '''
    def entryDectect(self,inputRtsp):
        
        # opencv读取rtsp流，有时第一次抓不到，要多次抓取。    
        count_open_cap = 0
        print ('开始抓取！')
        cap = cv2.VideoCapture(inputRtsp)
        
        cv2.namedWindow("entry",2)
        
        while 1:
            if cap.isOpened():
                print ('抓取成功！')
                w,h,fps = int(cap.get(3)),int(cap.get(4)),int(cap.get(5))
                ret,img = cap.read()
                if ret:        
                    break
                else:
                    cap = cv2.VideoCapture(inputRtsp)
            else:
                count_open_cap += 1
                print ('尝试抓取第'+str(count_open_cap+1)+'次！')
                cap = cv2.VideoCapture(inputRtsp)
                if count_open_cap == 20:
                    break
            count_open_cap = 0
        while True:
            ret,img = cap.read()

            if ret == 0:
                count_open_cap += 1
                cap = cv2.VideoCapture(inputRtsp)
                print ('中断后，尝试抓取第'+str(count_open_cap+1)+'次！')
                if count_open_cap == 4:
                    print ('中断后，尝试抓取了5次，失败！')
                    break
                if count_open_cap != 0:
                    count_open_cap = 0
                    print ('抓取成功！')
                continue
            
            #读取了图片，开始处理
            # faceLocations = faceRcog.detect_byDlib(img,1)
            faceLocations = self.faceRcog.detect_byOpencv(img)
            for (top, right, bottom, left) in faceLocations:
                cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)
            encodeds = self.faceRcog.faceEncode(img,faceLocations)
            #保存
            self.saveEncodings(encodeds)
            cv2.imshow("entry",img)
            if cv2.waitKey(1) == ord('q'):#这个窗口按q退出
                break

        cap.release()
        cv2.destroyAllWindows()
        

    def leaveRecognition(self,inputRtsp):
        
        # opencv读取rtsp流，有时第一次抓不到，要多次抓取。    
        count_open_cap = 0
        print ('开始抓取！')
        cap = cv2.VideoCapture(inputRtsp)
        
        cv2.namedWindow("leave",2)
        
        while 1:
            if cap.isOpened():
                print ('抓取成功！')
                w,h,fps = int(cap.get(3)),int(cap.get(4)),int(cap.get(5))
                ret,img = cap.read()
                if ret:        
                    break
                else:
                    cap = cv2.VideoCapture(inputRtsp)
            else:
                count_open_cap += 1
                print ('尝试抓取第'+str(count_open_cap+1)+'次！')
                cap = cv2.VideoCapture(inputRtsp)
                if count_open_cap == 20:
                    break
            count_open_cap = 0
        while True:
            ret,img = cap.read()

            if ret == 0:
                count_open_cap += 1
                cap = cv2.VideoCapture(inputRtsp)
                print ('中断后，尝试抓取第'+str(count_open_cap+1)+'次！')
                if count_open_cap == 4:
                    print ('中断后，尝试抓取了5次，失败！')
                    break
                if count_open_cap != 0:
                    count_open_cap = 0
                    print ('抓取成功！')
                continue
            
            
            #读取到了图片
            # faceLocations = faceRcog.detect_byDlib(img,1)
            faceLocations = self.faceRcog.detect_byOpencv(img)
            for (top, right, bottom, left) in faceLocations:
                cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)
            encodeds = self.faceRcog.faceEncode(img,faceLocations)
            
            #识别
            self.compareEncodings(encodeds)
            
            #显示
            cv2.imshow("leave",img)
            if cv2.waitKey(1) == ord('q'):#这个窗口按q退出
                break
            
        cap.release()

if __name__ == "__main__":

    # entryRtsp = "rtsp://admin:boyun@192.168.31.193:554/live"
    # leaveRtsp = "rtsp://admin:boyun@192.168.31.228:554/live"
    entryRtsp = 0
    leaveRtsp = 2
    
    #开启多进程
    manager = multiprocessing.Manager()
    GateDetect = GatePersonsLOG('test')
    # GateDetect.entryDectect(2)
    # GateDetect.leaveRecognition(2)
    
    #开启一个进程
    t1 = Process(target=GateDetect.entryDectect,args=(entryRtsp,))
    t1.start()

    t2 = Process(target=GateDetect.leaveRecognition,args=(leaveRtsp,))
    t2.start()


    
    
