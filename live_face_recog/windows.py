# -*- coding: utf-8 -*-
import time
import golbal_define as gd


from PyQt5 import QtCore, QtGui, QtWidgets,Qt
from PyQt5.QtWidgets import QApplication, QLineEdit, QWidget, QFormLayout, QPushButton, QTableWidget,QTableWidgetItem,QAbstractItemView

class Ui_TabWidget(object):

    def setupUi(self, TabWidget):

        #主窗口设置
        TabWidget.setObjectName("打卡记录测试demo")       
        TabWidget.setGeometry(gd.big_x,gd.big_y,gd.big_w, gd.big_h)
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(5, 30, 90, 46))
        self.pushButton.setObjectName("pushButton")

        self.pushButton1 = QtWidgets.QPushButton(self)
        self.pushButton1.setGeometry(QtCore.QRect(5, 200, 90, 46))
        self.pushButton1.setObjectName("pushButton")

        self.pushButton3 = QtWidgets.QPushButton(self)
        self.pushButton3.setGeometry(QtCore.QRect(5, 80, 90, 46))
        self.pushButton3.setObjectName("按A打卡")

        self.pushButton2 = QtWidgets.QPushButton(self)
        self.pushButton2.setGeometry(QtCore.QRect(5, 300, 90, 46))
        self.pushButton2.setObjectName("pushButton")


        self.labeldate = QtWidgets.QLabel(self)
        self.labeldate.setGeometry(QtCore.QRect(400, gd.show_y-30, gd.show_w, 30))
    

        self.item = QtWidgets.QTableWidget(100,4,self)
        self.item.setGeometry(QtCore.QRect(gd.show_x + gd.show_w+10, gd.show_y, 500, gd.show_h))
        #self.item.setColumnWidth(0,30)
        #self.item.setRowHeight(0,30)
        self.item.setHorizontalHeaderLabels([' 工号','姓名','打卡时间','打卡备注'])
        self.item.setVerticalHeaderLabels(['1','2','3','4','5','6','7','8','9','10'])
        #self.item.setItem(0,1,QTableWidgetItem('test'))
        self.item.setEditTriggers(QAbstractItemView.NoEditTriggers) 
        self.item.setSelectionBehavior(2)
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(gd.show_x, gd.show_y, gd.show_w, gd.show_h))
        self.label.setText("")
        self.label.setObjectName("label")

        self.retranslateUi(TabWidget)
        TabWidget.setCurrentIndex(0)
        self.pushButton.clicked.connect(TabWidget.videoprocessing) 

        self.pushButton2.clicked.connect(TabWidget.quit_system) 

        self.pushButton3.clicked.connect(TabWidget.pushButtonA) 

        QtCore.QMetaObject.connectSlotsByName(TabWidget)



    def retranslateUi(self, TabWidget):
        _translate = QtCore.QCoreApplication.translate
        TabWidget.setWindowTitle(_translate("TabWidget", "打卡记录测试Demo"))
        self.pushButton.setText(_translate("TabWidget", "开始考勤"))

        self.pushButton1.setText(_translate("TabWidget", "用户登录"))

        self.pushButton2.setText(_translate("TabWidget", "退出系统"))

        self.pushButton3.setText(_translate("TabWidget", "按A打卡"))

        TabWidget.setTabText(TabWidget.indexOf(self), _translate("TabWidget", " "))
        self.pushButton3.setEnabled(False)





