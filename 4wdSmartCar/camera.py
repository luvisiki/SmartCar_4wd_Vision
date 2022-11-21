import cv2
import numpy as np
import imutils


# @@
# @
# @
# @@
def camera_stream(mode):
    try:
        if mode == 1:  ## camera
            capture = cv2.VideoCapture(0)
            ret, frame = capture.read()
        if mode == 2:
            frame = cv2.imread('test.png')
            frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
            ret = 0
    except KeyboardInterrupt:
        pass
    return frame, ret


def camera_catch_color():
    capture = cv2.VideoCapture(0)
    ret, frame = capture.read()
    # frame = imutils.resize(frame, height=320, width=480)
    # 高斯模糊
    # frame = cv2.imread('../img/step1/1-8.png')
    # print(frame.shape)
    # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    blurr = cv2.GaussianBlur(frame, (11, 11), 0)
    # 转换为hsv空间颜色
    hsv = cv2.cvtColor(blurr, cv2.COLOR_BGR2HSV)
    # 进行颜色锁定（黑色）
    lower_hsv = np.array([0, 0, 0])
    higer_hsv = np.array([180, 255, 46])
    # 二值化处理
    mask = cv2.inRange(hsv, lower_hsv, higer_hsv)
    # 腐蚀操作
    mask = cv2.erode(mask, None, iterations=2)
    # 膨胀操作
    mask = cv2.dilate(mask, None, iterations=2)
    cv2.imshow('test', mask)
    # print(mask[0])
    # c = cv2.waitKey(0)
    # print(mask[])
    # if c == 27:
    #     pass


def Canny(frame):
    pic = cv2.imread(frame)
    gass = cv2.GaussianBlur(pic, (11, 11), 0)
    pic = cv2.Canny(gass, 0, 100)
    cv2.imshow('test', pic)


if __name__ == '__main__':
    while 1:
        # capture = cv2.VideoCapture()
        # frame, ret = capture.read()
        camera_catch_color()
    cv2.waitKey(0)
