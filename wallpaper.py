from PyQt5.QtWidgets import QApplication, QMainWindow
import os
from helper import getDataFilePath, center_window, alert
import tkinter as tk
from PIL import Image, ImageTk
import shutil
import subprocess
import psutil

class InstallApp(QMainWindow):
    def __init__(self):
        install = tk.Tk()

        # Set the window title
        install.title("PCP wallpaper installer")
        install.iconbitmap(getDataFilePath("data/icon/wallpaper.ico"))

        # Set the window size
        center_window(install, 600, 400)
        
        def uninstall_success() :
            uninstall_success_screen = tk.Toplevel()
            center_window(uninstall_success_screen, 300, 150)
            alert(uninstall_success_screen, "Uninstalled successfully", ("Helvetica", 12), "green", "You have just uninstalled program", getDataFilePath("data/icon/delete.ico"))
     
        def uninstall_error() :
            uninstall_error_screen = tk.Toplevel()
            center_window(uninstall_error_screen, 320, 150)
            alert(uninstall_error_screen, "Uninstalled failed", ("Helvetica", 12), "red", "This program has already been uninstalled", getDataFilePath("data/icon/delete.ico"))

        # Start install app
        def Install_App() :
            install.destroy()

            #  copy window.exe to start up folder
            exe_file = getDataFilePath("files/window.exe")
            print(f"exe_file:::{exe_file}")

            # Destination path (Startup folder for the current user)
            startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')

            # Copy the executable to the Startup folder
            destination_path = os.path.join(startup_folder, "window.exe")
            print(f"destination_path::: {destination_path}")
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
                    print("-------------------")
                    subprocess.run([exe_file])
                except Exception as e:
                    print(f"skydragon ::: {e}")
                    pass
        def Uninstall_App() :
            exe_file = "window.exe"

            # delete uninstall file
            uninstall_file = "uninstall.exe"
            current_directory = os.getcwd()
            uninstall_path = os.path.join(current_directory, uninstall_file)

            # Destination path (Startup folder for the current user)
            startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')

            # Copy the executable to the Startup folder
            destination_path = os.path.join(startup_folder, exe_file)

            # If window.exe is running now, stop it first.
            for process in psutil.process_iter(['pid','name']):
                if process.info['name'] == "window.exe" :
                    try :
                        pid = process.info['pid']
                        p = psutil.Process(pid)
                        p.terminate()
                    except:
                        pass

            if(os.path.exists(destination_path)) :
                os.remove(destination_path)
                uninstall_success()
            else : 
                print("Your program has already been uninstalled")
                uninstall_error()
            if(os.path.exists(uninstall_path)) :
                os.unlink(uninstall_path)
                os.remove(uninstall_path)
            else :
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
        uninstall_btn = tk.Button(install, text="Uninstall", width=6, command=Uninstall_App)
        uninstall_btn.place(x=285, y=330)
        close_btn = tk.Button(install, text="Cancel", width=5, command=install.quit)
        close_btn.place(x=120, y=330)

        
        # Run the main event loop
        install.mainloop()
    
    


if __name__ == '__main__':
    app = QApplication([])
    window = InstallApp()
    # window.show()

