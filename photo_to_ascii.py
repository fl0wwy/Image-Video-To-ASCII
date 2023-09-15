from PIL import Image
import matplotlib.pyplot as plt
from math import floor

# Decorator to display edited images
def preview(f):
    def wrapper(*args):
        image = f(*args)
        plt.imshow(image, cmap="gray")
        plt.axis("off")
        plt.show()
        return image
    return wrapper

@preview
def get_image(path):
    return Image.open(path)

#@preview
def resize_image(image):
    maximum_width = 200
    maximum_height = 100
    
    width, height = image.size
    if width > maximum_width or height > maximum_height:
        aspect_ratio = width / height
        if width > height:
            new_width = maximum_width
            new_height = int(maximum_width / aspect_ratio)
        else:
            new_height: maximum_height
            new_width = int(maximum_height * aspect_ratio)    

    return image.resize((new_width, new_height))

#@preview
def noir(image):
    return image.convert("L")

# pixel intensity to character converter
ASCII_DENSITY = " ._-=+*#%@"
def brightness_mapping(brightness, invert):
    order = ASCII_DENSITY if invert == False else ASCII_DENSITY[::-1]
    length = len(order) - 1
    mapped_value = floor(brightness / 255 * length) 
    return order[mapped_value] 

def main(path, invert=False):
    DEFAULT_IMG = get_image(path)
    
    # resizing and turing image into grayscale
    NOIR_IMG = noir(DEFAULT_IMG)
    resized_image = resize_image(NOIR_IMG)
    IMG_SIZE = resized_image.size

    for y in range(IMG_SIZE[1]):
        line = []
        for x in range(IMG_SIZE[0]):
            intensity = resized_image.getpixel((x,y)) # getting pixel intensity
            line.append(brightness_mapping(intensity, invert))
        print("".join(line))  

if __name__ == "__main__":
    path = input("Image path: ")
    
    invert = input("invert? [y/n]: ")
    invert = True if invert.lower() == "y" else False
    
    main(path, invert)