import cv2
import numpy as np
import glob

img_array = []
file_array = []
base = 'C:/Users/nicor/.vscode/Developing_Graphics_Frameworks_with_Python_and_OpenGL/lotus/'
for i in range(0, 16):
    file_array.append(base + str(i) + '.jpg')


print(file_array)
for filename in file_array:
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)




out = cv2.VideoWriter('lotus.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 2, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()