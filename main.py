import os
import threading
from queue import Queue, Empty, Full

import boto3
import cv2
import pyglet
from PIL import Image
from pyglet import shapes
from pyglet.media import StaticSource, load
from pyglet.window import key

#############
# AWS call

ACCESS_KEY = os.getenv('AWS_ACCESS_KEY', "# enter your key here #")
SECRET_KEY = os.getenv('AWS_SECRET_KEY', "# enter your key here #")

client = boto3.client(
    'rekognition',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)

queue = Queue(1)
score = 0


def requester():
    global score

    thread = threading.currentThread()
    while getattr(thread, "do_run", True):
        try:
            image = queue.get(timeout=1)
        except Empty:
            continue

        print("Processing...", end='')
        smiling = is_smile(image)

        if smiling:
            score += 1
            up_sound.play()

        print(smiling, score)


def is_smile(image):
    is_success, buffer = cv2.imencode(".png", image)
    if not is_success:
        print("Encoding Failed")
        return False

    result = client.detect_faces(
        Image={'Bytes': buffer.tobytes()},
        Attributes=['ALL']
    )

    if not result['FaceDetails']:
        return False

    for face in result['FaceDetails']:
        return face['Smile']['Value']

    return False


##########
# AUDIO

up_sound = StaticSource(load('smw_coin_nrom.wav'))

###########
#  GUI

window = pyglet.window.Window()
score_label = pyglet.text.Label('Score: ',
                          font_name='DungGeunMo',
                          font_size=48,
                          x=30, y=30,
                          color=(22, 80, 192, 255))

hold_label = pyglet.text.Label('!! HOLD !!',
                          font_name='DungGeunMo',
                          font_size=48,
                          x=160, y=200,
                          color=(255, 200, 200, 255))

screen = shapes.Rectangle(0,0, 640, 480, color=(0,0,0))
screen.opacity = 200

hold_mode = False

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.ESCAPE:
        print('Application Exited with Key Press')
        window.close()

    if symbol == key.ENTER:
        global score
        score = 0
        score_label.text = f'Score: {score}'
        score_label.draw()

    if symbol == key.SPACE:
        global hold_mode
        hold_mode = not hold_mode



@window.event
def on_draw():
    score_label.text = f'Score: {score}'
    score_label.draw()

    if hold_mode:
        screen.draw()
        hold_label.draw()


def cv2glet(img):
    """Assumes image is in BGR color space. Returns a pyimg object"""
    rows, cols, channels = img.shape
    raw_img = Image.fromarray(img).tobytes()

    top_to_bottom_flag = -1
    bytes_per_row = channels * cols
    pyimg = pyglet.image.ImageData(width=cols,
                                   height=rows,
                                   format='BGR',
                                   data=raw_img,
                                   pitch=top_to_bottom_flag * bytes_per_row)
    return pyimg


def update(_):
    ret, img = camera.read()
    if not ret:
        return

    try:
        if not hold_mode:
            queue.put_nowait(img)

    except Full:
        pass

    cv2glet(cv2.flip(img, 1)).blit(0, 0)


# Entry point
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if __name__ == '__main__':
    requester_thread = threading.Thread(target=requester)
    requester_thread.start()

    pyglet.clock.schedule_interval(update, 1 / 60)
    pyglet.app.run()

    requester_thread.do_run = False
    requester_thread.join()
