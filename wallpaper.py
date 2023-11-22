from PyQt5.QtWidgets import QApplication, QMainWindow
import os
from helper import getDataFilePath
import tkinter as tk
from PIL import Image, ImageTk
from window import MainWindow
import shutil
import window

class InstallApp(QMainWindow):
    def __init__(self):
        install = tk.Tk()

        # Set the window title
        install.title("PCP wallpaper installer")
        install.iconbitmap(getDataFilePath("data/icon/wallpaper.ico"))

        # Set the window size
        install.geometry("600x400")

        def Install_App() :
            install.destroy()

            #  copy window.exe to start up folder
            exe_file = getDataFilePath("data/files/window.exe")
            print(f"window::{exe_file}")

            # Destination path (Startup folder for the current user)
            startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
            uninstall_file = getDataFilePath("data/files/uninstall.exe")
            print(f"uninstall:::{uninstall_file}")
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            destination_uninstall_path = os.path.join(desktop_path, os.path.basename("uninstall.exe"))

            # Copy the executable to the Startup folder
            destination_path = os.path.join(startup_folder, "window.exe")
            if(os.path.exists(destination_path)) :
                print("already exist")
                return
            else : 
                try:
                    print("There is no file in startup folder")
                    shutil.copy(exe_file, destination_path)
                    shutil.copy(uninstall_file, destination_uninstall_path)
                    MainWindow(QMainWindow)
                except Exception as e:
                    # print(f"error : {e}")
                    pass


        #    window.destroy()
        def cancel_app():
            install.destroy()
        # Add a label to the window
        text_tk = "Hello, Everyone! Welcome to wallpaper"
        text_label = tk.Label(install, text=text_tk)
        text_label.place(x=160, y=10)
        
        # text_label.pack()

        # Open and resize the image
        original_image = Image.open(getDataFilePath("data/theme/computer.png"))
        resized_image = original_image.resize((530, 320))

        # Convert the resized image to Tkinter PhotoImage
        image_tk = ImageTk.PhotoImage(resized_image)
        image_label = tk.Label(install, image=image_tk)
        image_label.place(x=35, y=50)
        # image_label.pack()
        

        # add button
        install_btn = tk.Button(install, text="Install", width=5, command=Install_App)
        install_btn.place(x=450, y=330)
        close_btn = tk.Button(install, text="Cancel", width=5, command=cancel_app)
        close_btn.place(x=120, y=330)

        
        # Run the main event loop
        install.mainloop()
    
    


if __name__ == '__main__':
    app = QApplication([])
    window = InstallApp()
    # window.show()

