from tkinter import *
from tkinterdnd2 import TkinterDnD, DND_ALL
import customtkinter as ctk
from PIL import Image, ImageTk
import os

#Local Scripts
from utils import AspectRatio

#Object Initialization
Obj_ratio = AspectRatio() 


class Tk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

ctk.set_appearance_mode("system")


# Define a custom label widget that includes an "image_path" attribute
class ImageLabel(Label):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.image_path = ""

def get_aspect_ratio(width, height):
    gcd = math.gcd(width, height)
    return f"{int(width/gcd)}:{int(height/gcd)}"

# Define a function to handle the "Drop" event
def handle_drop(event):
    try:
        #Filepath validator
        if "{" in event.data and "}" in event.data:
            event_path = event.data.replace("{","") 
            event_data_path = event_path.replace("}","")
        else:
            event_data_path = event.data


        # Check if file is a supported image format
        image_formats = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".ico",".webp")
        data_formatted = r'%s' % event_data_path.lower()
        if not data_formatted.endswith(image_formats):
            raise ValueError("Invalid image file format")


        # Open and display the image
        img = Image.open(event_data_path)
        hei = img.size[1]
        wid = img.size[0]
        new_width, new_height = 150, 150
        width_ratio = new_width / img.size[0]
        height_ratio = new_height / img.size[1]
        scale_factor = min(width_ratio, height_ratio)
        img = img.resize((int(img.size[0] * scale_factor), int(img.size[1] * scale_factor)), Image.BICUBIC)
        img_tk = ImageTk.PhotoImage(img)
        default_image_label.configure(image=img_tk)
        default_image_label.image = img_tk
        default_image_label.image_path = event.data
        
        # Display image resolution
        resolutionLabel.configure(text=f"{wid} x {hei}")

        #Aspect ratio
        ratio = Obj_ratio.get(wid,hei)
        checkbox.configure(text=f"Aspect Ratio - {ratio}")
        
    
    except Exception as e:
        print(e)
        default_image_label.configure(text=str(e))
        resolutionLabel.configure(text="Sorry, invalid image")

def convert():
    try:
        # Get the input image path
        input_path = default_image_label.image_path
        print(input_path)
        # Check if the input file is a supported image format
        image_formats = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".ico",".webp")
        if not input_path.lower().endswith(image_formats):
            raise ValueError("Invalid image file format")
        
        # Get the output folder path
        output_folder = os.path.join(os.path.dirname(input_path), "output")
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # Get the new height and width values entered by the user
        new_width = int(entryWidget_width.get())
        new_height = int(entryWidget_height.get())
        
        # Open the input image and resize it
        img = Image.open(input_path)
        img = img.resize((new_width,new_height), Image.BICUBIC)
        
        # Save the resized image in the output folder with the same file name
        output_path = os.path.join(output_folder, os.path.basename(input_path))
        img.save(output_path)
        
        # Display the resized image in the GUI
        img_tk = ImageTk.PhotoImage(img)
        imageLabel.configure(image=img_tk)
        imageLabel.image = img_tk
        
        # Display the new image resolution
        resolutionLabel.configure(text=f"{new_width} x {new_height}")

        #Aspect ratio
        ratio = Obj_ratio.get(new_width,new_height)
        checkbox.configure(text=f"Aspect Ratio - {ratio}")
        
    except Exception as e:
        imageLabel.configure(text=str(e))
        resolutionLabel.configure(text="Sorry, invalid image")

root = Tk()
root_x = 350
root_y = 450
root.geometry(f"{root_x}x{root_y}")
root.title("DnD Image Resizar")
root.iconbitmap(r"resources\root_icon.ico")
header_label = ctk.CTkLabel(master=root,
                                      text='Add image to resize',
                                      font=(None,24))
header_label.pack(pady=20)

entryWidget_width = ctk.CTkEntry(master=root, 
                                    placeholder_text="Enter Width")
entryWidget_width.pack(side=TOP, padx=5, pady=10)

entryWidget_height = ctk.CTkEntry(master=root, 
                                    placeholder_text="Enter Height")
entryWidget_height.pack(side=TOP, padx=5, pady=10)

conv_button = ctk.CTkButton(master=root,text="Resize",command=convert)
conv_button.pack(pady=10)


checkbox_var = ctk.BooleanVar()  # create a variable to store the checkbox state
checkbox = ctk.CTkCheckBox(master=root, text=f"Aspect Ratio", variable=checkbox_var)  # create the checkbox widget
#checkbox.place(x=(root_x//2)-10)
checkbox.configure(checkbox_height=0,checkbox_width=0)
#checkbox.pack(side=BOTTOM)
checkbox.pack(anchor="center")


# Load the default image file and create a PhotoImage object
default_img = Image.open(r"resources\drag-drop.png")
default_img = default_img.resize((150, 150), Image.BICUBIC)
default_img_tk = ImageTk.PhotoImage(default_img)

# Create a labelwidget to display the default image
default_image_label = ImageLabel(root, image=default_img_tk, width=150, height=150)
default_image_label.pack(side=TOP, pady=10)
default_image_label.image_path = ""

resolutionLabel = Label(root, text = "-SiddharthSky-")
resolutionLabel.pack(side=TOP, pady=5)

imageLabel = Label(root, width=150, height=150)
imageLabel.pack(side=TOP, pady=10)

# Make the label widget accept drops and bind the "Drop" event to the handle_drop() function
default_image_label.drop_target_register(DND_ALL)
default_image_label.dnd_bind('<<Drop>>', handle_drop)

root.mainloop()
