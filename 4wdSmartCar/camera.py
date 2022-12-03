import cv2
from multiprocessing import Process, Queue
import numpy as np
import threading
import Motor
import pid
import time

# @@
# @
# @
# @@
# global cx

# cx = 0


def camera_catch_color(car, q):
    # global cx
    # global frame
    capture = cv2.VideoCapture(0)
    capture.set(3, 320)  # CV_CAP_PROP_FRAME_WIDTH=3   帧宽度
    capture.set(4, 240)  # CV_CAP_PROP_FRAME_HEIGHT=4  帧高度

    while True:
        ret, frame = capture.read()

        # frame = frame[120:240, :]  # 320*240，只取高度的下半部分，减小计算量，较少其他因素
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

        flag, mode = Count255(mask)
        print("标志位：", flag)

        # @ Find the contours of the frame
        # @ cv2.findcontours args**: img, mode, method
        # @ cv2.RETR_EXTERNAL:只检测外轮廓
        # @ cv2.CHAIN_APPROX_NONE:存储所有的轮廓点，相邻的两个点的像素位置差不超过1
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
            cv2.line(frame, (cx, 0), (cx, 320), (255, 0, 0), 1)
            cv2.line(frame, (0, cy), (240, cy), (255, 0, 0), 1)
            cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)
        else:
            print('there is no black lines')
            cx = 0
            cy = 0
            # time.sleep(0.1)
            # car.Motor_stop()
            # car.SmartCar_turn_Right(30,30,2)
        cv2.waitKey(10)
        # cv2.imshow('test', frame)
        q.put((cx, cy, frame, flag, mode))
        # attention：
        #   when using cv2.videocapture read, there has lots of index haven't been handle in time
        #   using q.qsize()to make sure get the newest frame and handle it.
        #####
        length = q.qsize()
        # print('Queue length : ', length)
        if length > 5:
            for i in range(length-5):
                cx, cy, frame, flag, mode = q.get()
    capture.release()


def Motor_State(c, q):

    while True:
        pointX, pointY, frame, flag, mode = q.get()
        # # print((pointX, pointY))
        cv2.imshow('test', frame)
        cv2.waitKey(10)
        # servo_pid.SystemOutput = pointX
        # xservo_pid.SystemOutput = pointX
        # xservo_pid.SetStepSignal(150)
        # xservo_pid.SetInertiaTime(0.01, 0.1)
        # targer_valuex = int(1500+xservo_pid.SystemOutput)
        # yservo_pid.SystemOutput = pointY
        # yservo_pid.SetStepSignal(150)
        # yservo_pid.SetInertiaTime(0.01, 0.1)
        # targer_valuey = int(150+yservo_pid.SystemOutput)
        # time.sleep(0.008)
        # if times == 5:
        #     times = 0
        #     servo.Servo_control(targer_valuex, targer_valuey)
        if mode == 1:
            if flag == 1:
                c.SmartCar_turn_Right(50, 0, 0.2)
                print("直角右转")
            elif flag == 2:
                c.SmartCar_turn_Left(50, 0, 0.2)
                print("直角左转")

        if mode == 0:

            if pointX == 0 and pointY == 0:
                # c.Motor_stop()
                print("后退")
                c.SmartCar_back(20, 20, 0.1)
                c.Motor_stop()
                time.sleep(0.5)

            elif (0 < pointX < 120):
                c.SmartCar_turn_Left(25, 15, 0.1)
                print("左转")

            elif (180 < pointX < 320):
                c.SmartCar_turn_Right(25, 15, 0.1)
                print("右转")

            elif (pointX >= 120 and pointX <= 200):
                print("直走")
                c.SmartCar_run(20, 0.1)
                c.Motor_stop()


def Count255(frame):
    # frame 's cols
    line1 = 39
    line2 = 119
    line3 = 200

    Value1 = frame[line1]
    Value2 = frame[line2]
    Value3_Left = frame[line3, :160]
    Value3_Right = frame[line3, 160:320]
    count1 = len(np.where(Value1 == 255)[0])
    count2 = len(np.where(Value2 == 255)[0])
    count3_left = len(np.where(Value3_Left)[0])
    count3_right = len(np.where(Value3_Right)[0])

    if count1 == 0 and count2 == 0 and (count3_left, count3_right != 0) and (count3_left > count3_right):
        flag = 1
        mode = 1
    elif count1 == 0 and count2 == 0 and (count3_left, count3_right != 0) and (count3_left < count3_right):
        flag = 2
        mode = 1
    else:
        flag = 0
        mode = 0
    return flag, mode


if __name__ == '__main__':
    # global cx, cy, frame
    lock = threading.RLock()
    try:
        c = Motor.MotorControl()
        c.Motor_init()
        q = Queue()

        t1 = threading.Thread(target=camera_catch_color, args=(c, q))
        t2 = threading.Thread(target=Motor_State, args=(c, q))
        # t2 = Process(target=Motor_State, args=(c, q))
        t1.start()
        t2.start()
        # Motor_State(c, q)

        # t2.start()

    except KeyboardInterrupt:
        pass

    c.Motor_stop()
    c.Motor_init()
    t1.join()
    t2.join()
