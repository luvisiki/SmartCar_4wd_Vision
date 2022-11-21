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

3. choose the OS in burner and burn into the RaspberryPI 4B board. Our group choose the **Raspberry Pi OS (32-bit) -(Recommed)** as system.

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
| drive the robot                      | RPI.GPIO-BCM |
| Follow Track according to the camera | OPENCV       |
| Obstacle detection method            | OPENCV       |

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

> If you want to write code in RaspberryPI  I highly recommend VSCODE;
>
> Download ```Remote-SSH``` in expands and do some easy config,It can upgrade your code experience.

<img src="https://github.com/luvisiki/SmartCar_4wd_Vision/blob/main/img/step2/2-2.png?raw=true" alt="2-2" style="zoom: 50%;" />



# Step three: Try to use the motor to move the car.

##	RPI.GPIO and wiringPI

In Raspberry Pi, if we want to use ```GPIO``` operation, we have two choices: use the ```wiringPI``` or ```RPI``` library,  but according to the ```RPI``` developer's explanation, the ```RPI``` library is not suitable for too complicated operations, and in order to be closer to the style of the ```Arduino```, we use the ```wiringPI library``` to drive the motor and make the car move.
