from aiohttp import web
import socketio
from pca9685_driver import Device
from picamera.array import PiRGBArray
from picamera import PiCamera
import datetime
import cv2

# PWM Channel 14 - Steering Servo, 90 center, 91 left, 89 right 
# PWM Channel 15 - Motor Servo, 133 center, 134 forward, 132 back  


# socketio setup
sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)

# set angle of a servo
def set_angle(channel, angle):
    pulse = (int(angle)*2.5) + 150
    # print("angle=%s pulse=%s\n" % (angle, pulse))
    pwm.set_pwm(channel, int(pulse))


async def index(request):
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


@sio.on('connect', namespace='/test')
async def test_connect(sid, environ):
    await sio.emit('my response', {'data': 'Connected', 'count': 0}, room=sid,
                   namespace='/test')


@sio.on('disconnect', namespace='/test')
def test_disconnect(sid):
    print('Client disconnected')


@sio.on('disconnect request', namespace='/test')
async def disconnect_request(sid):
    await sio.disconnect(sid, namespace='/test')


@sio.on('steering_event', namespace='/test')
async def steering_event(sid, angle):
    set_angle(14, angle)	# set steering servo angle
    if(int(angle) >= 91): # greater than or equal to 91 is left
        raw_capture = PiRGBArray(camera, size=(imageResolution[0], imageResolution[1]))
        camera.capture(raw_capture, format="bgr")
        cv2.imwrite("img_cap/" + str(datetime.datetime.utcnow()) + "_left_" + angle + ".jpg", process_frame(raw_capture.array))	# edge detection
        #cv2.imwrite("img_cap/" + str(datetime.datetime.utcnow()) + "_left_" + angle + ".jpg", raw_capture.array)	# normal image
        print("Steering val (left):  ", angle)
		
    if(int(angle) <= 89): # less than or equal to 89 is right
        raw_capture = PiRGBArray(camera, size=(imageResolution[0], imageResolution[1]))
        camera.capture(raw_capture, format="bgr")
        cv2.imwrite("img_cap/" + str(datetime.datetime.utcnow()) + "_right_" + angle + ".jpg", process_frame(raw_capture.array))	# edge detection
        #cv2.imwrite("img_cap/" + str(datetime.datetime.utcnow()) + "_right_" + angle + ".jpg", raw_capture.array)	# normal image
        print("Steering val (right):  ", angle)
		
    if(int(angle) == 90): # 90 is centered
        raw_capture = PiRGBArray(camera, size=(imageResolution[0], imageResolution[1]))
        camera.capture(raw_capture, format="bgr")
        cv2.imwrite("img_cap/" + str(datetime.datetime.utcnow()) + "_steering_centered_" + angle + ".jpg", process_frame(raw_capture.array))	# edge detection
        #cv2.imwrite("img_cap/" + str(datetime.datetime.utcnow()) + "_steering_centered_" + angle + ".jpg", raw_capture.array)	# normal image
        print("Steering val (centered):  ", angle)

		
@sio.on('motor_event', namespace='/test')
async def motor_event(sid, angle):
    set_angle(15, angle)
    if(int(angle) >= 134): # greater than or equal to 134 is forward
        raw_capture = PiRGBArray(camera, size=(imageResolution[0], imageResolution[1]))
        camera.capture(raw_capture, format="bgr")
        cv2.imwrite("img_cap/" + str(datetime.datetime.utcnow()) + "_forward_" + str(angle) + ".jpg", process_frame(raw_capture.array))	# edge detection
        #cv2.imwrite("img_cap/" + str(datetime.datetime.utcnow()) + "_forward_" + str(angle) + ".jpg", raw_capture.array)	# normal image
        print("Motor value (forward): ", angle)
		
    if(int(angle) <= 132): # less than or equal to 132 is back
        raw_capture = PiRGBArray(camera, size=(imageResolution[0], imageResolution[1]))
        camera.capture(raw_capture, format="bgr")
        cv2.imwrite("img_cap/" + str(datetime.datetime.utcnow()) + "_back_" + str(angle) + ".jpg", process_frame(raw_capture.array))	# edge detection
        #cv2.imwrite("img_cap/" + str(datetime.datetime.utcnow()) + "_back_" + str(angle) + ".jpg", raw_capture.array)	# normal image
        print("Motor value (back): ", angle)
		
    if(int(angle) == 133):  # 133 is centered
        raw_capture = PiRGBArray(camera, size=(imageResolution[0], imageResolution[1]))
        camera.capture(raw_capture, format="bgr")
        cv2.imwrite("img_cap/" + str(datetime.datetime.utcnow()) + "_motor_centered_" + str(angle) + ".jpg", process_frame(raw_capture.array))	# edge detection
        #cv2.imwrite("img_cap/" + str(datetime.datetime.utcnow()) + "_motor_centered_" + str(angle) + ".jpg", raw_capture.array)	# normal image
        print("Motor value (centered): ", angle)


def process_frame(original_image):   # detect edges in an image
    # convert to greyscale
    greyscale_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    # mask pixels that are not white
    masked_white_image = cv2.inRange(greyscale_image, 200, 255)
    # apply gaussian blur to image
    gaussian_blurred_image = cv2.GaussianBlur(masked_white_image, (5, 5), 0)
    # use canny edges
    canny_edges_image = cv2.Canny(gaussian_blurred_image, 50, 150)
    center_line_image = cv2.line(canny_edges_image, (320, 0), (320, 480), (255, 0, 0), 5)   #white, black,
    #return canny_edges_image
    return center_line_image		
		
		
# setup pi camera
imageResolution = [320, 240]    # 320x240 camera resolution
camera = PiCamera()
camera.resolution = (imageResolution[0], imageResolution[1])
camera.framerate = 30	# set framerate to 30fps


# setup PCA9685 (servo controller)
pwm = Device(0x40)
pwm.set_pwm_frequency(60)

app.router.add_static('/static', 'static')
app.router.add_get('/', index)
app.router.add_static('/prefix', '/home/pi/webServer/static')    # static files for running on pi
# app.router.add_static('/prefix', 'C:\\Users\\danie\\PycharmProjects\\untitled1\\web_server')    # static files for running on laptop


if __name__ == '__main__':
    print("Starting server.py..")
    web.run_app(app)
