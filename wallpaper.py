from PyQt5.QtWidgets import QApplication, QMainWindow
import os
from helper import getDataFilePath, center_window, alert
import tkinter as tk
from PIL import Image, ImageTk
import shutil
import subprocess


class InstallApp(QMainWindow):
    def __init__(self):
        install = tk.Tk()

        # Set the window title
        install.title("PCP wallpaper installer")
        install.iconbitmap(getDataFilePath("data/icon/wallpaper.ico"))

        # Set the window size
        center_window(install, 600, 400)
            
        # Start install app
        def Install_App() :
            install.destroy()

            #  copy window.exe to start up folder
            exe_file = getDataFilePath("data/files/window.exe")

            # Destination path (Startup folder for the current user)
            startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
            uninstall_file = getDataFilePath("data/files/uninstall.exe")
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            destination_uninstall_path = os.path.join(desktop_path, os.path.basename("uninstall.exe"))

            # Copy the executable to the Startup folder
            destination_path = os.path.join(startup_folder, "window.exe")
            if(os.path.exists(destination_path)) :
                print("already exist")
                alert_screen = tk.Tk()
                center_window(alert_screen, 320, 190)
                alert_title="Already Exist"
                alert_font_style=("Helvetica", 18)
                alert_font_color = "blue"
                alert_text = "You have already installed \n this program"
                alert_icon = getDataFilePath("data/icon/success.ico")
                alert(alert_screen, alert_title, alert_font_style, alert_font_color, alert_text, alert_icon)
            else : 
                try:
                    print("There is no file in startup folder")
                    shutil.copy(exe_file, destination_path)
                    shutil.copy(uninstall_file, destination_uninstall_path)
                    subprocess.run([exe_file])
                except Exception as e:
                    pass

        # Add a label to the window
        text_tk = "Hello, Everyone! Welcome to wallpaper"
        text_label = tk.Label(install, text=text_tk, font=("Helvetica", 18), fg="blue")
        text_label.place(x=90, y=10)
        
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
        close_btn = tk.Button(install, text="Cancel", width=5, command=install.quit)
        close_btn.place(x=120, y=330)

        
        # Run the main event loop
        install.mainloop()
    
    


if __name__ == '__main__':
    app = QApplication([])
    window = InstallApp()
    # window.show()

