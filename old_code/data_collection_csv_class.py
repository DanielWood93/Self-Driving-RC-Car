from picamera.array import PiRGBArray  # camera
from picamera import PiCamera  # camera
from threading import Thread
import cv2
import time
import datetime
from time import sleep
from approxeng.input.selectbinder import ControllerResource  # for controller
from pca9685_driver import Device  # for servo driver
import frame  # for image processing
import csv


def map_value(val, low1, high1, low2, high2):
    """map values between controller and servo angle"""
    new_value = low2 + (high2 - low2) * (val - low1) / (high1 - low1)
    return new_value


class DataCapture:
    def __init__(self, thread_id, name):
        self.thread_id = thread_id
        self.name = name
        # setup PCA9685 (servo driver)
        self.pwm = Device(0x40)
        self.pwm.set_pwm_frequency(60)
        self.stream = frame.Frame(1, "SaveFrame")	# new thread
        self.stream.start()							#start thread

        self.steering_angle = 90
        self.motor_angle = 133
        self.img_cap_location = "img_cap/"
		
        self.csv_file = "dataset.csv"
        #self.npy_file = "dataset.npy"
		

        #print("From init: Data collection for NN, connect controller and drive around to collect data")
        print("From init: ThreadId: {}, Name: {}".format(self.thread_id, self.name))

    def start(self):
        Thread(target=self.gather_data(), args=()).start()
        return self

    def set_angle(self, channel, angle):
        """calculate servo angle"""
        pulse = (int(angle) * 2.5) + 150
        self.pwm.set_pwm(channel, int(pulse))

    def save_data(self, current_id, csv_writer, stream, processed):
        """save image to dir and save data to csv file"""
        current_id += 1
        csv_writer.writerow([current_id, datetime.datetime.utcnow(), self.steering_angle, self.motor_angle])
        stream.save("{}{},{},{},{}.jpg".format(self.img_cap_location, current_id, datetime.datetime.utcnow(), self.steering_angle, self.motor_angle), processed)
        print("{}{},{},{},{}.jpg".format(self.img_cap_location, current_id, datetime.datetime.utcnow(), self.steering_angle, self.motor_angle))

    def flatten_img(self, image):
        """flatten image to array"""
        return image.flatten()
        np.savetxt(file, flat, fmt="%s")


    #def process_dataset(self):
        #for(i, imagepath) in enumerate(imagepaths):

    def gather_data(self):
        with open(self.csv_file, "a+") as file:
            csv_reader = csv.reader(file)
            csv_writer = csv.writer(file)
            starting_id = len(list(csv_reader))
            current_id = starting_id
            print("Current id set is: {}".format(current_id))
            print("--Ready--")

            while 1:
                current_frame = self.stream.read()
                processed = self.stream.process(current_frame, (320, 240))
                key = cv2.waitKey(1) & 0xFF
                try:
                    with ControllerResource(print_events=False, controller_class=None, hot_zone=0.1,
                                            dead_zone=0.1) as controller:
                        print('Found a controller')
                        self.set_angle(14, steering_angle)
                        self.set_angle(15, motor_angle)
                        while controller.connected:
                            #self.set_angle(14, steering_angle)
                            #self.set_angle(15, motor_angle)

                            # left stick pressed (steering)
                            if controller['lx'] != 0:
                                stick_val = controller['lx']
                                mapped_steering_value = int(map_value(stick_val, -1, 1, 120, 60))
                                if mapped_steering_value != steering_angle:
                                    steering_angle = mapped_steering_value
                                    self.save_data(current_id, csv_writer, self.stream, processed)

                            # left stick released (steering)
                            if controller['lx'] == 0:
                                steering_angle = 90

                            # left trigger pressed (motor back)
                            if controller['lt'] != 0:
                                trigger_val = controller['lt']
                                mapped_trigger_value = int(map_value(trigger_val, 0, 1, 133, 180))
                                if mapped_trigger_value != motor_angle:
                                    motor_angle = mapped_trigger_value
                                    self.save_data(current_id, csv_writer, self.stream, processed)

                            # left trigger released (motor)
                            if controller['lt'] == 0:
                                motor_angle = 133

                            # right trigger pressed (motor forward)
                            if controller['rt'] != 0:
                                trigger_val = controller['rt']
                                mapped_trigger_value = int(map_value(trigger_val, 0, 1, 133, 0))
                                if mapped_trigger_value != motor_angle:
                                    motor_angle = mapped_trigger_value
                                    self.save_data(current_id, csv_writer, self.stream, processed)

                            # right trigger released (motor)
                            if controller['rt'] == 0:
                                motor_angle = 133

                            if controller['circle']:
                                print("Stopping collection")
                                self.stream.stop()

                        print('Controller disconnected!')

                except IOError:
                    print('Waiting for controller...')
                    sleep(1)

    def stop(self):
        current_id = len(list(self.reader_file))
        print("Captured data from {} to {} ({} samples)".format(self.starting_id, current_id, self.starting_id-current_id))
        cv2.destroyAllWindows()
        self.stream.stop()
        print("Closing ", self.file.name)
        self.file.close()


def main():
    #print("From main: Threaded prepare frames to file")
    dc = DataCapture(1, "DataCapture")
    dc.start()


if __name__ == '__main__':
    main()
