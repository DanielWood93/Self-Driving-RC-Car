import numpy as np
import cv2


def resize_image(image, desired_width):     # resize images from a given desired width
    reduction = desired_width / image.shape[1]  # desired width / original image width
    dimensions = (int(desired_width), int(image.shape[0] * reduction))
    resized_image = cv2.resize(image, dimensions, interpolation=cv2.INTER_AREA)
    return resized_image


def process_frame(original_image, desired_width):   # detect edges and draw hough lines
    # resize image
    resized_image = resize_image(original_image, desired_width)

    # convert to greyscale
    greyscale_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    # mask pixels that are not white
    masked_white_image = cv2.inRange(greyscale_image, 200, 255)
    # apply gaussian blur to image
    gaussian_blurred_image = cv2.GaussianBlur(masked_white_image, (5, 5), 0)
    # use canny edges
    canny_edges_image = cv2.Canny(gaussian_blurred_image, 50, 150)

    # region of interest points, (0,0 is top left)
    top_left = [240, 240]
    top_right = [400, 240]
    bottom_left = [640, 480]
    bottom_right = [0, 480]
    # mask image
    vertices = [np.array([top_left, top_right, bottom_left, bottom_right], dtype=np.int32)]
    mask = np.zeros_like(canny_edges_image)
    cv2.fillPoly(mask, vertices, 255)
    roi_image = cv2.bitwise_and(canny_edges_image, mask)

    # draw lines
    lines = cv2.HoughLinesP(roi_image, 2, np.pi/180, 20, np.array([]), minLineLength=50, maxLineGap=200)
    hough_lines_image = np.zeros((roi_image.shape[0], roi_image.shape[1], 3), dtype=np.uint8)

    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(hough_lines_image, (x1, y1), (x2, y2), [255, 0, 0], 5)

    result = cv2.addWeighted(hough_lines_image, 1, resized_image, 1, 0.)

    return result
    #return hough_lines_image


desiredImgWidth = 640.0
#originalImg = cv2.imread('img/curved.jpg')
#originalImg = cv2.imread('img/corner.jpg')
originalImg = cv2.imread('img/T.jpg')

final_image = process_frame(originalImg, desiredImgWidth)
cv2.imshow("Image", final_image)
cv2.waitKey(0)

# save images
#cv2.imwrite("gray_image.jpg", gray_image)
#cv2.imwrite("gauss_gray.jpg", gauss_gray)
#cv2.imwrite("canny_edges.jpg", canny_edges)
#cv2.imwrite("houghLines.jpg", line_image)
