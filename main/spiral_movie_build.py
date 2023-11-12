import cv2
import numpy as np
import glob

img_array = []
for filename in glob.glob('C:/Users/nicor/.vscode/Developing_Graphics_Frameworks_with_Python_and_OpenGL/spiral/*.jpg'):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)


out = cv2.VideoWriter('spiral.mp4v',cv2.VideoWriter_fourcc(*'MP4V'), 60, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()