"""Add station module"""
import os
import sys
import shutil
import re
from PyQt5.QtWidgets import (QDialog, QWidget, QVBoxLayout, QHBoxLayout, QFileDialog,
							 QLabel, QPushButton, QComboBox, QLineEdit, QFormLayout)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize, QDir
from . import paths, styles


class Add_Station(QDialog):
	"""Add station class"""
	def __init__(self):
		super().__init__()
		self.create_add_window()

	def create_add_window(self):
		"""Create window"""
		self.FILE_ICON = ''
		#vbox_main
		self.vbox_main = QVBoxLayout()
		self.setLayout(self.vbox_main)
		
		#form_layout
		self.form_layout = QFormLayout()
		self.vbox_main.addLayout(self.form_layout)
		
		#Widgets
		self.entry_name = QLineEdit()
		self.entry_stream = QLineEdit()
		self.combo_country = QComboBox()
		self.combo_genres = QComboBox()
		self.button_icon = QPushButton()
		
		#add rows
		self.form_layout.addRow(self.tr("NAME:"), self.entry_name)
		self.form_layout.addRow(self.tr("URL:"), self.entry_stream)
		self.form_layout.addRow(self.tr("COUNTRY:"), self.combo_country)
		self.form_layout.addRow(self.tr("GENRE:"), self.combo_genres)
		self.form_layout.addRow(self.tr("ICON:"), self.button_icon)

		#ADD COUNTRIES
		paths.BASE_CURSOR.execute("SELECT * FROM Lands")
		list_countries = paths.BASE_CURSOR.fetchall()
		list_countries.sort()
		self.combo_country.addItem(self.tr("Choose: "))
		for item in list_countries:
			self.combo_country.addItem(item[0])
		
		#ADD GENRES
		self.combo_genres.addItem(self.tr('Choose:'))
		list_genres = ['Pop','Relax','Retro','Child','Shanson',
						'Love', 'Rock', 'Humor', 'Classic', 'Rap', 'Jazz', 'Metal','Films',
						'Club','Ballads','Blues','Groove','Grunge','Hip-Hop',
						'Pank','Reggae','Dj','News','Religion','Sport',
						'Other',]
		list_genres.sort()
		for item in list_genres:
			self.combo_genres.addItem(item)
		
		#button_icon
		self.button_icon.setCursor(Qt.PointingHandCursor)
		self.button_icon.setFixedSize(32, 32)
		self.button_icon.setIconSize(QSize(30, 30))
		self.button_icon.setFocusPolicy(Qt.NoFocus)
		self.button_icon.clicked.connect(self.press_button_add_icon)
			

	#add label added
		self.label_added_station = QLabel()
		self.label_added_station.setAlignment(Qt.AlignCenter)
		self.label_added_station.setStyleSheet("color:blue")
		self.vbox_main.addWidget(self.label_added_station)

	#add stretch
		self.vbox_main.addStretch()

	#add hbox for buttons OK
		self.hbox_ok_cancel = QHBoxLayout()
		self.vbox_main.addLayout(self.hbox_ok_cancel)
		#add stretch
		self.hbox_ok_cancel.addStretch()
		#add button OK
		self.button_ok = QPushButton(self.tr("Save"))
		self.button_ok.setCursor(Qt.PointingHandCursor)
		self.button_ok.setMinimumHeight(35)
		self.button_ok.setMinimumWidth(80)
		self.button_ok.setStyleSheet(styles.get_button_style())
		self.button_ok.clicked.connect(self.press_save)
		self.hbox_ok_cancel.addWidget(self.button_ok)
		
		###
		self.setAttribute(Qt.WA_DeleteOnClose, True)
		self.setFixedSize(500, 250)
		self.setModal(True)
		self.setWindowTitle(self.tr("Add station to Base"))

#######################################################################

	def press_save(self):
		"""Press save"""
		name_station = self.entry_name.text().strip()
		stream = self.entry_stream.text().strip()
		if (name_station and stream and self.combo_country.currentIndex() > 0 
			and self.combo_genres.currentIndex() > 0):
			name_countries = self.combo_country.currentText()
			name_genre = self.combo_genres.currentText()
			if self.FILE_ICON:
				with open(self.FILE_ICON, "rb") as get_image:
					f = get_image.read()
					icon = bytearray(f)
			else:
				icon = ''
			add_params = [name_station, stream, icon, name_genre, name_countries]
			paths.BASE_CURSOR.execute("INSERT INTO AllBase(name, url, image, genre, land) VALUES(?,?,?,?,?)", add_params)
			paths.BASE_CONNECTION.commit()
			self.label_added_station.setText(self.tr("The station ") + name_station + self.tr(" was added."))
			self.clear_info()
			
	def clear_info(self):
		"""Clear"""
		self.entry_name.clear()
		self.entry_stream.clear()
		self.combo_country.setCurrentIndex(0)
		self.combo_genres.setCurrentIndex(0)
		self.button_icon.setIcon(QIcon(''))
			
	def set_info(self, name, stream):
		"""Set name and stream"""
		self.entry_name.setText(name.strip())
		self.entry_stream.setText(stream.strip())

	def press_button_add_icon(self):
		"""Press add icon"""
		fileName = QFileDialog.getOpenFileName(self, self.tr('Choose icon'), QDir.homePath(), ("Image Files (*.png *.jpg *.bmp)"))
		if fileName[0]:
			self.FILE_ICON = fileName[0]
			if os.path.exists(self.FILE_ICON):
				self.button_icon.setIcon(QIcon(self.FILE_ICON))
