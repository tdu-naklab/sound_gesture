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
t1 = time.time()
#sound1=pygame.mixer.Sound("/home/pcn004/Documents/sekkei/iemen.wav")        #効果音の設定
#sound2=pygame.mixer.Sound("/home/pcn004/Documents/sekkei/iizemen.wav")
#sound3=pygame.mixer.Sound("/home/pcn004/Documents/sekkei/respectmen.wav")
key = cv2.waitKey(60)&0xff
center_x = 0
center_y = 0
center_x1 = 600
center_y1 = 0
center_x2 = 0
center_y2 = 550
center_x3 = 600
center_y3 = 500


s1 = 100
s2 = 50
tokuten = 0
great = 0
good = 0
bad = 0
# ストリーミング開始
pipeline = rs.pipeline()
profile = pipeline.start(config)

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

        cv2.rectangle(color_image, (170, 90), (270, 190), (255,0,0),3)
        cv2.rectangle(color_image, (170, 290), (270, 390), (255,0,0),3)
        cv2.rectangle(color_image, (370, 90), (470, 190), (255,0,0),3)
        cv2.rectangle(color_image, (370, 290), (470, 390), (255,0,0),3)
        #cv2.circle(color_image, (220, 165), 50, (255, 0, 0), 5)
        #cv2.rectangle(color_image, (200, 200), (100, 100), (255,0,0),3)
        #cv2.rectangle(color_image, (400, 200), (500, 100), (255,0,0),3)
        #cv2.rectangle(color_image, (200, 400), (100, 300), (255,0,0),3)
        #cv2.rectangle(color_image, (400, 400), (500, 300), (255,0,0),3)
        cv2.putText(color_image, 'score', (225, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)
        cv2.putText(color_image, 'great', (225, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)
        cv2.putText(color_image, 'good', (230, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)        
        cv2.putText(color_image, 'bad', (250, 120), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)
        cv2.putText(color_image, str(tokuten), (330, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)
        cv2.putText(color_image, str(great), (330, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)
        cv2.putText(color_image, str(good), (330, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)        
        cv2.putText(color_image, str(bad), (330, 120), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)
        #edframe = RaFrame
        t2 = time.time()       


        if t2-t1 > 2:
            cv2.circle(color_image, (center_x, center_y), 30, (255, 0, 0), 5)
            center_x += 4
            center_y += 3       


        if key == ord('z'):
            cv2.rectangle(color_image, (170, 90), (270, 190), (255,255,0),-1)
            if center_x > 200 and center_x < 240:
                tokuten += 100
                great += 1
                center_x = 600
                center_y = 600
            if center_x > 170 and center_x < 199 or center_x > 241 and center_x < 270 :
                tokuten += 50
                good += 1            
                center_x = 600
                center_y = 600
            if center_x <= 170 and center_x >= 270:
                bad += 1            
                center_x = 600
                center_y = 600
            if t2-t1 == 10:
                break
        
        if t2-t1 > 3:
            cv2.circle(color_image, (center_x1, center_y1), 30, (255, 0, 0), 5)
            center_x1 -= 4
            center_y1 += 3    
        
        if key == ord('c'):
            cv2.rectangle(color_image, (370, 90), (470, 190), (255,255,0),-1)
            if center_x1 > 320 and center_x1 < 400:
                tokuten += 100
                great += 1
                center_x1 = 600
                center_y1 = 600
            if center_x1 >= 400 and center_x1 < 550 or center_x1 > 190 and center_x1 <= 320 :
                tokuten += 50
                good += 1            
                center_x1 = 600
                center_y1 = 600
            if center_x1 < 190 and center_x1 >= 550:
                bad += 1            
                center_x1 = 600
                center_y1 = 600
            if t2-t1 == 10:
                break

        if t2-t1 > 4:
            cv2.circle(color_image, (center_x2, center_y2), 30, (255, 0, 0), 5)
            center_x2 += 4
            center_y2 -= 3       


        if key == ord('x'):
            cv2.rectangle(color_image, (170, 290), (270, 390), (255,255,0),-1)
            if center_x2 > 170 and center_x2 < 270:
                tokuten += 100
                great += 1
                center_x2 = 600
                center_y2 = 550
            if center_x2 >= 150 and center_x2 <= 170 or center_x2 >= 270 and center_x2 < 290 :
                tokuten += 50
                good += 1            
                center_x2 = 600
                center_y2 = 550
            if center_x2 < 150 and center_x2 > 290:
                bad += 1            
                center_x2 = 600
                center_y2 = 550
            if t2-t1 == 10:
                break

        if t2-t1 > 5:
            cv2.circle(color_image, (center_x3, center_y3), 30, (255, 0, 0), 5)
            center_x3 -= 4
            center_y3 -= 3       


        if key == ord('s'):
            cv2.rectangle(color_image, (370, 290), (470, 390), (255,255,0),-1)
            if center_x3 > 370 and center_x3 < 470:
                tokuten += 100
                great += 1
                center_x3 = 700
                center_y3 = 0
            if center_x3 >= 350 and center_x2 <= 370 or center_x2 >= 470 and center_x2 < 500 :
                tokuten += 50
                good += 1            
                center_x3 = 700
                center_y3 = 0
            if center_x3 < 350 and center_x3 > 500:
                bad += 1            
                center_x3 = 700
                center_y3 = 0
            if t2-t1 == 10:
                break




       # if key == ord('s'):
          #  cv2.rectangle(color_image, (200, 200), (100, 100), (255,0,0),-1)
        #    cv2.rectangle(color_image, (400, 200), (500, 100), (255,0,0),-1)
         #   sound2.play()
            #t2 = time.time()
            #elapsed_time = t2-t1
            #print(elapsed_time)

        

        if key == ord('q'):


             break 
            
           
            
           
        
        images = np.hstack((color_image, depth_color_image))
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
         

        key = cv2.waitKey(1)&0xff
            
        if key == ord('q'):
            break
    time.sleep(0.01)

#得点の表示、greatで100点、goodで50点追加
    print("得点:" + str(tokuten))

finally:
    # ストリーミング停止
    pipeline.stop()
    cv2.destroyAllWindows()