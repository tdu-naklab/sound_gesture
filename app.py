# -*- coding: utf-8 -*-
import gesturegame
import cv2


def main():
    game = gesturegame.GestureGame()
    try:
        while True:
            screen = game.update()
            cv2.namedWindow("game", cv2.WINDOW_AUTOSIZE)
            cv2.imshow('game', screen)
            cv2.waitKey(1)

    finally:
        pass


if __name__ == "__main__":
    main()
