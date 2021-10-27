import cv2
import numpy as np
import matplotlib.pyplot as plt

pathf = 'data/img3.png'

img = cv2.imread(pathf, cv2.IMREAD_COLOR)

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

img_gray_blur = cv2.blur(img_gray, (5,5))

detected_circles = cv2.HoughCircles(img_gray_blur,cv2.HOUGH_GRADIENT, 1, 20,
                                    param1 = 50, param2 = 30, minRadius = 1,
                                    maxRadius = 40)
if detected_circles is not None:
    detected_circles = np.uint16(np.around(detected_circles))

    for pt in detected_circles[0,:]:
        a, b, r = pt[0], pt[1], pt[2]

        cv2.circle(img,(a, b),r,(0,255,0),2)

        cv2.circle(img,(a, b),1,(0,0,255),3)
cv2.imwrite("imagem.png",img)
plt.imshow(img,"gray")
plt.show()