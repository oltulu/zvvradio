"""Equalizer module"""
import os
import sys
import json
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
							 QLabel, QPushButton, QSlider, 
							 QComboBox, QLineEdit, QCheckBox,
							 QScrollArea, QMenu)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSettings, QSize
from . import vlc, paths, styles


class Equalizer(QWidget):
	"""Equalizer class"""
	def __init__(self, parentWidget):
		super().__init__()
		self.parentWidget = parentWidget
		self.create_widgets()

	def create_widgets(self):
		"""Create widgets"""
		self.USER_PRESETS_PATH = os.path.join(paths.APP_FOLDER, "presets")
		if not os.path.exists(self.USER_PRESETS_PATH):
			os.mkdir(self.USER_PRESETS_PATH)
		self.settings = QSettings(paths.CONFIG_PATH, QSettings.IniFormat)
		
		#EQUALIZER
		self.eq = vlc.AudioEqualizer()
		
#vbox_main
		self.vbox_main = QVBoxLayout()
		self.vbox_main.setContentsMargins(1, 1, 1, 1)
		self.vbox_main.setSpacing(3)
		self.setLayout(self.vbox_main)

	#add hbox turn and presets
		self.hbox_presets = QHBoxLayout()
		self.vbox_main.addLayout(self.hbox_presets)
		#turn
		self.turn_eq = QCheckBox(self.tr("Eq on/off"))
		self.turn_eq.stateChanged.connect(self.on_off_eq)
		self.hbox_presets.addWidget(self.turn_eq)
		#combo presets
		self.combo_presets = QComboBox()
		self.combo_presets.setFixedHeight(32)
		self.hbox_presets.addWidget(self.combo_presets)
		default_path_presets = os.path.join(os.getcwd(), "presets")
		list_presets = os.listdir(default_path_presets)
		list_presets.sort()
		self.combo_presets.addItem(self.tr("Choose:"))
		for item in list_presets:
			self.combo_presets.addItem(item)
		user_presets_list = os.listdir(self.USER_PRESETS_PATH)
		user_presets_list.sort()
		for item in user_presets_list:
			self.combo_presets.addItem(item)
		self.combo_presets.activated.connect(self.choose_preset)
		#button_menu
		self.button_menu = QPushButton()
		self.button_menu.setFixedSize(32, 32)
		self.button_menu.setIconSize(QSize(28, 28))
		self.button_menu.setIcon(QIcon(':/more_icon.png'))
		self.button_menu.setStyleSheet(styles.get_button_style())
		self.button_menu.setCursor(Qt.PointingHandCursor)
		self.hbox_presets.addWidget(self.button_menu)
		self.menu_tools = QMenu()
		self.menu_tools.addAction(QIcon(':/accept_icon.png'), self.tr("Accept"), self.press_accept)
		self.menu_tools.addAction(QIcon(':/save_icon.png'), self.tr("Save"), self.open_widget_save)
		self.menu_tools.addAction(QIcon(':/reset_icon.png'), self.tr("Reset"), self.press_reset)
		self.button_menu.setMenu(self.menu_tools)
		
	#widget_preset_save
		self.widget_preset_save = Widget_save(self)
		self.widget_preset_save.hide()
		self.vbox_main.addWidget(self.widget_preset_save)

	#add scroll slider
		self.scroll_sliders = QScrollArea()
		self.scroll_sliders.setWidgetResizable(True)
		self.vbox_main.addWidget(self.scroll_sliders)
		#add sliders vbox
		self.widget_sliders = QWidget()
		self.scroll_sliders.setWidget(self.widget_sliders)
		self.vbox_sliders = QVBoxLayout()
		self.widget_sliders.setLayout(self.vbox_sliders)
		
		#list_sliders
		self.list_sliders = []
		
		#list_sliders_names
		self.list_slider_names = [
								"Preamp:", "31 Hz:", "62 Hz:",
								"125 Hz:", "250 Hz:", "500 Hz:",
								"1 KHz:", "2 KHz", "4 KHz:",
								"8 KHz:", "16 KHz:",
							]
		for item in self.list_slider_names:
			index = self.list_slider_names.index(item)
			self.hbox = QHBoxLayout()
			self.vbox_sliders.addLayout(self.hbox)
			self.label_name = QLabel(item + '\t')
			self.hbox.addWidget(self.label_name)
			self.slider = Slider_band()
			self.list_sliders.append(self.slider)
			self.slider.BAND_NUM = index
			self.slider.valueChanged.connect(self.change_slider_num)
			self.hbox.addWidget(self.slider)
			self.label_value = QLabel()
			self.hbox.addWidget(self.label_value)
			
		#AUTORUN
		self.check_sliders()
##############################################################################

	def press_save_new_preset(self):
		"""Press save new preset"""
		name_preset = self.widget_preset_save.line_preset_name.text()
		if name_preset:
			name_preset = "*" + name_preset + '.json'
			full_path_preset = os.path.join(self.USER_PRESETS_PATH, name_preset)
			#get values
			list_nums = []
			for slider in self.list_sliders:
				list_nums.append(slider.value())
			#save
			with open(full_path_preset, 'w', encoding='utf-8') as file_save:
				json.dump(list_nums, file_save)
			self.widget_preset_save.hide()
			self.combo_presets.addItem(name_preset)

	def open_widget_save(self):
		"""Show/hide save widget then save button pressed"""
		if self.widget_preset_save.isVisible():
			self.widget_preset_save.hide()
		else:
			self.widget_preset_save.show()

	def choose_preset(self):
		"""Choose preset"""
		if self.combo_presets.currentIndex() > 0:
			presets_path = os.path.join(os.getcwd(), "presets")
			current_text = self.combo_presets.currentText()
			if current_text[0] == "*":
				presets_path = self.USER_PRESETS_PATH
			get_preset_path = os.path.join(presets_path, current_text)
			if os.path.exists(get_preset_path):
				with open(get_preset_path, 'r', encoding='utf-8') as file_load:
					list_nums = json.load(file_load)
					for slider in self.list_sliders:
						index = self.list_sliders.index(slider)
						value = list_nums[index]
						slider.setValue(value)
						if index == 0:
							self.eq.set_preamp(value)
							self.vbox_sliders.itemAt(index).itemAt(2).widget().setText(str(value))
						else:
							if index > 0:
								self.eq.set_amp_at_index(value, index-1)
								self.vbox_sliders.itemAt(index).itemAt(2).widget().setText(str(value))
			self.press_accept()
		else:
			self.press_reset()

	def on_off_eq(self):
		"""On/Off equalizer"""
		self.check_sliders()
		self.check_equalizer()
		
	def check_sliders(self):
		"""Check sliders"""
		if self.turn_eq.isChecked():
			self.combo_presets.setEnabled(True)
			for slider in self.list_sliders:
				slider.setEnabled(True)
		else:
			self.combo_presets.setEnabled(False)
			for slider in self.list_sliders:
				slider.setEnabled(False)

	def check_equalizer(self):
		"""Check equalizer"""
		if self.turn_eq.isChecked():
			self.press_accept()
		else:
			self.parentWidget.PLAYER.set_equalizer(None)

	def press_reset(self):
		band_count = vlc.libvlc_audio_equalizer_get_band_count()
		for i in range(band_count):
			self.eq.set_amp_at_index(0.0, i)
		for item in self.list_sliders:
			item.setValue(0)
		self.combo_presets.setCurrentIndex(0)
		
	def change_slider_num(self):
		"""Change slider num"""
		if self.turn_eq.isChecked():
			slider = self.sender()
			value = slider.value()
			index = slider.BAND_NUM
			if index == 0:
				self.eq.set_preamp(value)
			else:
				self.eq.set_amp_at_index(value, index-1)
			self.press_accept()
			self.vbox_sliders.itemAt(index).itemAt(2).widget().setText(str(value))

	def press_accept(self):
		"""Press accept"""
		if self.turn_eq.isChecked():
			self.parentWidget.PLAYER.set_equalizer(self.eq)

############################################################################################

class Slider_band(QSlider):
	"""Slider band"""
	def __init__(self):
		super().__init__()
		self.setOrientation(Qt.Horizontal)
		self.setStyleSheet(styles.get_slider_style())
		self.setRange(-20, 20)
		self.BAND_NUM = 0
		
#############################################################################################

class Widget_save(QWidget):
	"""Widget save"""
	def __init__(self, parentWidget):
		super().__init__()
		self.parentWidget = parentWidget
		self.create_widgets()
	
	def create_widgets(self):
		"""Create widgets"""
		self.hbox_main = QHBoxLayout()
		self.setLayout(self.hbox_main)
		#line edit
		self.line_preset_name = QLineEdit()
		self.line_preset_name.setFixedHeight(30)
		self.line_preset_name.setPlaceholderText(self.tr("Enter name of preset"))
		self.hbox_main.addWidget(self.line_preset_name)
		#button_preset_save
		self.button_preset_save = QPushButton()
		self.button_preset_save.setFixedSize(30, 30)
		self.button_preset_save.setIconSize(QSize(25, 25))
		self.button_preset_save.setIcon(QIcon(':/check_icon.png'))
		self.button_preset_save.setCursor(Qt.PointingHandCursor)
		self.button_preset_save.setFocusPolicy(Qt.NoFocus)
		self.button_preset_save.setStyleSheet(styles.get_button_style())
		self.button_preset_save.clicked.connect(self.press_button_save)
		self.hbox_main.addWidget(self.button_preset_save)
		#button_preset_cancel
		self.button_preset_cancel = QPushButton()
		self.button_preset_cancel.setFixedSize(30, 30)
		self.button_preset_cancel.setIconSize(QSize(25, 25))
		self.button_preset_cancel.setIcon(QIcon(':/remove_icon.png'))
		self.button_preset_cancel.setCursor(Qt.PointingHandCursor)
		self.button_preset_cancel.setFocusPolicy(Qt.NoFocus)
		self.button_preset_cancel.setStyleSheet(styles.get_button_style())
		self.button_preset_cancel.clicked.connect(self.press_button_cancel)
		self.hbox_main.addWidget(self.button_preset_cancel)
		
	def press_button_save(self):
		"""Press button save"""
		self.parentWidget.press_save_new_preset()
		
	def press_button_cancel(self):
		"""Press button cancel"""
		self.line_preset_name.clear()
		self.hide()
