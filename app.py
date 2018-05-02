"""Main app for Self-Driving RC Car Project

Setup and load model, read processed frames from stream and process with edge detection, feed processed image into
placeholder to reshape into into 4D tensor, continuously run predictions using placeholder, set direction of rc car

partly modified from: github.com/tensorflow/tensorflow/blob/master/tensorflow/examples/label_image/label_image.py
to accept numpy image array instead of .jpg files, uses a placeholder for numpy array in reshape_array_and_read_tensor()
"""

import RPi.GPIO as GPIO     # raspberry pi GPIO
import tensorflow as tf
import numpy as np
import time
import threading
import logging
import frame    # my frame module, for image processing
import drive    # my drive module, for controlling motors
import ultrasonic   # my ultrasonic module, for measuring distance


def load_graph(model):
    """load graph from model file

    Args:
        model (.pb model): trained model to load
    Returns:
        graph (tensorflow graph): graph from model
    """
    logging.info("load_graph: {}".format(model))
    graph = tf.Graph()
    graph_def = tf.GraphDef()
    with open(model, "rb") as f:
        graph_def.ParseFromString(f.read())
    with graph.as_default():
        tf.import_graph_def(graph_def)
    return graph


def reshape_array_and_read_tensor():
    """Reshape image array into a 4-D Tensor of [batch, height, width, channels]

    create a placeholder for an image array of shape [120, 320]
    add channels, convert to rgb, add batch size, resize image data to [224,224]
    which will be from [height(120), width(320)] -> [batch(1), height(120), width(320), channels(3)]
    which is expected shape for image data tensor to be fed into graph

    Returns:
        normalized (tensorflow Tensor): which is Tensor("truediv:0", shape=(1, 224, 224, 3), dtype=float32)
    """
    logging.info('reshape_array_and_read_tensor')
    numpy_array_placeholder = tf.placeholder("float32", name="numpy_img_arr", shape=[120, 320])
    add_channels = tf.expand_dims(numpy_array_placeholder, 2)   # Tensor("ExpandDims:0", shape=(120, 320, 1), dtype=float32)
    rgb_image = tf.image.grayscale_to_rgb(add_channels)         # Tensor("grayscale_to_rgb:0", shape=(120, 320, 3), dtype=float32))
    add_batch = tf.expand_dims(rgb_image, 0)                    # Tensor("ExpandDims_1:0", shape=(1, 120, 320, 3), dtype=float32)
    resized = tf.image.resize_bilinear(add_batch, [224, 224])   # Tensor("ResizeBilinear:0", shape=(1, 224, 224, 3), dtype=float32)
    normalized = tf.divide(tf.subtract(resized, [0]), [255])    # Tensor("truediv:0", shape=(1, 224, 224, 3), dtype=float32)
    return normalized


# for logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
)

stream = frame.Frame(1, "Frame")    # setup stream from Frame class
car = drive.Drive(2, 'Drive')       # setup car motors from Drive class
ultrasonic = ultrasonic.Ultrasonic(3, "Ultrasonic", 23, 24)  # setup distance sensor from Ultrasonic class

car.car_stopped()   # stop motors

# setup model
model_file = "mobilenet_v2_graph.pb"    # model file to use
input_height = 224  # image height expected in the model
input_width = 224   # image width expected in the model
input_mean = 0      # mean per channel
input_std = 255     # standard deviation associated
input_layer = "Placeholder"
output_layer = "final_result"
graph = load_graph(model_file)  # load the graph from the model file
input_name = "import/" + input_layer
output_name = "import/" + output_layer
input_operation = graph.get_operation_by_name(input_name)
output_operation = graph.get_operation_by_name(output_name)

labels = ['left', 'forward', 'right']   # output labels
stream.start()
ultrasonic.start()
time.sleep(1)

logging.info('Start app')
try:
    with tf.Session(graph=graph) as sess:
        logging.info('tf.Session(graph=graph) as sess')
        tensor_with_input_placeholder = reshape_array_and_read_tensor()

        while True:
            original_frame = stream.read()   # read frame from stream
            edge_detection_image = stream.process(original_frame)    # edge detection on frame

            # feed edge detection image data from stream into placeholder numpy_img_arr:0
            t = sess.run(tensor_with_input_placeholder, feed_dict={"numpy_img_arr:0": edge_detection_image})
            results = sess.run(output_operation.outputs[0], {input_operation.outputs[0]: t})

            results = np.squeeze(results)
            top_prediction = results.argsort()[-3:][::-1]  # [-3:] is last 3, then [::-1] to reverse list
            direction_dict = {'left': [1, 0, 0], 'forward': [0, 1, 0], 'right': [0, 0, 1]}
            direction = labels[top_prediction[0]]
            best_prediction = direction_dict[labels[top_prediction[0]]]
            accuracy = results[top_prediction[0]]
            print("prediction: {} {} {:.2%}".format(best_prediction, direction, accuracy))

            if ultrasonic.measure() > 10:   # measure distance and set direction of car
                if best_prediction == [1, 0, 0]:
                    car.drive_left()
                elif best_prediction == [0, 1, 0]:
                    car.drive_forward()
                elif best_prediction == [0, 0, 1]:
                    car.drive_right()
            else:
                car.car_stopped()
                print("Object detected")


except KeyboardInterrupt:
    car.car_stopped()   # stop motors
    logging.info('KeyboardInterrupt')
    GPIO.cleanup()  # cleanup GPIO ports after use
    logging.info('Exiting')
    exit()
