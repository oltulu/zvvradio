"""Player module"""
import os
import re
import random
import time
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QMenu,
							 QPushButton, QLabel, QSlider, QButtonGroup, QSizePolicy,
							 QAbstractItemView, QHeaderView, QTableWidget, QTableWidgetItem,
							 QFileDialog, QProgressBar, QStyle)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSettings, QSize, QUrl, QFileInfo, QDir
from . import control_player, zslider, paths


class Player(QWidget):
	"""Player class"""
	def __init__(self):
		super().__init__()
		self.create_widgets()
		
	def create_widgets(self):
		"""Create widgets"""
		self.slider_state = False
		
	#vbox_main
		self.vbox_main = QVBoxLayout()
		self.vbox_main.setContentsMargins(1, 1, 1, 1)
		self.vbox_main.setSpacing(1)
		self.setLayout(self.vbox_main)
		
	#table_widget
		self.table_widget = MyTableWidget()
		self.table_widget.setRowCount(0)
		self.table_widget.setColumnCount(1)
		self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.table_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.table_widget.setHorizontalHeaderLabels(("Name",))
		self.table_widget.verticalHeader().hide()
		self.table_widget.setShowGrid(True)
		self.table_widget.itemDoubleClicked.connect(self.press_double_item)
		self.vbox_main.addWidget(self.table_widget)
		self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
		
		#create_hbox_controls
		self.create_hbox_controls()
		
		###
		self.player.setVolume(30)
		self.button_volume.setValue(30)
		self.setAttribute(Qt.WA_DeleteOnClose, True)
##################################################################################

	def create_hbox_controls(self):
		"""Create hbox_controls"""
		self.BUTTON_SIZE = 40
		MY_BUTTON_SIZE = 40
		self.hbox_controls = QHBoxLayout()
		self.hbox_controls.setContentsMargins(0,0,0,0)
		self.vbox_main.addLayout(self.hbox_controls)
		#button group
		self.control_buttons_group = QButtonGroup()
		self.control_buttons_group.setExclusive(True)
		#button_play
		self.button_play = QPushButton()
		self.button_play.setCheckable(True)
		self.style_button(self.button_play, QIcon("./icons/player/play.gif"))
		self.button_play.clicked.connect(self.press_play_button)
		self.hbox_controls.addWidget(self.button_play)
		self.control_buttons_group.addButton(self.button_play)
		#..stop
		self.button_stop = QPushButton()
		self.button_stop.setCheckable(True)
		self.style_button(self.button_stop, QIcon("./icons/player/stop_mode.gif"))
		self.button_stop.clicked.connect(self.press_stop)
		self.hbox_controls.addWidget(self.button_stop)
		self.control_buttons_group.addButton(self.button_stop)
		#...pause
		self.button_pause = QPushButton()
		self.button_pause.setCheckable(True)
		self.style_button(self.button_pause, QIcon("./icons/player/pause.gif"))
		self.button_pause.clicked.connect(self.press_button_pause)
		self.hbox_controls.addWidget(self.button_pause)
		self.control_buttons_group.addButton(self.button_pause)
		#button_volume
		self.button_volume = ZVolume()
		self.hbox_controls.addWidget(self.button_volume)
		#modes combo
		self.combo_playmodes = QComboBox()
		self.combo_playmodes.setMaximumHeight(self.BUTTON_SIZE)
		self.combo_playmodes.setMaximumWidth(100)
		self.combo_playmodes.setFocusPolicy(Qt.NoFocus)
		self.combo_playmodes.addItem(QIcon("./icons/player/stop_mode.gif"), "Stop")
		self.combo_playmodes.addItem(QIcon("./icons/player/replay_mode.gif"), "Replay")
		self.combo_playmodes.addItem(QIcon("./icons/player/next_mode.gif"), "Next")
		self.combo_playmodes.addItem(QIcon("./icons/player/shuffle_mode.gif"), "Shuffle")
		self.hbox_controls.addWidget(self.combo_playmodes)
		#
		self.hbox_controls.addStretch()
		#button_menu
		self.button_menu = QPushButton()
		self.style_button(self.button_menu, QIcon("./icons/menu_icon.gif"))
		self.hbox_controls.addWidget(self.button_menu)
		#add menu
		font = QFont()
		font.setPointSize(14)
		self.menu_tools = QMenu()
		self.menu_tools.setFont(font)
		self.menu_tools.addAction(QIcon("./icons/open_icon.gif"), 'Add folder', self.press_add_folder)
		self.menu_tools.addAction(QIcon("./icons/add_files_icon.gif"), 'Add file(s)', self.press_add_files)
		self.menu_tools.addSeparator()
		self.menu_tools.addAction(QIcon("./icons/playlist.gif"), 'Create playlist', self.press_create_playlist)
		self.menu_tools.addSeparator()
		self.menu_tools.addAction(QIcon("./icons/remove_file.gif"), 'Remove item(s)', self.press_remove_items)
		self.menu_tools.addAction(QIcon("./icons/clear_icon.gif"),'Clear all', self.press_clear_list)
		self.menu_tools.addSeparator()
		self.menu_tools.addAction(QIcon("./icons/about_icon.gif"),'About', self.press_about_button)
		self.button_menu.setMenu(self.menu_tools)
		
	def style_button(self, button, icon):
		"""Style button"""
		button.setIconSize(QSize(self.BUTTON_SIZE-4, self.BUTTON_SIZE-4))
		button.setIcon(icon)
		button.setFixedSize(self.BUTTON_SIZE, self.BUTTON_SIZE)
		button.setCursor(Qt.PointingHandCursor)
		button.setStyleSheet(paths.get_button_style())
		
	def press_clear_list(self):
		"""Press clear button"""
		self.table_widget.setRowCount(0)
		
	def press_remove_items(self):
		"""Press remove items"""
		selected_items = self.table_widget.selectedItems()
		if selected_items:
			for item in selected_items:
				self.table_widget.removeRow(item.row())
				
	def press_create_playlist(self):
		"""Press create playlist"""
		if self.table_widget.rowCount() > 0:
			file_name = os.path.join(QDir.homePath(), 'playlist.m3u')
			filePath = QFileDialog.getSaveFileName(self, "Save playlist", file_name, ("Playlists (*.pls *.m3u *.m3u8)"))
			if filePath:
				path = filePath[0]
				if path:
					with open(path, 'a') as file_save:
						file_save.write('#EXTM3U\n')
						for row in range(self.table_widget.rowCount()):
							item = self.table_widget.item(row, 0)
							title = item.TITLE
							url = item.PATH
							file_save.write('#EXTINF:-1,{0}\n'.format(title))
							file_save.write('{0}\n'.format(url))
						
	def read_playlist(self, pls_file):
		"""Read playlist"""
		self.table_widget.setRowCount(0)
		with open(pls_file, 'r') as file_load:
			title = None
			path = None
			for line in file_load.readlines():
				if '#EXTINF' in line:
					line = line.split('\n')[0]
					title = line.split(',', 1)[1]
				if os.path.exists(line.split('\n')[0]):
					path = line.split('\n')[0]
				if title and path:
					self.add_one_row(title, path)
					title = None
					path = None
					
	def press_add_files(self):
		"""Press add files"""
		get_files = QFileDialog.getOpenFileNames(self, 'Add file(s)', QDir.homePath(),
										 ("Audio (*.mp3 *.wav *.ogg *.ac3 *.flac)"), options = QFileDialog.DontUseNativeDialog)
		if get_files[0]:
			get_files = set(get_files[0])
			for item in get_files:
				title = os.path.split(item)[1]
				self.add_one_row(title, item)
		
	def press_add_folder(self):
		"""Press add folder"""
		get_folder = QFileDialog.getExistingDirectory(self, 'Choose folder', QDir.homePath(),
								QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks | 
								QFileDialog.DontUseNativeDialog)
		if get_folder:
			self.add_folder(get_folder)
		
	def add_folder(self, folder_path):
		"""Add folder"""
		musics_reg_exp = ["*.mp3", "*.wav", "*.ogg", "*.ac3", "*.flac",]
		files = QDir(folder_path).entryInfoList(musics_reg_exp, QDir.Files)
		for music_file in files:
			path = music_file.filePath()
			title = music_file.fileName()
			self.add_one_row(title, path)
			
	def press_about_button(self):
		"""Press about button"""
		self.about_win = about.About()
		self.about_win.show()
##################################################################################

	def add_one_row(self, name, path):
		"""Add one row"""
		#set
		font = QFont()
		font.setPointSize(12)
		#name
		fileNameItem = MyItem()
		fileNameItem.setText(name)
		fileNameItem.setIcon(QIcon('./icons/music_icon.gif'))
		fileNameItem.setFont(font)
		fileNameItem.TITLE = name
		fileNameItem.PATH = path
		#set
		row = self.table_widget.rowCount()
		self.table_widget.insertRow(row)
		self.table_widget.setItem(row, 0, fileNameItem)

	def press_double_item(self, tableItem):
		"""Press table item"""
		path = tableItem.PATH
		self.player_play(path)
		self.label_title.setText(os.path.split(path)[1][:50])
		
##################################PLAYER##########################################

	def player_play(self, url):
		"""Player play"""
		self.push_stop = False
		self.CURRENT_URL = url
		self.player.setMedia(QMediaContent(QUrl.fromLocalFile(url)))
		self.player.play()
		
	def change_media_status(self, status):
		"""Change media status"""
		if self.push_stop == False:
			if status == QMediaPlayer.EndOfMedia:
				self.change_mode_play()
		
	def check_player_state(self, state):
		"""Check player state"""
		if state == QMediaPlayer.StoppedState:
			if not self.button_stop.isChecked():
				self.button_stop.setChecked(True)
		if state == QMediaPlayer.PlayingState:
			if not self.button_play.isChecked():
				self.button_play.setChecked(True)
		if state == QMediaPlayer.PausedState:
			if not self.button_pause.isChecked():
				self.button_pause.setChecked(True)
	
	def volume_change(self, value):
		"""Change volume"""
		self.player.setVolume(value)
		
	def set_position_time(self):
		"""Set position time"""
		last_time = self.player.duration()
		if last_time > 0:
			self.control_widget.position_slider.setRange(0,last_time)
			last_time = time.strftime('%H:%M:%S', time.gmtime(last_time/1000.0))
			self.control_widget.label_pos_last.setText(str(last_time))
		else:
			self.control_widget.position_slider.setRange(0,0)
			self.control_widget.position_slider.setValue(0)
			self.control_widget.label_pos_last.clear()
			self.control_widget.label_pos_current.clear()

	def change_position_time(self, position):
		"""Change position time"""
		if position > 0:
			if self.player.duration() > 0 and self.slider_state == False:
				self.control_widget.position_slider.setValue(position)
			current_time = time.strftime('%H:%M:%S', time.gmtime(position/1000.0))
			self.control_widget.label_pos_current.setText(str(current_time))

	def hand_pos_changed(self):
		value = self.control_widget.position_slider.value()
		self.change_position_time(value)
		self.player.setPosition(value)
		self.slider_state = False
		self.control_widget.label_move_time.hide()
		
	def move_time(self, position):
		if self.slider_state == True:
			current_time = time.strftime('%H:%M:%S', time.gmtime(position/1000.0))
			self.control_widget.label_move_time.show()
			self.control_widget.label_move_time.setText(str(current_time))
	
	def set_slider_pressed(self):
		self.slider_state = True
		
	def press_button_pause(self):
		if self.player.state() == QMediaPlayer.PausedState:
			self.player.play()
		else:
			self.player.pause()
		
	def press_stop(self):
		self.push_stop = True
		self.player.stop()

	def press_play_button(self):
		self.player.play()
		
	def change_mode_play(self):
		"""Change mode play"""
		current_mode = self.combo_playmodes.currentText().lower()
		mode_list = ["next", "shuffle",]
		if current_mode == "stop":
			self.player.stop()
		if current_mode == "replay":
			self.player.play()
		if current_mode in mode_list:
			self.press_next_file()
		
	def press_next_file(self):
		"""Press next file"""
		if self.table_widget.rowCount() > 0:
			current_item = self.table_widget.currentItem()
			if current_item:
				if self.combo_playmodes.currentText().lower() == "shuffle":
					row_num = random.randrange(0, self.table_widget.rowCount())
				else:
					row_num = current_item.row()
					row_num += 1
					if row_num == self.table_widget.rowCount():
						row_num = 0
				self.choose_next_file(row_num)
				
	def choose_next_file(self, row_num):
		"""Choose next file"""
		next_item = self.table_widget.item(row_num, 0)
		self.table_widget.setCurrentItem(next_item)
		self.press_double_item(next_item)
		
	def press_prev_file(self):
		"""Press prev file"""
		if self.table_widget.rowCount() > 0:
			current_item = self.table_widget.currentItem()
			if current_item:
				row_num = current_item.row()
				row_num -= 1
				if row_num <= 0:
					row_num = 0
				self.choose_next_file(row_num)

	def press_minus_time(self):
		"""Press minus time"""
		if self.player.state() == QMediaPlayer.PlayingState:
			if self.player.duration() > 0:
				current_position = self.player.position()
				current_position -= 10000
				self.player.setPosition(current_position)
					
	def press_plus_time(self):
		"""Press plus time"""
		if self.player.state() == QMediaPlayer.PlayingState:
			if self.player.duration() > 0:
				current_position = self.player.position()
				current_position += 15000
				self.player.setPosition(current_position)

##################################################################

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
			music_extensions = ['mp3', 'wav', 'ogg', 'ac3', 'flac',]
			pls_extension = ['pls', 'm3u', 'm3u8',]
			if os.path.isfile(QUrl(item.url()).toLocalFile()):
				path = QUrl(item.url()).toLocalFile()
				if QFileInfo(path).suffix() in music_extensions:
					title = os.path.split(path)[1]
					self.parent().add_one_row(title, path)
				if QFileInfo(path).suffix() in pls_extension:
					self.parent().read_playlist(path)
			if os.path.isdir(QUrl(item.url()).toLocalFile()):
				folder_path = QUrl(item.url()).toLocalFile()
				self.parent().add_folder(folder_path)

##################################################################

class MyItem(QTableWidgetItem):
	"""MyItem class"""
	def __init__(self):
		super().__init__()
		self.TITLE = None
		self.PATH = None
		self.setFlags(self.flags() ^ Qt.ItemIsEditable)
		
##################################################################

class ZVolume(QProgressBar):
	"""ZVolume class"""
	def __init__(self):
		super().__init__()
		self.create_widget()
		
	def create_widget(self):
		"""Create widget"""
		self.setOrientation(Qt.Vertical)
		self.setFixedSize(40, 40)
		self.setAlignment(Qt.AlignCenter)
		self.setRange(0, 100)
		self.setStyleSheet("""
						QProgressBar{
							color:black;
							border:1px solid silver;
							border-radius:5px;
							text-align:center;
						}
						
						QProgressBar::chunk{
							background-color:lightgreen;
						}
					""")
		
	def wheelEvent(self, event):
		"""Wheel event"""
		value = self.parent().player.volume()
		pd = event.pixelDelta()
		ad = event.angleDelta()
		if pd.y() > 0 or ad.y() > 0:
			value += 2
		if pd.y() < 0 or ad.y() < 0:
			value -= 2
		self.setValue(value)
		self.change_volume(value)
		
	def mousePressEvent(self, ev):
		""" Jump to click position """
		value = QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), ev.y(), self.height(), True)
		self.setValue(value)
		self.change_volume(value)
		
	def mouseMoveEvent(self, ev):
		""" Jump to pointer position while moving """
		value = QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), ev.y(), self.height(), True)
		self.setValue(value)
		self.change_volume(value)
		
	def change_volume(self, value):
		"""Change volume"""
		self.parent().player.setVolume(value)
