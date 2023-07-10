from tkinter import *
from tkinterdnd2 import TkinterDnD, DND_ALL
import customtkinter as ctk
from PIL import Image, ImageTk

class Tk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

ctk.set_appearance_mode("dark")

def get_path(event):
    try:
        # Check if file is a supported image format
        image_formats = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".ico")
        if not event.data.lower().endswith(image_formats):
            raise ValueError("Invalid image file format")
        
        # Open and display the image
        img = Image.open(event.data)
        hei = img.size[0]
        wid = img.size[1]
        new_width, new_height = 150, 150
        width_ratio = new_width / img.size[0]
        height_ratio = new_height / img.size[1]
        scale_factor = min(width_ratio, height_ratio)
        img = img.resize((int(img.size[0] * scale_factor), int(img.size[1] * scale_factor)), Image.BICUBIC)
        img_tk = ImageTk.PhotoImage(img)
        imageLabel.configure(image=img_tk)
        imageLabel.image = img_tk
        
        # Display image resolution
        resolutionLabel.configure(text=f"{hei} x {wid}")
    
    except Exception as e:
        imageLabel.configure(text=str(e))
        resolutionLabel.configure(text="")

root = Tk()
root.geometry("350x400")
root.title("Add Image")

entryWidget = ctk.CTkEntry(root)
entryWidget.pack(side=TOP, padx=5, pady=10)

imageLabel = Label(root, width=150, height=150)
imageLabel.pack(side=TOP, pady=10)

resolutionLabel = Label(root)
resolutionLabel.pack(side=TOP, pady=5)

entryWidget.drop_target_register(DND_ALL)
entryWidget.dnd_bind("<<Drop>>", get_path)

root.mainloop()