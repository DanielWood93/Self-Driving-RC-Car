import cv2


def resize_image(image, desired_width):     # resize images from a given desired width
    reduction = desired_width / image.shape[1]  # desired width / original image width
    dimensions = (int(desired_width), int(image.shape[0] * reduction))
    resized_image = cv2.resize(image, dimensions, interpolation=cv2.INTER_AREA)
    return resized_image


def process_frame(original_image, desired_width):   # detect edges in an image
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


def show_demo():    # show edge detection demo on an image
    original_img = cv2.imread('img/T.jpg')
    final_image = process_frame(original_img, desiredImgWidth)
    cv2.imshow("Image", final_image)
    cv2.waitKey(0)


def process_all_images(input_folder, output_folder, num_of_images):
    for image_num in range(1, num_of_images+1):
        file_name = "(" + str(image_num) + ")" + ".jpg"
        original_img = cv2.imread(input_folder + file_name)
        final_image = process_frame(original_img, desiredImgWidth)
        print "Output file: " + output_folder + str(image_num) + ".jpg"
        cv2.imwrite(output_folder + str(image_num) + ".jpg", final_image)


desiredImgWidth = 640.0
inputFolder = "C:\Users\danie\Desktop\FYP\Tape_Track\originals\\"
outputFolder = "C:\Users\danie\Desktop\FYP\Tape_Track\edge_detection\\"

#show_demo()    # show single image demo

process_all_images(inputFolder, outputFolder, 196)  # process 196 images
