# Auto_maching_learning 自动机器学习平台
自动机器学习平台：     
自定义数据分析方式，生成可视化图表    
一键读取数据、预处理数据、训练模型、评估模型。    
生成 .py、.ipynb等格式的Python源码。


### 一、配置信息
* 运行平台:windows/linux
* python version:3.6
* 前端框架:vue 2.9.6
* 后端框架:django 3.0
* 数据库:mongodb,mysql
* 依赖库；django、numpy、pandas、sklearn、matplotlib、mongoengine

### 二、目录结构

├─Auto_maching_learning    
│  │  asgi.py    
│  │  settings.py    
│  │  urls.py    
│  │  wsgi.py    
│  │  __init__.py    
│  │  
├─Datasets    
│      hour.csv    
├─model_selection    
│  │  admin.py    
│  │  apps.py    
│  │  models.py    
│  │  tests.py    
│  │  urls.py    
│  │  views.py    
│  │  __init__.py    
│  │  
│  ├─migrations    
    
│              
└─templates    
    └─dist    
        │  .gitkeep    
        │  index.html    
        │      
        └─static    
            
│  manage.py    
│  Readme.md    

           
### 三、mongodb出现问题
1、开放远程端口
`sudo /sbin/iptables -I INPUT -p tcp --dport 27017 -j ACCEPT`
2、`systemctl restart mongod`失败
- 原因:没有给sockw文件设置权限
- 解决方法:`sudo chown mongod:mongod /tmp/mongodb-27017.sock`

### 四、问题代办
- [ ] 选择数据集后，数据集各列的响应速度性能优化（考虑存储文件的时候新增cols列） 