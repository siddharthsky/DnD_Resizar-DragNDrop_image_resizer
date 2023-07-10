from tkinter import *
from tkinterdnd2 import TkinterDnD, DND_ALL
import customtkinter as ctk
from PIL import Image, ImageTk

class Tk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

ctk.set_appearance_mode("dark")

# Define a function to handle the "Drop" event
def handle_drop(event):
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
        default_image_label.configure(image=img_tk)
        default_image_label.image = img_tk
        
        # Display image resolution
        resolutionLabel.configure(text=f"{hei} x {wid}")
    
    except Exception as e:
        default_image_label.configure(text=str(e))
        resolutionLabel.configure(text="")

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
root.geometry("350x420")
root.title("DnD Image Resizar")
header_label = ctk.CTkLabel(master=root,
                                      text='Add image to resize',
                                      font=(None,24))
header_label.pack(pady=20)

entryWidget = ctk.CTkEntry(master=root, 
                                    placeholder_text="Enter Height")
entryWidget.pack(side=TOP, padx=5, pady=10)

entryWidget2 = ctk.CTkEntry(master=root, 
                                    placeholder_text="Enter Width")
entryWidget2.pack(side=TOP, padx=5, pady=10)


def convert():
    print("HI send")
    hei1 = entryWidget.get()
    wid1 = entryWidget2.get()
    print(f"{hei1} x {wid1}")

    #sports = []
    #if football_checkbox.get():
       # sports.append('Football')
    #if boxing_checkbox.get():
      #  sports.append('Boxing')
   # print(name + ' likes: ' + ', '.join(sports))

conv_button = ctk.CTkButton(master=root,text="Resize",command=convert)
conv_button.pack(pady=10)

# Load the default image file and create a PhotoImage object
default_img = Image.open("drag-drop.png")
default_img = default_img.resize((150, 150), Image.BICUBIC)
default_img_tk = ImageTk.PhotoImage(default_img)

# Create a label widget to display the default image
default_image_label = Label(root, image=default_img_tk, width=150, height=150)
default_image_label.pack(side=TOP, pady=10)

resolutionLabel = Label(root, text = "-SiddharthSky-")
resolutionLabel.pack(side=TOP, pady=5)

imageLabel = Label(root, width=150, height=150)
imageLabel.pack(side=TOP, pady=10)

#resolutionLabel = Label(root)
#resolutionLabel.pack(side=TOP, pady=5)

#entryWidget.drop_target_register(DND_ALL)
#entryWidget.dnd_bind("<<Drop>>", get_path)

# Register the label widget as a drop target
default_image_label.drop_target_register(DND_ALL)

# Bind the "Drop" event to the handle_drop function
default_image_label.dnd_bind("<<Drop>>", handle_drop)
#default_image_label.dnd_bind("<<Drop>>", get_path)


root.mainloop()