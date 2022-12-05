import cv2
from multiprocessing import Process, Queue
import numpy as np
import threading
import Motor
import pid
import time
import RPi.GPIO as GPIO





def camera_catch_color(car, q):

    '''
    @@@@@@@@
    @@ Developer: QianRong LIU , id:202244060130 , ZongZhen Liu id:202244060131 
    @@ Function name: camera_catch_color 
    @@ Input: An instance of the class , An instance of the Queue
    @@ put into Queue: cx, cy, frame, flag, mode 
    @@ Description: loop the frame. using Gaussian blur, Corrosion, Expansion:Morphological operation to Remove the noise of the current frame and And convert the frame into an HSV space for binary operation.
    @@@@@@@@
    '''

    capture = cv2.VideoCapture(0)   # An instance of the video0
    # set frame's Height and Length
    capture.set(3, 320)  # CV_CAP_PROP_FRAME_WIDTH=3   帧宽度
    capture.set(4, 240)  # CV_CAP_PROP_FRAME_HEIGHT=4  帧高度

    while True:
        ret, frame = capture.read()

        
        blurr = cv2.GaussianBlur(frame, (13, 13), 0)
        # 转换为hsv空间颜色 turn into hsv space color
        hsv = cv2.cvtColor(blurr, cv2.COLOR_BGR2HSV)
        # 进行颜色锁定（黑色）hsv focus in black color
        lower_hsv = np.array([0, 0, 0])
        higer_hsv = np.array([180, 255, 46])
        # turn mask into 255 or 0
        mask = cv2.inRange(hsv, lower_hsv, higer_hsv)

        # 腐蚀操作 Corrosion operation
        mask = cv2.erode(mask, None, iterations=2)
        # 膨胀操作 Expansion operation
        mask = cv2.dilate(mask, None, iterations=2)

        flag, mode = Count255(car, mask)
        print("falg: ", flag)

        # @ Find the contours of the frame
        # @ cv2.findcontours args**: img, mode, method
        # @ cv2.RETR_EXTERNAL:只检测外轮廓
        # @ cv2.CHAIN_APPROX_NONE:存储所有的轮廓点，相邻的两个点的像素位置差不超过1
        contours, hierarchy = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) > 0:
            # cv2.contourArea轮廓面积，返回面积最大的轮廓 return biggest
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)  # cv2.moments计算图像矩，然后通过图象矩计算质心

            # 几何中心的数学表示方式则(cx,cy)就是质心坐标 
            # (cx,cy) means Mass coordinates
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
    '''
    @@@@@@@@
    @@ Developer: QianRong LIU , id:202244060130 , ZongZhen Liu id:202244060131 
    @@ Function name: Motor_State 
    @@ Input: An instance of the class , An instance of the Queue
    @@ Description: get cx,cy,frame,flag and mode from Queue (where put in camera_catch_color fuction) , according to the value of mode and (cx,cy)Mass coordinates. drive the 4WDcar and follow the black line in Map. More information check the user document.
    @@@@@@@@
    '''

    while True:
        pointX, pointY, frame, flag, mode = q.get()
        # print(mode)
        if mode == 2:
            c.Motor_stop()
            c.Motor_init()
            print("There is something in front of 4WDCar, Stop the car.")

        elif mode == 1:

            if flag == 1:

                c.SmartCar_turn_Left(40, 5, 1, 0.5)
                # time.sleep(1)
                print("right angle(left)")
            elif flag == 2:
                c.SmartCar_turn_Right(40, 5, 1, 0.5)
                # time.sleep(1)
                print("right angle(right)")
            elif flag == 3:
                c.SmartCar_turn_Left(40, 0, 2, 1.7)
                print("Sharp angle(left)")
            elif flag == 4:
                c.SmartCar_turn_Right(40, 0, 2, 1.7)
                print("Sharp angle(right)")
            elif flag == 5:
                c.SmartCar_turn_Left(25, 10, 1, 0.1)
                print("Turn left")
            elif flag == 6:
                c.SmartCar_turn_Right(25, 10, 1, 0.1)
                print("Turn right")

        elif mode == 0:

            if pointX == 0 and pointY == 0:
                # c.Motor_stop()
                print("Back")
                c.SmartCar_back(20, 20, 0.1)
                c.Motor_stop()
                time.sleep(0.5)

            elif (0 < pointX < 120):
                c.SmartCar_turn_Left(25, 10, 1, 0.1)
                print("Turn left")
                # time.sleep(0.001)

            elif (180 < pointX < 320):
                c.SmartCar_turn_Right(25, 10, 1, 0.1)
                print("Turn Right")
                # time.sleep(0.001)

            elif (pointX >= 120 and pointX <= 200):
                print("GO Straight")
                c.SmartCar_run(15, 0.1)
                # time.sleep(0.001)

                c.Motor_stop()


def Count255(c, frame):
    # frame 's cols
    '''
    @@@@@@@@
    @@ Developer: QianRong LIU , id:202244060130 
    @@ Function name: Count255 
    @@ Input: An instance of the class , frame 
    @@ return : mode,flag
    @@ Description: input a binary frame ,  check 3 cols (line1,2,3) and divide col into 2 parts, and compare them. Divide into six categories and make judgments.
    @@@@@@@@
    '''

    line1 = 40
    line2 = 119
    line3 = 200

    Value1 = frame[line1]
    Value2 = frame[line2]
    Value3 = frame[line3]
    Value2_Left = frame[line2, :160]
    Value2_Right = frame[line2, 160:320]
    Value3_Left = frame[line3, :160]
    Value3_Right = frame[line3, 160:320]
    count1 = len(np.where(Value1 == 255)[0])
    count2 = len(np.where(Value2 == 255)[0])
    count2_left = len(np.where(Value2_Left)[0])
    count2_right = len(np.where(Value2_Right)[0])
    count3 = len(np.where(Value3)[0])
    count3_left = len(np.where(Value3_Left)[0])
    count3_right = len(np.where(Value3_Right)[0])
    cm = c.ultarsonic_ExaminDistant()
    print("distant:", cm)
    mode = 0
    flag=0


    
    if cm <= 20:
        mode = 2
    '''
    flag1:Solve the right-angle bending (turn left)
    flag2:Solve the right-angle bending (turn right)
    flag3:Solve the sharp angle bending (turn left)
    flag4:Solve the sharp angle bending (turn right)
    flag5:solve the angle shifting *left shift
    flag6:solve the angle shifting *right shift
    '''
    if mode != 2:
        
        if count1 == 0 and count2 == 0 and (count3_left, count3_right != 0) and (count3_left > count3_right) and count3_left > 80:
            flag = 1
            mode = 1
        elif count1 == 0 and count2 == 0 and (count3_left, count3_right != 0) and (count3_left < count3_right) and count3_right > 80:
            flag = 2
            mode = 1
        elif count1 == 0 and count3 != 0 and (count2_left > count2_right) and count2_left > 60:
            flag = 3
            mode = 1
        elif count1 == 0 and count3 != 0 and (count2_right > count2_left) and count2_right > 60:
            flag = 4
            mode = 1
        elif count1 != 0 and (count2_left > count2_right) and count2_left > 40:
            flag = 5
            mode = 1
        elif count1 != 0 and (count2_right > count2_left) and count2_right > 40:
            flag = 6
            mode = 1
        else:
            flag = 0
            mode = 0
    return flag, mode


if __name__ == '__main__':
    '''
    @@@@@@@@
    @@ Developer: QianRong LIU , id:202244060130 , ZongZhen LIU , id:202244060131 , Han Cao , id:202244060101
    @@ Function name: main  
    @@ Description: CREATE two sub thread
    @@ Thread one: catch frame and do Morphological operation. put the Status variables(mode,flag,...) into Queue
    @@ Thread two: get Status variables from Queue . According to the Status value to drvie the 4WDcar.
    @@@@@@@@
    '''
    try:
        c = Motor.MotorControl()
        c.Motor_init()
        q = Queue()

        t1 = threading.Thread(target=camera_catch_color, args=(c, q))
        t2 = threading.Thread(target=Motor_State, args=(c, q))
        # t2 = Process(target=Motor_State, args=(c, q))
        t1.start()
        t2.start()
        Motor_State(c, q)

        # t2.start()

    except KeyboardInterrupt:
        pass
        c.Motor_stop()
        c.Motor_init()
        GPIO.cleanup()
        t1.join()
        t2.join()
