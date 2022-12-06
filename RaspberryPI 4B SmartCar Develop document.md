# Technical-Project : 4wdSmartCar User Build Document

**Data:_2022-11_**

A programe from Technical Project

Instruct the teacher：@Dr. Louis LECROSNIER_ESIGELEC


# Table of Contents
- [Technical-Project : 4wdSmartCar User Build Document](#technical-project--4wdsmartcar-user-build-document)
- [Table of Contents](#table-of-contents)
- [Prepare OS env](#prepare-os-env)
  - [\*Option](#option)
    - [Raspberry Pi Software Configuration Tool](#raspberry-pi-software-configuration-tool)
- [Code env build](#code-env-build)
  - [list of tasks](#list-of-tasks)
    - [install package](#install-package)
    - [build X11Display](#build-x11display)
    - [Using VSCODE iDE](#using-vscode-ide)
- [Try to use the motor to drive the 4WDcar.](#try-to-use-the-motor-to-drive-the-4wdcar)
  - [RPI.GPIO and wiringPI](#rpigpio-and-wiringpi)
- [Algorithm for tracking lines and Object avoidance](#algorithm-for-tracking-lines-and-object-avoidance)
  - [Composition of the map](#composition-of-the-map)
  - [Turing graph into binary graph](#turing-graph-into-binary-graph)
  - [Mass coordinates](#mass-coordinates)
  - [Handle corners at different angles](#handle-corners-at-different-angles)
    - [Right corners](#right-corners)
    - [Sharp corners](#sharp-corners)
    - [Shifting lines](#shifting-lines)
  - [Object avoidance](#object-avoidance)
- [⛯Start the experiment.](#start-the-experiment)
  - [Camera and ultrasonic assembly](#camera-and-ultrasonic-assembly)
  - [Possible problems in the detection](#possible-problems-in-the-detection)



# Prepare OS env

1. First download the software from offical website in [raspberry website](https://www.raspberrypi.com/software/)
<img src="https://github.com/luvisiki/SmartCar_4wd_Vision/blob/main/img/step1/1-1.png?raw=true" alt="1-1" style="zoom: 25%;" />

2. choose the OS in burner and burn into the RaspberryPI 4B board. Our group choose the **Raspberry Pi OS (32-bit) -(Recommed)** as system.

   <img src="https://github.com/luvisiki/SmartCar_4wd_Vision/blob/main/img/step1/1-3.png?raw=true" alt="1-3" style="zoom: 50%;" />

3. choose the sd card we Get in the class before.

   <img src="https://github.com/luvisiki/SmartCar_4wd_Vision/blob/main/img/step1/1-4.png?raw=true" alt="1-4" style="zoom: 50%;" />

4. Well..if we burn now wo will figure out some problems , the OS haven't open some basic service such as: SSH, VNC and so on. We should Set up in “Advanced settings”.**Prioritize ssh configuration** and we can connect the RaspberryPi through **Ethernet port**.

   <img src="https://github.com/luvisiki/SmartCar_4wd_Vision/blob/main/img/step1/1-5.png?raw=true" alt="1-5" style="zoom: 50%;" />

    **User name** set:raspberrypi.local

   <img src="https://github.com/luvisiki/SmartCar_4wd_Vision/blob/main/img/step1/1-6.png?raw=true" alt="1-6" style="zoom: 50%;" />

​	

As your favourite to fill the blank.

sure we use default Username and password

```
Username:pi
password:raspberry
WIFI：xxxx
WIFI_pd:xxxxx
```

**We can build more config after in PI OS*

1. After waiting for a few minutes, after the machine burns the system, the opportunity has the following tips.

<img src="https://github.com/luvisiki/SmartCar_4wd_Vision/blob/main/img/step1/1-7.png?raw=true" alt="1-7" style="zoom: 50%;" />

And then we can remove the sd card safely, and push into raspberryPI.Power on and wait for a while.

Use the ARP command to the find currently connected device.

<img src="https://github.com/luvisiki/SmartCar_4wd_Vision/blob/main/img/step1/1-8.png?raw=true" alt="1-8" style="zoom: 50%;" />

We can clearly find the raspberrypi.lan show(through WIFI) as 192.168.2.219, using SSH service and Terminal to connect it.

```powershell
ssh pi@192.168.2.129 
```

Then enter the password given above.

<img src="https://github.com/luvisiki/SmartCar_4wd_Vision/blob/main/img/step1/1-9.png?raw=true" alt="1-9" style="zoom: 50%;" />

The system was successfully connected through the ssh.

## *Option

### Raspberry Pi Software Configuration Tool

So if you don't wan to show the image in screen , maybe VNC connect is you best friend.

Terminal input  ```sudo raspi-config ``` ,choose "Interface Options" -> "VNC"

<img src="https://github.com/luvisiki/SmartCar_4wd_Vision/blob/main/img/step1/1-10.png?raw=true" alt="1-10" style="zoom: 50%;" />

<img src="https://github.com/luvisiki/SmartCar_4wd_Vision/blob/main/img/step1/1-11.png?raw=true" alt="1-11" style="zoom: 50%;" />

> For subsequent development, we should also Enable the "Remote GPIO" and "Legacy Camera"
>
> *"Serial port": if we can want to use audrino to connect the raspberryPI
>
> Later, you can also come to this interface for setup according to relevant needs.



# Code env build

## list of tasks

| task                                 | Library file |
| ------------------------------------ | ------------ |
| drive the robot                      | wiring-pi    |
| Follow Track according to the camera | OPENCV       |
| Obstacle detection method            | RPI-GPIO-BCM |

### install package

Opencv build：

> When configuring the environment, we need to pay special attention to the version problems between library files.
>
> example：now newest version of ```opencv-python is 4.6.0.66``` , require ```numpy >= 1.19.3``` well if you follow the document to build OS env , the numpy version should be ```1.19.5```. However it will make bug while use ```1.19.5```. Be sure update the numpy version.
>
> *In order to use automatic completion  in VSCODE, the version uses：4.5.5.62
> Other version check :[pypi-opencv](https://pypi.org/project/opencv-python/)

```python
pip install -U numpy	#numpy-1.23.5 in 2022.11
pip install opencv-python==4.5.5.62 # opencv-python-4.6.0.66 in 2022.11
pip install opencv-python-headless==4.5.5.62# opencv-python-headless-4.6.0.66 in 2022.11
pip install opencv-contrib-python==4.5.5.62 #2022.11:not 4.6.0.66 in armv7l 

#tool-chains:
sudo apt-get install libhdf5-dev
sudo apt-get install libatlas-base-dev
```

<img src="https://github.com/luvisiki/SmartCar_4wd_Vision/blob/main/img/step2/2-1.png?raw=true" alt="2-1" style="zoom: 50%;" />

> **When i first time install opencv-contrib-python ,there is not arm7vl version in 4.6.0.66 , so pypi will auto install other linux arm version , (150MB+) i guess, it will make wheels forever; Be careful about it and Select the historical version after cancellation.**

### build X11Display

> well, if we won't use hdmi to show the graph , X11 is a choice to remote show RaspberryPI graph but use client GPU
>
> * following in the ***macOS 13.0***(windows are the same logical ,find some tips in nets)

In raspberryPI ```vi /etc/ssh/sshd_config ``` find ```X11Forwarding``` and ```X11DisplayOffset ```

Set the Value ```X11Forwarding yes X11DisplayOffset 10 ```

And restart the ssh service ``` service ssh restart```

And then edit on Mac ``` vi /private/etc/ssh/ssh_config``` find and fill```ForwardX11 yes```

this step is complete.

> when you use ssh to connect RaspberryPI , fill ``` -X``` before your usename

### Using VSCODE iDE

If you want to write code in RaspberryPI  I highly recommend VSCODE;
Download ```Remote-SSH``` in expands and do some easy config,It can upgrade your code experience.



# Try to use the motor to drive the 4WDcar.

##	RPI.GPIO and wiringPI

In Raspberry Pi, if we want to use ```GPIO``` operation, we have two choices: use the ```wiringPI``` or ```RPI``` library,  but according to the ```RPI``` developer's explanation, the ```RPI``` library is not suitable for too complicated operations, and in order to be closer to the style of the ```Arduino```, we use the ```wiringPI library``` to drive the motor and make the car move, and use GPIO to drive the ultrasonic .

> using 4wd Expansion board （Yabo smart car accessories）
>
> <img src="https://github.com/luvisiki/SmartCar_4wd_Vision/blob/main/img/step3/3-1.png?raw=true" alt="3-1" style="zoom: 50%;" />
>
> 

| GPIO  | Encoding format | position |       Function        |
| :---: | :-------------: | :------: | :-------------------: |
| IO20  |    Wiringpi     |    28    |    LeftMotor_Font     |
| IO21  |    Wiringpi     |    29    |    LeftMotor_Back     |
| IO19  |    Wiringpi     |    24    |    RightMotor_Font    |
| IO26  |    Wiringpi     |    25    |    RightMotor_Back    |
| IO16  |    Wiringpi     |    27    | LeftMotor_PWMcontorl  |
| IO13  |    Wiringpi     |    23    | RightMotor_PWMcontorl |
| ID_SC |       BCM       |    0     |  ultrasonic_EchoPin   |
| ID_SD |       BCM       |    1     |  ultrasonic_TrigPin   |

All the needed pin is checked and the following code is based on it.
# Algorithm for tracking lines and Object avoidance

##  Composition of the map

<img src="https://github.com/luvisiki/SmartCar_4wd_Vision/blob/main/img/step4/4-1.png?raw=true" alt="4-1" style="zoom: 50%;" />

The pic above is the map we use this time to track the black and Avoid obstacles

> **see more information in this web [map](https://detail.tmall.com/item.htm?abbucket=0&id=608358800983&rn=7655da43a24ab506fcad65360d2b235b&spm=a1z10.5-b-s.w4011-22651484606.42.6f6170b0thTocv)

This map include five patrs:

- sharp angle

- right angle

- curve

- straight line

- crossing line

## Turing graph into binary graph

  Use opencv to morphologically operate on the picture to remove excess noise.For example: Gaussian fuzzy, open and closed operation.after that convert RGB space into HSV space and using filter to focus in black color gamut.

  ```python
  
  #@@@@@ in main.py:
  
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
  ```

  We get a **mask** with only value in 0 or 255.

  <center class="half">
      <img src="https://github.com/luvisiki/SmartCar_4wd_Vision/blob/main/img/step4/4-2.jpg?raw=true" width="200">
      <img src="https://github.com/luvisiki/SmartCar_4wd_Vision/blob/main/img/step4/4-3.jpg?raw=true" width="200">
  </center>
  
  

> ###### From the pic it's clear see that binary graph is  affected by light. but not that serious , We can clearly see the outlines.
>
> Corrosion operation and Expansion operation can Make the lines more coherent. 

## Mass coordinates

In above binary graph , we can Find the largest outline. get the Mass coordinates , and help us to Fix the position of the car later.

```python
#@@@@@ in main.py:

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
```

<img src="https://github.com/luvisiki/SmartCar_4wd_Vision/blob/main/img/step4/4-4.png?raw=true" alt="4-4" style="zoom: 50%;" />

Adjust the position of the car according to the coordinates of the center of mass, so that the center of mass can be at the center of the image as much as possible. _grph cx(0-319)_  When cx between (120-200) drive the car go straight.If cx<120 turn left ,if cx>200 turn right.

the base control is done.

```python
# in main.py: cx->pointX cy->pointY
if cx == 0 and cy == 0:
  # when there is no External outline in this frame,(no black line)
  print("Back")
  c.SmartCar_back(20, 20, 0.1)
  c.Motor_stop()
  time.sleep(0.5)

elif (0 < cx < 120):
  c.SmartCar_turn_Left(25, 10, 1, 0.1)
  print("Turn left")
  # time.sleep(0.001)

elif (180 < cx < 320):
  c.SmartCar_turn_Right(25, 10, 1, 0.1)
  print("Turn Right")
  # time.sleep(0.001)

elif (cx >= 120 and cx <= 200):
  print("GO Straight")
  c.SmartCar_run(15, 0.1)
  # time.sleep(0.001)

  c.Motor_stop()
```

However The judgment conditions are too simple.we have seen the  Map composition above. 

I suggested try at first and find out questions about base control code.

## Handle corners at different angles
If you have conducted a simple test, you will find that the above simple control car code will run out of the track for some tricky corners.Take separate photos of unrecognized corners and analyze them.
<center class="half">
<img src="https://github.com/luvisiki/SmartCar_4wd_Vision/blob/main/img/step4/4-5.jpg?raw=true" alt="4-5" style="zoom: 50%;" width="200"/>
<img src="https://github.com/luvisiki/SmartCar_4wd_Vision/blob/main/img/step4/4-6.jpg?raw=true" alt="4-6" style="zoom: 50%;" width="200"/>
</center>
Probably the most troublesome corners are right corners and sharp corner corners.
According to the binary image, his characteristics can be analyzed. When the car shoots them in a certain position, the feature shape can be judged to be the only one.

### Right corners
<img src="https://github.com/luvisiki/SmartCar_4wd_Vision/blob/main/img/step4/4-7.jpg?raw=true" alt="4-7" style="zoom: 50%;" width="300"/>

So we came up with a way to solve the right-angle turning (left/right) , and use three lines to locate the current frame, namely, line1, which is the farthest from the image, line line2 at the center of the image, and line line3 closest to the car.

<img src="https://github.com/luvisiki/SmartCar_4wd_Vision/blob/main/img/step4/4-9.jpg?raw=true" alt="4-9" style="zoom: 50%;" width="300"/>

like the purple line in frame , divide the frame into 2 pices.
using ```numpy.where()``` to **count the number of ```255```** , compare it and decide it whether need to turn right or left.
```python
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
```
We add a condition to the definition so that he can identify it as a right angle.
```python
# right-angle turn left
if count1 == 0 and count2 == 0 and (count3_left, count3_right != 0) and (count3_left > count3_right) and count3_left > 80:
```
In order to reduce the error, it is judged to be a right angle when the 255 value accounts for 50% of the left/right majority.Then debug the speed and delaytime of the motor driver, which will be very simple through right angles.

### Sharp corners

<img src="https://github.com/luvisiki/SmartCar_4wd_Vision/blob/main/img/step4/4-10.jpg?raw=true" alt="4-10" width="300"/>

> this frame is token from usb camera in 4wdcar

The treatment of sharp angle is very similar to that of right angle, but in order not to confuse the judgment of sharp angle with other curvatures, he will start with ```line2``` instead of ```line3```.
```python
elif count1 == 0 and count3 != 0 and (count2_left > count2_right) and count2_left > 60:
```

### Shifting lines

<img src="https://github.com/luvisiki/SmartCar_4wd_Vision/blob/main/img/step4/4-11.jpg?raw=true" alt="4-11" width="300"/>

In the test, it is often found that when there is a offset straight line on the current surface, it will be detected as sharp angles or right angles. In order to solve this bug, add a more situation judgment.

```python
elif count1 != 0 and (count2_left > count2_right) and count2_left > 40:
```

## Object avoidance

using the ultrasonic to avoid the object.

<img src="https://github.com/luvisiki/SmartCar_4wd_Vision/blob/main/img/step5/5-1.png?raw=true" alt="5-1" width="300"/>

According to the principle of the ultrasonic sensor: by calculating the high level of the receiving end, the approximate distance of the front obstacle can be calculated through the formula.

```python
def ultarsonic_ExaminDistant(self):
        '''
        @@@@@@@@
        @@ Developer: Han Cao, id:202244060101
        @@ Fuction name: ultarsonic_ExaminDistant
        @@ Input: none
        @@ output: Distance measurements
        @@ Description: Use the ultrasonic principle to detect the high level time of the EchoPin time.Then use the formula to calculate the distance from the obstacle.
        @@@@@@@@
        '''
        GPIO.output(self.TrigPin, GPIO.HIGH)
        time.sleep(0.000015)
        GPIO.output(self.TrigPin, GPIO.LOW)
        while not GPIO.input(self.EchoPin):
            pass
        t1 = time.time()
        while GPIO.input(self.EchoPin):
            pass
        t2 = time.time()
        # print ("distance is %d " % (((t2 - t1) * 340 / 2) * 100))
        time.sleep(0.01)
        return int(((t2 - t1) * 340 / 2) * 100)
```

# ⛯Start the experiment.

> **🔥Attention: It can be clearly seen in the tracking algorithm that the binary results are very affected by light. Please reduce the impact of dazzling as much as possible when copying the experiment, or stand next to the car and use your own shadows to cover the reflection on the map.**

## Camera and ultrasonic assembly

<img src="https://github.com/luvisiki/SmartCar_4wd_Vision/blob/main/img/step6/6-1.png?raw=true" alt="5-1" width="300"/>

In order to find the best camera shooting angle, we did not use the official installation method, but assembled it through existing tools.

The sizes of the copper column are 3cm and 6cm respectively.And just debug the camera when he doesn't take the ultrasonic module.

## Possible problems in the detection

> 1.  When the car is stuck, it is likely because the light affects the road ahead and tries to block the reflection.
> 2. The car starts testing from the straight road.
> 3. When you need to stop the program , press ```crtl C ``` more times and wait. **If the car stops incorrectly and runs at full speed, try to run the program again and run the previous step again.**