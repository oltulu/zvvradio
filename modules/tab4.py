import os
import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
							 QGroupBox, QLabel, QPushButton, 
							 QComboBox, QScrollArea, QLineEdit,
							 QCheckBox, QFileDialog, QProgressBar,
							 QApplication)
from PyQt5.QtGui import QIcon, QFont, QDesktopServices
from PyQt5.QtCore import Qt, QSettings, QTimer, QProcess, QDir, QStandardPaths, QUrl
from . import add_station, paths, styles


class Tab4_config(QWidget):
	def __init__(self, parentWidget):
		super().__init__()
		self.parentWidget = parentWidget
		self.create_tab4()

	def create_tab4(self):
		"""Create tools widgets"""
		self.settings = QSettings(paths.CONFIG_PATH, QSettings.IniFormat)
		
		#main font
		main_font = QFont()
		main_font.setPointSize(10)
		
#vbox_main
		self.vbox_main = QVBoxLayout()
		self.vbox_main.setContentsMargins(1, 1, 1, 1)
		self.setLayout(self.vbox_main)
		
	#scroll_area_tools
		self.scroll_area_tools = QScrollArea()
		self.scroll_area_tools.setWidgetResizable(True)
		self.scroll_area_tools.setStyleSheet(styles.get_scrollarea_style() + styles.get_scrollbar_style())
		self.vbox_main.addWidget(self.scroll_area_tools)
		
	#widget_tools
		self.widget_tools = QWidget()
		self.scroll_area_tools.setWidget(self.widget_tools)
		
	#add vbox_tools
		self.vbox_tools = QVBoxLayout()
		self.vbox_tools.setContentsMargins(1, 1, 1, 1)
		self.widget_tools.setLayout(self.vbox_tools)
		
	#add hbox check entry
		self.hbox_check_stream = QHBoxLayout()
		self.vbox_tools.addLayout(self.hbox_check_stream)
		#add entry
		self.stream_entry_check = QLineEdit()
		self.stream_entry_check.setFixedHeight(25)
		self.stream_entry_check.setPlaceholderText(self.tr("Put your stream here and press 'Check'"))
		self.stream_entry_check.setStyleSheet("QLineEdit{border:1px solid silver; font-size:11px;}")
		self.stream_entry_check.setClearButtonEnabled(True)
		self.hbox_check_stream.addWidget(self.stream_entry_check)
		#add button check
		self.button_check_stream = QPushButton()
		self.button_check_stream.setFixedSize(25, 25)
		self.button_check_stream.setCursor(Qt.PointingHandCursor)
		self.button_check_stream.setIcon(QIcon(':/check_icon.png'))
		self.button_check_stream.setStyleSheet(styles.get_button_style())
		self.button_check_stream.clicked.connect(self.press_check_stream)
		self.hbox_check_stream.addWidget(self.button_check_stream)

########################################GLOBAL####################################
	#add group tabs
		self.GROUP_GLOBAL = QGroupBox(self.tr("GLOBAL"))
		self.vbox_tools.addWidget(self.GROUP_GLOBAL)
		self.GROUP_GLOBAL.setAlignment(Qt.AlignHCenter)
		self.vbox_global = QVBoxLayout()
		self.GROUP_GLOBAL.setLayout(self.vbox_global)
	#add hbox add new station
		self.hbox_add_station = QHBoxLayout()
		self.hbox_add_station.setAlignment(Qt.AlignTop)
		self.vbox_global.addLayout(self.hbox_add_station)
		#add label
		self.label_add_station = QLabel(self.tr("Add station:"))
		self.label_add_station.setFont(main_font)
		self.hbox_add_station.addWidget(self.label_add_station)
		#add button add
		self.btn_add_station = QPushButton()
		self.btn_add_station.setIcon(QIcon(':/add_icon.png'))
		self.btn_add_station.setFixedSize(25, 25)
		self.btn_add_station.setStyleSheet(styles.get_button_style())
		self.btn_add_station.setCursor(Qt.PointingHandCursor)
		self.btn_add_station.setFont(main_font)
		self.btn_add_station.clicked.connect(self.press_add_station)
		self.hbox_add_station.addWidget(self.btn_add_station)

	#add combo for change lang
		self.hbox_langs = QHBoxLayout()
		self.vbox_global.addLayout(self.hbox_langs)
		#add label
		self.label_langs = QLabel(self.tr("Change language:"))
		self.label_langs.setFont(main_font)
		self.hbox_langs.addWidget(self.label_langs)
		#add combobox
		self.combobox_langs = QComboBox()
		self.hbox_langs.addWidget(self.combobox_langs)
		list_langs = [self.tr('Choose:'),'System','Eng','Rus','Ukr',]
		for item in list_langs:
			self.combobox_langs.addItem(item)
		self.combobox_langs.activated.connect(self.change_language)

####################################PANEL##################################
	#add group panel
		self.GROUP_PANEL = QGroupBox(self.tr("PANEL"))
		self.vbox_tools.addWidget(self.GROUP_PANEL)
		self.GROUP_PANEL.setAlignment(Qt.AlignHCenter)
		self.vbox_panel = QVBoxLayout()
		self.GROUP_PANEL.setLayout(self.vbox_panel)

	#add hbox panel mode
		self.hbox_panel_mode = QHBoxLayout()
		self.vbox_panel.addLayout(self.hbox_panel_mode)
		#add label_panel
		self.label_panel = QLabel(self.tr("Switch to Panel mode:"))
		self.label_panel.setFont(main_font)
		self.hbox_panel_mode.addWidget(self.label_panel)
		#add panel button
		self.button_panel = QPushButton()
		self.button_panel.setText(self.tr("Panel"))
		self.button_panel.setIcon(QIcon(':/down_icon.png'))
		self.button_panel.setStyleSheet(styles.get_button_style())
		self.button_panel.setMinimumHeight(25)
		self.button_panel.setMinimumWidth(90)
		self.button_panel.setCursor(Qt.PointingHandCursor)
		self.button_panel.setFont(main_font)
		self.button_panel.clicked.connect(self.press_panel_button)
		self.hbox_panel_mode.addWidget(self.button_panel)

	#add minimize to panel mode
		self.hbox_minimize_panel = QHBoxLayout()
		self.vbox_panel.addLayout(self.hbox_minimize_panel)
		#add label
		self.label_minimize_panel = QLabel(self.tr("Minimize to panel:"))
		self.label_minimize_panel.setFont(main_font)
		self.hbox_minimize_panel.addWidget(self.label_minimize_panel)
		#add checkbox
		self.checkbox_minimize_panel = QCheckBox()
		self.checkbox_minimize_panel.setTristate(False)
		self.checkbox_minimize_panel.setCheckState(int(self.settings.value('config/minimize_panel')))
		self.checkbox_minimize_panel.stateChanged.connect(self.change_minimize_panel)
		self.hbox_minimize_panel.addWidget(self.checkbox_minimize_panel)
		self.hbox_minimize_panel.setAlignment(self.checkbox_minimize_panel, Qt.AlignRight)

##########################################RECORD#####################################

	#add group record
		self.GROUP_RECORD = QGroupBox(self.tr("RECORD"))
		self.vbox_tools.addWidget(self.GROUP_RECORD)
		self.GROUP_RECORD.setAlignment(Qt.AlignHCenter)
		self.record_vbox = QVBoxLayout()
		self.GROUP_RECORD.setLayout(self.record_vbox)

	#hbox record place
		self.hbox_record_place = QHBoxLayout()
		self.record_vbox.addLayout(self.hbox_record_place)
		#label
		self.record_place_label = QLabel(self.tr("Open records folder:"))
		self.record_place_label.setFont(main_font)
		self.hbox_record_place.addWidget(self.record_place_label)
		##
		self.record_place_folder = QPushButton()
		self.record_place_folder.setFixedSize(25, 25)
		self.record_place_folder.setCursor(Qt.PointingHandCursor)
		self.record_place_folder.setStyleSheet(styles.get_button_style())
		self.record_place_folder.setIcon(QIcon(':/folder_icon.png'))
		self.record_place_folder.clicked.connect(self.press_record_place_button)
		self.hbox_record_place.addWidget(self.record_place_folder)

#########################TIMER#########################################

	#add timer hbox
		self.hbox_timer = QHBoxLayout()
		self.vbox_tools.addLayout(self.hbox_timer)
		#label
		self.label_timer = QLabel(self.tr("Set timer: "))
		self.hbox_timer.addWidget(self.label_timer)
		#combo_time
		self.combo_time = QComboBox()
		self.hbox_timer.addWidget(self.combo_time)
		self.time_list = [self.tr("Time:"),"1","5","10","15","30","45","60","90","120",]
		for item in self.time_list:
			self.combo_time.addItem(item)
		self.combo_time.activated.connect(self.set_time)
		#after time
		self.combo_what_do = QComboBox()
		self.hbox_timer.addWidget(self.combo_what_do)
		self.do_list = [self.tr("After:"),self.tr("Close"),self.tr("Suspend"),self.tr("Shutdown"),]
		for item in self.do_list:
			self.combo_what_do.addItem(item)
		#progress_bar
		self.progress_bar = QProgressBar()
		self.progress_bar.setOrientation(Qt.Horizontal)
		self.progress_bar.hide()
		self.vbox_main.addWidget(self.progress_bar)
			
		#add stretch
		self.vbox_tools.addStretch()
		
		#TIMER_SHUTDOWN
		self.timer_shutdown = QTimer()
		self.timer_shutdown.setInterval(60000)
		self.timer_shutdown.timeout.connect(self.change_time)

###################################################################################
###################################################################################

	def press_record_place_button(self):
		"""Choose record folder"""
		QDesktopServices.openUrl(QUrl.fromLocalFile(QStandardPaths.writableLocation(QStandardPaths.MusicLocation)))

	def change_language(self):
		"""Change language"""
		current_item = self.combobox_langs.currentIndex()
		if current_item == 1:
			self.settings.setValue('config/language','system')
		if current_item == 2:
			self.settings.setValue('config/language','english')
		if current_item == 3:
			self.settings.setValue('config/language','russian')
		if current_item == 4:
			self.settings.setValue('config/language','ukrainian')
		self.settings.sync()
		
	def press_add_station(self):
		"""Press add station"""
		self.add_win = add_station.Add_Station()
		self.add_win.show()

	def press_check_stream(self):
		"""Press check stream"""
		stream = self.stream_entry_check.text()
		if stream:
			title = self.tr("Stream")
			self.parent().parent().parent().player_play(title, stream)

	def change_minimize_panel(self, state):
		"""Change minimize to panel"""
		if state:
			self.settings.setValue('config/minimize_panel',2)
		else:
			self.settings.setValue('config/minimize_panel',0)
		self.settings.sync()

######################################TIMER############################

	def start_progress(self, time):
		self.progress_bar.show()
		self.progress_bar.setRange(0, time)
		self.progress_bar.setValue(time)
		self.progress_bar.setFormat(str(time) + " min")

	def set_time(self):
		if self.combo_time.currentIndex() > 0:
			self.timer_shutdown.stop()
			time = int(self.combo_time.currentText())
			self.start_progress(time)
			self.timer_shutdown.start()
		if self.combo_time.currentIndex() == 0:
			self.timer_shutdown.stop()
			self.progress_bar.hide()

	def change_time(self):
		"""Change time"""
		value = self.progress_bar.value()
		value -= 1
		self.progress_bar.setValue(value)
		self.progress_bar.setFormat(str(value) + " min")
		if value <= 0:
			self.timer_shutdown.stop()
			if self.combo_what_do.currentIndex() == 0:
				self.progress_bar.hide()
			if self.combo_what_do.currentIndex() == 1:
				QApplication.exit()
			if self.combo_what_do.currentIndex() == 2:
				try:
					if sys.platform.startswith("linux"):
						QProcess.startDetached("systemctl suspend")
					if sys.platform.startswith("win"):
						QProcess.startDetached("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
				except:
					pass
			if self.combo_what_do.currentIndex() == 3:
				if sys.platform.startswith("win"):
					QProcess.startDetached("shutdown.exe /s")
				if sys.platform.startswith("linux"):
					QProcess.startDetached("shutdown -P now")
		
	def press_panel_button(self):
		"""Press panel button"""
		from . import hpanel
		self.parentWidget.parent().hide()
		volume = self.parentWidget.PLAYER.audio_get_volume()
		self.new_panel_win = hpanel.Hpanel(self.parentWidget)
		self.new_panel_win.volume_change(volume)
		self.new_panel_win.show()
