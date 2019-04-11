# FaceRecognizition
增加c++版本；opencv 2.4.10


4.11更新c++版本：
替代生成csv文件的py文件，不再用c++调用py;
实现功能，录入样本存取在txt中，方便目录查找与识别到后的label显示;
问题：while((ptr = readdir(dir)) != NULL) //循环读取目录数据 //（为什么这个遍历机制不会在扫描完成之前重复扫描）!!!
