# xx_lab_weather_positioning_system

## 0 系统作用
- 本系统包括北斗定位模块、气象百叶窗以及气象定位系统软件。  
- 北斗定位模块内含双模定位芯片，快速定位位置，并且将定位信息以 RS485 接口和 Modbus 协议的方式提供给用户使用。  
- 气象百叶箱一种固定式的多合一地面自动观测设备，主要监测温度和湿度。  
- 气象定位系统软件将采集外设与PC端的数据库互联，实现实时存储采集数据的任务。

## 1 系统环境
|名称|内容|
|:---:|:---:|
|主机环境：|Windows10|
|气象百叶窗：|JXBS-3001-BYX|
|北斗定位模块：|HS6601|
|数据库：|mysql-8.0.27|  
 
**note：该版本未适配于Ubuntu系统**

## 2 系统参数
- 检测参数  

|技术参数|测量范围|分辨率|精度|单位|  
|:---:|:---:|:---:|:---:|:---:| 
|温度|-40 - 80|0.1|±0.2|℃|
|湿度|0-100|0.1|±3|%RH|
|纬度|0 - 90|10-5|2.5米|N / S|
|经度|0 - 180|10-5|2.5米|E / W|  

- 系统参数 

|参数|范围|
|:---:|:---:|
|气象供电|12-24V|
|北斗供电|DC 5 ~ 28 V|
|通信方式|RS485|
|工作温度|-40-70℃|
|气象工作湿度|0-95%RH 无凝露|
|北斗工作湿度|5-95%RH 无凝露|

## A 系统介绍
- [硬件说明](./details/hw_details.md)。
- [数据库配置](./details/db_config.md)。
- [系统测试](./details/system_test.md)。
- [系统常见问题](./details/Q&A.md)。


