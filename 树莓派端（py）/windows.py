# -*- coding: utf-8 -*-
import time
import golbal_define as gd
from HARDWARE import HardWare 

from PyQt5 import QtCore, QtGui, QtWidgets,Qt
from PyQt5.QtWidgets import QApplication, QLineEdit, QWidget, QFormLayout, QPushButton

class Ui_TabWidget(object):

    def setupUi(self, TabWidget):

        TabWidget.setObjectName("人脸识别Demo")          #创建的是"TabWidget"
        TabWidget.setGeometry(gd.big_x,gd.big_y,gd.big_w, gd.big_h)
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("camera")                    #"第一个子窗口"
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(5, 30, 90, 23))
        self.pushButton.setObjectName("pushButton")

        self.pushButton1 = QtWidgets.QPushButton(self.tab)
        self.pushButton1.setGeometry(QtCore.QRect(5, 100, 90, 46))
        self.pushButton1.setObjectName("pushButton")

        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(gd.show_x, gd.show_y, gd.show_w, gd.show_h))
        self.label.setText("")
        self.label.setObjectName("label")

        TabWidget.addTab(self.tab, "")                      #显示tab

        self.retranslateUi(TabWidget)
        TabWidget.setCurrentIndex(0)
        self.pushButton.clicked.connect(TabWidget.videoprocessing) #将按键与事件相连

        self.pushButton1.clicked.connect(TabWidget.showdialog) #将按键与事件相连

        QtCore.QMetaObject.connectSlotsByName(TabWidget)



    def retranslateUi(self, TabWidget):
        _translate = QtCore.QCoreApplication.translate
        TabWidget.setWindowTitle(_translate("TabWidget", "人脸识别Demo"))
        self.pushButton.setText(_translate("TabWidget", "打开摄像头"))

        self.pushButton1.setText(_translate("TabWidget", "输入密码"))

        TabWidget.setTabText(TabWidget.indexOf(self.tab), _translate("TabWidget", "Tab 1"))


    def showdialog(self):
        global dialog
        global pNormalLineEdit
        global pPasswordLineEdit
        dialog = QtWidgets.QDialog()
        dialog.setGeometry(QtCore.QRect(300, 300, 260, 160))
        btn1 = QPushButton("确定", dialog)
        btn1.move(20, 100)
        btn2 = QPushButton("退出", dialog)
        btn2.move(140, 100)

        flo = QFormLayout()

        pNormalLineEdit = QLineEdit()
        pPasswordLineEdit = QLineEdit()

        flo.addRow("Username", pNormalLineEdit)
        flo.addRow("Password", pPasswordLineEdit)

        pNormalLineEdit.setPlaceholderText("Normal")
        pPasswordLineEdit.setPlaceholderText("Password")
        pNormalLineEdit.setMaxLength(4)
        pPasswordLineEdit.setMaxLength(4)                      #密码为四位

        # 设置显示效果
        pNormalLineEdit.setEchoMode(QLineEdit.Normal)
        pPasswordLineEdit.setEchoMode(QLineEdit.Password)                      #密码隐藏

        dialog.setLayout(flo)


        btn1.clicked.connect(self.input_detect)
        btn2.clicked.connect(dialog.close)
        dialog.exec_()

#用户在该函数下改密码和名字,相关定义见 global_define.py中  修改名字和密码
    def input_detect(self):

        name = pNormalLineEdit.text()
        pwd = pPasswordLineEdit.text()
        if name == gd.usr1:
            if pwd == gd.pwd1:
                self.text_ok()
            else:
                self.text_err()
        elif name == gd.usr2:
            if pwd == gd.pwd2:
                self.text_ok()
            else:
                self.text_err()
        elif name == gd.usr3:
            if pwd == gd.pwd3:
                self.text_ok()
            else:
                self.text_err()
        elif name == gd.usr4:
            if pwd == gd.pwd4:
                self.text_ok()
            else:
                self.text_err()
        elif name == gd.usr5:
            if pwd == gd.pwd5:
                self.text_ok()
            else:
                self.text_err()
        elif name == gd.usr6:
            if pwd == gd.pwd6:
                self.text_ok()
            else:
                self.text_err()
        else:
            self.text_none()
        dialog.close()

    def text_ok(self):
        text = QtWidgets.QMessageBox.about(self,"说明","验证通过")
        HardWare.openDoor()
        time.sleep(5)							#设置延迟时间：验证成功后开门，之后关闭
        HardWare.closeDoor()
        print(HardWare.io_lever(21))					#门的状态，0为关，1为开
        dialog.close()

    def text_err(self):
        text = QtWidgets.QMessageBox.about(self,"说明","验证失败")
        HardWare.closeDoor()
        print(HardWare.io_lever(21))
        dialog.close()

    def text_none(self):
        text = QtWidgets.QMessageBox.about(self,"说明","没有该用户")
        HardWare.closeDoor()
        print(HardWare.io_lever(21))
        dialog.close()


