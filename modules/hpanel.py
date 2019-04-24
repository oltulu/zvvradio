"""HPanel module"""
import os
import sys
from PyQt5.QtWidgets import QFrame, QPushButton, QLabel, QHBoxLayout, QApplication, QMenu, QDesktopWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSettings, QRect, QPoint, QSize
from . import mini_tab, paths, zslider, styles


class Hpanel(QFrame):
	"""HPanel class"""
	def __init__(self, parentWidget):
		super().__init__()
		self.parentWidget = parentWidget
		self.create_widgets()

	def create_widgets(self):
		"""Create widgets"""
		self.settings = QSettings(paths.CONFIG_PATH, QSettings.IniFormat)
		self.button_size = 25
#hbox_main
		self.hbox_main = QHBoxLayout()
		self.hbox_main.setContentsMargins(5, 1, 5, 1)
		self.setLayout(self.hbox_main)
		#add grab_label
		self.label_grab = ZLabel()
		self.hbox_main.addWidget(self.label_grab)
		#add play button
		self.btn_play = Hbutton()
		self.btn_play.set_icon(QIcon(':/play_icon.png'))
		self.btn_play.clicked.connect(self.press_button_play)
		self.hbox_main.addWidget(self.btn_play)
		#add stop button
		self.btn_stop = Hbutton()
		self.btn_stop.set_icon(QIcon(':/stop_icon.png'))
		self.btn_stop.clicked.connect(self.press_button_stop)
		self.hbox_main.addWidget(self.btn_stop)
		#add volume
		self.volume_slider = zslider.Zslider()
		self.volume_slider.setStyleSheet(styles.get_slider_style())
		self.volume_slider.setMinimumWidth(90)
		self.volume_slider.setRange(0, 100)
		self.volume_slider.valueChanged.connect(self.volume_change)
		self.hbox_main.addWidget(self.volume_slider)
		#add label volume
		self.label_volume = QLabel()
		self.label_volume.setAlignment(Qt.AlignCenter)
		self.label_volume.setFixedSize(self.button_size, self.button_size)
		self.label_volume.setStyleSheet('QLabel{border:1px solid silver;border-radius:6px;}')
		self.label_volume.setText(str(self.volume_slider.sliderPosition()))
		self.hbox_main.addWidget(self.label_volume)
		#add button show main
		self.button_show_main = Hbutton()
		self.button_show_main.set_icon(QIcon(':/menu_icon.png'))
		self.hbox_main.addWidget(self.button_show_main)
		self.panel_menu = QMenu()
		self.panel_menu.addAction(QIcon(':/stations_icon.png'), self.tr('Show stations'), self.press_show_main)
		self.panel_menu.addAction(QIcon(':/show_info_icon.png'), self.tr('Show info'), self.press_show_artist)
		self.panel_menu.addAction(QIcon(':/up_icon.png'), self.tr('Normal mode'), self.press_button_window)
		self.panel_menu.addSeparator()
		self.panel_menu.addAction(QIcon(':/remove_icon.png'), self.tr('Close app'), self.press_close_app)
		self.button_show_main.setMenu(self.panel_menu)
		
		#set up
		self.setAttribute(Qt.WA_DeleteOnClose, True)
		self.setWindowFlags(Qt.Window | Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
		self.setStyleSheet('QFrame{border:1px solid #5782c6;}')
		
		#move panel
		self.move_panel()
		
#################################################################################

	def closeEvent(self, event):
		"""Close event"""
		x_pos = self.x()
		y_pos = self.y()
		self.save_position()
		
	def save_position(self):
		x_pos = self.x()
		y_pos = self.y()
		self.settings.setValue('config/panel_x', x_pos)
		self.settings.setValue('config/panel_y', y_pos)
		self.settings.sync()

	def move_panel(self):
		x_start = int(self.settings.value('config/panel_x'))
		#y_start = int(self.config_file.value('config/panel_y'))
		rec = QRect()
		rec = QApplication.desktop().screenGeometry()
		max_y = rec.height() - self.sizeHint().height()
		height = max_y
		width = (rec.width() / 2) - (self.sizeHint().width() / 2)
		self.move(width, height)

	def press_show_main(self):
		"""Press show main"""
		self.main_win = mini_tab.Mini_tab(self.parentWidget)
		self.main_win.show()
		self.main_win.add_all_buttons()

	def volume_change(self, value):
		"""Volume change"""
		self.parentWidget.volume_change(value)
		self.label_volume.setText(str(self.volume_slider.sliderPosition()))
		self.volume_slider.setValue(value)

	def press_button_play(self):
		"""Press button play"""
		self.parentWidget.press_button_play()
		
	def press_button_stop(self):
		"""Press button stop"""
		self.parentWidget.press_button_stop()
		
	def press_button_window(self):
		"""Press toggle to normal window"""
		self.close()
		self.parentWidget.parent().show()
		self.parentWidget.parent().setWindowState(Qt.WindowActive)
		
	def press_show_artist(self):
		"""Press show artist"""
		artist_text = self.parentWidget.label_artist.TITLE
		if artist_text:
			self.artist_win = Artist_win()
			self.artist_win.setText(artist_text)
			self.artist_win.show()
		
	def press_close_app(self):
		"""Press close app"""
		QApplication.quit()
		
#########################################################################################

class ZLabel(QLabel):
	"""ZLabel class"""
	def __init__(self):
		super().__init__()
		self.create_label()

	def create_label(self):
		"""Create label"""
		self.setText("|||")
		self.setStyleSheet("border:1px solid transparent;")
		self.setCursor(Qt.OpenHandCursor)

	def mousePressEvent(self, event):
		"""Mouse release event"""
		self.oldPos = event.globalPos()

	def mouseMoveEvent(self, event):
		"""Mouse move event"""
		delta = QPoint(event.globalPos() - self.oldPos)
		self.parent().move(self.parent().x() + delta.x(), 
							self.parent().y() + delta.y())
		self.oldPos = event.globalPos()

	def mouseReleaseEvent(self, event):
		"""Mouse release event"""
		size = self.sizeHint()
		rec = QRect()
		rec = QApplication.desktop().screenGeometry()
		max_y = rec.height() - self.parent().sizeHint().height()
		if self.parent().y() > max_y:
			height = max_y
			self.move_panel(height)
		if self.parent().y() < 0:
			height = 0
			self.move_panel(height)

	def move_panel(self, height):
		"""Move panel"""
		width = self.parent().x()
		self.parent().move(width, height)

################################################################

class Hbutton(QPushButton):
	"""HButton class"""
	def __init__(self):
		super().__init__()
		self.create_button()
		
	def create_button(self):
		"""Create button"""
		button_size = 25
		icon_size = button_size - 5
		self.setIconSize(QSize(icon_size, icon_size))
		self.setFixedSize(button_size, button_size)
		self.setCursor(Qt.PointingHandCursor)
		self.setStyleSheet(styles.get_button_style())
		
	def set_icon(self, q_icon):
		"""Set icon"""
		self.setIcon(q_icon)

################################################################

class Artist_win(QLabel):
	"""Artist win class"""
	def __init__(self):
		super().__init__()
		self.setFixedSize(250, 150)
		self.setAlignment(Qt.AlignCenter)
		self.setWordWrap(True)
		self.setTextInteractionFlags(Qt.TextSelectableByMouse)
		self.setWindowTitle('Info')
		self.setWindowIcon(QIcon(':/show_info_icon.png'))
		self.setStyleSheet('QLabel{background:lightyellow; color:brown; font-weight:bold;}')
		self.center()
		
	def center(self):
		# geometry of the main window
		qr = self.frameGeometry()
		# center point of screen
		cp = QDesktopWidget().availableGeometry().center()
		# move rectangle's center point to screen's center point
		qr.moveCenter(cp)
		# top left of rectangle becomes top left of window centering it
		self.move(qr.topLeft())
		
	def closeEvent(self, event):
		"""Close to hide"""
		self.hide()
		event.ignore()
