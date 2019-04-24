"""Styles module"""

def get_button_style():
	"""Get QPushButton style"""
	BUTTON_STYLE = ("""QPushButton{
						border:1px solid silver;
						border-radius:6px;
						font-size:12px;
						font-weight:bold;
					} 
					QPushButton::hover{
						border:1px solid orange; 
						background-color:lightyellow;
					}
					QPushButton::menu-indicator{image: url(' '); width:0px;}
					QPushButton::checked{
						border: 1px solid red; 
						background-color:#ffc6c6;

					}""")
	return BUTTON_STYLE

def get_label_style():
	"""Get label style"""
	LABEL_STYLE = ("QLabel{border:1px solid transparent;}")
	return LABEL_STYLE

def get_countries_label_style():
	"""Get tab2 label style"""
	STYLE = """QLabel{
					border:1px solid silver;
			}"""
	return STYLE

def get_scrollarea_style():
	"""Get scrollarea style"""
	STYLE = 'QScrollArea{border:1px solid transparent;}'
	return STYLE

def get_scrollbar_style():
	"""Get scrollbar style"""
	SCROLL_BAR_STYLE = ("""QScrollBar:vertical {           
		border: 1px solid #999999;
		background:white;
		width:10px;
		margin: 0px 0px 0px 0px;
		}
		QScrollBar::handle:vertical {
			background: #c1c1c1;
			min-height: 0px;
		}
		QScrollBar::add-line:vertical {
			background: #c1c1c1;
			height: 0px;
			subcontrol-position: bottom;
			subcontrol-origin: margin;
			}
		QScrollBar::sub-line:vertical {
			background: #c1c1c1;
			height: 0 px;
			subcontrol-position: top;
			subcontrol-origin: margin;
			}
		""")
	return SCROLL_BAR_STYLE

def get_slider_style():
	"""Get slider style"""
	SLIDER_STYLE = ("""
		QSlider::groove:horizontal {
			border: 1px solid #bbb;
			background: white;
			height: 10px;
			border-radius: 4px;
		}

		QSlider::sub-page:horizontal {
			background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,
				stop: 0 #66e, stop: 1 #bbf);
			background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,
				stop: 0 #bbf, stop: 1 #55f);
			border: 1px solid #777;
			height: 10px;
			border-radius: 4px;
		}

		QSlider::add-page:horizontal {
			background: #fff;
			border: 1px solid #777;
			height: 10px;
			border-radius: 4px;
		}

		QSlider::handle:horizontal {
			background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
				stop:0 #eee, stop:1 #ccc);
			border: 1px solid #777;
			width: 13px;
			margin-top: -2px;
			margin-bottom: -2px;
			border-radius: 4px;
		}

		QSlider::handle:horizontal:hover {
			background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
				stop:0 #fff, stop:1 #ddd);
			border: 1px solid #444;
			border-radius: 4px;
		}

		QSlider::sub-page:horizontal:disabled {
			background: #bbb;
			border-color: #999;
		}

		QSlider::add-page:horizontal:disabled {
			background: #eee;
			border-color: #999;
		}

		QSlider::handle:horizontal:disabled {
			background: #eee;
			border: 1px solid #aaa;
			border-radius: 4px;
		}""")
	return SLIDER_STYLE

def get_lineedit_style():
	"""Get LineEdit style"""
	STYLE = """
		QLineEdit{
			border:1px solid silver;
		}
		QLineEdit::focus{
			border:1px solid orange;
		}
	"""
