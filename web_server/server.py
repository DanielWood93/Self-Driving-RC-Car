from aiohttp import web
import socketio
from pca9685_driver import Device
from picamera.array import PiRGBArray
from picamera import PiCamera
import datetime
import cv2


sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)


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
    # 90 is center
    # 120 is
    # 60 is
    set_angle(14, angle)
    if(angle > 91): # greater than 91
        print("left")
        raw_capture = PiRGBArray(camera, size=(imageResolution[0], imageResolution[1]))
        cv2.imwrite("img_cap/" + datetime.datetime.utcnow() + "_left_" + angle + ".jpg", raw_capture)
    if(angle < 89): # less than 89
        print("right")
        raw_capture = PiRGBArray(camera, size=(imageResolution[0], imageResolution[1]))
        cv2.imwrite("img_cap/" + datetime.datetime.utcnow() + "_right_" + angle + ".jpg", raw_capture)
    print("Steering val:  ", angle)


@sio.on('motor_event', namespace='/test')
async def motor_event(sid, angle):
    # 74 is center
    # 120 is forward
    # 60 is back
    # set_angle(15, angle)
    if(angle > 75): # greater than 75
        print("forward")
        raw_capture = PiRGBArray(camera, size=(imageResolution[0], imageResolution[1]))
        cv2.imwrite("img_cap/" + datetime.datetime.utcnow() + "_forward_" + angle + ".jpg", raw_capture)
    if(angle < 73): # less than 73
        print("back")
        raw_capture = PiRGBArray(camera, size=(imageResolution[0], imageResolution[1]))
        cv2.imwrite("img_cap/" + datetime.datetime.utcnow() + "_back_" + angle + ".jpg", raw_capture)
    print("Motor value: ", angle)


# setup camera
imageResolution = [320, 240]    # 320x240 camera resolution
camera = PiCamera()
camera.resolution = (imageResolution[0], imageResolution[1])
camera.framerate = 30

# setup PCA9685
pwm = Device(0x40)
pwm.set_pwm_frequency(60)

app.router.add_static('/static', 'static')
app.router.add_get('/', index)
app.router.add_static('/prefix', '/home/pi/webServer/static')    # static files for pi
# app.router.add_static('/prefix', 'C:\\Users\\danie\\PycharmProjects\\untitled1\\web_server')    # static files for laptop


if __name__ == '__main__':
    print("Starting server.py..")
    web.run_app(app)
