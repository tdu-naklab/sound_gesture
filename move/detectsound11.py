# -*- coding: utf-8 -*-

#############################################
##      D415 Depth画像の表示&キャプチャ
#############################################
import pyrealsense2 as rs
import numpy as np
import cv2
import pygame
from pygame.locals import*
import sys
import time
#import time
TARGET_DISTANCEMAX = 1.2
TARGET_DISTANCEMIN = 0.5
HEIGHT = 480
WIDTH = 640
DETECTION_DISTANCE_MAX=0.7
MEDIAN_KERNEL_SIZE = 9
GAUSSIAN_KERNEL_SIZE = 9
flag = 0
#otodasu.py
pygame.init()
count=4
pygame.mixer.set_num_channels(count)
sound1=pygame.mixer.Sound("/home/endot/seisaku/m-art_Extra2.wav")        #効果音の設定
sound2=pygame.mixer.Sound("/home/endot/seisaku/m-art_ItemUse1.wav")
sound3=pygame.mixer.Sound("/home/endot/seisaku/m-art_Magic3.wav")
sound4=pygame.mixer.Sound("/home/endot/seisaku/respectmen.wav")

left_up_x=100 #左上x
left_up_y=100 #左上y

right_up_x=500 #右上x
right_up_y=100 #右上y

left_down_x=100 #左下x
left_down_y=400 #左下y

right_down_x=500 #右下x
right_down_y=400 #右下y





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
    #時間計測開始
    time_sta = time.time()
    s1 = 100
    s2 = 50
    tokuten = 0
    center_x4 = 0
    center_y4 = 0
    center_x1 = 600
    center_y1 = 0
    center_x2 = 0
    center_y2 = 550
    center_x3 = 600
    center_y3 = 500
    great = 0
    good = 0
    bad = 0
    t1 = time.time()
    tt1 = time.time()
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
            
            """cv2.putText(color_image, 'score', (225, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)
            cv2.putText(color_image, 'great', (225, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)
            cv2.putText(color_image, 'good', (230, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)        
            cv2.putText(color_image, 'bad', (250, 120), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)
            #cv2.putText(color_image, str(tokuten), (330, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)
            cv2.putText(color_image, str(great), (330, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)
            cv2.putText(color_image, str(good), (330, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)        
            cv2.putText(color_image, str(bad), (330, 120), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)
            """
         





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

            cv2.rectangle(color_image,(left_up_x,left_up_y),(left_up_x+30,left_up_y+30),(0,255,0),thickness=-1)
            cv2.rectangle(color_image,(right_up_x,right_up_y),(right_up_x+30,right_up_y+30),(0,255,0),thickness=-1)
            cv2.rectangle(color_image,(left_down_x,left_down_y),(left_down_x+30,left_down_y+30),(0,255,0),thickness=-1)
            cv2.rectangle(color_image,(right_down_x,right_down_y),(right_down_x+30,right_down_y+30),(0,255,0),thickness=-1)
            t2 = time.time()
            tt2 = time.time()
            
            if t2-t1 > 2:
                cv2.circle(color_image, (center_x4, center_y4), 30, (255, 0, 0), 5)
                center_x4 += 2
                center_y4 += 2 
                if center_x4 == 210:
                    center_x4 = 0
                    center_y4 = 0
            
            
            if tt2-tt1 > 3:
                cv2.circle(color_image, (center_x1, center_y1), 30, (255, 0, 0), 5)
                center_x1 -= 2
                center_y1 += 2 
                if center_x1 == 350:
                    center_x1 = 600
                    center_y1 = 0

            if t2-t1 > 4:
                cv2.circle(color_image, (center_x2, center_y2), 30, (255, 0, 0), 5)
                center_x2 += 2
                center_y2 -= 2
                if center_x2 == 210:
                    center_x2 = 0
                    center_y2 = 550

            if t2-t1 > 5:
                cv2.circle(color_image, (center_x3, center_y3), 30, (255, 0, 0), 5)
                center_x3 -= 2
                center_y3 -= 2 
                if center_x3 == 350:
                    center_x3 = 600
                    center_y3 = 550

            
                #70cm以内に物体が入る
            if ((depth_image < 700) & (depth_image > 0)).any():
                
                labels,label_images,object_data,center_pos=cv2.connectedComponentsWithStats(depth_filtered_image)
                for label in range(1,labels):
                    center_x,center_y = center_pos[label]
                    color_image = cv2.circle(color_image, (int(center_x),int(center_y)), 1, (0,0,255), -1)
                    pos_x,pos_y,width,height,area_px = object_data[label]
                    color_image = cv2.rectangle(color_image, (pos_x,pos_y), (pos_x+width,pos_y+height), (255,255,0), 1)

                    data=np.where(depth_filtered_image == 255,True,False)

                    for k in range(left_up_y,left_up_y+30):
                        for l in range(left_up_x,left_up_x+30):
                            if data[k,l]==True:
                                cv2.rectangle(color_image, (left_up_x,left_up_y),(left_up_x+30,left_up_y+30), (0,0,255),-1)
                                speaker1 = pygame.mixer.Channel(0)

                                if speaker1.get_busy()!=True:
                                    speaker1.play(sound1)
                                    print("play sound1")
                                    #tokuten = tokuten + s1
                                    if center_x4 > 100 and center_x4 < 130:
                                        tokuten += 100
                                        great += 1
                                        center_x4 = 0
                                        center_y4 = 0
                                    if center_x4 > 0 and center_x4 <= 100 or center_x4 > 130 and center_x4 < 200 :
                                        tokuten += 50
                                        good += 1            
                                        center_x4 = 0
                                        center_y4 = 0
                                    
                                   
                                    
                
                                #else:
                                    #print("spekaer1_is_busy")

                    for k in range(right_up_y,right_up_y+30):
                        for l in range(right_up_x,right_up_x+30):
                            if data[k,l]==True:
                                
                                cv2.rectangle(color_image, (right_up_x,right_up_y),(right_up_x+30,right_up_y+30), (0,255,255),-1)
                                speaker2 = pygame.mixer.Channel(1)
                                
                                if speaker2.get_busy()!=True:
                                    speaker2.play(sound2)
                                    print("play sound2")
                                    #tokuten = tokuten + s1
                                    if center_x1 > 500 and center_x1 < 530:
                                        tokuten += 100
                                        great += 1
                                        center_x1 = 600
                                        center_y1 = 0
                                    if center_x1 >= 400 and center_x1 < 500 or center_x1 > 530 and center_x1 <= 560 :
                                        tokuten += 50
                                        good += 1            
                                        center_x1 = 600
                                        center_y1 = 0
                        
                                   
                                                               #else:
                                    #print("spekaer2_is_busy")

                    for k in range(left_down_y,left_down_y+30):
                        for l in range(left_down_x,left_down_x+30):
                            if data[k,l]==True:
                                cv2.rectangle(color_image, (left_down_x,left_down_y),(left_down_x+30,left_down_y+30), (255,255,0),-1)
                                speaker3 = pygame.mixer.Channel(2)
                                
                                if speaker3.get_busy()!=True:
                                    speaker3.play(sound3)
                                    print("play sound3")
                                    #tokuten = tokuten + s1
                                    if center_x2 > 100 and center_x2 < 130:
                                        tokuten += 100
                                        great += 1
                                        center_x2 = 0
                                        center_y2 = 550
                                    if center_x2 >= 50 and center_x2 <= 100 or center_x2 >= 130 and center_x2 < 230 :
                                        tokuten += 50
                                        good += 1            
                                        center_x2 = 0
                                        center_y2 = 550
                                    
                                    #print("spekaer3_is_busy")

                    for k in range(right_down_y,right_down_y+30):
                        for l in range(right_down_x,right_down_x+30):
                            if data[k,l]==True:
                                cv2.rectangle(color_image, (right_down_x,right_down_y),(right_down_x+30,right_down_y+30), (255,0,0),-1)
                                speaker4 = pygame.mixer.Channel(3)
                                
                                if speaker4.get_busy()!=True:
                                    speaker4.play(sound4)
                                    print("play sound4")
                                    #tokuten = tokuten + s1
                                    if center_x3 > 500 and center_x3 < 530:
                                        tokuten += 100
                                        great += 1
                                        center_x3 = 600
                                        center_y3 = 550
                                    if center_x3 >= 400 and center_x3 <= 500 or center_x3 >= 530 and center_x3 < 560 :
                                        tokuten += 50
                                        good += 1            
                                        center_x3 = 600
                                        center_y3 = 550
                            
                               #else:
                                    #print("spekaer4_is_busy")
           
        


            else:
                print("not_hand")
            
            

            # 入力画像表示

            color_image = cv2.flip(color_image,1)
            cv2.putText(color_image, 'score', (225, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)
            cv2.putText(color_image, 'great', (225, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)
            cv2.putText(color_image, 'good', (230, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)        
            cv2.putText(color_image, 'bad', (250, 120), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)
            cv2.putText(color_image, str(tokuten), (330, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)
            cv2.putText(color_image, str(great), (330, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)
            cv2.putText(color_image, str(good), (330, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)        
            cv2.putText(color_image, str(bad), (330, 120), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)

            
            
            images = np.hstack((color_image, depth_color_image))
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense', images)

            if cv2.waitKey(1) & 0xff == 27:
                break
            #得点の表示、greatで100点、goodで50点追加
        print("得点:" + str(tokuten))
    finally:
        # ストリーミング停止
        pipeline.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()