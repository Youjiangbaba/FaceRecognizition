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
string haar_face_datapath = "haarcascade_frontalface_alt.xml";//������������λ��
string listpath = "train_list.csv";//csv�ļ�λ�ã�ͼƬ·���ͱ�ǩ��ɵ��ı���  //train_list


//����py������ csv�ļ�
void runPy_getcsv()
{
	Py_Initialize();
	//ֱ������python����
	PyRun_SimpleString("import get_csv");
	//����ģ�飨get_csv.py��
	PyRun_SimpleString("get_csv.get_csv()");
	Py_Finalize(); //����python���������ͷ���Դ
}

/*
	������⣬����������
	�����������������
*/
int save_FaceSamples(int NUMS)
{
	string face_id;
	char s[50];//�ַ����飬���ڴ���ַ�����ÿһ���ַ�
	cout << "Please input a name" << endl;
	
	cin.get(s,50);           //�ն����������ļ���
	face_id = s;//�˵�����
	cout << face_id << endl;
	printf ("\n ��������ͷ�����ȴ� ...");

	VideoCapture capture(0);//������ͷ

	//Size S = Size((int)capture.get(CAP_PROP_FRAME_WIDTH), (int)capture.get(CAP_PROP_FRAME_HEIGHT));
	//int fps = capture.get(CAP_PROP_FPS);

	//����������������
	CascadeClassifier faceDetector;
	faceDetector.load(haar_face_datapath);


	Mat frame;
	vector<Rect>faces;
	int count = 0;
	int	num = 0;
	 
	//�����������������Ϊ��������
	while (1)
	{
		 capture.read(frame);
		 faceDetector.detectMultiScale(frame, faces,1.2,2, 0 | CV_HAAR_SCALE_IMAGE, cv::Size(80, 80));         //�����ԣ���Ѳ���
		 for (int i = 0; i < faces.size(); i++) 
		 {	
			 if (count % 10 == 0)
			 {
				 num++;
				 Mat dst;
				 resize(frame(faces[i]), dst, Size(100, 100));
				 cvtColor(dst, dst, COLOR_BGR2GRAY);
				 string path = "../face/" + face_id + "/";	//���ļ���·��
				 mkdir(path.c_str(),S_IRWXU);//��������Ϊ�ļ��������ļ���
				 imwrite( path + face_id +"_"+ to_string(num) + ".jpg",dst);	//�ڶ�Ӧ�ļ�����д���Ӧ�˵�ͼƬ���磺��Ϊ��С�������ļ����д���С����ͼƬ��
			 }
			 rectangle(frame, faces[i], Scalar(0, 0, 255), 2, 8, 0);//�������
			 count++;
		 }
		flip(frame, frame, 1);//����ת
		imshow("window", frame);//��ʾ�Ĵ���
		char c = waitKey(1);
		if (c == 27)//Esc���˳�
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
	//outFile.open(listpath, ios::out); // ��ģʽ��ʡ��

 	DIR * dir; 
	struct dirent * ptr; 
	char file_list[100][40]; 
	int i=0; 
	char srcFile1[1][100]; 
	string rootdirPath = "../face/"; 
	string x,dirPath; 
	dir = opendir((char *)rootdirPath.c_str()); //��һ��Ŀ¼ 
	char **dir_name;
	while((ptr = readdir(dir)) != NULL) //ѭ����ȡĿ¼���� 
	{ 
		printf("d_name : %s\n", ptr->d_name); //����ļ��� 
		x=ptr->d_name; 
		dirPath = rootdirPath + x; 
		printf("d_name : %s\n", dirPath.c_str()); //����ļ�����·�� //        
		x = dirPath.c_str(); 
		strcpy(srcFile1[i],dirPath.c_str()); //�洢������ 
		if ( ++i>=100 ) 
		break;
	}
	//outFile.close();
}

/*
// io.h ������
void getFiles(string path, vector<string>& files)
{
    //�ļ����  
    long long hFile = 0;//����ط���Ҫ�ر�ע�⣬win10�û�������long long ���ͣ�win7������long����
    //�ļ���Ϣ  
    struct _finddata_t fileinfo;
    string p;
    if ((hFile = _findfirst(p.assign(path).append("\\*").c_str(), &fileinfo)) != -1)
    {
        do
        {
            //�����Ŀ¼,����֮  
            //�������,�����б�  
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
	���� 0 ����ѵ����ֱ�Ӷ�ȡ�ɹ���
	���� 1 ������ѵ������Ԥ�⡣
	����ѵ��֮ǰ��Ҫ��ɾ���Ѵ��ڵ� xml �ļ������߸�����
*/
bool start_train()
{
	fstream xmlfile; 
	xmlfile.open(filepath, ios::in);                 //�����Լ���Ҫ�����ʵ���ѡȡ ios::in|ios::out|ios::binary
	if (xmlfile)                  //����ѵ���õ�xml
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
		getline(lines, path, separator);//��ȡ����ͼƬ·��
		getline(lines, classlabel);//��ȡ��ǩ
		//printf("%s---\n", classlabel.c_str());
	
		if (!path.empty() && !classlabel.empty())
		{
			//printf("ok:::path:%s\n", path.c_str());
			image_one = imread(path, 0);
			if(!image_one.data){
				cout << "err1"<<endl;
				break;
			}
			images.push_back(image_one);//����ͼƬ��������
			labels.push_back(atoi(classlabel.c_str()));//��ǩ��������
		}
	}

	if (images.size() < 1 || labels.size() < 1) 
	{
		printf("invalid image path...\n"); 
		return -1; 
	}

	//ѵ��ģ��
	Ptr<FaceRecognizer> model = createEigenFaceRecognizer();
	model->train(images, labels);
	model->save(filepath);
	
	xmlfile.close();
	return 1;
}
/*
	����ʶ��Ԥ�⺯��
*/
int start_predict()
{
	bool flag_train = 0;
	flag_train = start_train();
	//ʶ�������
	Ptr<FaceRecognizer> model = createEigenFaceRecognizer();
	model->load(filepath);

	//���ؼ�������
	CascadeClassifier faceDetector;
	faceDetector.load(haar_face_datapath);

	VideoCapture capture(0);//������ͷ
	if (!capture.isOpened())
	{
		printf("could not open camera...\n");
		return -1;
	}
	Mat frame;
	vector<Rect>faces;
	namedWindow("face-recognition", WINDOW_AUTOSIZE);//ͼƬ��ʾ�Ĵ���
	while (1)
	{
		capture.read(frame);//����ͷ��ȡͼƬ

		flip(frame, frame, 1);//����ת
		faceDetector.detectMultiScale(frame, faces, 1.08, 3, 0, Size(50, 60), Size(380, 400));
		for (int i = 0; i < faces.size(); i++)
		{
			Mat dst;
			resize(frame(faces[i]), dst, Size(100, 100));//�淶�ߴ����ں�������ʶ��
			cvtColor(dst, dst, COLOR_BGR2GRAY);//�ҶȻ�
			rectangle(frame, faces[i], Scalar(0, 255, 0), 2, 8, 0);//�ڴ����п������
			int predictedLabel = -1;
			double confidence = 0.0;
		    	model->predict(dst, predictedLabel, confidence);//�Դ�������������ʶ�𣬸���Ԥ���ǩ������predictedLabel
			string result_message = format("Predicted number = %d / confidence = %2f.", predictedLabel, confidence);//�鿴��ǩ�����Ŷ�
			cout << result_message << endl;
		
			//��ͬ�˶�Ӧ�Ĳ�ͬ��ǩ
		if(confidence > 3100){
			predictedLabel = 100;
		}
		
	     	switch (predictedLabel)
			{
				case 0:
					putText(frame, "linxi", faces[i].tl(), FONT_HERSHEY_PLAIN, 1.0, Scalar(0, 255, 0), 1, 8);//����������ʾ����
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

