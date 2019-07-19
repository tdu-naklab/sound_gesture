# -*- coding: utf-8 -*-

#############################################
##      D415 Depth画像の表示&キャプチャ
#############################################
import pyrealsense2 as rs
import numpy as np
import cv2
import time
import pygame
from pygame.locals import*
import sys
pygame.init()

TARGET_DISTANCEMAX = 1.2
TARGET_DISTANCEMIN = 0.5
HEIGHT = 480
WIDTH = 640
DETECTION_DISTANCE_MAX=0.7
MEDIAN_KERNEL_SIZE = 9
GAUSSIAN_KERNEL_SIZE = 9

sound1=pygame.mixer.Sound("/home/endot/seisaku/m-art_ItemUse1.wav")		#効果音の設定

def generate_depth_binary_image(depth_image,max_dist):
    depth_filtered_image = (depth_image < max_dist) * depth_image
    depth_gray_filtered_image = (depth_filtered_image * 255. / max_dist).reshape((HEIGHT, WIDTH)).astype(np.uint8)
    ret, depth_binary_image = cv2.threshold(depth_gray_filtered_image, 1, 255, cv2.THRESH_BINARY)

    return depth_binary_image

def main():
    kernel = np.ones((5,5),np.uint8)
    # Configure depth and color streams
    align = rs.align(rs.stream.color)
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, WIDTH, HEIGHT, rs.format.z16, 60)
    config.enable_stream(rs.stream.color, WIDTH, HEIGHT, rs.format.bgr8, 60)
    
    # ストリーミング開始
    profile = pipeline.start(config)
    
    # Depthスケール取得
    # 距離[m] = depth * depth_scale 
    depth_sensor = profile.get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()
    # 対象範囲の閾値
    distance_max = TARGET_DISTANCEMAX/depth_scale
    distance_min = TARGET_DISTANCEMIN/depth_scale
    detection_distance_max=DETECTION_DISTANCE_MAX/depth_scale
    
    print('Depth Scale = {} -> {}'.format(depth_scale, distance_max))
    
    try:
        while True:
            # フレーム待ち(Depth & Color)
            frames = pipeline.wait_for_frames()
            aligned_frames = align.process(frames)
            depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()
            if not depth_frame or not color_frame:
                continue
            color_image = np.asanyarray(color_frame.get_data())

            # Depth画像をカラーで取得
            depth_color_frame = rs.colorizer().colorize(depth_frame)
            depth_color_image = np.asanyarray(depth_color_frame.get_data())
            depth_color_image = cv2.morphologyEx(depth_color_image, cv2.MORPH_CLOSE, kernel)
            depth_color_image = cv2.bilateralFilter(depth_color_image, 15, 20, 20)

            #深度二値化画像取得
            depth_image = np.asanyarray(depth_frame.get_data())
            depth_binary_image=generate_depth_binary_image(depth_image,detection_distance_max)

            depth_binary_image = cv2.medianBlur(depth_binary_image, MEDIAN_KERNEL_SIZE)
            depth_filtered_image = cv2.GaussianBlur(depth_binary_image, (GAUSSIAN_KERNEL_SIZE, GAUSSIAN_KERNEL_SIZE), 0)
            cv2.imshow("depth_filtered_image",depth_filtered_image)
            
            #30cm以内に物体が入る
            if ((depth_image < 300) & (depth_image > 0)).any():
                sound1.play(1)
                

                labels,label_images,object_data,center_pos=cv2.connectedComponentsWithStats(depth_filtered_image)
                for label in range(1,labels):
                    center_x,center_y = center_pos[label]
                    color_image = cv2.circle(color_image, (int(center_x),int(center_y)), 1, (0,0,255), -1)    
                    pos_x,pos_y,width,height,area_px = object_data[label]
                    color_image = cv2.rectangle(color_image, (pos_x,pos_y), (pos_x+width,pos_y+height), (255,255,0), 1)  
            
            else:
                print("not_hand")


            # 入力画像表示        
            images = np.hstack((color_image, depth_color_image))
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense', images)

            if cv2.waitKey(1) & 0xff == 27:
                break
    finally:
        # ストリーミング停止
        pipeline.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()