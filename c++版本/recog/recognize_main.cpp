#include <opencv2/opencv.hpp>
#include <iostream>
#include <fstream>
#include <string>

#include <dirent.h>
//#include <x86_64-linux-gnu/sys/io.h>

#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <stdio.h>

#include <python2.7/Python.h>

using namespace cv;
using namespace std;

string filepath = "trainer2.yml";
string haar_face_datapath = "haarcascade_frontalface_alt.xml";//人脸检测分类器位置
string listpath = "train_list.csv";//csv文件位置（图片路径和标签组成的文本）  //train_list


//调用py库生成 csv文件
void runPy_getcsv()
{
	Py_Initialize();
	//直接运行python代码
	PyRun_SimpleString("import get_csv");
	//引入模块（get_csv.py）
	PyRun_SimpleString("get_csv.get_csv()");
	Py_Finalize(); //结束python解释器，释放资源
}

/*
	人脸检测，保存样本。
	输入参数：样本数量
*/
int save_FaceSamples(int NUMS)
{
	string face_id;
	char s[50];//字符数组，用于存放字符串的每一个字符
	cout << "Please input a name" << endl;
	
	cin.get(s,50);           //终端输入样本文件夹
	face_id = s;//人的名字
	cout << face_id << endl;
	printf ("\n 看着摄像头，并等待 ...");

	VideoCapture capture(0);//打开摄像头

	//Size S = Size((int)capture.get(CAP_PROP_FRAME_WIDTH), (int)capture.get(CAP_PROP_FRAME_HEIGHT));
	//int fps = capture.get(CAP_PROP_FPS);

	//加载人脸检测分类器
	CascadeClassifier faceDetector;
	faceDetector.load(haar_face_datapath);


	Mat frame;
	vector<Rect>faces;
	int count = 0;
	int	num = 0;
	 
	//检测人脸并将人脸作为样本存入
	while (1)
	{
		 capture.read(frame);
		 faceDetector.detectMultiScale(frame, faces,1.2,2, 0 | CV_HAAR_SCALE_IMAGE, cv::Size(80, 80));         //经测试，最佳参数
		 for (int i = 0; i < faces.size(); i++) 
		 {	
			 if (count % 10 == 0)
			 {
				 num++;
				 Mat dst;
				 resize(frame(faces[i]), dst, Size(100, 100));
				 cvtColor(dst, dst, COLOR_BGR2GRAY);
				 string path = "../face/" + face_id + "/";	//新文件夹路径
				 mkdir(path.c_str(),S_IRWXU);//创建人名为文件名的新文件夹
				 imwrite( path + face_id +"_"+ to_string(num) + ".jpg",dst);	//在对应文件夹中写入对应人的图片（如：名为‘小明’的文件夹中存入小明的图片）
			 }
			 rectangle(frame, faces[i], Scalar(0, 0, 255), 2, 8, 0);//框出人脸
			 count++;
		 }
		flip(frame, frame, 1);//镜像翻转
		imshow("window", frame);//显示的窗口
		char c = waitKey(1);
		if (c == 27)//Esc键退出
		{
			break;
		}
		if (num >= NUMS )
		{
			break;
		}
	}
	return 0;
}



//dirent.h
void get_csvfile()
{
	//ofstream outFile;
	//outFile.open(listpath, ios::out); // 打开模式可省略

 	DIR * dir; 
	struct dirent * ptr; 
	char file_list[100][40]; 
	int i=0; 
	char srcFile1[1][100]; 
	string rootdirPath = "../face/"; 
	string x,dirPath; 
	dir = opendir((char *)rootdirPath.c_str()); //打开一个目录 
	char **dir_name;
	while((ptr = readdir(dir)) != NULL) //循环读取目录数据 
	{ 
		printf("d_name : %s\n", ptr->d_name); //输出文件名 
		x=ptr->d_name; 
		dirPath = rootdirPath + x; 
		printf("d_name : %s\n", dirPath.c_str()); //输出文件绝对路径 //        
		x = dirPath.c_str(); 
		strcpy(srcFile1[i],dirPath.c_str()); //存储到数组 
		if ( ++i>=100 ) 
		break;
	}
	//outFile.close();
}

/*
// io.h 不能用
void getFiles(string path, vector<string>& files)
{
    //文件句柄  
    long long hFile = 0;//这个地方需要特别注意，win10用户必须用long long 类型，win7可以用long类型
    //文件信息  
    struct _finddata_t fileinfo;
    string p;
    if ((hFile = _findfirst(p.assign(path).append("\\*").c_str(), &fileinfo)) != -1)
    {
        do
        {
            //如果是目录,迭代之  
            //如果不是,加入列表  
            if ((fileinfo.attrib &  _A_SUBDIR))
            {
                if (strcmp(fileinfo.name, ".") != 0 && strcmp(fileinfo.name, "..") != 0)
                    getFiles(p.assign(path).append("\\").append(fileinfo.name), files);
            }
            else
            {
                files.push_back(p.assign(path).append("\\").append(fileinfo.name));
            }
        } while (_findnext(hFile, &fileinfo) == 0);
        _findclose(hFile);
    }
}
*/



/*
	返回 0 ，不训练，直接读取成功；
	返回 1 ，进行训练，再预测。
	进行训练之前需要先删除已存在的 xml 文件，或者改名。
*/
bool start_train()
{
	fstream xmlfile; 
	xmlfile.open(filepath, ios::in);                 //根据自己需要进行适当的选取 ios::in|ios::out|ios::binary
	if (xmlfile)                  //存在训练好的xml
	{
		std::cout <<"xml is existed" <<std::endl;
		xmlfile.close();
		return 0;
	}
	
	ifstream file(listpath.c_str(), ifstream::in);
	if (!file) 
	{ 
		printf("could not load file correctly...\n"); 
		return -1; 
	}

	string line, path, classlabel;
	vector<Mat>images;
	vector<int>labels;
	char separator = ' ';
	cv::Mat image_one;
	while (!file.eof())
	{
		getline(file, line);
		//cout << line << endl;
		stringstream lines(line);
		getline(lines, path, separator);//获取样本图片路径
		getline(lines, classlabel);//获取标签
		//printf("%s---\n", classlabel.c_str());
	
		if (!path.empty() && !classlabel.empty())
		{
			//printf("ok:::path:%s\n", path.c_str());
			image_one = imread(path, 0);
			if(!image_one.data){
				cout << "err1"<<endl;
				break;
			}
			images.push_back(image_one);//样本图片放入容器
			labels.push_back(atoi(classlabel.c_str()));//标签放入容器
		}
	}

	if (images.size() < 1 || labels.size() < 1) 
	{
		printf("invalid image path...\n"); 
		return -1; 
	}

	//训练模型
	Ptr<FaceRecognizer> model = createEigenFaceRecognizer();
	model->train(images, labels);
	model->save(filepath);
	
	xmlfile.close();
	return 1;
}
/*
	人脸识别预测函数
*/
int start_predict()
{
	bool flag_train = 0;
	flag_train = start_train();
	//识别分类器
	Ptr<FaceRecognizer> model = createEigenFaceRecognizer();
	model->load(filepath);

	//加载检测分类器
	CascadeClassifier faceDetector;
	faceDetector.load(haar_face_datapath);

	VideoCapture capture(0);//打开摄像头
	if (!capture.isOpened())
	{
		printf("could not open camera...\n");
		return -1;
	}
	Mat frame;
	vector<Rect>faces;
	namedWindow("face-recognition", WINDOW_AUTOSIZE);//图片显示的窗口
	while (1)
	{
		capture.read(frame);//摄像头获取图片

		flip(frame, frame, 1);//镜像翻转
		faceDetector.detectMultiScale(frame, faces, 1.08, 3, 0, Size(50, 60), Size(380, 400));
		for (int i = 0; i < faces.size(); i++)
		{
			Mat dst;
			resize(frame(faces[i]), dst, Size(100, 100));//规范尺寸用于后续人脸识别
			cvtColor(dst, dst, COLOR_BGR2GRAY);//灰度化
			rectangle(frame, faces[i], Scalar(0, 255, 0), 2, 8, 0);//在窗口中框出人脸
			int predictedLabel = -1;
			double confidence = 0.0;
		    	model->predict(dst, predictedLabel, confidence);//对窗口中人脸进行识别，给出预测标签并赋于predictedLabel
			string result_message = format("Predicted number = %d / confidence = %2f.", predictedLabel, confidence);//查看标签和置信度
			cout << result_message << endl;
		
			//不同人对应的不同标签
		if(confidence > 3100){
			predictedLabel = 100;
		}
		
	     	switch (predictedLabel)
			{
				case 0:
					putText(frame, "linxi", faces[i].tl(), FONT_HERSHEY_PLAIN, 1.0, Scalar(0, 255, 0), 1, 8);//在人脸旁显示人名
					break;
				case 1:
					putText(frame, "youjiang", faces[i].tl(), FONT_HERSHEY_PLAIN, 1.0, Scalar(0, 255, 0), 1, 8);
					break;
				default:
					putText(frame, "unknown", faces[i].tl(), FONT_HERSHEY_PLAIN, 1.0, Scalar(0, 255, 0), 1, 8);
					break;
					
			}
			
		}
		imshow("face-recognition", frame);
		char c = waitKey(1);
		if (c == 27)
		{
			break;
		}
	}
	return 0;
}

int main(int argc, char**argv)
{
	string cmd1 = "save";
	string cmd2 = "predict";
	if (argv[1] == cmd1){
		cout << "start save samples" <<endl;
		save_FaceSamples(10);
		runPy_getcsv();
	}
	else if(argv[1] == cmd2){
		cout << "start predict" <<endl;
		start_predict();
	}
	return 0;
}

