"""About module"""
import os
from PyQt5.QtWidgets import QDialog, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QUrl


class About(QDialog):
	"""About window class"""
	def __init__(self):
		super().__init__()
		self.create_about_window()

	def create_about_window(self):
		"""Create widgets"""
		self.vbox_main = QVBoxLayout()
		self.setLayout(self.vbox_main)

		#add image
		self.label_image = QLabel()
		self.label_image.setAlignment(Qt.AlignCenter)
		self.label_image.setFixedSize(100, 100)
		self.label_image.setScaledContents(True)
		self.pixmap = QPixmap(":/app_icon.ico")
		#self.pixmap = self.pixmap.scaled(100,100)
		self.label_image.setPixmap(self.pixmap)
		self.vbox_main.addWidget(self.label_image)
		self.vbox_main.setAlignment(self.label_image, Qt.AlignCenter)

		#add label name_program
		self.label_program = QLabel("ZVVRadio v.3.1 (21.04.2019)")
		self.label_program.setStyleSheet('QLabel{font-weight:bold; color:brown;}')
		self.label_program.setAlignment(Qt.AlignCenter)
		self.vbox_main.addWidget(self.label_program)
		#add label author
		self.label_author = QLabel(self.tr("Author: <b>Vyacheslav Zubik</b>. Ukraine, Kherson"))
		self.label_author.setAlignment(Qt.AlignCenter)
		self.vbox_main.addWidget(self.label_author)
		#add blog
		self.label_blog = QLabel(self.tr("Follow to my blog:<a href = 'http://zvvubuntu.blogspot.com'>ZVVUbuntu`s Blog</a>"))
		self.label_blog.setAlignment(Qt.AlignCenter)
		self.label_blog.setOpenExternalLinks(True)
		self.vbox_main.addWidget(self.label_blog)
		#add label email
		self.label_email = QLabel("Email:  ZVVUbuntu@gmail.com")
		self.label_email.setAlignment(Qt.AlignCenter)
		self.label_email.setTextInteractionFlags(Qt.TextSelectableByMouse)
		self.vbox_main.addWidget(self.label_email)
		#add donate label
		self.label_donate = QLabel("Попробуйте мою игру <a href = 'https://play.google.com/store/apps/details?id=com.ZVV.ZVVMinis'><b>ZVVMinis</b></a> - сборник мини игр.")
		self.label_donate.setOpenExternalLinks(True)
		self.label_donate.setWordWrap(True)
		self.label_donate.setAlignment(Qt.AlignCenter)
		self.vbox_main.addWidget(self.label_donate)
		#label_goodness
		self.label_goodness = QLabel()
		self.label_goodness.setText(self.tr('Have a nice day!'))
		self.label_goodness.setAlignment(Qt.AlignCenter)
		self.label_goodness.setStyleSheet('QLabel{font-weight:bold; color:brown; font-size:14px;}')
		self.vbox_main.addWidget(self.label_goodness)

		###
		self.setAttribute(Qt.WA_DeleteOnClose, True)
		self.setWindowTitle(self.tr("About"))
		self.setWindowIcon(QIcon(':/about_icon.png'))
		self.setModal(True)
		self.setFixedSize(450, 350)
