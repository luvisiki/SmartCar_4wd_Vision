# Technical-Project : 4wdSmartCar User Build Document

#Author:_Liu qianrong 202244060130_
				_Cao Han 202244060101_
				_Liu zongzhen 202244060131_

#Group:_1.7_

#Data:_2022-11_

# Step one: Prepare OS env



1. First download the software from offical website in [raspberry website](https://www.raspberrypi.com/software/)
<img src="https://github.com/luvisiki/SmartCar_4wd_Vision/blob/main/img/step1/1-1.png?raw=true" alt="1-1" style="zoom: 25%;" />

​	***Attention**:Author using macOS13.0 ,while something different in WINODWS and LINUX,The official burner solves this problem very well.

2. Open the software we download in 1.

   <img src="https://github.com/luvisiki/SmartCar_4wd_Vision/blob/main/img/step1/1-2.png?raw=true" alt="1-2" style="zoom: 50%;" />

3. choose the OS in burner and burn into the RaspberryPI 4B board. Our group choose the **Raspberry Pi OS Full(32-bit) -2.6GBytes** as system.

   <img src="https://github.com/luvisiki/SmartCar_4wd_Vision/blob/main/img/step1/1-3.png?raw=true" alt="1-3" style="zoom: 50%;" />

4. choose the sd card we Get in the class before.

   <img src="https://github.com/luvisiki/SmartCar_4wd_Vision/blob/main/img/step1/1-4.png?raw=true" alt="1-4" style="zoom: 50%;" />

5. Well..if we burn now wo will figure out some problems , the OS haven't open some basic service such as: SSH, VNC and so on. We should Set up in “Advanced settings”.**Prioritize ssh configuration** and we can connect the RaspberryPi through **Ethernet port**.

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

6. After waiting for a few minutes, after the machine burns the system, the opportunity has the following tips.

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



# Step two: Code env build

## list of tasks1.0

| task                                 | Library file |
| ------------------------------------ | ------------ |
| drive the robot                      | RPI.GPIO     |
| Follow Track according to the camera | OPENCV       |
| Obstacle detection method            | OPENCV       |

