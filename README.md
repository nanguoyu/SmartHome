# SmartHome
这是一个在树莓派运行的智能家居DEMO.
## 这是什么？
这是我在2018年3月-2018年5月期间给同学写的基于树莓派的智能家居DEMO.
该项目基于python的flask开发，实现了在web端:
1. 控制摄像头采集图片
2. 读取DHT11传感器数据
3. 读取人体红外传感器的数据
4. 读取光照强度传感器的数据

项目简单，易部署。但是需要完善的树莓派环境。

## 前期准备

待补充

## 如何部署？
1. 下载全部代码到你的树莓派
2. 初始化摄像头
```shell
cd SmartHome
./SmartHomeInit.sh
```
3. 启动程序
```python
cd Web
python view.py
```
你可以在0.0.0.0:10086 访问

## 示例

web界面
![截图](http://ww1.sinaimg.cn/large/8268f477ly1g0n82rmbfjj20vd0qgdv5.jpg)

DHT11温湿度传感器在客户端的读数
![截图](http://ww1.sinaimg.cn/large/8268f477ly1g0n7yvnkvnj20wv03mmx1.jpg)

室外温湿度与穿衣建议
![截图](http://ww1.sinaimg.cn/large/8268f477ly1g0n7zxje5zj20y305idft.jpg)

视频监控
![截图](http://ww1.sinaimg.cn/large/8268f477ly1g0n80t7jrvj20w50g6qjl.jpg)

开关控制
![截图](http://ww1.sinaimg.cn/large/8268f477ly1g0n81ff431j20yl056wed.jpg)


