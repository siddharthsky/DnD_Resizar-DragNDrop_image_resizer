from tkinter import *
from tkinterdnd2 import TkinterDnD, DND_ALL
from PIL import Image, ImageTk
import customtkinter as ctk
import os
from utils import MasterUtils

# Drag and Drop Init
class Tk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

# Define a custom label widget that includes an "image_path" attribute
class ImageLabel(Label):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.image_path = ""

#Initializing the Utilities class
Utils= MasterUtils() 

# Define a function to handle the "Drop" event
def handle_drop(event):
    try:
        #Filepath validator
        event_data_path = Utils.file_path_validator(event.data)

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
        ratio = Utils.get_aspect_ratio(wid,hei)
        checkbox.configure(text=f"Aspect Ratio - {ratio}")
        

    except Exception as e:
        print(e)
        default_img = Image.open(r"resources\drag-drop-try-again.png")
        default_img_tk = ImageTk.PhotoImage(default_img)
        default_image_label.configure(image=default_img_tk)
        default_image_label.image = default_img_tk
        resolutionLabel.configure(text="Sorry, invalid image")


# This function converte the image to custom resoltion using Pillow 
def convert():
    try:
        # Get the input image path
        get_input_path = default_image_label.image_path
        print(get_input_path)

        #Filepath validator
        input_path = Utils.file_path_validator(get_input_path)
        
        # Get the output folder path
        output_folder = os.path.join(os.path.dirname(input_path), "output")
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # Get the new height and width values entered by the user
        new_width = int(entryWidget_width.get())
        new_height = int(entryWidget_height.get())

        get_checkbox_aspect = checkbox_var.get()

        img = Image.open(input_path)
        hei = img.size[1]
        wid = img.size[0]

        if get_checkbox_aspect: #for true check
            print("hi siri")
            new_height_aspect = int((hei/wid)*new_width)
            img = img.resize((new_width,new_height_aspect), Image.BICUBIC)
        else: #for false check
            img = img.resize((new_width,new_height), Image.BICUBIC)
            

        # Open the input image and resize it
        #img = Image.open(input_path)
        #img = img.resize((new_width,new_height), Image.BICUBIC)
        
        # Save the resized image in the output folder with the same file name
        output_path = os.path.join(output_folder, os.path.basename(input_path))
        img.save(output_path)
        
        # Display the resized image in the GUI
        img_tk = ImageTk.PhotoImage(img)
        imageLabel.configure(image=img_tk)
        imageLabel.image = img_tk
        
        # Display the new image resolution
        resolutionLabel.configure(text=f"Resized : {new_width} x {new_height}")

        #Aspect ratio
        ratio = Utils.get_aspect_ratio(new_width,new_height)
        checkbox.configure(text=f"Aspect Ratio - {ratio}")

    except ValueError:
        #Invalid text
        resolutionLabel.configure(text="Please enter an integer value.")
        
    except Exception as e:
        print(e)
        imageLabel.configure(text=str(e))
        resolutionLabel.configure(text="Sorry, invalid image")


# GUI Framework Configurations
root = Tk()
root_x = 350
root_y = 450
ctk.set_appearance_mode("system")
root.geometry(f"{root_x}x{root_y}")
root.title("DnD Image Resizer")
root.iconbitmap(r"resources\root_icon.ico")

# Master Header
header_label = ctk.CTkLabel(master=root, text='Add image to resize', font=(None, 24))
header_label.pack(pady=20)

# Width input box
entryWidget_width = ctk.CTkEntry(master=root, placeholder_text="Enter Width")
entryWidget_width.pack(side=TOP, padx=5, pady=10)

# Height input box
entryWidget_height = ctk.CTkEntry(master=root, placeholder_text="Enter Height")
entryWidget_height.pack(side=TOP, padx=5, pady=10)

# Resize Btn
conv_button = ctk.CTkButton(master=root, text="Resize", command=convert)
conv_button.pack(pady=10)

# Temp. Check box to keep aspect ratio
checkbox_var = ctk.BooleanVar()  # create a variable to store the checkbox state
checkbox = ctk.CTkCheckBox(master=root, text=f"Keep Aspect Ratio", variable=checkbox_var)
checkbox.configure(checkbox_height=16, checkbox_width=16)
checkbox.pack(anchor="center")

# Load the default image file and create a PhotoImage object
default_img = Image.open(r"resources\drag-drop.png")
default_img = default_img.resize((150, 150), Image.BICUBIC)
default_img_tk = ImageTk.PhotoImage(default_img)

# Resolution Label to display the default image
default_image_label = ImageLabel(root, image=default_img_tk, width=150, height=150)
default_image_label.pack(side=TOP, pady=10)
default_image_label.image_path = ""

# Resolution Label to display the resolution
resolutionLabel = Label(root, text="-SiddharthSky-")
resolutionLabel.pack(side=TOP, pady=5)

# Create an Image label to display the new image
imageLabel = Label(root, width=150, height=150)
imageLabel.pack(side=TOP, pady=10)

# Make the label widget accept drops and bind the "Drop" event to the handle_drop() function
default_image_label.drop_target_register(DND_ALL)
default_image_label.dnd_bind('<<Drop>>', handle_drop)

# Running
root.mainloop()

