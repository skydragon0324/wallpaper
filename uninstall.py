from PyQt5.QtWidgets import QMainWindow
import os
import sys
from helper import getDataFilePath, alert
import tkinter as tk
from helper import center_window


class Uninstall(QMainWindow):
    def __init__(self):
        uninstall = tk.Tk()
        uninstall.title("Uninstall program")
        uninstall.iconbitmap(getDataFilePath("data/icon/delete.ico"))
        center_window(uninstall, 400, 200)
        text = tk.Label(uninstall, text="Do you want to uninstall\n this program really ?",font=("Helvetica", 18), fg="blue")
        text.pack(fill=tk.X, padx=10, pady=30)

        def uninstall_success() :
            uninstall_success_screen = tk.Toplevel()
            center_window(uninstall_success_screen, 300, 150)
            alert(uninstall_success_screen, "Uninstalled successfully", ("Helvetica", 12), "green", "You have just uninstalled program", getDataFilePath("data/icon/delete.ico"))
     
        def uninstall_error() :
            uninstall_error_screen = tk.Toplevel()
            center_window(uninstall_error_screen, 320, 150)
            alert(uninstall_error_screen, "Uninstalled failed", ("Helvetica", 12), "red", "This program has been already uninstalled", getDataFilePath("data/icon/delete.ico"))

        def uninstall_app():
            exe_file = "window.exe"

            # delete uninstall file
            uninstall_file = "uninstall.exe"
            current_directory = os.getcwd()
            uninstall_path = os.path.join(current_directory, uninstall_file)
            if(os.path.exists(uninstall_path)) :
                os.remove(uninstall_path)
            else :
                pass

            # Destination path (Startup folder for the current user)
            startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')

            # Copy the executable to the Startup folder
            destination_path = os.path.join(startup_folder, exe_file)
            if(os.path.exists(destination_path)) :
                os.remove(destination_path)
                uninstall_success()
            else : 
                print("Your program has been already uninstalled")
                uninstall_error()
        
        # add button
        uninstall_btn = tk.Button(uninstall, text="Uninstall", font=("Helvetica", 12), fg="#FFB6C1", bg="gray", width=7, command=uninstall_app)
        uninstall_btn.place(x=280, y=130)
        close_btn = tk.Button(uninstall, text="Cancel",font=("Helvetica", 12), fg="blue", bg="gray", width=7, command=uninstall.quit)
        close_btn.place(x=50, y=130)

        uninstall.mainloop()


if __name__ == "__main__" :
    window = Uninstall()