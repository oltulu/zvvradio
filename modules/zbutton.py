"""ZButton module"""
import os
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
from . import styles, paths


class MyButton(QPushButton):
	"""My ListWidgetItem class"""
	def __init__(self):
		super().__init__()
		self.RADIO_ID = None
		self.TITLE = None
		self.URL = None
		self.setFixedSize(64, 64)
		self.setIconSize(QSize(60, 60))
		self.setCursor(Qt.PointingHandCursor)
		self.setStyleSheet(self.get_style())
		self.setContextMenuPolicy(Qt.CustomContextMenu)

	def set_info(self, radio_id, text, url, icon):
		"""Set info"""
		self.RADIO_ID = radio_id
		if icon:
			pixmap = QPixmap()
			pixmap.loadFromData(bytearray(icon))
			self.setIcon(QIcon(pixmap))
		else:
			title = self.get_first_letters(text)
			self.setText(title)
		self.setStatusTip(text)
		self.TITLE = text
		self.URL = url
		
	def set_icon(self, icon):
		"""Set icon"""
		pixmap = QPixmap()
		pixmap.loadFromData(bytearray(icon))
		self.setIcon(QIcon(pixmap))
		self.setText('')
		
	def get_first_letters(self, text):
		"""Get first letter"""
		if len(text) > 5:
			name = ''
			split_text = text.split(' ')
			for word in split_text:
				if word[0]:
					name += word[0]
			if len(name) < 4:
				name = text[:4]
			return name
		else:
			return text
		
	def get_style(self):
		"""Get style"""
		BUTTON_STYLE = ("""
					QPushButton{
						border:1px solid silver;
						font-size:12px;
						font-weight:bold;
					} 
					QPushButton::hover{
						border:1px solid orange; 
						background-color:#fffae0;
					} 
					QPushButton::checked{
						border: 1px solid red; 
						background-color:#ffc6c6;

					}""")
		return BUTTON_STYLE
