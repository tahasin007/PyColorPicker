import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import colorsys
import pyperclip

def generate_gradient(width, height, hue, saturation):
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    for y in range(height):
        for x in range(width):
            saturation_val = x / width
            brightness = 1.0 - (y / height) * saturation
            rgb_color = colorsys.hsv_to_rgb(hue, saturation_val, brightness)
            r, g, b = [int(255 * c) for c in rgb_color]
            draw.point((x, y), fill=(r, g, b))
    return img

def update_color(value):
    hue = float(value) / 360.0
    saturation = 1.0 
    gradient_img = generate_gradient(color_frame.winfo_width(), color_frame.winfo_height(), hue, saturation)
    gradient_photo = ImageTk.PhotoImage(gradient_img)
    color_frame.configure(image=gradient_photo)
    color_frame.image = gradient_photo 
    
    rgb_color = colorsys.hsv_to_rgb(hue, saturation, 1)
    r, g, b = [int(255 * c) for c in rgb_color]
    rgb_label.config(text=f"RGB: {r}, {g}, {b}")
    hex_label.config(text=f"HEX: #{r:02x}{g:02x}{b:02x}")

def copy_to_clipboard(value):
    pyperclip.copy(value)
    print(f"Value {value} copied to clipboard")

root = tk.Tk()
root.title("Color Picker")

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

color_frame = tk.Label(root, bg="#FFFFFF", width=360, height=360)
color_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

hue_slider = tk.Scale(root, from_=0, to=360, orient='vertical', command=update_color)
hue_slider.grid(row=0, column=2, padx=10, pady=10, sticky="ns")

def create_icon(canvas, x, y, command, icon_path):
    icon = Image.open(icon_path) 
    width, height = icon.size
    new_width = 25
    new_height = int((new_width / width) * height)
    icon = icon.resize((new_width, new_height))
    icon = ImageTk.PhotoImage(icon)
    button = tk.Button(canvas, image=icon, command=command, bd=0, highlightthickness=0)
    button.image = icon
    button.place(x=x, y=y)

def on_mouse_motion(event):
    width, height = color_frame.winfo_width(), color_frame.winfo_height()
    hue = hue_slider.get()
    saturation = 1.0 - (float(event.y) / height)
    
    rgb_color = colorsys.hsv_to_rgb(hue / 360.0, saturation, 1)
    r, g, b = [int(255 * c) for c in rgb_color]
    rgb_label.config(text=f"RGB: {r}, {g}, {b}")
    hex_label.config(text=f"HEX: #{r:02x}{g:02x}{b:02x}")

def on_mouse_click(event):
    on_mouse_motion(event)

icon_path = "./asset/clipboard_icon.png"  
canvas_rgb = tk.Canvas(root, bg="white", highlightthickness=0, width=120, height=40)
canvas_rgb.grid(row=1, column=0, padx=10, pady=10, sticky="we")
rgb_label = tk.Label(canvas_rgb, text="RGB: 255, 255, 255")
rgb_label.place(x=35, y=10)
create_icon(canvas_rgb, 5, 5, lambda: copy_to_clipboard(rgb_label.cget("text").split(': ')[1]), icon_path)

canvas_hex = tk.Canvas(root, bg="white", highlightthickness=0, width=120, height=40)
canvas_hex.grid(row=1, column=1, padx=10, pady=10, sticky="we")
hex_label = tk.Label(canvas_hex, text="HEX: #FFFFFF")
hex_label.place(x=35, y=10)
create_icon(canvas_hex, 5, 5, lambda: copy_to_clipboard(hex_label.cget("text").split(': ')[1]), icon_path)

update_color(0)

color_frame.bind("<Button-1>", on_mouse_click)
color_frame.bind("<B1-Motion>", on_mouse_motion)

root.mainloop()
