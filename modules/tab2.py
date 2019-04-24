"""Tab 2 - Countries module"""
import os
import re
from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, 
							 QVBoxLayout, QHBoxLayout, QMenu, 
							 QScrollArea, QLineEdit, QComboBox)
from PyQt5.QtGui import QIcon, QCursor, QPixmap, QPalette, QColor
from PyQt5.QtCore import Qt, QCoreApplication, QSettings, QSize
from . import flowbox, paths, styles, zbutton


class Tab2_stations(QWidget):
	"""Tab 2 class"""
	def __init__(self, parentWidget):
		super().__init__()
		self.parentWidget = parentWidget
		self.create_tab2()

	def create_tab2(self):
		"""Create tab2 widgets"""
		self.CURRENT_LAND = None
		self.CURRENT_BUTTON = None
		self.settings = QSettings(paths.CONFIG_PATH, QSettings.IniFormat)
	#vbox_main
		self.vbox_main = QVBoxLayout()
		self.vbox_main.setContentsMargins(0, 0, 0, 0)
		self.setLayout(self.vbox_main)
		
	#hbox_search
		self.hbox_search = QHBoxLayout()
		self.vbox_main.addLayout(self.hbox_search)
		#label_current_country
		self.label_current_country = QLabel()
		self.label_current_country.setScaledContents(True)
		self.label_current_country.setFixedSize(30, 30)
		self.label_current_country.setStyleSheet(styles.get_countries_label_style())
		self.hbox_search.addWidget(self.label_current_country)
		#line_search
		self.line_search = QLineEdit()
		self.line_search.setPlaceholderText(self.tr('Search + press Enter'))
		self.line_search.setClearButtonEnabled(True)
		self.line_search.setFixedHeight(30)
		self.line_search.setStyleSheet(styles.get_lineedit_style())
		self.line_search.returnPressed.connect(self.press_search)
		self.hbox_search.addWidget(self.line_search)
		#combobox_genres
		self.combobox_genres = QComboBox()
		self.combobox_genres.setFocusPolicy(Qt.NoFocus)
		self.combobox_genres.addItem(self.tr('Genres:'))
		self.all_genres = ['Pop','Relax','Retro','Child','Shanson',
						'Love', 'Rock', 'Humor', 'Classic', 'Rap','Jazz', 'Metal', 'Films',
						'Club','Ballads','Blues','Groove','Grunge','Hip-Hop',
						'Pank','Reggae','Dj','News','Religion','Sport',
						'Other',]
		self.all_genres.sort()
		for item in self.all_genres:
			self.combobox_genres.addItem(item)
		self.combobox_genres.activated.connect(self.press_choose_genre)
		self.hbox_search.addWidget(self.combobox_genres)

	#add scroll area
		self.scrollarea = QScrollArea()
		self.scrollarea.setStyleSheet(styles.get_scrollarea_style() + styles.get_scrollbar_style())
		self.scrollarea.setWidgetResizable(True)
		self.vbox_main.addWidget(self.scrollarea)
		
		#create countries
		self.set_default_icon()
		self.create_countries()
		
###############################################################################

	def set_default_icon(self):
		"""Set default icon"""
		self.set_current_icon(':/url_icon.png')

	def set_current_icon(self, icon):
		"""Set current icon"""
		self.label_current_country.setPixmap(QPixmap(icon))

	def create_flowbox(self):
		"""Create flowbox"""
		self.flowbox = flowbox.Window()
		self.flowbox.flowLayout.setSpacing(10)
		self.scrollarea.setWidget(self.flowbox)
		pal = self.flowbox.palette()
		pal.setColor(QPalette.Window, QColor('white'))
		self.flowbox.setPalette(pal)

	def create_countries(self):
		"""Create countries"""
		self.create_flowbox()
		paths.BASE_CURSOR.execute("SELECT * FROM Lands")
		list_countries = paths.BASE_CURSOR.fetchall()
		list_countries.sort()
		for country in list_countries:
			country = country[0]
			self.button_country = Button_land()
			self.button_country.set_info(country)
			self.button_country.clicked.connect(self.choose_country)
			self.flowbox.flowLayout.addWidget(self.button_country)

	def choose_country(self):
		"""Choose country"""
		land_name = self.sender().TITLE
		self.CURRENT_LAND = land_name
		search_params = [land_name]
		paths.BASE_CURSOR.execute("SELECT * FROM AllBase WHERE land=(?) ORDER BY name", search_params)
		found_stations_list = paths.BASE_CURSOR.fetchall()
		self.create_flowbox()
		for station in found_stations_list:
			if found_stations_list.index(station) > 30:
				QCoreApplication.processEvents()
			radio_id, name, url, icon = station[0], station[1], station[2], station[3]
			self.create_button(radio_id, name, url, icon)
		self.set_current_icon(':/{0}.png'.format(land_name.title()))
		
	def create_button(self, radio_id, name, url, icon):
		"""Create button"""
		self.button = zbutton.MyButton()
		self.button.set_info(radio_id, name, url, icon)
		self.button.clicked.connect(self.open_station)
		self.button.customContextMenuRequested.connect(self.right_button_click)
		self.flowbox.flowLayout.addWidget(self.button)

	def right_button_click(self):
		"""Right button click"""
		self.CURRENT_BUTTON = self.sender()
		self.menu = QMenu()
		self.menu.addAction(QIcon(':/fav_icon.png'), self.tr("Add to Main"), self.press_add_main)
		self.menu.addAction(QIcon(':/info_icon.png'), self.tr("Info"), self.press_right_info)
		self.menu.addAction(QIcon(':/edit_icon.png'), self.tr("Edit"), self.press_right_edit)
		self.menu.addSeparator()
		self.menu.addAction(QIcon(':/remove_icon.png'), self.tr("Remove fully"), self.press_remove_fully)
		x = QCursor.pos().x()
		y = QCursor.pos().y()
		height = self.menu.height()
		height_menu = self.menu.sizeHint().height()
		self.menu.move(x, (y - height_menu))
		self.menu.show()
		
	def press_right_info(self):
		"""Right button info"""
		from . import info_win
		self.new_info_win = info_win.Info_Win()
		self.new_info_win.set_info(self.CURRENT_BUTTON.TITLE, self.CURRENT_BUTTON.URL)
		self.new_info_win.show()

	def press_right_edit(self):
		"""Right button edit"""
		from . import edit_window
		self.new_edit_win = edit_window.Edit(self.CURRENT_BUTTON)
		self.new_edit_win.set_info(self.CURRENT_BUTTON.TITLE, self.CURRENT_BUTTON.URL)

	def press_add_main(self):
		"""Press add to FAV"""
		search_params = [self.CURRENT_BUTTON.RADIO_ID]
		paths.BASE_CURSOR.execute("SELECT * FROM AllBase WHERE radio_id=(?)", search_params)
		found_station = paths.BASE_CURSOR.fetchone()
		paths.BASE_CURSOR.execute("SELECT * FROM Main")
		list_main = paths.BASE_CURSOR.fetchall()
		if found_station not in list_main:
			paths.BASE_CURSOR.execute("INSERT INTO Main VALUES(?)", search_params)
			paths.BASE_CONNECTION.commit()
			radio_id = search_params[0]
			name = found_station[1]
			url = found_station[2]
			icon = found_station[3]
			self.parentWidget.tab1.add_one_button(radio_id, name, url, icon)
			self.parentWidget.tab1.flow_box.flowLayout.update()

	def press_back(self):
		"""Press back"""
		self.create_countries()
		self.set_default_icon()
		self.CURRENT_LAND = None

	def open_station(self):
		"""Open station"""
		self.button = self.sender()
		name = self.button.TITLE
		url = self.button.URL
		self.parentWidget.player_play(name, url)

	def press_remove_fully(self):
		"""Press remove fully"""
		radio_id = self.CURRENT_BUTTON.RADIO_ID
		remove_params = [radio_id,]
		paths.BASE_CURSOR.execute("DELETE FROM AllBase WHERE radio_id=(?)", remove_params)
		paths.BASE_CONNECTION.commit()
		self.CURRENT_BUTTON.hide()
		self.flowbox.flowLayout.removeWidget(self.CURRENT_BUTTON)
		self.CURRENT_BUTTON = None
		
	def press_search(self):
		"""Press search"""
		text = self.line_search.text().strip()
		if text:
			text = ("%" + text + "%")
			if self.CURRENT_LAND:
				search_params = [text, self.CURRENT_LAND]
				paths.BASE_CURSOR.execute("SELECT * FROM AllBase WHERE name LIKE ? AND land=?", search_params)
			else:
				search_params = [text]
				paths.BASE_CURSOR.execute("SELECT * FROM AllBase WHERE name LIKE ?", search_params)
			found_stations = paths.BASE_CURSOR.fetchall()
			found_stations.sort()
			self.create_flowbox()
			for item in found_stations:
				if found_stations.index(item) > 30:
					QCoreApplication.processEvents()
				self.button = zbutton.MyButton()
				radio_id, name, url, icon = item[0], item[1], item[2], item[3]
				self.create_button(radio_id, name, url, icon)
		else:
			self.press_back()

	def press_choose_genre(self, index):
		"""Choose genre"""
		if index > 0:
			self.create_flowbox()
			genre = self.combobox_genres.currentText()
			if self.CURRENT_LAND:
				search_params = [genre, self.CURRENT_LAND]
				paths.BASE_CURSOR.execute("SELECT * FROM AllBase WHERE genre=(?) and land=?", search_params)
			else:
				search_params = [genre]
				paths.BASE_CURSOR.execute("SELECT * FROM AllBase WHERE genre=(?)", search_params)
			found_genre_stations_list = paths.BASE_CURSOR.fetchall()
			for item in found_genre_stations_list:
				if found_genre_stations_list.index(item) > 30:
					QCoreApplication.processEvents()
				radio_id, name, url, icon = item[0], item[1], item[2], item[3]
				self.create_button(radio_id, name, url, icon)
		else:
			self.press_back()

########################################################################

class Button_land(zbutton.MyButton):
	"""Button land class"""
	def __init__(self):
		super().__init__()
		self.setContextMenuPolicy(Qt.NoContextMenu)
		
	def set_info(self, country):
		"""Set info"""
		icon = ':/{0}.png'.format(country.title())
		self.TITLE = country
		self.setIcon(QIcon(icon))
