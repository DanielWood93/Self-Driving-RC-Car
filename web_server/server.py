from aiohttp import web
import socketio
from pca9685_driver import Device

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)


def set_angle(channel, angle):
    pulse = (int(angle)*2.5) + 150
    #print("angle=%s pulse=%s\n" % (angle, pulse))
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
    set_angle(14, angle)
    print("Steering val:  ", angle)


@sio.on('motor_event', namespace='/test')
async def motor_event(sid, angle):
    set_angle(15, angle)
    print("Motor value: ", angle)


app.router.add_static('/static', 'static')
app.router.add_get('/', index)
app.router.add_static('/prefix', '/home/pi/webServer/static')    # static files for webpage

# setup PCA9685
pwm = Device(0x40)
pwm.set_pwm_frequency(60)

if __name__ == '__main__':
    print("Starting server.py..")
    web.run_app(app)
