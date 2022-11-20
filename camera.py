import cv2
import numpy as np
import imutils


def camera_catch():
    capture = cv2.VideoCapture(0)
    while 1:
        ret, frame = capture.read()
        frame = imutils.resize(frame, height=320, width=480)
        # 高斯模糊
        blurr = cv2.GaussianBlur(frame, (11, 11), 0)
        # 转换为hsv空间颜色
        hsv = cv2.cvtColor(blurr, cv2.COLOR_BGR2HSV)
        # 进行颜色锁定（橙色）
        lower_hsv = np.array([11, 43, 46])
        higer_hsv = np.array([25, 255, 255])
        # 二值化处理
        mask = cv2.inRange(hsv, lower_hsv, higer_hsv)
        # # 腐蚀操作
        # mask = cv2.erode(mask, None, iterations=2)
        # # 膨胀操作
        # mask = cv2.dilate(mask, None, iterations=2)
        cv2.imshow('test', mask)
        # print(mask[0])
        c = cv2.waitKey(25)
        # print(mask[])
        if c == 27:
            break


if __name__ == '__main__':
    camera_catch()
