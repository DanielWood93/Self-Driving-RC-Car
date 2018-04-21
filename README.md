# Self-Driving-RC-Car
BEng (Hons) Computer & Electronic Engineering Final Year Project


### Dependencies
* Raspberry Pi: 
  - Picamera
  - OpenCV
  - Numpy
* PCA9685 PWM Servo Driver
* Raspberry Pi Camera Module v2


### About
- data_collection/
  - ***dataset_jpg/***: For samples converted to .jpg images
      - ***forward/***
      - ***left/***
      - ***right/***
  - ***datasets/*** : Created datasets
  -	***augment_samples.py***: Agument dataset samples by mirroring images and labels
  -	***balance_dataset.py***: Balance numpy dataset to get an even number of samples for each direction label
  -	***collect_data.py***: Use USB controller to collect dataset containing images and labels as a numpy file
  -	***convert_to_jpg.py***: Convert images from numpy array to .jpg images
  -	***join_datasets.py***: Join multiple numpy datasets together
  -	***playback_dataset.py***: Playback captured data from numpy file
  -	***relabel_dataset.py***: Relabel dataset samples
  -	***sort_gui.py***: GUI for viewing, sorting and relableing samples
  -	***sort_gui_support.py***:  GUI for viewing, sorting and relableing samples

- old_code/
  -	***capture_image.py***: Edge detection
  - ***data_collection_npy_10_percent.py***: Data collection to npy file in 10% value increments
  - ***faceDetectStaticImg.py***: Face detection on still images
  - ***houghLinesStillImage.py***: Edge detection and hough lines on still image
  - ***houghLinesVideoStream.py***: Edge detection and hough lines on video stream
  
- tests/
  -	***drive_with_controller.py***: Test to drive car with Xbox One controller
  
-	***app.py***: Main app to drive car autonomously
-	***drive.py***: Class for controling direction of car
- ***frame.py***: Class for camera setup and edge detection image processing
-	***ultrasonic.py***: Class for ultrasonic distance sensor setup and distance measurement
