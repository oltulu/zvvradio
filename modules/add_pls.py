from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os, sys, shutil, re
from . import paths

class Add_Station(QDialog):
	def __init__(self, name, url):
		super().__init__()
		self.path_image_station = []
		self.name_pls_st = name
		self.url_pls_st = url
		self.resize(500,400)
		self.setFixedSize(500,400)
		self.setModal(True)
		self.setWindowTitle(self.tr("Add station"))
		self.create_add_window()

	def create_add_window(self):

		self.APP_FOLDER = paths.APP_FOLDER
		self.PLS_FOLDER = paths.PLS_FOLDER
		self.CONFIG_PATH = paths.CONFIG_PATH
		self.ICONS_PATH = paths.ICONS_PATH
		self.BACKUP_FOLDER = paths.BACKUP_FOLDER
		self.BASE_PATH = paths.BASE_PATH
		self.RECORD_PATH = paths.RECORD_PATH


		self.vbox_main = QVBoxLayout()
		self.setLayout(self.vbox_main)
	
		#add label
		self.label_add = QLabel()
		self.label_add.setText(self.tr("Add new station:"))
		self.label_add.setAlignment(Qt.AlignCenter)
		self.vbox_main.addWidget(self.label_add)

	#add hbox_name_station
		self.hbox_name_station = QHBoxLayout()
		self.vbox_main.addLayout(self.hbox_name_station)
		#add label
		self.label_name = QLabel(self.tr("Enter name of station -->\t"))
		self.hbox_name_station.addWidget(self.label_name)
		#add entry
		self.entry_name = QLineEdit(self)
		self.entry_name.setText(self.name_pls_st)
		self.hbox_name_station.addWidget(self.entry_name)

	#add hbox_stream_station
		self.hbox_stream_station = QHBoxLayout()
		self.vbox_main.addLayout(self.hbox_stream_station)
		#add label
		self.label_stream = QLabel(self.tr("Put your stream -->\t"))
		self.hbox_stream_station.addWidget(self.label_stream)
		#add entry
		self.entry_stream = QLineEdit()
		self.entry_stream.setText(self.url_pls_st)
		self.hbox_stream_station.addWidget(self.entry_stream)

		#add hbox filechooser
		self.hbox_filechooser = QHBoxLayout()
		self.vbox_main.addLayout(self.hbox_filechooser)
		#add label filechooser
		self.label_filechooser = QLabel(self.tr("Choose image for station --> "))
		self.hbox_filechooser.addWidget(self.label_filechooser)

		#add filechooser dialog
		self.filechooser = QPushButton()
		self.image = QIcon()
		self.filechooser.setMinimumWidth(67)
		self.filechooser.setMinimumHeight(67)
		self.filechooser.setMaximumWidth(67)
		self.filechooser.setMaximumHeight(67)
		self.filechooser.setFocusPolicy(Qt.NoFocus)
		self.filechooser.clicked.connect(self.press_filechooser)
		self.hbox_filechooser.addWidget(self.filechooser)

	#add hbox country
		self.hbox_country_choose = QHBoxLayout()
		self.vbox_main.addLayout(self.hbox_country_choose)
		#add label
		self.label_country_choose = QLabel(self.tr("Choose country of station --> "))
		self.hbox_country_choose.addWidget(self.label_country_choose)
		#add combobox
		self.combo_country = QComboBox()
		self.hbox_country_choose.addWidget(self.combo_country)
		
		paths.BASE_CURSOR.execute("SELECT * FROM Lands")
		list_countries = paths.BASE_CURSOR.fetchall()
		list_countries.sort()

		self.combo_country.addItem(self.tr("Choose: "))
		for item in list_countries:
			self.combo_country.addItem(item[0])

	#add hbox genres
		self.hbox_genres_choose = QHBoxLayout()
		self.vbox_main.addLayout(self.hbox_genres_choose)
		#add label
		self.label_genres_choose = QLabel(self.tr("Choose genre of station --> "))
		self.hbox_genres_choose.addWidget(self.label_genres_choose)
		#add combobox
		self.combo_genres = QComboBox()
		self.hbox_genres_choose.addWidget(self.combo_genres)
		list_genres = [self.tr('Choose:'), 'Pop','Relax','Retro','Child','Shanson',
						'Love', 'Rock', 'Humor', 'Classic', 'Rap', 'Jazz', 'Metal','Films',
						'Club','Ballads','Blues','Groove','Grunge','Hip-Hop',
						'Pank','Reggae','Dj','News','Religion','Sport',
						'Other',]
		for item in list_genres:
			self.combo_genres.addItem(item)

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
		self.button_ok.clicked.connect(self.press_save)
		self.hbox_ok_cancel.addWidget(self.button_ok)


		#set main window
		self.show()

	def press_save(self):
		name_station = self.entry_name.text()
		stream = self.entry_stream.text()
		if name_station != "" and stream != "" and self.combo_country.currentIndex() > 0 and self.combo_genres.currentIndex() > 0:
			
			name_countries = self.combo_country.currentText()
			name_genre = self.combo_genres.currentText()
			
			if self.path_image_station != []:
				src = self.path_image_station[0]
				src_name = os.path.split(self.path_image_station[0])[1]
				dst = self.ICONS_PATH
				dst_name_path = (dst + src_name)
				if os.path.exists(dst_name_path):
					pass
				else:
					shutil.copy(src, dst)
				icon = dst_name_path
			else:
				icon = "none"

			add_params = [name_station,stream,icon,name_genre,name_countries]
			
			paths.BASE_CURSOR.execute("INSERT INTO AllBase VALUES(?,?,?,?,?)", add_params)
			paths.BASE_CONNECTION.commit()

			self.label_added_station.clear()
			self.label_added_station.setText(self.tr("The station ") + name_station + self.tr(" was added."))
			self.entry_name.clear()
			self.entry_stream.clear()
			self.filechooser.setIcon(QIcon())
			self.combo_country.setCurrentIndex(0)
			self.combo_genres.setCurrentIndex(0)

	def press_filechooser(self):
		self.file_open = File_choose()
		self.file_open.fileSelected.connect(self.choose_image)

	def choose_image(self, image):
		self.path_image_station.clear()
		self.path_image_station.append(image)
		self.image = QIcon(str(image))
		self.filechooser.setIcon(self.image)
		self.filechooser.setIconSize(QSize(60,60))
		

class File_choose(QFileDialog):
	def __init__(self):
		super().__init__()
		self.resize(700,500)
		self.setFixedSize(700,500)
		self.setNameFilter("Images(*png *jpeg *jpg)")
		self.setModal(True)
		self.show()
