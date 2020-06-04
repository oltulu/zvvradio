##!/usr/bin/env python3
"""Main file"""
import sys
import os
from PyQt5.QtWidgets import (QMainWindow, QApplication, QSystemTrayIcon,
							QMenu, QDesktopWidget)
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import QSettings, Qt, QTranslator, QLocale
from modules import widgets, paths, resources


class ZVVRadio(QMainWindow):
	"""Main class"""
	def __init__(self):
		super().__init__()
		self.create_window()

	def create_window(self):
		"""create window"""
		# settigs
		self.settings = QSettings(paths.CONFIG_PATH, QSettings.IniFormat)
		#central widget
		self.central_widget = widgets.Widgets()
		self.setCentralWidget(self.central_widget)

		#add statusbar
		self.statusbar = self.statusBar()
		self.setStatusBar(self.statusbar)
		self.statusbar.setSizeGripEnabled(False)
		self.statusbar.setStyleSheet("QStatusBar{color:blue; font-size:13px;}")
		
		###
		self.setFixedSize(350, 500)
		self.setWindowTitle("ZVVRadio")
		self.setWindowIcon(QIcon(':/app_icon.ico'))
		self.show()

		#autostart
		pal = self.palette()
		pal.setColor(QPalette.Window, QColor('white'))
		self.setPalette(pal)
		self.center()

#############################################################################

	def center(self):
		# geometry of the main window
		qr = self.frameGeometry()
		# center point of screen
		cp = QDesktopWidget().availableGeometry().center()
		# move rectangle's center point to screen's center point
		qr.moveCenter(cp)
		# top left of rectangle becomes top left of window centering it
		self.move(qr.topLeft())

	def changeEvent(self, event):
		"""Hide main window from taskbar if minimize"""
		if self.isMinimized():
			panel_state = int(self.settings.value('config/minimize_panel'))
			if panel_state == 2:
				self.central_widget.tab4.press_panel_button()
				
	def closeEvent(self, event):
		"""Close event"""
		volume = self.central_widget.PLAYER.audio_get_volume()
		self.settings.setValue('config/volume', volume)
		self.settings.sync()
		event.accept()

#############################################################################
APP = QApplication(sys.argv)
SETTINGS = QSettings(paths.CONFIG_PATH, QSettings.IniFormat)
CURRENT_LANG = SETTINGS.value('config/language')
TRANSLATOR = QTranslator()
if CURRENT_LANG == 'system':
	lang = QLocale.system().name()
	if 'ru' in lang:
		TRANSLATOR.load('./langs/lang_rus')
	if 'uk' in lang:
		TRANSLATOR.load('./langs/lang_ukr')
	if 'tr' in lang:
		TRANSLATOR.load('./langs/lang_tr')
else:
	if CURRENT_LANG == 'russian':
		TRANSLATOR.load('./langs/lang_rus')
	if CURRENT_LANG == 'ukrainian':
		TRANSLATOR.load('./langs/lang_ukr')
	if CURRENT_LANG == 'turkish':
		TRANSLATOR.load('./langs/lang_tr')
APP.installTranslator(TRANSLATOR)
WIN = ZVVRadio()
sys.exit(APP.exec_())
