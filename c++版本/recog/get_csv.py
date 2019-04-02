#! /usr/bin/env python
#coding=utf-8
import os

def get_csv():
	path = "../face"
	dirnames = os.listdir(path)
	strText = ""
	i = 0
	with open("train_list.csv", "w") as fid:
	    for a in dirnames:
		filenames = os.listdir(path + os.sep + a)
		for b in range(len(filenames)):
		    strText = path + os.sep + a + os.sep + filenames[b] + " " + str(i) + "\n"
		    fid.write(strText)
		i += 1
	print ("csv update!")
	fid.close()
