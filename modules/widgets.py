"""Widgets module"""
import os
import re
import sys
import time
import json
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
							 QLabel, QPushButton, QTabWidget, 
							 QButtonGroup, QLineEdit, QMenu,
							 QApplication)
from PyQt5.QtGui import QFont, QIcon, QClipboard
from PyQt5.QtCore import Qt, QTimer, QSize, QSettings, QStandardPaths, QDir
from . import (vlc, styles, tab1, tab2, pls, search_radio, tab4, paths, zslider, equalizer)


class Widgets(QWidget):
	"""Widgets class"""
	def __init__(self):
		super().__init__()
		self.create_buttons()

	def create_buttons(self):
		"""Create widgets"""
		#init
		self.SETTINGS = QSettings(paths.CONFIG_PATH, QSettings.IniFormat)
		self.instance = vlc.Instance()
		self.PLAYER = self.instance.media_player_new()
		self.CURRENT_URL = None
		
		#events
		self.player_events = self.PLAYER.event_manager()
		self.player_events.event_attach(vlc.EventType.MediaPlayerPlaying, self.check_player_playing)
		self.player_events.event_attach(vlc.EventType.MediaPlayerEncounteredError, self.player_gets_error)
		
	#vbox_main
		self.vbox_main = QVBoxLayout()
		self.vbox_main.setContentsMargins(1, 1, 1, 1)
		self.vbox_main.setSpacing(0)
		self.setLayout(self.vbox_main)
		
	#hbox_control
		self.hbox_control = QHBoxLayout()
		self.hbox_control.setSpacing(3)
		self.vbox_main.addLayout(self.hbox_control)
		#button_play
		self.button_play = Tool_button()
		self.button_play.set_info(QIcon(':/play_icon.png'), "Play")
		self.button_play.clicked.connect(self.press_button_play)
		self.hbox_control.addWidget(self.button_play)
		#add stop button
		self.button_stop = Tool_button()
		self.button_stop.set_info(QIcon(':/stop_icon.png'), "Stop")
		self.button_stop.clicked.connect(self.press_button_stop)
		self.hbox_control.addWidget(self.button_stop)
		#add button record
		self.button_record = Tool_button()
		self.button_record.set_info(QIcon(':/record_icon.png'), "Record")
		self.button_record.setCheckable(True)
		self.button_record.toggled.connect(self.press_record)
		self.hbox_control.addWidget(self.button_record)
		#volume
		self.vbox_volume = QVBoxLayout()
		self.hbox_control.addLayout(self.vbox_volume)
		#add label volume
		self.label_volume = QLabel()
		self.label_volume.setStyleSheet(styles.get_label_style())
		self.label_volume.setAlignment(Qt.AlignCenter)
		self.vbox_volume.addWidget(self.label_volume)
		#add volume
		self.volume_slider = zslider.Zslider()
		self.volume_slider.setStyleSheet(styles.get_slider_style())
		self.volume_slider.setRange(0, 100)
		self.volume_slider.valueChanged.connect(self.volume_change)
		self.vbox_volume.addWidget(self.volume_slider)
		#add mwnu button
		self.button_menu = Tool_button()
		self.button_menu.set_info(QIcon(":/menu_main.png"), 'Menu')
		self.hbox_control.addWidget(self.button_menu)
		###
		self.tools_menu = QMenu()
		self.tools_menu.addAction(QIcon(':/add_icon.png'), self.tr('Add station'), self.add_station)
		self.tools_menu.addAction(QIcon(':/down_icon.png'), self.tr('Panel'), self.switch_to_panel)
		self.button_menu.setMenu(self.tools_menu)
		#add about button
		self.button_about = Tool_button()
		self.button_about.set_info(QIcon(":/about_icon.png"), 'About')
		self.button_about.clicked.connect(self.press_button_about)
		self.hbox_control.addWidget(self.button_about)

	#add vbox label name of station
		self.vbox_label_station = QVBoxLayout()
		self.vbox_label_station.setSpacing(0)
		self.vbox_main.addLayout(self.vbox_label_station)
		#add label name of station
		self.LABEL_STATION = QPushButton()
		self.LABEL_STATION.setFlat(True)
		self.LABEL_STATION.setFocusPolicy(Qt.NoFocus)
		self.LABEL_STATION.setStyleSheet("QPushButton{font-size:16px; font-weight:bold;}QPushButton{border:1px solid transparent;}")
		self.vbox_label_station.addWidget(self.LABEL_STATION)
		#add label artist
		self.label_artist = Artist_button(self)
		self.label_artist.clicked.connect(self.press_copy_artist)
		self.vbox_label_station.addWidget(self.label_artist)

	#add tabber
		self.tabber = QTabWidget(self)
		self.tabber.tabBar().setIconSize(QSize(20, 20))
		self.tabber.tabBarClicked.connect(self.press_tab_countries)
		self.vbox_main.addWidget(self.tabber)
		#FAV_TAB
		self.tab1 = tab1.Tab1_main(self)
		self.tabber.addTab(self.tab1, QIcon(':/fav_icon.png'), "")
		#COUNTRIES_TAB
		self.tab2 = tab2.Tab2_stations(self)
		self.tabber.addTab(self.tab2, QIcon(':/url_icon.png'), "")
		#PLS_TAB
		self.pls_tab = pls.Pls()
		self.tabber.addTab(self.pls_tab, QIcon(":/pls_icon.png"), "")
		#SEARCH_RADIO
		self.search_tab = search_radio.Search_radio()
		self.tabber.addTab(self.search_tab, QIcon(":/search_icon.png"), "")
		#EQ_TAB
		self.eq_tab = equalizer.Equalizer()
		self.tabber.addTab(self.eq_tab, QIcon(":/eq_icon.png"), "")
		#TOOLS_TAB
		self.tab4 = tab4.Tab4_config(self)
		self.tabber.addTab(self.tab4, QIcon(":/config_icon.png"), "")
		
		###autorun
		self.volume_change(int(self.SETTINGS.value('config/volume')))
		
##########################################################################################

	def check_player_playing(self, event):
		"""Check playing"""
		self.label_artist.get_artist()
		
	def player_gets_error(self, event):
		"""Get error"""
		self.label_artist.set_artist('Error')
		
##########################################################################################

	def press_copy_artist(self):
		"""Press copy"""
		copy_text = self.label_artist.TITLE
		if copy_text:
			QApplication.clipboard().setText(copy_text)

	def press_record(self, record_state):
		"""Press record"""
		if record_state:
			time_current = time.strftime('%Y%m%d_%H%M%S', time.gmtime())
			file_name = "zvvradio_{0}_record.ac3".format(time_current)
			try:
				music_path = QStandardPaths.writableLocation(QStandardPaths.MusicLocation)
			except:
				music_path = QDir.homePath()
			music_file_path = os.path.join(music_path, file_name)
			try:
				self.PLAYER._set_property('record-file', music_file_path)
			except:
				pass
		else:
			self.cancel_record()
			
	def cancel_record(self):
		"""Cancel record"""
		try:
			if self.PLAYER._get_property('record-file'):
				self.PLAYER._set_property('record-file', '')
			if self.button_record.isChecked():
				self.button_record.setChecked(False)
		except:
			pass
		
	def clear_labels(self):
		"""Clear artist"""
		self.LABEL_STATION.setText('')
		self.label_artist.setText('')
		
	def check_player_error(self, event):
		self.LABEL_STATION.setText("Error")

	def press_tab_countries(self, index):
		"""Press tab"""
		if index == 1:
			self.tab2.press_back()

	def press_button_about(self):
		"""Press about"""
		from . import about
		self.win_about = about.About()
		self.win_about.show()

	def press_button_play(self):
		"""Press play button"""
		self.PLAYER.play()
		
	def press_button_stop(self):
		"""Press controls"""
		self.PLAYER.stop()
		self.clear_labels()
		#self.cancel_record()

	def volume_change(self, value):
		"""Volume change"""
		volume_text = 'Volume: {0}'.format(str(value))
		self.PLAYER.audio_set_volume(value)
		self.volume_slider.setValue(value)
		self.label_volume.setText(volume_text)
		
	def player_play(self, title, url):
		"""Player play"""
		#self.cancel_record()
		self.set_title(title)
		self.CURRENT_URL = url
		self.media = self.instance.media_new(url)
		self.PLAYER.set_media(self.media)
		self.PLAYER.play()
		self.label_artist.get_artist()
		
	def set_title(self, name):
		"""Get land"""
		if len(name) > 25:
			self.LABEL_STATION.setText(name[:25] + '...')
		else:
			self.LABEL_STATION.setText(name)
			
	def switch_to_panel(self):
		"""Switch to panel"""
		self.tab4.press_panel_button()
		
	def add_station(self):
		"""Add station"""
		self.tab4.press_add_station()
#########################################################################################

class Tool_button(QPushButton):
	"""Tool button class"""
	def __init__(self):
		super().__init__()
		self.create_button()
		
	def create_button(self):
		"""Create button"""
		self.setIconSize(QSize(35, 35))
		self.setFixedSize(40, 40)
		self.setCursor(Qt.PointingHandCursor)
		self.setStyleSheet(styles.get_button_style())
		
	def set_info(self, icon, text):
		"""Set info"""
		self.setIcon(icon)
		self.setStatusTip(self.tr(text))

###########################################################################################

class Artist_button(QPushButton):
	"""Artist Button class"""
	def __init__(self, parentWidget):
		super().__init__()
		self.parentWidget = parentWidget
		self.TITLE = None
		self.setFlat(True)
		self.setFocusPolicy(Qt.NoFocus)
		self.setCursor(Qt.PointingHandCursor)
		self.setStyleSheet("QPushButton{font-size:10px}")
		self.timer_artist = QTimer()
		self.timer_artist.setInterval(30000)
		self.timer_artist.timeout.connect(self.get_artist)
		self.timer_artist.start()
		
	def set_artist(self, title):
		"""Set artist"""
		if type(title) is bytes:
			try:
				title = title.decode('windows-1251', 'replace')
			except:
				title = title.decode('utf-8', 'ignore')
		self.TITLE = title
		self.setText(title[:50])
		self.setToolTip(title)
				
	def get_artist(self):
		"""Get artist"""
		self.setText('')
		if self.parentWidget.PLAYER.get_state() == vlc.State.Playing:
			media = self.parentWidget.PLAYER.get_media()
			if media:
				title = media.get_meta(vlc.Meta.Title)
				nowplaying = media.get_meta(vlc.Meta.NowPlaying)
				if "101.ru" in media.get_mrl():
					nowplaying = "101.ru"
				if not nowplaying:
					nowplaying = title
					if not title:
						nowplaying = ' - '
				self.set_artist(nowplaying)
				
