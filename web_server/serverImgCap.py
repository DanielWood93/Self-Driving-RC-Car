from aiohttp import web
import socketio
from pca9685_driver import Device
from picamera.array import PiRGBArray
from picamera import PiCamera
import datetime
import cv2
import numpy as np

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)

# setup PCA9685
pwm = Device(0x40)
pwm.set_pwm_frequency(60)

# setup camera
##imageResolution = [320, 240]    # 320x240 camera resolution
imageResolution = [320, 120]    # 320x120 camera resolution
camera = PiCamera()
camera.resolution = (imageResolution[0], imageResolution[1])
camera.framerate = 30


def set_angle(channel, angle):
    pulse = (int(angle)*2.5) + 150
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


@sio.on('movement_event', namespace='/test')
async def movement_event(sid, steering, motor):
    #print("Start movement event: {}".format(datetime.datetime.utcnow()))
    file.write("{}, {}, {}\n".format(datetime.datetime.utcnow(), steering, motor))
    print("img_cap/{}, {}, {}.jpg".format(datetime.datetime.utcnow(), steering, motor))
    #process_frame(steering, motor)
    #print("Start capture image:  {}".format(datetime.datetime.utcnow()))
    camera.capture("img_cap/t:{}, s:{}, m:{}.jpg".format(datetime.datetime.utcnow(), steering, motor))	#400ms to save image, need to add threads
    set_angle(14, steering)
    set_angle(15, motor)
    #print("End movement event:   {}\n\n".format(datetime.datetime.utcnow()))
    


def process_frame(steering, motor):
    raw_capture = PiRGBArray(camera, size=(imageResolution[0], imageResolution[1]))
	
    #time_now = datetime.datetime.utcnow()
	
    camera.capture(raw_capture, format="bgr")
    image = raw_capture.array
	
    ##define region of interest (bottom half of frame)
    top_left = [0, int(imageResolution[1] / 2)]
    top_right = [int(imageResolution[0]), int(imageResolution[1] / 2)]
    bottom_left = [imageResolution[0], imageResolution[1]]
    bottom_right = [0, imageResolution[1]]
	
    greyscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	
    ##mask image
    vertices = [np.array([top_left, top_right, bottom_left, bottom_right], dtype=np.int32)]
    mask = np.zeros_like(greyscale_image)
    cv2.fillPoly(mask, vertices, 255)
    roi_image = cv2.bitwise_and(greyscale_image, mask)

    ##edge detection
    masked_white_image = cv2.inRange(roi_image, 200, 255)
    gaussian_blurred_image = cv2.GaussianBlur(masked_white_image, (5, 5), 0)
    canny_edges_image = cv2.Canny(gaussian_blurred_image, 50, 150)

    ##draw lines on top of image
    cv2.line(canny_edges_image, (160, 120), (160, 320), (255, 0, 255), 1)  # (b,g,r), horizontal center line
    cv2.line(canny_edges_image, (0, 120), (320, 120), (255, 0, 255), 1)  # (b,g,r), vertical center line
	
    cv2.imwrite("img_cap/t:{}, s:{}, m:{}.jpg".format(time_now, steering, motor), canny_edges_image)
	
	
	
	
def main():
    app.router.add_static('/static', 'static')
    app.router.add_get('/', index)
    app.router.add_static('/prefix', '/home/pi/webServer/static')    # static files for pi


if __name__ == '__main__':
    file_name = "dataset.txt"
    file = open(file_name, "a+")
    print("Opening ", file.name)
    print("Starting server.py..")
    main()
    web.run_app(app)
    camera.stop_recording()
    print("Closing ", file.name)
    file.close()
