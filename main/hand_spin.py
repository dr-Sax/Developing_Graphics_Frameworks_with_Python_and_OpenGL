import cv2
import numpy as np
import glob
import os

img_array = []
file_array = []
base = f"C:/Users/nicor/.vscode/Developing_Graphics_Frameworks_with_Python_and_OpenGL/Visualizations_Frames/hex_hand/"
frame_cnt = len([entry for entry in os.listdir(base) if os.path.isfile(os.path.join(base, entry))])


def funcRotate(degree, img):
    height, width, layers = img.shape
    rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), degree, 1)
    rotated_image = cv2.warpAffine(img, rotation_matrix, (width, height))
    return rotated_image

def zoom_center(img, zoom_factor=1.5):

    y_size = img.shape[0]
    x_size = img.shape[1]
    
    # define new boundaries
    x1 = int(0.5*x_size*(1-1/zoom_factor))
    x2 = int(x_size-0.5*x_size*(1-1/zoom_factor))
    y1 = int(0.5*y_size*(1-1/zoom_factor))
    y2 = int(y_size-0.5*y_size*(1-1/zoom_factor))

    # first crop image then scale
    img_cropped = img[y1:y2,x1:x2]
    return cv2.resize(img_cropped, None, fx=zoom_factor, fy=zoom_factor)

for i in range(0, frame_cnt):
    file_array.append(base + str(i) + '.jpg')



for i in range(0, len(file_array)):
    img = cv2.imread(file_array[i], 1)
    result = funcRotate(180, img)
    result = funcRotate(360 * i / frame_cnt, result)
    result = zoom_center(result, zoom_factor= 1 + abs(np.sin(np.pi * i / frame_cnt)))
    height, width, layers = result.shape
    size = (width,height)
    img_array.append(result)




out = cv2.VideoWriter(f'../Visualizations_Frames/vids/spin_hand.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 10, size)

for i in range(len(img_array)):
    out.write(img_array[i])
out.release()