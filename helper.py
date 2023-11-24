from PIL import Image, ImageDraw
import time
import os
import sys
import tkinter as tk

def calcColor(pct):
    pct_diff = 1.0 - pct
    green_color = int(min(255, pct_diff*2 * 255))
    red_color = int(min(255, pct*2 * 255))

    return (red_color, green_color, 0)

def draw_ellipse(image, bounds, width, outline, antialias):
    mask = Image.new(
        size=[int(dim * antialias) for dim in image.size],
        mode='L', color='black')
    draw = ImageDraw.Draw(mask)

    # draw outer shape in white (color) and inner shape in black (transparent)
    for offset, fill in (width/-2.0, 'white'), (width/2.0, 'black'):
        left, top = [(value + offset) * antialias for value in bounds[:2]]
        right, bottom = [(value - offset) * antialias for value in bounds[2:]]
        draw.ellipse([left, top, right, bottom], fill=fill)
    mask = mask.resize(image.size, Image.LANCZOS)
    image.paste(outline, mask=mask)

def draw_arc(image, bounds, start_angle, end_angle, width, outline, antialias, arc_width):
    mask = Image.new(
        size=[int(dim * antialias) for dim in image.size],
        mode='L', color='black')
    draw = ImageDraw.Draw(mask)
    for offset, fill in (width/-2.0, 'white'), (width/2.0, 'black'):
        left, top = [(value + offset) * antialias for value in bounds[:2]]
        right, bottom = [(value - offset) * antialias for value in bounds[2:]]
        draw.arc([left, top, right, bottom], start_angle, end_angle, fill=fill, width=arc_width)
    mask = mask.resize(image.size, Image.LANCZOS)
    image.paste(outline, mask=mask)

def drawTextCenter (draw, point, text, color, font ):
    text_width, text_height = draw.textsize(text, font=font)
    text_x = point[0] - text_width // 2
    draw.text((text_x, point[1]), text, font=font, fill=color) 

def drawTextRight (draw, point, text, fill, font ):
    text_width, text_height = draw.textsize(text, font=font)
    text_x = point[0] - text_width
    draw.text((text_x, point[1]), text, font=font, fill=fill)

def getDataFilePath(file_name):
        bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        file_path = os.path.abspath(os.path.join(bundle_dir,file_name))
        # print(f'file_path ------------------------------------ {file_path}')
        return file_path


# Set window at the centen
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


# If you have already installed this program, you will receive this message
def alert(window, title, font_style, font_color, text, icon):
    window.title(title)
    window.iconbitmap(icon)
    text = tk.Label(window, text=text, font=font_style, fg=font_color).pack(padx=10, pady=30)
    btn = tk.Button(window, text="Close", width=5, font=(12), command=window.quit).pack(padx=10, pady=10)

