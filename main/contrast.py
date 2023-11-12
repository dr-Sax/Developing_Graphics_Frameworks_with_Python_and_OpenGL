import cv2
import numpy as np
import glob
import os

img_array = []
file_array = []
base = f"C:/Users/nicor/.vscode/Developing_Graphics_Frameworks_with_Python_and_OpenGL/Visualizations_Frames/spiro/5_megan_5.24_0/frames/"
frame_cnt = len([entry for entry in os.listdir(base) if os.path.isfile(os.path.join(base, entry))])


for i in range(0, frame_cnt):
    file_array.append(base + str(i) + '.jpg')



for i in range(0, len(file_array)):
    img = cv2.imread(file_array[i], 1)

    # converting to LAB color space
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)

    # Applying CLAHE to L-channel
    # feel free to try different values for the limit and grid size:
    clahe = cv2.createCLAHE(clipLimit=10.0, tileGridSize=(20, 20))
    cl = clahe.apply(l_channel)

    def create_img(i, amp, phi):
        b1 = b + amp + int(10*np.sin(2*np.pi * i / 5 + phi))
        print(i)
        # merge the CLAHE enhanced L-channel with the a and b channel
        try:
            limg = cv2.merge((cl,a,b1))
        except:
            limg = cv2.merge((cl,a,b))

        # Converting image from LAB Color model to BGR color spcae
        enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        return enhanced_img
    
    img01 = create_img(i, 120, 0)
    img12 = create_img(i, 140, np.pi/2)
    img21 = create_img(i, 160, np.pi)
    img10 = create_img(i, 200, 3*np.pi/2)

    # Stacking the original image with the enhanced image
    
    r1 = np.hstack((img, img01, img))
    r2 = np.hstack((img10, img, img12))
    r3 = np.hstack((img, img21, img))

    result = np.vstack((r1, r2, r3))
    height, width, layers = result.shape
    size = (width,height)
    img_array.append(result)




out = cv2.VideoWriter(f'../Visualizations_Frames/spiro/5_megan_5.24_0/vout_contrast.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 10, size)

for i in range(len(img_array)):
    out.write(img_array[i])
out.release()