import cv2
import numpy as np
 

#エスカレータの下から見たやつ（精度良い）
cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture("/home/endot/seisaku/IMG_1878.MOV")
#エスカレータを上から見たやつ（精度悪い）
#cap = cv2.VideoCapture("/home/endot/seisaku/IMG_1876.MOV")
#cap = cv2.VideoCapture("/home/endot/seisaku/IMG_1879.MOV")

#width,height=840,680
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# VideoWriter を作成する。
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
#writer = cv2.VideoWriter('/home/endot/seisaku/result/esc2.avi', fourcc, fps, (width, height))
while(1):
 
    # フレームを取得
    ret, frame = cap.read()
    
   # cv2.putText(frame, str(tokuten), (330, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)
    #cv2.putText(frame, str(great), (330, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)
    #cv2.putText(frame, str(good), (330, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)        
    #cv2.putText(frame, str(bad), (330, 120), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)
    
 
    # フレームをHSVに変換
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
    # 取得する色の範囲を指定する
    lower_yellow = np.array([0, 58, 88])
    upper_yellow = np.array([25, 173, 229])
 
    # 指定した色に基づいたマスク画像の生成
    img_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
 
    # フレーム画像とマスク画像の共通の領域を抽出する。
    img_color = cv2.bitwise_and(frame, frame, mask=img_mask)


    
    img = cv2.resize(img_color,(width, height))
    cv2.rectangle(img_color, (170, 90), (270, 190), (0,58,88),3)
    cv2.rectangle(img_color, (170, 290), (270, 390), (0,58,88),3)
    cv2.rectangle(img_color, (370, 90), (470, 190), (0,58,88),3)
    cv2.rectangle(img_color, (370, 290), (470, 390), (,58,88),3)

  
   
   # writer.write(img)  # フレームを書き込む。
 
    cv2.imshow("SHOW COLOR IMAGE", img)
    if not ret:
        break  # 映像取得に失敗

    
    
 
    # qを押したら終了
    k = cv2.waitKey(1)
    if k == ord('q'):
        break
         
#writer.release()
cap.release()
 