"""ZSlider module"""
from PyQt5.QtWidgets import QSlider, QStyle
from PyQt5.QtCore import Qt


class Zslider(QSlider):
	"""ZSlider class"""
	def __init__(self):
		super().__init__()
		self.setOrientation(Qt.Horizontal)

	def mousePressEvent(self, ev):
		""" Jump to click position """
		self.setValue(QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), ev.x(), self.width()))
		
	def mouseMoveEvent(self, ev):
		""" Jump to pointer position while moving """
		self.setValue(QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), ev.x(), self.width()))
