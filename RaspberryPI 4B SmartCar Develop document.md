# Technical-Project : SmartCar develop

#Author:_Liu qianrong_
				_Cao Han_
				_Liu zongzhen_

#Group:_1.7_

#Data:_2022-11_

# Step one-Prepare env



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
