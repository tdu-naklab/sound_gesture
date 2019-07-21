# -*- coding: utf-8 -*-
import gesturegame


def main():
    game = gesturegame.GestureGame()
    try:
        while True:
            game.update()

    finally:
        pass


if __name__ == "__main__":
    main()
