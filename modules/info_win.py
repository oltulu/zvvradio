"""Info win module"""
from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout, QLabel, QFormLayout, QSizePolicy, QTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class Info_Win(QDialog):
	"""Info win class"""
	def __init__(self):
		super().__init__()
		self.create_widgets()

	def create_widgets(self):
		"""Create widgets"""
		#add vbox main
		self.vbox_main = QVBoxLayout()
		self.vbox_main.setSpacing(20)
		self.setLayout(self.vbox_main)

		#form_layout
		self.form_layout = QFormLayout()
		#self.form_layout.setRowWrapPolicy(QFormLayout.WrapLongRows)
		self.vbox_main.addLayout(self.form_layout)

		#add labels
		self.label_name = QLabel()
		self.label_name.setStyleSheet('QLabel{font-weight:bold;}')

		#label_url
		self.label_url = QTextEdit()
		self.label_url.setReadOnly(True)
		self.label_url.setTextInteractionFlags(Qt.TextSelectableByMouse)
		self.label_url.setStyleSheet('QTextEdit{font-size:12px;}')

		#add rows
		self.form_layout.addRow(self.tr('Name:'), self.label_name)
		self.form_layout.addRow(self.tr('Url:'), self.label_url)

		#set main window
		self.setAttribute(Qt.WA_DeleteOnClose, True)
		self.setFixedSize(450, 200)
		self.setModal(True)
		self.setWindowTitle(self.tr("Info"))

###########################################################################

	def set_info(self, name, url):
		"""Set info"""
		self.label_name.setText(name)
		self.label_url.setText(url)
