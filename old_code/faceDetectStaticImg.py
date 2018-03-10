import numpy as np
import cv2
import matplotlib.pyplot as plt
import time


def convertToRGB(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

	
def detect_faces(f_cascade, colored_img, scaleFactor=1.1):
    img_copy = np.copy(colored_img)
    # convert the test image to gray image as opencv face detector expects gray images
    gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

    # let's detect multiscale (some images may be closer to camera than others) images
    faces = f_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=5);

    # go over list of faces and draw them as rectangles on original colored img
    for (x, y, w, h) in faces:
        cv2.rectangle(img_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return img_copy


def faceDetectAndSave(img_file):
    currentImg = cv2.imread('data/' + img_file)
    print('loaded image: ' + img_file)
    img_with_faces_detected = detect_faces(lbp_face_cascade, currentImg)
    plt.imshow(convertToRGB(img_with_faces_detected))
    savedImgName = 'result_of_' + img_file
    cv2.imwrite(savedImgName, img_with_faces_detected)
    print('saved: ' + savedImgName)


lbp_face_cascade = cv2.CascadeClassifier('data/lbpcascade_frontalface.xml')
faceDetectAndSave('test_img_1.jpg')
faceDetectAndSave('test_img_2.jpg')
faceDetectAndSave('test_img_3.jpg')


