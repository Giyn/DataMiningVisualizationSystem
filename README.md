# DataMiningVisualizationSystem

[![](https://img.shields.io/badge/release-beta-blue.svg)](https://github.com/Giyn/DataMiningVisualizationSystem/releases/tag/1.0) [![https://github.com/Giyn/DataMiningVisualizationSystem/releases/tag/1.0](https://img.shields.io/badge/version-1.0.0-red.svg)](https://github.com/Giyn/DataMiningVisualizationSystem/releases/tag/1.0) [![https://github.com/Giyn/DataMiningVisualizationSystem/releases/tag/1.0](https://img.shields.io/badge/build-passing-green.svg)](https://github.com/Giyn/DataMiningVisualizationSystem/releases/tag/1.0)



## :scroll: Introduction

🌀 数据挖掘可视化系统（Data Mining Visualization System）通过数据挖掘理论、机器学习算法以及数据可视化等信息技术，并基于 Flask 框架搭建 Web 服务器，实现数据挖掘可视化。

后台技术：Flask

前端技术：HTML、JS、CSS、Echarts



## :arrow_right_hook: Instruction

配置完 Python 虚拟环境后，修改 `.\js\DMVSystem.js` 文件中的 `var serverAddress` 为本机地址后，运行 `.\App\main.py`，接着打开 `DMVSystem.html` 文件，即可进行本地测试。



## :sparkle: Features

### 1. 系统主界面

进入系统主界面，系统提供 6 个数据集，用户可以选择导入其中 1 个数据集。

![系统主界面.png](https://github.com/Giyn/DataMiningVisualizationSystem/blob/master/Screenshot/%E7%B3%BB%E7%BB%9F%E4%B8%BB%E7%95%8C%E9%9D%A2.png?raw=true)



### 2. 导入数据集

选择导入数据集后，静候片刻，数据集即加载完毕。

![导入数据集.png](https://github.com/Giyn/DataMiningVisualizationSystem/blob/master/Screenshot/%E5%AF%BC%E5%85%A5%E6%95%B0%E6%8D%AE%E9%9B%86.png?raw=true)



### 3. 原始数据可视化

进入可视化模块，系统以平行坐标图、RadViz图、Andrew图等多种方式将原始多维数据可视化。

![可视化界面1.png](https://github.com/Giyn/DataMiningVisualizationSystem/blob/master/Screenshot/%E5%8F%AF%E8%A7%86%E5%8C%96%E7%95%8C%E9%9D%A21.png?raw=true)

![可视化界面2.png](https://github.com/Giyn/DataMiningVisualizationSystem/blob/master/Screenshot/%E5%8F%AF%E8%A7%86%E5%8C%96%E7%95%8C%E9%9D%A22.png?raw=true)



### 4. 原始数据集表格展示

下拉页面可以看到原始数据的表格展示，用户可点击数据预处理并进行训练。

![原始数据集表格展示.png](https://github.com/Giyn/DataMiningVisualizationSystem/blob/master/Screenshot/%E5%8E%9F%E5%A7%8B%E6%95%B0%E6%8D%AE%E9%9B%86%E8%A1%A8%E6%A0%BC%E5%B1%95%E7%A4%BA.png?raw=true)



### 5. 模型训练及数据挖掘结果可视化

静候片刻，即出现模型训练及数据挖掘的可视化结果。

![模型训练及数据挖掘结果可视化.png](https://github.com/Giyn/DataMiningVisualizationSystem/blob/master/Screenshot/%E6%A8%A1%E5%9E%8B%E8%AE%AD%E7%BB%83%E5%8F%8A%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98%E7%BB%93%E6%9E%9C%E5%8F%AF%E8%A7%86%E5%8C%96.png?raw=true)

