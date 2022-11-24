import cv2
from multiprocessing import Process,Queue
import threading
import numpy as np
import time
import Motor


# @@
# @
# @
# @@
# global cx

# cx = 0
lock = threading.Lock

def camera_catch_color(car,q):
    # global cx
    global frame
    capture = cv2.VideoCapture(0)
    capture.set(3, 320)
    capture.set(4, 240)  # 像素高度？
    
    while True:
        
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
            car.Motor_init()
            # car.SmartCar_turn_Right(30,30,2)
        cv2.waitKey(25)
        cv2.imshow('test', frame)
        q.put(cx)
        # cv2.waitKey(1)
        
    

def Motor_State(c,q):
    # global cx
    # print(cx)
    while True:
        point = q.get()
        print(point)
        if point >= 200 and point <= 270:
            print("偏右")
            c.SmartCar_turn_Right(30, 20, 0.3)
            c.Motor_init()
            # time.sleep(0.5)
            # print(cv2.CAP_PROP_FPS)
        if point > 270:
            c.SmartCar_turn_Right(40,20,0.2)
            c.Motor_init()
        if point <= 200 and point > 120:
            print("直走")
            c.SmartCar_run(30, 0.3)
            c.Motor_init()
            # print(cv2.CAP_PROP_FPS)
        if point <= 120 and point > 50:
            print("偏左")
            c.SmartCar_turn_Left(30, 20, 0.3)
            # print(LEFT_MOTOR_BACK)
            c.Motor_init()
            # time.sleep(0.5)
            # print(cv2.CAP_PROP_FPS)
        if point <= 50:
            c.SmartCar_turn_Left(40,20,0.2)
            c.Motor_init()
    


if __name__ == '__main__':
    # global cx, cy, frame
    try:
        c = Motor.MotorControl()
        c.Motor_init()
        q = Queue()

        t1 = threading.Thread(target=camera_catch_color, args=(c,q))
        t2 = threading.Thread(target=Motor_State,args=(c,q))
        
        # t1 = Process(target=camera_catch_color,args=(c,q))
        # t2 = Process(target=Motor_State,args=(c,q))
        # t3 = Process(target=Camera_show,args=(q,))
        t1.start()
        t2.start()
        
        # while 1:
        #     # cx,cy,frame = camera_catch_color(capture)
        #     Motor_State(c)

        # camera_catch_color(capture)
        # cv2.imshow('test',frame)
        # cv2.waitKey(1)

    except KeyboardInterrupt:
        pass
    c.Motor_stop()
    t1.join()
    t2.join()
