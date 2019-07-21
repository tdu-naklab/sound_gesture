# -*- coding: utf-8 -*-
import pyrealsense2 as rs
import numpy as np
import cv2
import pygame
import time


class GestureGame:
    # 定数
    HEIGHT = 480                    # 画像の縦サイズ
    WIDTH = 640                     # 画像の横サイズ
    FPS = 30                        # フレームレート
    TARGET_DISTANCE_MAX = 1.2
    TARGET_DISTANCE_MIN = 0.5
    DETECTION_DISTANCE_MAX = 0.7
    MEDIAN_KERNEL_SIZE = 9
    GAUSSIAN_KERNEL_SIZE = 9

    # コンストラクタ
    def __init__(self):
        # RealSenseの初期化
        self.__init_realsense()
        # ノーツ生成
        self.__notes = [Notes(100, 100),
                        Notes(500, 100),
                        Notes(100, 400),
                        Notes(500, 400)]

    # デストラクタ
    def __del__(self):
        pass

    # RealSenseの初期化
    def __init_realsense(self):
        # 初期化処理
        config = rs.config()
        config.enable_stream(rs.stream.color, self.WIDTH, self.HEIGHT, rs.format.bgr8, self.FPS)
        config.enable_stream(rs.stream.depth, self.WIDTH, self.HEIGHT, rs.format.z16, self.FPS)
        self.__pipeline = rs.pipeline()
        # 画角情報の取得
        self.__align = rs.align(rs.stream.color)
        # ストリーミング開始
        profile = self.__pipeline.start(config)

        depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()
        # 対象範囲の閾値
        self.__distance_max = self.TARGET_DISTANCE_MAX / depth_scale
        self.__distance_min = self.TARGET_DISTANCE_MIN / depth_scale
        self.__detection_distance_max = self.DETECTION_DISTANCE_MAX / depth_scale

    # フレームの取得
    def __get_camera_image(self):
        frames = self.__pipeline.wait_for_frames()  # フレーム取得
        aligned_frames = self.__align.process(frames)  # 画角補正
        # カラー画像のフレームと深度画像のフレームに分割
        color_frame = aligned_frames.get_color_frame()
        depth_frame = aligned_frames.get_depth_frame()
        # 深度画像のフレームを彩色
        depth_color_frame = rs.colorizer().colorize(depth_frame)

        # フレームからカラー画像を生成
        color_image = np.asanyarray(color_frame.get_data())
        # フレームから深度画像を生成
        depth_image = np.asanyarray(depth_frame.get_data())
        # フレームから彩色した深度画像を生成
        depth_color_image = np.asanyarray(depth_color_frame.get_data())
        depth_color_image = cv2.morphologyEx(depth_color_image, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))  # モルフォロジー処理
        depth_color_image = cv2.bilateralFilter(depth_color_image, 15, 20, 20)  # バイラテラルフィルタ

        return color_image, depth_image, depth_color_image

    # 深度画像の二値化処理
    def __generate_depth_binary_image(self, depth_image, max_dist):
        # 一定距離以下の画素のみ抽出する
        depth_filtered_image = (depth_image < max_dist) * depth_image
        # 0~255に値を収める
        depth_filtered_image = (depth_filtered_image*255./max_dist).reshape((self.HEIGHT, self.WIDTH)).astype(np.uint8)
        # 画像を二値化
        ret, depth_binary_image = cv2.threshold(depth_filtered_image, 1, 255, cv2.THRESH_BINARY)
        depth_binary_image = cv2.medianBlur(depth_binary_image, self.MEDIAN_KERNEL_SIZE)  # メディアンフィルタ

        return depth_binary_image

    # フレームごとの更新処理
    def update(self):
        # 画像を取得
        color_image, depth_image, depth_color_image = self.__get_camera_image()
        # 深度画像を二値化処理
        depth_binary_image = self.__generate_depth_binary_image(depth_image, self.__detection_distance_max)

        game_screen = color_image  # ゲーム画面

        # ノーツ更新
        for note in self.__notes:
            game_screen = note.update(game_screen)

        cv2.namedWindow("demo2", cv2.WINDOW_AUTOSIZE)
        cv2.imshow('demo2', game_screen)
        cv2.waitKey(1)


# ノーツ
class Notes:
    # コンストラクタ
    def __init__(self, pos_x, pos_y):
        self.__pos_x = pos_x
        self.__pos_y = pos_y

    # デストラクタ
    def __del__(self):
        pass

    # ノーツの更新処理
    def update(self, game_screen):
        # アイコン描画
        cv2.rectangle(game_screen,
                      (self.__pos_x-15, self.__pos_y-15),
                      (self.__pos_x+15, self.__pos_y+15),
                      (0, 255, 0),
                      thickness=-1)

        return game_screen
