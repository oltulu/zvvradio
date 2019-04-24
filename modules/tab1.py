"""Tab Fav module"""
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QScrollArea, QMenu)
from PyQt5.QtGui import QIcon, QFont, QCursor, QPalette, QColor
from PyQt5.QtCore import Qt, QCoreApplication, QSize, QSettings
from . import paths, styles, flowbox, zbutton


class Tab1_main(QWidget):
	"""Tab FAV class"""
	def __init__(self, parentWidget):
		super().__init__()
		self.parentWidget = parentWidget
		self.create_widgets()
		
	def create_widgets(self):
		"""Create widgets"""
		self.SETTINGS = QSettings(paths.CONFIG_PATH, QSettings.IniFormat)
		self.CURRENT_BUTTON = None
		
	#vbox_main
		self.vbox_main = QVBoxLayout()
		self.vbox_main.setContentsMargins(0, 0, 0, 0)
		self.setLayout(self.vbox_main)
		
		#scroll_area
		self.scroll_area = QScrollArea()
		self.scroll_area.setStyleSheet(styles.get_scrollarea_style() + styles.get_scrollbar_style())
		self.scroll_area.setWidgetResizable(True)
		self.vbox_main.addWidget(self.scroll_area)
		
		#create_flowbox
		self.create_flowbox()
		
		#autorun
		self.add_all_buttons()
############################################################################################

	def create_flowbox(self):
		"""Create flowbox"""
		self.flow_box = flowbox.Window()
		self.flow_box.flowLayout.setSpacing(10)
		self.scroll_area.setWidget(self.flow_box)
		pal = self.flow_box.palette()
		pal.setColor(QPalette.Window, QColor('white'))
		self.flow_box.setPalette(pal)
		
	def add_all_buttons(self):
		"""Create all buttons"""
		self.create_flowbox()
		paths.BASE_CURSOR.execute("SELECT * FROM Main")
		main_station_list = paths.BASE_CURSOR.fetchall()
		main_station_list.sort()
		list_id = [i[0] for i in main_station_list]
		sql = '?' * len(list_id)
		paths.BASE_CURSOR.execute("SELECT * FROM AllBase WHERE radio_id IN ({}) ORDER BY name".format(','.join(sql)), list_id)
		found_stations = paths.BASE_CURSOR.fetchall()
		for item in found_stations:
			radio_id = item[0]
			name = item[1]
			url = item[2]
			image = item[3]
			self.add_one_button(radio_id, name, url, image)
			
	def add_one_button(self, radio_id, name, url, icon):
		"""Add one button"""
		self.button = zbutton.MyButton()
		self.button.set_info(radio_id, name, url, icon)
		self.button.clicked.connect(self.press_button)
		self.button.customContextMenuRequested.connect(self.right_button_click)
		self.flow_box.flowLayout.addWidget(self.button)
		
	def right_button_click(self):
		"""Press right button"""
		self.CURRENT_BUTTON = self.sender()
		self.create_context_menu()
		
	def press_button(self):
		"""Press button"""
		name = self.sender().TITLE
		url = self.sender().URL
		self.parentWidget.player_play(name, url)
			
	def get_stations(self):
		"""Get all stations"""
		paths.BASE_CURSOR.execute("SELECT * FROM Main")
		main_station_list = paths.BASE_CURSOR.fetchall()
		main_station_list.sort()
		return main_station_list

	def create_context_menu(self):
		"""Create context menu"""
		self.menu = QMenu()
		self.menu.addAction(QIcon(':/info_icon.png'), self.tr("Info"), self.press_right_info)
		self.menu.addSeparator()
		self.menu.addAction(QIcon(":/remove_icon.png"),self.tr("Remove from Main"), self.press_remove_main)
		x = QCursor.pos().x()
		y = QCursor.pos().y()
		height = self.menu.height()
		height_menu = self.menu.sizeHint().height()
		self.menu.move(x, (y - height_menu))
		self.menu.show()

	def press_remove_main(self):
		"""Press remove main"""
		remove_params = [self.CURRENT_BUTTON.RADIO_ID,]
		paths.BASE_CURSOR.execute("DELETE FROM Main WHERE main_id=(?)", remove_params)
		paths.BASE_CONNECTION.commit()
		self.CURRENT_BUTTON.hide()
		self.flow_box.flowLayout.removeWidget(self.CURRENT_BUTTON)
		self.CURRENT_BUTTON = None

	def press_right_info(self):
		"""Press right info"""
		from . import info_win
		name = self.CURRENT_BUTTON.TITLE
		url  = self.CURRENT_BUTTON.URL
		self.new_info_win = info_win.Info_Win()
		self.new_info_win.set_info(name, url)
		self.new_info_win.show()
			
########################################################
