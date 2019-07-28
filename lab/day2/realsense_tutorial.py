import pyrealsense2 as rs
import cv2
import numpy as np

WIDTH = 640
HEIGHT = 480
FPS = 60
THRESHOLD = 0.7


def main():
    # RealSenseの初期設定
    config = rs.config()
    config.enable_stream(rs.stream.color, WIDTH, HEIGHT, rs.format.bgr8, FPS)  # RGB
    config.enable_stream(rs.stream.depth, WIDTH, HEIGHT, rs.format.z16, FPS)   # 深度

    pipeline = rs.pipeline()
    profile = pipeline.start(config)
    align = rs.align(rs.stream.depth)

    # depth scaleの取得
    depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()

    try:
        while True:
            # フレーム取得
            frames = pipeline.wait_for_frames()

            # RGB画像のフレームと深度画像のフレームに分割(画角補正なし)
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()

            # RGB画像のフレームと深度画像のフレームに分割(画角補正あり)
            """
            aligned_frames = align.process(frames)
            color_frame = aligned_frames.get_color_frame()
            depth_frame = aligned_frames.get_depth_frame()
            """

            # フレーム取得に失敗した場合
            if not depth_frame or not color_frame:
                continue

            # 深度画像の彩色
            depth_color_frame = rs.colorizer().colorize(depth_frame)
            depth_color_image = np.asanyarray(depth_color_frame.get_data())

            color_image = np.asanyarray(color_frame.get_data())
            depth_image = np.asanyarray(depth_frame.get_data())

            cv2.imshow('color', color_image)
            cv2.imshow('depth', depth_image)
            cv2.waitKey(1)

    finally:
        pipeline.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
