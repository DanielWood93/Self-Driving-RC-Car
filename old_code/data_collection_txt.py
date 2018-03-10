from picamera.array import PiRGBArray  # camera
from picamera import PiCamera  # camera
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


def set_angle(channel, angle):
    """calculate servo angle"""
    pulse = (int(angle) * 2.5) + 150
    pwm.set_pwm(channel, int(pulse))

	
def save_data(current_id, csv, stream):
	current_id += 1
	csv.writerow([current_id, datetime.datetime.utcnow(), steering_angle, motor_angle])
	stream.save("{}{},{},{},{}.jpg".format(img_cap_location, current_id, datetime.datetime.utcnow(), steering_angle, motor_angle), processed)
	print("{}{},{},{},{}.jpg".format(img_cap_location, current_id, datetime.datetime.utcnow(), steering_angle, motor_angle))
	
	
# setup PCA9685 (servo driver)
pwm = Device(0x40)
pwm.set_pwm_frequency(60)

print("Data collection for NN, connect controller and drive around to collect data")
stream = frame.Frame(1, "SaveFrame")
stream.start()

steering_angle = 90
motor_angle = 133
time.sleep(1.0)

img_cap_location = "img_cap/"
csv_file = "dataset.csv"




with open(csv_file, "a+") as file:	
	file_reader = csv.reader(file)
	starting_id = len(list(file_reader))
	current_id = starting_id
	print("Current id set is: {}".format(current_id))
	#formatted_entry = "{},{},{},{}.jpg".format(current_id, datetime.datetime.utcnow(), steering_angle, motor_angle)
	csv = csv.writer(file)

	print("--Ready--")
	
	while 1:
		frame = stream.read()
		processed = stream.process(frame, (320, 240))
		key = cv2.waitKey(1) & 0xFF
		try:
			with ControllerResource(print_events=False, controller_class=None, hot_zone=0.1, dead_zone=0.1) as controller:
				print('Found a controller')
				while controller.connected:
					set_angle(14, steering_angle)
					set_angle(15, motor_angle)

					# left stick pressed (steering)
					if controller['lx'] != 0:
						stick_val = controller['lx']
						mapped_steering_value = int(map_value(stick_val, -1, 1, 120, 60))
						if mapped_steering_value != steering_angle:
							steering_angle = mapped_steering_value
							save_data(current_id, csv, stream)
							

					# left stick released (steering)
					if controller['lx'] == 0:
						steering_angle = 90
						

					# left trigger pressed (motor back)
					if controller['lt'] != 0:
						trigger_val = controller['lt']
						mapped_trigger_value = int(map_value(trigger_val, 0, 1, 133, 180))
						if mapped_trigger_value != motor_angle:
							motor_angle = mapped_trigger_value
							save_data(current_id, csv, stream)
							
					# left trigger released (motor)
					if controller['lt'] == 0:
						motor_angle = 133

						
					# right trigger pressed (motor forward)
					if controller['rt'] != 0:
						trigger_val = controller['rt']
						mapped_trigger_value = int(map_value(trigger_val, 0, 1, 133, 0))
						if mapped_trigger_value != motor_angle:
							motor_angle = mapped_trigger_value
							save_data(current_id, csv, stream)
							
					# right trigger released (motor)
					if controller['rt'] == 0:
						motor_angle = 133
						
											
					if controller['circle']:
						current_id = len(list(reader_file))
						print("Captured data from {} to {} ({} samples)".format(starting_id, current_id, starting_id-current_id))
						cv2.destroyAllWindows()
						stream.stop()
						print("Closing ", file.name)
						file.close()

						
				print('Controller disconnected!')
				
		except IOError:
			print('Waiting for controller...')
			sleep(1)	
	
	#current_id = len(list(reader_file))
	#print("Captured data from {} to {} ({} samples)".format(starting_id, current_id, starting_id-current_id))
	

cv2.destroyAllWindows()
stream.stop()
print("Closing ", file.name)
file.close()