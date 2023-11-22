from PyQt5.QtWidgets import QMainWindow
import os
from helper import getDataFilePath
import tkinter as tk


class Uninstall(QMainWindow):
    def __init__(self):
        uninstall = tk.Tk()
        uninstall.title("Uninstall program")
        uninstall.iconbitmap(getDataFilePath("data/icon/delete.ico"))
        uninstall.geometry("400x200")
        text = tk.Label(uninstall, text="Do you want to uninstall\n this program really ?",font=("Helvetica", 18), fg="blue")
        text.pack(fill=tk.X, padx=10, pady=30)
        def close_app():
            uninstall.destroy()

        def uninstall_success() :
            uninstall_success_screen = tk.Toplevel()
            uninstall_success_screen.title("Uninstalled successfully")
            uninstall_success_screen.iconbitmap(getDataFilePath("data/icon/delete.ico"))
            uninstall_text = tk.Label(uninstall_success_screen, text="You have just uninstalled program", font=("Helvetica", 12), fg="green").pack()
            close_btn = tk.Button(uninstall_success_screen, text="close", width=5, command=close_app).pack()

        def uninstall_error() :
            uninstall_error_screen = tk.Toplevel()
            uninstall_error_screen.geometry("300x100")
            uninstall_error_screen.title("Uninstalled failed")
            uninstall_error_screen.iconbitmap(getDataFilePath("data/icon/delete.ico"))
            uninstall_text = tk.Label(uninstall_error_screen, text="This program has been already uninstalled", font=("Helvetica", 12), fg="#FFB6C1").pack()
            close_btn = tk.Button(uninstall_error_screen, text="close", width=5, command=close_app)
            close_btn.place(x=110, y=30)


        def uninstall_app():
            exe_file = "window.exe"

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
        close_btn = tk.Button(uninstall, text="Cancel",font=("Helvetica", 12), fg="blue", bg="gray", width=7, command=close_app)
        close_btn.place(x=50, y=130)

        uninstall.mainloop()


if __name__ == "__main__" :
    window = Uninstall()