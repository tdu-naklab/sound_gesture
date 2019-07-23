# -*- coding: utf-8 -*-
import pyrealsense2 as rs
import numpy as np
import cv2
import pygame
import time


# ゲーム本体
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
        self.__notes = [Note(np.array([self.WIDTH / 2 - 150, self.HEIGHT / 2 - 100]),  # アイコンの座標
                             np.array([0, 0])),                                        # ノートの出現位置
                        Note(np.array([self.WIDTH / 2 + 150, self.HEIGHT / 2 - 100]),
                             np.array([self.WIDTH, 0])),
                        Note(np.array([self.WIDTH / 2 - 150, self.HEIGHT / 2 + 100]),
                             np.array([0, self.HEIGHT])),
                        Note(np.array([self.WIDTH / 2 + 150, self.HEIGHT / 2 + 100]),
                             np.array([self.WIDTH, self.HEIGHT]))]

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
        color_image = cv2.flip(np.asanyarray(color_frame.get_data()), 1)
        # フレームから深度画像を生成
        depth_image = cv2.flip(np.asanyarray(depth_frame.get_data()), 1)
        # フレームから彩色した深度画像を生成
        depth_color_image = cv2.flip(np.asanyarray(depth_color_frame.get_data()), 1)

        # フィルタ処理
        # depth_color_image = cv2.morphologyEx(depth_color_image, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))  # モルフォロジー処理
        # depth_color_image = cv2.bilateralFilter(depth_color_image, 15, 20, 20)  # バイラテラルフィルタ

        return color_image, depth_image, depth_color_image

    # 深度画像の二値化処理
    def __generate_depth_binary_image(self, depth_image, max_dist):
        # 一定距離以下の画素のみ抽出する
        depth_filtered_image = (depth_image < max_dist) * depth_image
        # 0~255に値を収める
        depth_filtered_image = (depth_filtered_image*255./max_dist).reshape((self.HEIGHT, self.WIDTH)).astype(np.uint8)
        # 画像を二値化
        ret, depth_binary_image = cv2.threshold(depth_filtered_image, 1, 255, cv2.THRESH_BINARY)
        # depth_binary_image = cv2.medianBlur(depth_binary_image, self.MEDIAN_KERNEL_SIZE)  # メディアンフィルタ

        return depth_binary_image

    # フレームごとの更新処理
    def update(self):
        # 画像を取得
        color_image, depth_image, depth_color_image = self.__get_camera_image()
        # 深度画像を二値化処理
        depth_binary_image = self.__generate_depth_binary_image(depth_image, self.__detection_distance_max)
        # depth_binary_image = cv2.GaussianBlur(depth_binary_image, (self.GAUSSIAN_KERNEL_SIZE, self.GAUSSIAN_KERNEL_SIZE), 0)

        # 画面表示用画像の定義
        game_screen = color_image  # ゲーム画面
        depth_binary_screen = cv2.cvtColor(depth_binary_image, cv2.COLOR_GRAY2BGR)  # 二値化した深度画像

        # ラベリング処理(cv2.connectedComponentsWithStats)
        #   - labels: ラベル総数
        #   - label_images: 各画素のラベル番号が入った配列
        #   - object_data: 各オブジェクトの詳細が入った配列[x, y, h, w, size]
        #   - center_pos: 重心座標(float)
        labels, label_images, object_data, center_pos = cv2.connectedComponentsWithStats(depth_binary_image)

        # ラベリング結果を画面に表示
        for label in range(1, labels):
            # 中心点を描画
            depth_binary_screen = cv2.circle(depth_binary_screen, tuple(center_pos[label].astype('int32')), 1, (0, 0, 255), -1)
            game_screen = cv2.circle(game_screen, tuple(center_pos[label].astype('int32')), 1, (0, 0, 255), -1)
            # 矩形の描画
            pos_x, pos_y, width, height, area_px = object_data[label]
            depth_binary_screen = cv2.rectangle(depth_binary_screen, (pos_x, pos_y), (pos_x + width, pos_y + height), (255, 255, 0), 1)
            game_screen = cv2.rectangle(game_screen, (pos_x, pos_y), (pos_x + width, pos_y + height), (255, 255, 0), 1)

        # 二値画像にラベリング結果をオーバーレイして表示
        cv2.namedWindow('labeled_binary', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('labeled_binary', depth_binary_screen)

        # ノーツ更新
        for note in self.__notes:
            note.generate()
            game_screen = note.update(game_screen, labels, label_images, object_data, center_pos)

        return game_screen


# ノート
class Note:
    notes_count = 0  # ノート総数

    # コンストラクタ
    def __init__(self, icon_pos, note_init_pos):
        self.__note_id = Note.notes_count
        Note.notes_count += 1  # ノート総数を加算

        self.__icon_pos = np.copy(icon_pos)  # アイコン座標の設定
        self.__note_init_pos = np.copy(note_init_pos.astype('float64'))  # ノートの出現位置の設定
        self.__note_pos = np.copy(self.__note_init_pos)  # ノート位置初期化

        # ノートの移動する目的座標 (出現位置とアイコン間のベクトルの2倍に指定)
        self.__destination_pos = self.__note_init_pos + (self.__icon_pos - self.__note_init_pos) * 2

        self.__start_time = time.time()  # 初期時間の取得

        self.__note_is_active = False  # ノートを非アクティブ化

    # 判定処理
    def __judge(self, labels, label_images, object_data, center_pos):
        # 押されなかった場合
        if np.linalg.norm(self.__note_pos - self.__note_init_pos) > np.linalg.norm(self.__icon_pos-self.__note_init_pos) * 1.5:
            self.destroy()

    # ノートを表示する
    def generate(self):
        # ノートが非アクティブな場合
        if self.__note_is_active is False:
            self.__note_pos = np.copy(self.__note_init_pos)  # ノーツ位置初期化
            self.__note_is_active = True  # ノーツをアクティブにする

    # ノートを非表示にする
    def destroy(self):
        # ノートがアクティブな場合
        if self.__note_is_active is True:
            self.__note_is_active = False  # ノーツを非アクティブにする

    # ノートの更新処理
    def update(self, game_screen, labels, label_images, object_data, center_pos):
        # アイコン描画
        cv2.rectangle(game_screen,
                      (int(self.__icon_pos[0])-15, int(self.__icon_pos[1])-15),
                      (int(self.__icon_pos[0])+15, int(self.__icon_pos[1])+15),
                      (0, 255, 0),
                      thickness=-1)

        # ノートがアクティブな場合，ノートの更新を行う
        if self.__note_is_active is True:
            # ノートの判定処理
            self.__judge(labels, label_images, object_data, center_pos)

            # ノートが移動するベクトルを計算
            move_vec = self.__destination_pos - self.__note_pos
            move_vec = move_vec / np.linalg.norm(move_vec)  # 正規化
            move_vec *= 3  # 移動量

            self.__note_pos += move_vec  # ノートを移動

            cv2.circle(game_screen, tuple(self.__note_pos.astype('int32')), 30, (255, 0, 0), 5)  # ノートを描画

        return game_screen

    # note_is_activeのゲッター
    @property
    def is_active(self):
        return self.__note_is_active
