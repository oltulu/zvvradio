"""PLS TAB module"""
import os
import sys
import re
import urllib
import urllib.request
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
							 QLineEdit, QPushButton, QTableWidget, 
							 QTableWidgetItem, QComboBox, QFileDialog,
							 QAbstractItemView, QHeaderView)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QCoreApplication, QSize, QUrl, QFileInfo
from . import paths, styles

class Pls(QWidget):
	"""PLS TAB class"""
	def __init__(self):
		super().__init__()
		self.create_widgets()

	def create_widgets(self):
		"""Create widgets"""
		self.LOAD_STATE = True
		BUTTON_SIZE = 30
		playlist_font = QFont()
		playlist_font.setPointSize(11)
		
		#vbox_main
		self.vbox_main = QVBoxLayout()
		self.vbox_main.setContentsMargins(1, 1, 1, 1)
		self.vbox_main.setSpacing(1)
		self.setLayout(self.vbox_main)
		
		#add hbox open playlist
		self.hbox_open_pls = QHBoxLayout()
		self.vbox_main.addLayout(self.hbox_open_pls)
		
		#button open file
		self.button_open_file = ToolButton()
		self.button_open_file.setIcon(QIcon(":/folder_icon.png"))
		self.button_open_file.clicked.connect(self.press_open_file)
		self.hbox_open_pls.addWidget(self.button_open_file)
		
		#add combo playlists
		self.combo_playlist = QComboBox()
		self.combo_playlist.setFocusPolicy(Qt.NoFocus)
		self.combo_playlist.setFont(playlist_font)
		self.combo_playlist.setFixedHeight(BUTTON_SIZE)
		self.hbox_open_pls.addWidget(self.combo_playlist)
		list_pls = os.listdir(paths.PLS_FOLDER)
		self.combo_playlist.addItem(QIcon(':/pls_icon.png'), "Playlists:")
		for item in list_pls:
			self.combo_playlist.addItem(QIcon(':/pls_icon.png'), item)
		self.combo_playlist.activated.connect(self.choose_pls)

		#add button add station
		self.button_add_plsStation = ToolButton()
		self.button_add_plsStation.setIcon(QIcon(':/add_icon.png'))
		self.button_add_plsStation.clicked.connect(self.press_add_plsStation)
		self.hbox_open_pls.addWidget(self.button_add_plsStation)
		
		#url button
		self.button_open_url = ToolButton()
		self.button_open_url.setIcon(QIcon(":/url_icon.png"))
		self.button_open_url.clicked.connect(self.press_button_url)
		self.hbox_open_pls.addWidget(self.button_open_url)
		
		#url widget
		self.url_line_edit = QLineEdit()
		self.url_line_edit.setPlaceholderText("Put url here + press ENTER")
		self.url_line_edit.setClearButtonEnabled(True)
		self.url_line_edit.hide()
		self.url_line_edit.returnPressed.connect(self.open_url_playlist)
		self.vbox_main.addWidget(self.url_line_edit)
		
		#table_widget
		self.table_widget = MyTableWidget()
		self.table_widget.setRowCount(0)
		self.table_widget.setColumnCount(1)
		self.table_widget.setSelectionMode(QAbstractItemView.SingleSelection)
		self.table_widget.horizontalHeader().hide()
		self.table_widget.setShowGrid(True)
		self.table_widget.itemDoubleClicked.connect(self.press_pls_item)
		self.vbox_main.addWidget(self.table_widget)
		self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		
		#button_stop
		self.button_stop_load = QPushButton(self.tr("Stop load"))
		self.button_stop_load.hide()
		self.button_stop_load.clicked.connect(self.press_button_stop_load)
		self.vbox_main.addWidget(self.button_stop_load)
		
##########################################################################################

	def press_button_stop_load(self):
		"""Press stop load button"""
		self.LOAD_STATE = False

	def press_pls_item(self, tableWidgetItem):
		"""Press PLS item"""
		name = tableWidgetItem.text()
		url = tableWidgetItem.URL
		self.parent().parent().parent().player_play(name, url)

	def press_add_plsStation(self):
		from . import add_station
		selected_item = self.table_widget.currentItem()
		if selected_item:
			name = selected_item.TITLE
			url = selected_item.URL
			self.add_win = add_station.Add_Station()
			self.add_win.set_info(name, url)
			self.add_win.show()
		
	def open_url_playlist(self):
		"""Press return on lineedit"""
		text_url = self.url_line_edit.text()
		if text_url:
			self.open_web_url_pls(text_url)

	def press_open_file(self):
		home_dir = os.getenv("HOME")
		self.fileName = QFileDialog.getOpenFileName(self, self.tr("Open File"), home_dir, self.tr("Files (*.pls *.m3u *.m3u8)"))[0]
		if self.fileName:
			self.check_pls_path(self.fileName)

	def choose_pls(self):
		"""Choose PLS"""
		if self.combo_playlist.currentIndex() > 0:
			current_pls = self.combo_playlist.currentText()
			full_path_pls = os.path.join(paths.PLS_FOLDER, current_pls)
			self.clear()
			self.check_pls_path(full_path_pls)
			
	def clear(self):
		"""Clear list"""
		self.table_widget.setRowCount(0)
		
	def press_button_url(self):
		if self.url_line_edit.isVisible():
			self.url_line_edit.hide()
		else:
			self.url_line_edit.show()
			
	def check_pls_path(self, path):
		if "(URL)".lower() in path.lower():
			with open(path, "r") as file_open:
				data = file_open.read()
			self.open_web_url_pls(data)
		else:
			with open(path, 'r') as file_open:
				data = file_open.readlines()
			self.open_playlist(data, "local")
			
	def open_web_url_pls(self, url):
		"""Open web url pls"""
		content = urllib.request.urlopen(url)
		self.open_playlist(content, "web")
		
	def open_playlist(self, content, type_file):
		"""Open playlist"""
		self.clear()
		self.LOAD_STATE = True
		#check button load show
		if not self.button_stop_load.isVisible():
			self.button_stop_load.show()
		name = re.compile(r"#EXTINF:.*", re.I)
		url = re.compile(r"http://|https://.*|rtsp://|udp://", re.I)
		name_station = ''
		url_station = ''
		for line in content:
			if self.LOAD_STATE:
				QCoreApplication.processEvents()
				if type_file == "web":
					line = line.decode()
				line_file = line.split("\n")[0]
				if name.search(line_file):
					if "," in line_file:
						line_file = str(line_file)
						name_station = re.search(r",.*", line_file).group(0).split(",")[1]
						name_station = name_station.strip()
				if url.search(line_file) and line_file[0] != "#":
					url_station = re.search(r"http://.*|https://.*|rtsp://.*|udp://.*", line_file).group(0)
					url_station = url_station.strip()
				else:
					if os.path.isfile(line_file) and os.path.exists(line_file):
						url_station = line_file
				if url_station:
					if not name_station:
						name_station = "station"
				if name_station and url_station:
					self.add_one_row(name_station, url_station)
					name_station = ''
					url_station = ''
		#hide button
		if self.button_stop_load.isVisible():
			self.button_stop_load.hide()
				
	def add_one_row(self, name, url):
		"""Create one pls row"""
		#name
		fileNameItem = MyTableWidgetItem()
		fileNameItem.setText(name)
		fileNameItem.setToolTip(name)
		fileNameItem.setFlags(fileNameItem.flags() ^ Qt.ItemIsEditable)
		fileNameItem.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
		fileNameItem.TITLE = name
		fileNameItem.URL = url
		#set
		row = self.table_widget.rowCount()
		self.table_widget.insertRow(row)
		self.table_widget.setItem(row, 0, fileNameItem)
		
###################################################################################################

class MyTableWidget(QTableWidget):
	"""MyTableWidget class"""
	def __init__(self):
		super().__init__()
		self.setAcceptDrops(True)
		
	def dragEnterEvent(self, event):
		event.accept()
		
	def dragMoveEvent(self, event):
		event.accept()
		
	def dropEvent(self, e):
		list_files = e.mimeData().urls()
		for item in list_files:
			pls_extension = ['pls', 'm3u', 'm3u8',]
			if os.path.isfile(QUrl(item.url()).toLocalFile()):
				path = QUrl(item.url()).toLocalFile()
				if QFileInfo(path).suffix() in pls_extension:
					self.parent().check_pls_path(path)
		
###################################################################################################

class MyTableWidgetItem(QTableWidgetItem):
	"""My TableWidgetItem class"""
	def __init__(self):
		super().__init__()
		self.TITLE = None
		self.URL = None
					
####################################################################################################

class ToolButton(QPushButton):
	"""ToolButton class"""
	def __init__(self):
		super().__init__()
		self.setStyleSheet(styles.get_button_style())
		self.setFocusPolicy(Qt.NoFocus)
		self.setCursor(Qt.PointingHandCursor)
		self.setFixedSize(30, 30)
		self.setIconSize(QSize(25, 25))
					
