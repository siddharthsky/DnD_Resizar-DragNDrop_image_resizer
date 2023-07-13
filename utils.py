import math

class MasterUtils():
    def get_aspect_ratio(self,width,height):
        gcd = math.gcd(width, height)
        aspect_ratio_str = f"{int(width/gcd)}:{int(height/gcd)}"
        return aspect_ratio_str
    

    def file_path_validator(self,imgpath):
        try:
            #Filepath validator
            if "{" in imgpath and "}" in imgpath:
                    input_path = imgpath[1:-1]
            else:
                input_path = imgpath

            # Check if the input file is a supported image format
            image_formats = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".ico",".webp")
            if not input_path.lower().endswith(image_formats):
                raise ValueError("Invalid image file format")
            
            return input_path
        except Exception as e:
            print(e)