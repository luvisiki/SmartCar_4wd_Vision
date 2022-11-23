import cv2
import numpy as np
import wiringpi
import time
import Motor

# @@
# @
# @
# @@



def camera_catch_color(a):
    capture = cv2.VideoCapture(0)
    capture.set(3, 320)
    capture.set(4, 240)  # 像素高度？
    time.sleep(5)
    while 1:
        ret, frame = capture.read()

        # frame = cv2.imread('./pic/left_angle.jpg')
        frame = frame[120:240, :]  # 320*240，只取高度的下半部分，减小计算量，较少其他因素
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

        # mask = cv2.line(mask, (120, 0), (120, 120), (255, 255, 255), 3, 8)
        # mask = cv2.line(mask, (240, 0), (240, 120), (255, 255, 255), 3, 8)

        # Find the contours of the frame
        # cv2.findcontours args**: img, mode, method
        # cv2.RETR_EXTERNAL:只检测外轮廓
        # cv2.CHAIN_APPROX_NONE:存储所有的轮廓点，相邻的两个点的像素位置差不超过1
        contours, hierarchy = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) > 0:
            # cv2.contourArea轮廓面积，返回面积最大的轮廓
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)  # cv2.moments计算图像矩，然后通过图象矩计算质心

            # 几何中心的数学表示方式则(cx,cy)就是质心坐标
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            # print(cx, cy)
            cv2.line(frame, (cx, 0), (cx, 10000), (255, 0, 0), 1)
            cv2.line(frame, (0, cy), (10000, cy), (255, 0, 0), 1)
            cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)
            if cx >= 220:
                print("偏右")
                a.SmartCar_turn_Right(20, 20, 0.1)
                a.Motor_init()
                # time.sleep(0.5)
                print(cv2.CAP_PROP_FPS)
            if cx < 220 and cx > 100:
                print("直走")
                a.SmartCar_run(30, 0.1)
                a.Motor_init()
                print(cv2.CAP_PROP_FPS)
            if cx < 100:
                print("偏左")
                a.SmartCar_turn_Left(20, 20, 0.1)
                # print(LEFT_MOTOR_BACK)
                a.Motor_init()
                # time.sleep(0.5)
                # print(cv2.CAP_PROP_FPS)
        cv2.imshow('test', frame)

        # print(mask[0])
        # c = cv2.waitKey(1)

        #   press e to exit process
        if cv2.waitKey(1) == ord('e'):
            break

if __name__ == '__main__':
    
    try:
        c = Motor.MotorControl()
        c.Motor_init()
        # c.ServoAngle(180)
        camera_catch_color(c)
    except KeyboardInterrupt:
        pass
    c.Motor_stop()
    
