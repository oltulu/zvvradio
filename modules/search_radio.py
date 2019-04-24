"""Search radio module"""
import urllib
import urllib.request
import json
import html
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
							QComboBox, QLabel, QPushButton, 
							QTableWidget, QTableWidgetItem, QAbstractItemView,
							QHeaderView, QApplication, QLineEdit)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from . import add_station


class Search_radio(QWidget):
	"""Search radio class"""
	def __init__(self):
		super().__init__()
		self.create_widgets()

	def create_widgets(self):
		"""Create widgets"""
		self.BUTTON_SIZE = 30
		self.BUTTON_ICON_SIZE = self.BUTTON_SIZE - 5
		self.TEMPLATE_COUNTRY = "http://www.radio-browser.info/webservice/json/stations/bycountry/{0}"
	#vbox_main
		self.vbox_main = QVBoxLayout()
		self.vbox_main.setContentsMargins(1, 1, 1, 1)
		self.setLayout(self.vbox_main)

	#hbox_tools
		self.hbox_tools = QHBoxLayout()
		self.vbox_main.addLayout(self.hbox_tools)
		#button_add_fav
		self.button_add_fav = QPushButton()
		self.button_add_fav.setFocusPolicy(Qt.NoFocus)
		self.button_add_fav.setFixedSize(self.BUTTON_SIZE, self.BUTTON_SIZE)
		self.button_add_fav.setIconSize(QSize(self.BUTTON_ICON_SIZE, self.BUTTON_ICON_SIZE))
		self.button_add_fav.setIcon(QIcon(":/add_icon.png"))
		self.button_add_fav.setCursor(Qt.PointingHandCursor)
		self.button_add_fav.clicked.connect(self.press_add_fav_button)
		self.hbox_tools.addWidget(self.button_add_fav)
		#lineedit
		self.line_search = QLineEdit()
		self.line_search.setPlaceholderText(self.tr('Search'))
		self.line_search.setClearButtonEnabled(True)
		self.line_search.setFixedHeight(self.BUTTON_SIZE)
		self.line_search.returnPressed.connect(self.press_search)
		self.hbox_tools.addWidget(self.line_search)
		#combo_countries
		self.combo_countries = QComboBox()
		self.combo_countries.setMinimumHeight(self.BUTTON_SIZE)
		self.hbox_tools.addWidget(self.combo_countries)
		self.combo_countries.addItem("Country: ")
		list_lands = [
						("Russia", ":/Russia.png",),
						("Ukraine", ":/Ukraine.png",),
						("Belarus", ":/Belarus.png",),
						("France", ":/France.png",),
						("Poland", ":/Poland.png",),
					]
		list_lands.sort()
		for item in list_lands:
			self.combo_countries.addItem(QIcon(item[1]),item[0])
		self.combo_countries.activated.connect(self.change_combobox_country)

	#table_widget
		self.table_widget = QTableWidget(0, 1)
		self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.table_widget.setSelectionMode(QAbstractItemView.SingleSelection)
		self.table_widget.setShowGrid(True)
		self.table_widget.horizontalHeader().hide()
		self.table_widget.itemDoubleClicked.connect(self.press_table_double_item)
		self.vbox_main.addWidget(self.table_widget)
		self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

#######################################################################################

	def change_combobox_country(self, index):
		"""Change combobox country"""
		if index > 0:
			url = self.TEMPLATE_COUNTRY.format(self.combo_countries.currentText())
			self.parse_site(url)
		else:
			self.table_widget.setRowCount(0)

	def press_add_fav_button(self):
		"""Press add fav button"""
		current_item = self.table_widget.currentItem()
		if current_item:
			title = current_item.TITLE
			url = current_item.URL
			self.add_win = add_station.Add_Station()
			self.add_win.set_info(title, url)
			self.add_win.show()

	def press_search(self):
		"""Press search"""
		text = self.line_search.text()
		if text:
			quote_text = urllib.request.quote(text)
			url = "http://www.radio-browser.info/webservice/json/stations/byname/{0}".format(quote_text)
			self.parse_site(url)

	def parse_site(self, url):
		"""Parse site"""
		self.table_widget.setRowCount(0)
		req = urllib.request.urlopen(url)
		result = req.read()#.decode()
		ls = json.loads(result)
		for item in ls:
			name = item.get('name')
			url = item.get('url')
			self.add_one_row(name, url)

	def add_one_row(self, name, url):
		"""Add one row"""
		#name
		fileNameItem = MyItem()
		fileNameItem.setText(name)
		fileNameItem.TITLE = name
		fileNameItem.URL = url
		fileNameItem.setFlags(fileNameItem.flags() ^ Qt.ItemIsEditable)
		fileNameItem.setToolTip(url)
		#insert row
		row = self.table_widget.rowCount()
		self.table_widget.insertRow(row)
		self.table_widget.setItem(row, 0, fileNameItem)

	def press_table_double_item(self, tableItem):
		"""Press table double item"""
		title = tableItem.TITLE
		url = tableItem.URL
		self.parent().parent().parent().player_play(title, url)

##############################################################

class MyItem(QTableWidgetItem):
	"""MyItem class"""
	def __init__(self):
		super().__init__()
		self.TITLE = None
		self.URL = None

#############################################################
