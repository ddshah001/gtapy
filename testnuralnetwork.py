import numpy as np
import cv2
import time
from draw_lanes import draw_lanes
from grabscreen import grab_screen
from getkeys import key_check
import os
from alexnet import alexnet
from directkeys import PressKey, ReleaseKey, W, A, S, D


WIDTH = 160
HEIGHT = 120
LR = 1e-3
EPOCHS = 10
MODEL_NAME = 'pygta5-car-fast-{}-{}-{}-epochs-300K-data.model'.format(LR,'alexnetv2',EPOCHS)

#pygta5-car-fast-0.001-alexnetv2-10-epochs-300K-data.model

def straight():
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(D)


def left():
    PressKey(A)
    PressKey(W)
    ReleaseKey(D)



def right():
    PressKey(D)
    PressKey(W)
    ReleaseKey(A)


model = alexnet(WIDTH,HEIGHT,LR)
model.load(MODEL_NAME)

def main():
    for i in list(range(4))[::-1]:
        print(i + 1)
        time.sleep(1)
    last_time = time.time()
    paused = False

    while True:
        if not paused:
            screen = grab_screen(region=(0, 40, 800, 640))
            screen = cv2.cvtColor(screen,cv2.COLOR_BGR2GRAY)
            screen = cv2.resize(screen,(160,120))

            print('Frame took {} seconds'.format(time.time() - last_time))
            last_time = time.time()

            prediction = model.predict([screen.reshape(WIDTH,HEIGHT,1)])[0]
            moves = list(np.around(prediction))
            print(moves, prediction)

            if moves == [1,0,0]:
                left()
            elif moves == [0,1,0]:
                straight()
            elif moves == [0,0,1]:
                right()

        keys = key_check()

        if 'T' in keys:
            if paused:
                paused = False
                time.sleep(1)
            else:
                paused = True
                ReleaseKey(A)
                ReleaseKey(W)
                ReleaseKey(D)
                time.sleep(1)


main()