"""Mini tab module"""
import os
from PyQt5.QtWidgets import (QDialog, QWidget, QVBoxLayout, 
							QHBoxLayout, QLabel, QPushButton, 
							QScrollArea, QDesktopWidget)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QCoreApplication, QSize
from . import paths, flowbox, styles, zbutton


class Mini_tab(QWidget):
	"""Mini tab class"""
	def __init__(self, player_widget):
		super().__init__()
		self.player_widget = player_widget
		self.create_widgets()

	def create_widgets(self):
		"""Create widgets"""
	#vbox_main
		self.vbox_main = QVBoxLayout()
		self.vbox_main.setContentsMargins(0, 0, 0, 0)
		self.setLayout(self.vbox_main)

	#scroll_area
		self.scroll_area = QScrollArea()
		self.scroll_area.setWidgetResizable(True)
		self.scroll_area.setViewportMargins(5, 5, 5, 5)
		self.scroll_area.setStyleSheet("QScrollArea{border: 2px solid #80a9ed;}")
		self.vbox_main.addWidget(self.scroll_area)
		
	#create flowbox
		self.create_flowbox()
		#self.add_all_buttons()
		
		###
		self.resize(400, 400)
		self.setWindowTitle(self.tr("Favorites"))
		self.setAttribute(Qt.WA_DeleteOnClose, True)
		self.setWindowFlags(Qt.Popup | Qt.WindowStaysOnTopHint)
		self.show()
		
		#autorun
		self.center()
		
#################################################

	def center(self):
		# geometry of the main window
		qr = self.frameGeometry()
		# center point of screen
		cp = QDesktopWidget().availableGeometry().center()
		# move rectangle's center point to screen's center point
		qr.moveCenter(cp)
		# top left of rectangle becomes top left of window centering it
		self.move(qr.topLeft())
		
	def create_flowbox(self):
		"""Create flowbox"""
		self.flow_box = flowbox.Window()
		self.scroll_area.setWidget(self.flow_box)
		
	def add_all_buttons(self):
		"""Create all buttons"""
		self.create_flowbox()
		paths.BASE_CURSOR.execute("SELECT * FROM Main")
		main_station_list = paths.BASE_CURSOR.fetchall()
		main_station_list.sort()
		list_id = [i[0] for i in main_station_list]
		sql = '?' * len(list_id)
		paths.BASE_CURSOR.execute("SELECT * FROM AllBase WHERE radio_id IN ({})".format(','.join(sql)), list_id)
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
		self.flow_box.flowLayout.addWidget(self.button)
		
	def press_button(self):
		"""Press button"""
		title = self.sender().TITLE
		url = self.sender().URL
		self.player_widget.player_play(title, url)
		self.hide()
		
