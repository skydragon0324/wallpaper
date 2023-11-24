from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu, QListWidget, QListWidgetItem, QLabel, QComboBox, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from display import WallpaperSys
import threading, json
from helper import getDataFilePath
import multiprocessing
import win32gui, win32con
import os
import shutil

class MainWindow(QMainWindow):
    
    def __init__(self):
        self.position = 0
        self.isblack = 0
        file_path = getDataFilePath('data/setting.json')
        # teste_file_path = getDataFilePath('data/image/computer.jpg')
        self.wallpaper = WallpaperSys.get_current_background_path(self)
        with open(file_path, "r") as file:
            self.theme_list = json.load(file)

        self.font = getDataFilePath(self.theme_list[0]['font'])
        self.style = self.theme_list[0]['style']
        self.stop_flag = threading.Event()
        self.real_time_thread = threading.Thread(target=WallpaperSys( self.font, stop_flag=self.stop_flag, style= self.style).run)
        super().__init__()
        self.init_ui()
        # self.real_time_thread.start()

    def init_ui(self):
        # Set up the window
        self.setWindowTitle('Wallpaper')
        self.setWindowIcon(QIcon(getDataFilePath('data/icon/icon.png')))
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setFixedSize(500, 250)
        # self.setStyleSheet('background-color: #333;')
        self.list_widget = QListWidget(self)
        self.list_widget.setGeometry(10, 10, 200, 225)
        self.list_widget.itemClicked.connect(self.change_preview_image)
        # self.list_widget.setStyleSheet('background-color: #222;border: 1px solid #555;color: white')
        # for i in range(10):
        for theme in self.theme_list:
            item = QListWidgetItem(theme['title'])
            self.list_widget.addItem(item)
        default_item = self.list_widget.item(0)
        self.list_widget.setCurrentItem(default_item)
        
        self.preview = QLabel(self)
        self.preview.setGeometry(230, 10, 250, 200)
        # self.preview.setStyleSheet('background-color: #f2f2f2; border-radius: 5px;')
        pixmap = QPixmap(getDataFilePath(self.theme_list[0]['preview']))
        self.preview.setPixmap(pixmap)
        self.preview.setScaledContents(True)

        # how to show window size end
        self.ok_button = QPushButton('Okay', self)
        self.ok_button.setGeometry(230, 225, 70, 25)
        self.ok_button.clicked.connect(self.on_ok_button_click)
        # self.ok_button.setStyleSheet('background-color: #4CAF50; color: white; border-radius: 5px;')
        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.setGeometry(320, 225, 70, 25)
        self.cancel_button.clicked.connect(self.on_cancel_button_click)
        # self.cancel_button.setStyleSheet('background-color: #f44336; color: white; border-radius: 5px;')
        self.apply_button = QPushButton('Apply', self)
        self.apply_button.setGeometry(410, 225, 70, 25)
        self.apply_button.clicked.connect(self.on_apply_button_click)
        # self.apply_button.setStyleSheet('background-color: #2196F3; color: white; border-radius: 5px;')

        # Set up the system tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.setWindowIcon(QIcon(getDataFilePath('data/icon/icon.png')))
        self.tray_icon.setIcon(QIcon(getDataFilePath('data/icon/icon.png')))
        self.tray_icon.setVisible(True)

        # Add a context menu to the tray icon
        self.tray_menu = QMenu(self)
        self.tray_menu.addAction('Open', self.showNormal)
        self.tray_menu.addAction('Close', self.close)
        self.tray_icon.setContextMenu(self.tray_menu)

    def closeEvent(self, event):
        event.ignore()
        self.hide()
    def close_app(self):
        if self.real_time_thread.is_alive():
            self.stop_flag.set()
            self.real_time_thread.join()
        self.hide()
        # set background as preview image
        # ctypes.windll.user32.SystemParametersInfoW(20, 0, self.wallpaper_path, 3)
        WallpaperSys.set_background(self.wallpaper)
        QApplication.quit()

    def on_combo_box_activated(self, text):
        self.position = self.combo_box.currentIndex()
    def change_preview_image(self, item):
        # Get the clicked item's text and find the corresponding image path
        selected_theme = item.text()
        image_path = None

        for theme in self.theme_list:
            if theme['title'] == selected_theme:
                image_path = getDataFilePath(theme['preview'])
                self.style = theme['style']
                self.font = getDataFilePath(theme['font'])
                break

        if image_path:
            pixmap = QPixmap(image_path)
            self.preview.setPixmap(pixmap)
    def on_ok_button_click(self):
        if self.real_time_thread.is_alive():
            self.stop_flag.set()  # Reset the stop flag
            self.real_time_thread.join()
        self.stop_flag.clear()
        self.real_time_thread = threading.Thread(target=WallpaperSys( self.font, stop_flag=self.stop_flag, style=self.style).run)
        self.real_time_thread.start()
        self.hide()
    def on_apply_button_click(self, ):
        if self.real_time_thread.is_alive():
            print('-')
            self.stop_flag.set()  # Reset the stop flag
            self.real_time_thread.join()
        self.stop_flag.clear()
        self.real_time_thread = threading.Thread(target=WallpaperSys( self.font, stop_flag=self.stop_flag, style=self.style).run)
        self.real_time_thread.start()
        pass
    def on_cancel_button_click(self):
        self.hide()

        
def main():
    app = QApplication([])
    multiprocessing.freeze_support()
    try:
        frgrnd_wndw = win32gui.GetForegroundWindow()
        wndw_title  = win32gui.GetWindowText(frgrnd_wndw)
        if wndw_title.endswith("window.exe"):
            win32gui.ShowWindow(frgrnd_wndw, win32con.SW_HIDE)
    except  :
        pass
    window = MainWindow()
    window.show()
    close_action = window.tray_menu.actions()[1]
    close_action.triggered.connect(window.close_app)

    app.exec_()

if __name__ == '__main__':
    app = QApplication([])
    multiprocessing.freeze_support()
    try:
        frgrnd_wndw = win32gui.GetForegroundWindow()
        wndw_title  = win32gui.GetWindowText(frgrnd_wndw)
        if wndw_title.endswith("window.exe"):
            win32gui.ShowWindow(frgrnd_wndw, win32con.SW_HIDE)
    except  :
        pass
    window = MainWindow()
    window.show()

    close_action = window.tray_menu.actions()[1]
    close_action.triggered.connect(window.close_app)

    app.exec_()