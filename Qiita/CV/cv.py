import cv2


img = cv2.imread('images/image.jpg',flags=cv2.IMREAD_COLOR)
img2 = cv2.rectangle(img,pt1=(319,122),pt2=(1168,775),color=(0,255,0),thickness=2)
cv2.imshow('image',img2)
cv2.waitKey(0)