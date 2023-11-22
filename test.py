import tkinter as tk
import time
import win32gui

# Create the main window
window = tk.Tk()

SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001
HWND_BOTTOM = 1
GWL_EXSTYLE = -20
WS_EX_NOACTIVATE = 0x08000000

# Configure the window to be full-screen
window.attributes('-fullscreen', True)
window.configure(background='black')
window.overrideredirect(True)
window.wm_attributes('-alpha', 0.7)
window.attributes("-topmost", False)

window.lower()
window_handle = win32gui.GetForegroundWindow()

extended_style = win32gui.GetWindowLong(window_handle, GWL_EXSTYLE)
win32gui.SetWindowLong(window_handle, GWL_EXSTYLE, extended_style | WS_EX_NOACTIVATE)
win32gui.SetWindowPos(window_handle, HWND_BOTTOM, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)

def move_window_behind_taskbar():
    window_handle = win32gui.GetForegroundWindow()
    win32gui.SetWindowPos(window_handle, HWND_BOTTOM, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)

# Update the window position behind the taskbar
window.after(10, move_window_behind_taskbar)


clock_label = tk.Label(window, font=('Arial', 80), fg='white', bg='black')
clock_label.pack(expand=True)

# Function to update the clock
def update_clock():
    current_time = time.strftime('%H:%M:%S')
    clock_label.config(text=current_time)
    clock_label.after(1000, update_clock)

# Start updating the clock
update_clock()

# Run the application main loop
window.mainloop()
