import cv2


def resize_image(image, desired_width):
    reduction = desired_width / image.shape[1]  # 640 / original image width
    dimensions = (int(desired_width), int(image.shape[0] * reduction))
    resized_image = cv2.resize(image, dimensions, interpolation=cv2.INTER_AREA)
    return resized_image


def process_frame(original_image, desired_width):
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
    return canny_edges_image


desiredImgWidth = 640.0
originalImg = cv2.imread('curved.jpg')
final_image = process_frame(originalImg, desiredImgWidth)
cv2.imshow("Image", final_image)
cv2.waitKey(0)
