# -*- coding: utf-8 -*-

#############################################
##      D415 Depth画像の表示
#############################################
import pyrealsense2 as rs
import numpy as np
import cv2
import pygame
from pygame.locals import*
import sys
import time

pygame.init()
# ストリーム(Color/Depth)の設定
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

#pygame.mixer.music.load("/home/endot/seisaku/adventurers.WAV")       #BGM再生
#pygame.mixer.music.play(-1)

sound1=pygame.mixer.Sound("/home/endot/seisaku/m-art_Extra2.wav")		#効果音の設定
sound2=pygame.mixer.Sound("/home/endot/seisaku/m-art_ItemUse1.wav")
sound3=pygame.mixer.Sound("/home/endot/seisaku/m-art_Magic3.wav")



# ストリーミング開始
pipeline = rs.pipeline()
profile = pipeline.start(config)
#t1 = time.time() 
time_sta = time.time()
try:
    while True:
        # フレーム待ち(Color & Depth)
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        if not depth_frame or not color_frame:
            continue
        color_image = np.asanyarray(color_frame.get_data())
        # Depth画像
        depth_color_frame = rs.colorizer().colorize(depth_frame)
        depth_color_image = np.asanyarray(depth_color_frame.get_data())
        
        cv2. imshow('Raw Frame', color_image)
        
        cv2.rectangle(color_image, (200, 200), (100, 100), (255,0,0),3)
        cv2.rectangle(color_image, (400, 200), (500, 100), (255,0,0),3)
        cv2.rectangle(color_image, (200, 400), (100, 300), (255,0,0),3)
        cv2.rectangle(color_image, (400, 400), (500, 300), (255,0,0),3)
        
        #edframe = RaFrame


        
        key = cv2.waitKey(60)&0xff

        if key == ord('f'):
            t1 = time.time()
            cv2.rectangle(color_image, (200, 200), (100, 100), (255,255,0),-1)
        
        #３秒経過で表示
        #if t1 == 3:
        #    cv2.rectangle(color_image, (200, 200), (100, 100), (255,255,0),-1)
        #    cv2.rectangle(color_image, (200, 200), (100, 100), (255,120,255),-1)

        if key == ord('g'):
            
            t2 = time.time()
           
            
            elapsed_time = t2-t1
            print(elapsed_time)
            if elapsed_time > 1:
                cv2.rectangle(color_image, (200, 200), (100, 100), (255,120,255),-1)
                cv2.putText(color_image, 'bad', (200, 170), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)
                sound2.play()

            if elapsed_time < 0.5:
                cv2.rectangle(color_image, (200, 200), (100, 100), (255,0,255),-1)
                cv2.putText(color_image, 'great', (200, 170), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)
                sound1.play()

            if  1 > elapsed_time > 0.5:
                cv2.rectangle(color_image, (200, 200), (100, 100), (255,0,0),-1)
                cv2.putText(color_image, 'good', (200, 170), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)
                sound3.play()



        if key == ord('w'):
             cv2.rectangle(color_image, (200, 200), (100, 100), (255,0,0),-1)
             sound1.play()
             
             
       
        if key == ord('s'):
            cv2.rectangle(color_image, (200, 200), (100, 100), (255,0,0),-1)
            cv2.rectangle(color_image, (400, 200), (500, 100), (255,0,0),-1)
            sound2.play()
            #t2 = time.time()
            #elapsed_time = t2-t1
            #print(elapsed_time)

        if key == ord('x'):
            cv2.rectangle(color_image, (400, 200), (500, 100), (255,0,0),-1)
            sound3.play()

        if key == ord('q'):

             break 
           
            
           
        
        images = np.hstack((color_image, depth_color_image))
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
         

        key = cv2.waitKey(1)&0xff
            
        if key == ord('q'):
            break

 
 


finally:
    # ストリーミング停止
    pipeline.stop()
    cv2.destroyAllWindows()