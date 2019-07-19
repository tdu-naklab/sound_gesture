# -*- coding: utf-8 -*-
import cv2
import numpy as np
from PIL import Image,ImageDraw


size = (400,400)
while True:
    # print(center_x)
    #中心座標(200,200),半径50、青色の円,先の太さが３
    img = np.zeros((400,400, 3))
    key = cv2.waitKey(0)&0xff
    cv2.imshow("img",img)

    #左上
    if key == ord('a'):
        center_x = 0
        center_y = 0
        while True:
            img = np.zeros((400,400, 3))
            cv2.circle(img, (center_x, center_y), 30, (255, 0, 0), 5)
            cv2.imshow('reftup',img)
            center_x += 1
            center_y += 1
            cv2.waitKey(1)
            if center_x == 400:
                break
    cv2.destroyWindow('reftup')
    if key == 27:
        break
    #右上
    if key == ord('b'):
        center_x = 400
        center_y = 0
        while True:
            img = np.zeros((400,400, 3))
            cv2.circle(img, (center_x, center_y), 50, (255, 0, 0), 5)
            cv2.imshow('rightup',img)
            center_x -= 1
            center_y += 1
            cv2.waitKey(1)
            if center_x == 0:
                break
    cv2.destroyWindow('rightup')
    if key == 13:
        break
    #右下
    if key == ord('c'):
        center_x = 400
        center_y = 400
        while True:
            img = np.zeros((400,400, 3))
            cv2.circle(img, (center_x, center_y), 50, (255, 0, 0), 5)
            cv2.imshow('rightdown',img)
            center_x -= 1
            center_y -= 1
            cv2.waitKey(1)
            if center_x == 0:
                break
    cv2.destroyWindow('rightdown')
    if key == 13:
        break
    #左下
    if key == ord('d'):
        center_x = 0
        center_y = 400
        while True:
            img = np.zeros((400,400, 3))
            cv2.circle(img, (center_x, center_y), 50, (255, 0, 0), 5)
            cv2.imshow('leftdown',img)
            center_x += 1
            center_y -= 1
            cv2.waitKey(1)
            if center_x == 400:
                break
    cv2.destroyWindow('leftdown')
    if key == 13:
        break
cv2.destroyAllWindows()