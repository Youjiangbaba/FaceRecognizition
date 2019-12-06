# FaceRecognizition
增加c++版本；opencv 2.4.10


4.11更新c++版本：
替代生成csv文件的py文件，不再用c++调用py;
实现功能，录入样本存取在txt中，方便目录查找与识别到后的label显示;
问题：while((ptr = readdir(dir)) != NULL) //循环读取目录数据 //（为什么这个遍历机制不会在扫描完成之前重复扫描）!!!


7.18
python利用dlib实现识别。
![image text](https://github.com/Youjiangbaba/FaceRecognizition/blob/master/c%2B%2B%E7%89%88%E6%9C%AC/test7-18.gif)


2019.12.6
 1. 增加眨眼、张嘴检测（活体检测）；
 2. 增加打卡界面；

 ***改动：***
**人脸检测：**opencv （haar cascade） ——> dlib （get_frontal_face_detector）
|  | opencv | dlib |
|--|-|--|
|10fps  |0. 1015s |0.1049s |
|稳定性||更稳定|
**增加68关键点：**`predictor = dlib.shape_predictor(face_landmark_path)#得到脸部68个关键点`
*opencv rect 得到关键点*
```
                def convert_rect(cv_faces):
                    dlib_faces = []
                    for  (x, y, w, h) in cv_faces:
                        rect = dlib.rectangle(int(x), int(y), int(x+w), int(y+h))
                        dlib_faces.append(rect)
                    return dlib_faces
                face_rects =  convert_rect(faces)
```
**眨眼、张嘴对比，每帧关键点位置与前一秒所有帧进行对比，差异较大则判为活体。
![image text](https://github.com/Youjiangbaba/FaceRecognizition/blob/master/live_face_recog/img/show/show.gif)
