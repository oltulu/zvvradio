import os
import sys
import shutil
import sqlite3
from PyQt5.QtCore import QDir, QStandardPaths, QSettings

if sys.platform.startswith("linux"):
	#system folder
	SYSTEM_FOLDER = os.path.join(os.getenv("HOME"), ".config")
	if not os.path.exists(SYSTEM_FOLDER):
		os.mkdir(SYSTEM_FOLDER)
	#app folder
	APP_FOLDER = os.path.join(SYSTEM_FOLDER, "ZVVRadio")
	if not os.path.exists(APP_FOLDER):
		os.mkdir(APP_FOLDER)
	#playlist folder
	PLS_FOLDER = os.path.join(APP_FOLDER, "playlists")
	if not os.path.exists(PLS_FOLDER):
		os.mkdir(PLS_FOLDER)
	#config.ini
	CONFIG_PATH = os.path.join(APP_FOLDER, "config.ini")
	if not os.path.exists(CONFIG_PATH):
		src_path = os.path.join(os.getcwd(), "config.ini")
		dst_path = APP_FOLDER
		shutil.copy(src_path, dst_path)
	else:
		if QSettings(CONFIG_PATH, QSettings.IniFormat).contains("config/version"):
			current_version = int(QSettings(CONFIG_PATH, QSettings.IniFormat).value("config/version"))
			if current_version < 11:
				src_path = os.path.join(os.getcwd(), "config.ini")
				dst_path = APP_FOLDER
				shutil.copy(src_path, dst_path)
				#copy base
				src_path = os.path.join(os.getcwd(), "zvvbase.db")
				dst_path = APP_FOLDER
				shutil.copy(src_path, dst_path)
	#base path
	BASE_PATH = os.path.join(APP_FOLDER, "zvvbase.db")
	if not os.path.exists(BASE_PATH):
		src_path = os.path.join(os.getcwd(), "zvvbase.db")
		dst_path = APP_FOLDER
		shutil.copy(src_path, dst_path)
	#record path
	RECORD_PATH = QStandardPaths.writableLocation(QStandardPaths.MusicLocation)

if sys.platform.startswith("win"):
	APP_FOLDER = os.getcwd()
	PLS_FOLDER = os.path.join(APP_FOLDER, "playlists")
	CONFIG_PATH = os.path.join(APP_FOLDER, "config.ini")
	BASE_PATH = os.path.join(APP_FOLDER, "zvvbase.db")
	
	
BASE_CONNECTION = sqlite3.connect(BASE_PATH)
BASE_CURSOR = BASE_CONNECTION.cursor()

###############################################################################################

