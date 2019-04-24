"""Edit Win module"""
import os
import sys
from PyQt5.QtWidgets import (QDialog, QWidget, QVBoxLayout, 
							QHBoxLayout, QLabel, QPushButton, 
							QLineEdit, QFormLayout, QFileDialog)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize, QDir
from . import paths, styles


class Edit(QDialog):
	"""Edit win class"""
	def __init__(self, parentButton):
		super().__init__()
		self.parentButton = parentButton
		self.create_edit_widgets()

	def create_edit_widgets(self):
		"""Create edit widgets"""
		self.FILE_ICON = ''
		self.OLD_URL = None
	#vbox_main
		self.vbox_edit = QVBoxLayout()
		self.setLayout(self.vbox_edit)
		
		#add main label
		label_font = QFont()
		label_font.setPointSize(14)
		label_font.setBold(True)
		self.label_main = QLabel()
		self.label_main.setFont(label_font)
		self.label_main.setAlignment(Qt.AlignCenter)
		self.vbox_edit.addWidget(self.label_main)

	#add hbox_stream_station
		self.form_layout = QFormLayout()
		self.vbox_edit.addLayout(self.form_layout)
		#add entry
		self.entry_stream = QLineEdit()
		self.entry_stream.setEnabled(False)
		#button_icon
		self.button_icon = QPushButton()
		self.button_icon.setEnabled(False)
		self.button_icon.setCursor(Qt.PointingHandCursor)
		self.button_icon.setFixedSize(32, 32)
		self.button_icon.setIconSize(QSize(28, 28))
		self.button_icon.setFocusPolicy(Qt.NoFocus)
		self.button_icon.clicked.connect(self.press_button_add_icon)
		self.button_icon.setIcon(QIcon(self.parentButton.icon()))
		#add row
		self.form_layout.addRow(self.tr("Change stream url:"), self.entry_stream)
		self.form_layout.addRow(self.tr("Change icon:"), self.button_icon)

	#add stretch
		self.vbox_edit.addStretch()

	#add hbox button unlock and save
		self.hbox_unlock_save = QHBoxLayout()
		self.vbox_edit.addLayout(self.hbox_unlock_save)
		#add button unlock
		self.button_unlock = QPushButton(self.tr("Unlock"))
		self.button_unlock.setEnabled(True)
		self.button_unlock.setCursor(Qt.PointingHandCursor)
		self.button_unlock.setStyleSheet(styles.get_button_style())
		self.button_unlock.setMinimumHeight(30)
		self.button_unlock.clicked.connect(self.press_unlock_button)
		self.hbox_unlock_save.addWidget(self.button_unlock)
		#add button save
		self.button_save = QPushButton(self.tr("Update"))
		self.button_save.setEnabled(False)
		self.button_save.setCursor(Qt.PointingHandCursor)
		self.button_save.setStyleSheet(styles.get_button_style())
		self.button_save.setMinimumHeight(30)
		self.button_save.clicked.connect(self.press_save_button)
		self.hbox_unlock_save.addWidget(self.button_save)

		###
		self.setAttribute(Qt.WA_DeleteOnClose, True)
		self.setWindowTitle(self.tr("Edit station"))
		self.setModal(True)
		self.setFixedSize(500, 300)
		self.show()

###########################################################################

	def press_unlock_button(self):
		self.entry_stream.setEnabled(True)
		self.button_icon.setEnabled(True)
		self.button_save.setEnabled(True)

	def press_save_button(self):
		"""Press save button"""
		new_url = self.entry_stream.text()
		if new_url or self.FILE_ICON:
			radio_id = self.parentButton.RADIO_ID
			if self.FILE_ICON:
				with open(self.FILE_ICON, "rb") as get_image:
					f = get_image.read()
					icon = bytearray(f)
				update_params = [icon, radio_id]
				paths.BASE_CURSOR.execute("UPDATE AllBase SET image=? WHERE radio_id=?", update_params)
				self.parentButton.set_icon(icon)
			if new_url != self.OLD_URL:
				if new_url:
					update_params = [new_url, radio_id]
					paths.BASE_CURSOR.execute("UPDATE AllBase SET url=? WHERE radio_id=?", update_params)
			paths.BASE_CONNECTION.commit()
			self.parentButton.URL = new_url
			self.close()

	def set_info(self, name, url):
		"""Set info"""
		self.label_main.setText(name)
		self.OLD_URL = url
		self.entry_stream.setText(url)
		
	def press_button_add_icon(self):
		"""Press add icon"""
		fileName = QFileDialog.getOpenFileName(self, self.tr('Choose icon'), QDir.homePath(), ("Image Files (*.png *.jpg *.bmp)"))
		if fileName[0]:
			self.FILE_ICON = fileName[0]
			if os.path.exists(self.FILE_ICON):
				self.button_icon.setIcon(QIcon(self.FILE_ICON))
