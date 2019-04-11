/*************************************************************************
    > File Name: c_plus_dirsfiles.h
    > Author: jiang
    > Mail: 760021776@qq.com 
    > Created Time: 2019年04月11日 星期四 16时13分48秒
 ************************************************************************/

#include<iostream>
#include <string>
#include <vector>

using namespace std;
extern string listpath;
extern bool save_samplename(char *name);
extern void read_names(vector<string> &name,vector<int> &label);
extern void get_namescsv();

