# Self-Driving-RC-Car
BEng (Hons) Computer & Electronic Engineering Final Year Project


### Dependencies
* Raspberry Pi: 
  - Picamera
  - OpenCV
* PCA9685 PWM Servo Driver
* Raspberry Pi Camera Module v2


### About
- neural_network/
  -	***alexnet.py***: AlexNet
  - ***collect_data.py***	Collect training images and controller values with USB Controller
  - ***frame.py***: Class for camera setup and edge detection image processing
  - ***playback_dataset.py***: Playback captured data from .npy file

- old_code/
  -	***capture_image.py***: Edge detection
  - ***data_collection_npy_10_percent.py***: Data collection to npy file in 10% value increments
  - ***faceDetectStaticImg.py***: Face detection on still images
  - ***houghLinesStillImage.py***: Edge detection and hough lines on still image
  - ***houghLinesVideoStream.py***: Edge detection and hough lines on video stream
  
- tests/
  -	***drive_with_controller.py***: Test to drive car with Xbox One controller
  
- threaded_app/
  -	***app.py***: Multithreaded app
  - ***frame.py***: Class for camera setup and edge detection image processing
