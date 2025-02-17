#!/usr/bin/python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys
import sip
import argparse
import configparser
from util import *
from pyqt_proxy import proxy
from MainWindow import MainWindow

class LoginWindow(QMainWindow):
	def __init__(self):
		super(LoginWindow, self).__init__(None)
		self.init_args();
		self.setup_ui()
		self.init_ui()
		set_win_center(self)
		if self.silent == True:
			self.on_connect()

	def init_args(self):
		# parser = argparse.ArgumentParser(description='hprd')
		parser = argparse.ArgumentParser()
		parser.add_argument('-a', '--ip', dest='ip', type=str, metavar='', required=False, help='Remote server ip addr')
		parser.add_argument('-s', '--silent', dest='silent', action='store_true', required=False, help='Silent mode, Direct connect')

		args = parser.parse_args()
		self.ip = args.ip
		self.silent = args.silent


	def setup_ui(self):
		self.resize(720, 400)
		self.setAnimated(True)
		self.centralwidget = QWidget(self)
		self.centralwidget.setObjectName("centralwidget")
		self.layout = QGridLayout()
		self.centralwidget.setLayout(self.layout)
		self.setCentralWidget(self.centralwidget)
		
		self.ip_lable = QLabel()
		self.ip_lable.setText("IP:")
		self.layout.addWidget(self.ip_lable,0,0,1,1, Qt.AlignRight)
		self.ip_edit = QLineEdit()
		self.ip_edit.setText(self.ip or "127.0.0.1:9999")
		self.layout.addWidget(self.ip_edit,0,1,1,3)

		self.user_lable = QLabel()
		self.user_lable.setText("Name:")
		self.layout.addWidget(self.user_lable,1,0,1,1, Qt.AlignRight)
		self.user_edit = QLineEdit()
		self.user_edit.setText("")
		self.layout.addWidget(self.user_edit,1,1,1,3)

		self.passwd_lable = QLabel()
		self.passwd_lable.setText("Password:")
		self.layout.addWidget(self.passwd_lable,2,0,1,1, Qt.AlignRight)
		self.passwd_edit = QLineEdit()
		self.passwd_edit.setText("")
		self.passwd_edit.setEchoMode(QLineEdit.Password)
		self.layout.addWidget(self.passwd_edit,2,1,1,3)

		self.conn_button = QPushButton()
		self.conn_button.setText("连接")
		self.layout.addWidget(self.conn_button,3,1,1,2)
 
	def init_ui(self):
		self.ip_edit.setFocus()
		self.ip_edit.setPlaceholderText("请输入ip地址")
		self.user_edit.setPlaceholderText("请输入用户名")
		self.passwd_edit.setPlaceholderText("请输入密码")

		self.conn_button.clicked.connect(self.on_connect)  # 登录

	def main_win_show(self, task):
		self.main_win = MainWindow()
		self.main_win.show()
		self.close()

	def on_connect(self):
		port = 0
		ip_port = self.ip_edit.text().split(":")

		if len(ip_port) == 2:
			port = int(ip_port[1])
		else:
			port = 9999

		ret = proxy().py_client_connect(ip_port[0].encode('utf-8'), port)
		if ret == 0:
			add_task(1, False, self.main_win_show)

if __name__=="__main__":
	app = QApplication(sys.argv)
	w = LoginWindow()
	w.show()

	timer = QTimer(app)
	timer.timeout.connect(on_timer)
	timer.start(int(1000 / 60))

	sys.exit(app.exec())