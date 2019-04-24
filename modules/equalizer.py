"""Equalizer module"""
import os
import sys
import json
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
							 QLabel, QPushButton, QSlider, 
							 QComboBox, QLineEdit, QCheckBox,
							 QScrollArea)
from PyQt5.QtCore import Qt, QSettings
from . import vlc, paths, styles


class Equalizer(QWidget):
	"""Equalizer class"""
	def __init__(self):
		super().__init__()
		self.create_widgets()

	def create_widgets(self):
		self.PRESETS_PATH = os.path.join(paths.APP_FOLDER, "presets")
		if not os.path.exists(self.PRESETS_PATH):
			os.mkdir(self.PRESETS_PATH)
		self.settings = QSettings(paths.CONFIG_PATH, QSettings.IniFormat)
		
		#EQUALIZER
		self.eq = vlc.libvlc_audio_equalizer_new()
		
#vbox_main
		self.vbox_main = QVBoxLayout()
		self.vbox_main.setContentsMargins(1, 1, 1, 1)
		self.vbox_main.setSpacing(3)
		self.setLayout(self.vbox_main)

	#add hbox turn and presets
		self.hbox_presets = QHBoxLayout()
		self.vbox_main.addLayout(self.hbox_presets)
		#turn
		self.turn_eq = QCheckBox(self.tr("Equalizer"))
		#self.turn_eq.setCheckState(int(self.settings.value('main/eq')))
		self.turn_eq.stateChanged.connect(self.on_off_eq)
		self.hbox_presets.addWidget(self.turn_eq)
		#combo presets
		self.combo_presets = QComboBox()
		self.hbox_presets.addWidget(self.combo_presets)
		default_path_presets = os.path.join(os.getcwd(), "presets")
		list_presets = os.listdir(default_path_presets)
		list_presets.sort()
		self.combo_presets.addItem(self.tr("Choose:"))
		for item in list_presets:
			self.combo_presets.addItem(item)
		user_presets_list = os.listdir(self.PRESETS_PATH)
		user_presets_list.sort()
		for item in user_presets_list:
			self.combo_presets.addItem(item)
		#self.combo_presets.setCurrentIndex(int(self.settings.value('main/preset')))
		self.combo_presets.activated.connect(self.choose_preset)

		#GET_EQ_BAND
		#band_count = vlc.libvlc_audio_equalizer_get_band_count()

	#add scroll slider
		self.scroll_sliders = QScrollArea()
		self.scroll_sliders.setWidgetResizable(True)
		self.vbox_main.addWidget(self.scroll_sliders)
		#add sliders vbox
		self.widget_sliders = QWidget()
		self.scroll_sliders.setWidget(self.widget_sliders)
		self.vbox_sliders = QVBoxLayout()
		self.widget_sliders.setLayout(self.vbox_sliders)
		
	#add sliders
		self.slider_preamp = QSlider(Qt.Horizontal)
		self.slider1 = QSlider(Qt.Horizontal)
		self.slider2 = QSlider(Qt.Horizontal)
		self.slider3 = QSlider(Qt.Horizontal)
		self.slider4 = QSlider(Qt.Horizontal)
		self.slider5 = QSlider(Qt.Horizontal)
		self.slider6 = QSlider(Qt.Horizontal)
		self.slider7 = QSlider(Qt.Horizontal)
		self.slider8 = QSlider(Qt.Horizontal)
		self.slider9 = QSlider(Qt.Horizontal)
		self.slider10 = QSlider(Qt.Horizontal)
		#list_sliders
		self.list_sliders = [
								self.slider_preamp, self.slider1, self.slider2,
								self.slider3, self.slider4, self.slider5,
								self.slider6, self.slider7, self.slider8,
								self.slider9, self.slider10,
							]
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
			self.slider = self.list_sliders[index]
			self.slider.setStyleSheet(styles.get_slider_style())
			self.slider.setRange(-20, 20)
			self.slider.valueChanged.connect(self.change_slider_num)
			self.hbox.addWidget(self.slider)
			self.label_value = QLabel()
			self.hbox.addWidget(self.label_value)

		#add buttons
		self.hbox_save_reset = QHBoxLayout()
		self.vbox_main.addLayout(self.hbox_save_reset)

		self.button_accept = QPushButton(self.tr("Accept"))
		self.button_accept.setStyleSheet(styles.get_button_style())
		self.button_accept.setCursor(Qt.PointingHandCursor)
		self.button_accept.clicked.connect(self.press_accept)
		self.hbox_save_reset.addWidget(self.button_accept)

		self.button_save = QPushButton(self.tr("Save"))
		self.button_save.setStyleSheet(styles.get_button_style())
		self.button_save.setCursor(Qt.PointingHandCursor)
		self.button_save.clicked.connect(self.save_new_preset)
		self.hbox_save_reset.addWidget(self.button_save)

		self.button_reset = QPushButton(self.tr("Reset"))
		self.button_reset.setStyleSheet(styles.get_button_style())
		self.button_reset.setCursor(Qt.PointingHandCursor)
		self.button_reset.clicked.connect(self.press_reset)
		self.hbox_save_reset.addWidget(self.button_reset)


		#add hbox for add presets
		self.save_preset_widget = QWidget()
		self.save_preset_widget.hide()
		self.vbox_main.addWidget(self.save_preset_widget)
		self.save_preset_box = QHBoxLayout()
		self.save_preset_widget.setLayout(self.save_preset_box)
		#line edit
		self.save_preset_line = QLineEdit()
		self.save_preset_line.setPlaceholderText(self.tr("Enter name of preset"))
		self.save_preset_box.addWidget(self.save_preset_line)

		#add button ok
		self.ok_preset = QPushButton("OK")
		self.ok_preset.setMaximumWidth(50)
		self.ok_preset.clicked.connect(self.press_save_new_preset)
		self.save_preset_box.addWidget(self.ok_preset)
		#add button cancel
		self.cancel_preset = QPushButton(self.tr("Cancel"))
		self.cancel_preset.setMaximumWidth(60)
		self.cancel_preset.clicked.connect(self.cancel_save_new_preset)
		self.save_preset_box.addWidget(self.cancel_preset)

##############################################################################

	def press_save_new_preset(self):
		name_preset = self.save_preset_line.text()
		if name_preset:
			path_presets = os.path.join(paths.APP_PATH, "presets")
			name_preset = "*" + name_preset + '.json'
			full_path_preset = os.path.join(path_presets, name_preset)
			#get values
			list_nums = []
			for slider in self.list_sliders:
				list_nums.append(slider.value())
			#save
			with open(full_path_preset, 'w') as file_save:
				json.dump(list_nums, file_save)
			self.save_preset_widget.hide()
			self.combo_presets.addItem(name_preset)
			
	def cancel_save_new_preset(self):
		"""Hide save widget"""
		self.save_preset_widget.hide()

	def save_new_preset(self):
		"""Show/hide save widget then save button pressed"""
		if self.save_preset_widget.isVisible():
			self.save_preset_widget.hide()
		else:
			self.save_preset_widget.show()

	def choose_preset(self):
		"""Choose preset"""
		if self.combo_presets.currentIndex() > 0:
			presets_path = os.path.join(os.getcwd(), "presets")
			current_text = self.combo_presets.currentText()
			if current_text[0] == "*":
				presets_path = self.PRESETS_PATH
			get_preset_path = os.path.join(presets_path, current_text)
			if os.path.exists(get_preset_path):
				with open(get_preset_path, 'r', encoding='utf-8') as file_load:
					list_nums = json.load(file_load)
					for slider in self.list_sliders:
						index = self.list_sliders.index(slider)
						value = list_nums[index]
						slider.setValue(value)
						if index == 0:
							vlc.libvlc_audio_equalizer_set_preamp(self.eq, value)
							self.vbox_sliders.itemAt(index).itemAt(2).widget().setText(str(value))
						else:
							if index > 0:
								vlc.libvlc_audio_equalizer_set_amp_at_index(self.eq, value, index-1)
								self.vbox_sliders.itemAt(index).itemAt(2).widget().setText(str(value))
			if self.turn_eq.isChecked():
				self.press_accept()
		else:
			self.press_reset()

	def on_off_eq(self):
		"""On/Off equalizer"""
		if self.turn_eq.isChecked():
			self.combo_presets.setEnabled(True)
			self.button_accept.setEnabled(True)
			self.button_save.setEnabled(True)
			self.button_reset.setEnabled(True)
			for slider in self.list_sliders:
				slider.setEnabled(True)
			self.settings.setValue('main/eq',2)

		else:
			self.combo_presets.setEnabled(False)
			self.button_accept.setEnabled(False)
			self.button_save.setEnabled(False)
			self.button_reset.setEnabled(False)
			for slider in self.list_sliders:
				slider.setEnabled(False)
			self.settings.setValue('main/eq',0)
		self.check_equalizer()
		self.settings.sync()

	def check_equalizer(self):
		"""Check equalizer"""
		if self.turn_eq.isChecked():
			self.parent().parent().parent().PLAYER.set_equalizer(self.eq)
		else:
			self.parent().parent().parent().PLAYER.set_equalizer(None)

	def press_reset(self):
		band_count = vlc.libvlc_audio_equalizer_get_band_count()
		for i in range(band_count):
			vlc.libvlc_audio_equalizer_set_amp_at_index(self.eq, 0.0, i)
		for item in self.list_sliders:
			item.setValue(0)
		vlc.libvlc_media_player_set_equalizer(self.parent().parent().parent().PLAYER, self.eq)
		self.combo_presets.setCurrentIndex(0)
		
	def change_slider_num(self):
		"""Change slider num"""
		slider = self.sender()
		value = slider.value()
		index = self.list_sliders.index(slider)
		if index == 0:
			vlc.libvlc_audio_equalizer_set_preamp(self.eq, value)
		else:
			vlc.libvlc_audio_equalizer_set_amp_at_index(self.eq, value, index-1)
		self.vbox_sliders.itemAt(index).itemAt(2).widget().setText(str(value))

	def press_accept(self):
		"""Press accept"""
		self.parent().parent().parent().PLAYER.set_equalizer(self.eq)

############################################################################################
