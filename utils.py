import math

class AspectRatio():
    def get(self,width,height):
        gcd = math.gcd(width, height)
        aspect_ratio_str = f"{int(width/gcd)}:{int(height/gcd)}"
        return aspect_ratio_str
    
class ConvertBTN():
    def __init__(self):
        pass



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