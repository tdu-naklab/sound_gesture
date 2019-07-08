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
TARGET_DISTANCEMAX = 1.2
TARGET_DISTANCEMIN = 0.5
HEIGHT = 480
WIDTH = 640
DETECTION_DISTANCE_MAX=0.7
MEDIAN_KERNEL_SIZE = 9
GAUSSIAN_KERNEL_SIZE = 9

#背景合成用
THRESHOLD = 1.5  # これより遠い距離の画素を無視する
BG_PATH1 = "/home/pcd0002/realsense_composite_demo/src/image/ginga.jpg"  # 背景画像のパス
BG_PATH2 = "/home/pcd0002/realsense_composite_demo/src/image/road.png"
BG_PATH3 = "/home/pcd0002/realsense_composite_demo/src/image/sky.png"
BG_PATH4 = "/home/pcd0002/realsense_composite_demo/src/image/green.png"

#otodasu.py
pygame.init()
count=4
pygame.mixer.set_num_channels(count)
sound1=pygame.mixer.Sound("/home/pcd0002/realsense_composite_demo/src/iemen.wav")        #効果音の設定
sound2=pygame.mixer.Sound("/home/pcd0002/realsense_composite_demo/src/wassamen.wav")
sound3=pygame.mixer.Sound("/home/pcd0002/realsense_composite_demo/src/iizemen.wav")
sound4=pygame.mixer.Sound("/home/pcd0002/realsense_composite_demo/src/respectmen.wav")

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

    
    
    #背景合成用
    max_dist = THRESHOLD/depth_scale
    bg_image1 = cv2.imread(BG_PATH1, cv2.IMREAD_COLOR)
    bg_image2 = cv2.imread(BG_PATH2, cv2.IMREAD_COLOR)
    bg_image3 = cv2.imread(BG_PATH3, cv2.IMREAD_COLOR)
    bg_image4 = cv2.imread(BG_PATH4, cv2.IMREAD_COLOR)
    


    print('Depth Scale = {} -> {}'.format(depth_scale, distance_max))
    flag = 1
    FLAG = 1
    

    try:
        while True:
      
            # フレーム待ち(Depth & Color)

            frames = pipeline.wait_for_frames()
            aligned_frames = align.process(frames)
            depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()

            if not depth_frame or not color_frame:
                continue
            #color_image = np.asanyarray(color_frame.get_data())
            image_color = np.asanyarray(color_frame.get_data())

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


            #kokokara
            # 指定距離以上を無視した深度画像
            depth_image = np.asanyarray(depth_frame.get_data())
            depth_filtered_image2 = (depth_image < max_dist) * depth_image
            depth_gray_filtered_image = (depth_filtered_image2 * 255. / max_dist).reshape((HEIGHT, WIDTH)).astype(np.uint8)
            ret, depth_mask = cv2.threshold(depth_gray_filtered_image, 1, 255, cv2.THRESH_BINARY)
            depth_mask = cv2.medianBlur(depth_mask, MEDIAN_KERNEL_SIZE)
            depth_mask = cv2.GaussianBlur(depth_mask, (GAUSSIAN_KERNEL_SIZE, GAUSSIAN_KERNEL_SIZE), 0)
            depth_mask = cv2.cvtColor(depth_mask, cv2.COLOR_GRAY2BGR)  # 深度マスク画像

            # 指定距離以上を無視したRGB画像
            depth_mask_norm = (depth_mask / 255.0)
            #color_filtered_image = (depth_mask_norm * image_color).astype(np.uint8)  # マスク済みRGB画像

            #if cv2.waitKey(1) & 0xff == ord('a'):
            if flag==1:
                bg_image1 = cv2.imread(BG_PATH1, cv2.IMREAD_COLOR)
                composite_image = bg_image1
            elif flag==2:
                bg_image2 = cv2.imread(BG_PATH2, cv2.IMREAD_COLOR)
                composite_image = bg_image2
            elif flag==3:
                bg_image3 = cv2.imread(BG_PATH3, cv2.IMREAD_COLOR)
                composite_image = bg_image3
            elif flag==4:
                bg_image4 = cv2.imread(BG_PATH4, cv2.IMREAD_COLOR)
                composite_image = bg_image4


            composite_image = (composite_image.astype(np.float32) * (1 - depth_mask_norm)).astype(np.uint8)
            composite_image[0:HEIGHT, 0:WIDTH] += (image_color * depth_mask_norm).astype(np.uint8)

            color_image=composite_image
            #kokomade

            cv2.rectangle(color_image,(left_up_x,left_up_y),(left_up_x+30,left_up_y+30),(0,255,0),thickness=-1)
            cv2.rectangle(color_image,(right_up_x,right_up_y),(right_up_x+30,right_up_y+30),(0,255,0),thickness=-1)
            cv2.rectangle(color_image,(left_down_x,left_down_y),(left_down_x+30,left_down_y+30),(0,255,0),thickness=-1)
            cv2.rectangle(color_image,(right_down_x,right_down_y),(right_down_x+30,right_down_y+30),(0,255,0),thickness=-1)

                #70cm以内に物体が入る
            if ((depth_image < 700) & (depth_image > 0)).any():
                
                labels,label_images,object_data,center_pos=cv2.connectedComponentsWithStats(depth_filtered_image)
                for label in range(1,labels):
                    center_x,center_y = center_pos[label]
                    #color_image = cv2.circle(color_image, (int(center_x),int(center_y)), 1, (0,0,255), -1)
                    cv2.circle(color_image, (int(center_x),int(center_y)), 1, (0,0,255), -1)
                    pos_x,pos_y,width,height,area_px = object_data[label]
                    #color_image = cv2.rectangle(color_image, (pos_x,pos_y), (pos_x+width,pos_y+height), (255,255,0), 1)
                    cv2.rectangle(color_image, (pos_x,pos_y), (pos_x+width,pos_y+height), (255,255,0), 1)


                    data=np.where(depth_filtered_image == 255,True,False)

                    for k in range(left_up_y,left_up_y+30):
                        for l in range(left_up_x,left_up_x+30):
                            if data[k,l]==True:
                                cv2.rectangle(color_image, (left_up_x,left_up_y),(left_up_x+30,left_up_y+30), (0,0,255),-1)
                                speaker1 = pygame.mixer.Channel(0)

                                flag=1

                                if speaker1.get_busy()!=True:
                                    speaker1.play(sound1)
                                    print("play sound1")
                                #else:
                                    #print("spekaer1_is_busy")

                    for k in range(right_up_y,right_up_y+30):
                        for l in range(right_up_x,right_up_x+30):
                            if data[k,l]==True:
                                cv2.rectangle(color_image, (right_up_x,right_up_y),(right_up_x+30,right_up_y+30), (0,255,255),-1)
                                speaker2 = pygame.mixer.Channel(1)

                                flag=2
                                
                                if speaker2.get_busy()!=True:
                                    speaker2.play(sound2)
                                    print("play sound2")
                                #else:
                                    #print("spekaer2_is_busy")

                    for k in range(left_down_y,left_down_y+30):
                        for l in range(left_down_x,left_down_x+30):
                            if data[k,l]==True:
                                cv2.rectangle(color_image, (left_down_x,left_down_y),(left_down_x+30,left_down_y+30), (255,255,0),-1)
                                speaker3 = pygame.mixer.Channel(2)

                                flag=3
                                
                                if speaker3.get_busy()!=True:
                                    speaker3.play(sound3)
                                    print("play sound3")
                                #else:
                                    #print("spekaer3_is_busy")

                    for k in range(right_down_y,right_down_y+30):
                        for l in range(right_down_x,right_down_x+30):
                            if data[k,l]==True:
                                cv2.rectangle(color_image, (right_down_x,right_down_y),(right_down_x+30,right_down_y+30), (255,0,0),-1)
                                speaker4 = pygame.mixer.Channel(3)

                                flag=4
                                
                                if speaker4.get_busy()!=True:
                                    speaker4.play(sound4)
                                    print("play sound4")
                                #else:
                                    #print("spekaer4_is_busy")
        


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