import cv2
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
 
# # Read the original image
# img = cv2.imread('hand1.png') 
# # Display original image
# # cv2.imshow('Original', img)
# # cv2.waitKey(0)
 
# # Convert to graycsale
# img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# # Blur the image for better edge detection
# img_blur = cv2.GaussianBlur(img_gray, (3,3), 0) 
 
# # Sobel Edge Detection
# sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5) # Sobel Edge Detection on the X axis
# sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5) # Sobel Edge Detection on the Y axis
# sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5) # Combined X and Y Sobel Edge Detection
# # Display Sobel Edge Detection Images
# # cv2.imshow('Sobel X', sobelx)
# # cv2.waitKey(0)
# # cv2.imshow('Sobel Y', sobely)
# # cv2.waitKey(0)
# # cv2.imshow('Sobel X Y using Sobel() function', sobelxy)
# # cv2.waitKey(0)
 
# # Canny Edge Detection
# edges = cv2.Canny(image=img_blur, threshold1=170, threshold2=300) # Canny Edge Detection
# xAxis, yAxis = np.nonzero(edges)
# print(min(yAxis))

# hand_lst = []
# for i in range(0, len(xAxis)):
#     hand_lst.append((xAxis[i], yAxis[i]))

# poly = Polygon(hand_lst)
# print(poly.contains(Point(50, 50)))

# #Display Canny Edge Detection Image
# # cv2.imshow('Canny Edge Detection', edges)
# # cv2.waitKey(0)

# cnts = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

 
# # cv2.destroyAllWindows()

import cv2

image = cv2.imread('hand_outline.png')
print(image.shape)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(gray, 120, 255, 1)
cnts = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

point1 = (25, 50)
point2 = (500, 800)
point3 = (700, 1000)

# Perform check if point is inside contour/shape
for c in cnts:
    cv2.drawContours(image, [c], -1, (36, 255, 12), 2)
    result1 = cv2.pointPolygonTest(c, point1, False)
    result2 = cv2.pointPolygonTest(c, point2, False)
    result3 = cv2.pointPolygonTest(c, point3, False)

# Draw points
cv2.circle(image, point1, 8, (100, 100, 255), -1)
cv2.putText(image, 'point1', (point1[0] -10, point1[1] -20), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), lineType=cv2.LINE_AA)
cv2.circle(image, point2, 8, (200, 100, 55), -1)
cv2.putText(image, 'point2', (point2[0] -10, point2[1] -20), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), lineType=cv2.LINE_AA)
cv2.circle(image, point3, 8, (150, 50, 155), -1)
cv2.putText(image, 'point3', (point3[0] -10, point3[1] -20), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), lineType=cv2.LINE_AA)

print('point1:', result1)
print('point2:', result2)
print('point3:', result3)
cv2.imshow('image', image)
cv2.waitKey()