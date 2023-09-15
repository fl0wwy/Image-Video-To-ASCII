import cv2
from math import floor
import os

def load_video(path):
    cap = cv2.VideoCapture(path)

    if not cap.isOpened():
        raise Exception("Error opening file!")
    return cap

def resize_frame(image):
    max_width = 200
    max_height = 100

    # Calculate the new dimensions while preserving the aspect ratio
    width = image.shape[0]
    height = image.shape[1]
    if width > max_width or height > max_height:
        aspect_ratio = width / height
        if width > height:
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:
            new_height = max_height
            new_width = int(max_height * aspect_ratio)

    return cv2.resize(image, (new_width, new_height))  

def main(path, invert):
    # opening video and getting its fps
    video = load_video(path)
    video_fps = int(video.get(cv2.CAP_PROP_FPS))

    # pixel intensity to character converter
    ASCII_DENSITY = " ._-=+*#%@"
    def brightness_mapping(brightness, invert=invert):
        order = ASCII_DENSITY if invert == False else ASCII_DENSITY[::-1]
        length = len(order) - 1
        mapped_value = floor(brightness / 255 * length) 
        return order[mapped_value] 

    while True:
        # reading video frames
        ret, frame = video.read()
        if not ret:
            break
                
        # manipulating frames
        gray_scale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized_frame = resize_frame(gray_scale_frame)

        resize_dimensions = (resized_frame.shape[0], resized_frame.shape[1])

        #printing frames to console 
        os.system("cls") # clear console   
        for y in range(resize_dimensions[1]):
            line = []
            for x in range(resize_dimensions[0]):
                line.append(brightness_mapping(resized_frame[y, x], False))
            print("".join(line))     

        delay = int(1000 / video_fps) #running video according to its original fps
        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break
    
    video.release()

if __name__ == "__main__":
    path = input("video path: ")
    invert = input("invert? [y/n]:")
    invert = True if invert.lower() == "y" else False
    
    main(path, invert)