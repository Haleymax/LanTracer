# LanTracer
基于Django和Vue3实现的局域网内设备信息监测平台

## 1. 运行环境
### 1.1 python环境
* python版本: python3.10 以上版本
* 创建python虚拟环境:
```shell
virtualenv env
source venv/bin/activate
```
* 依赖安装
```shell
pip install -r requirements.txt
```
* 如有更改需导入依赖
```shell
pip freeze > requirements.txt
```

### 1.2 系统环境
该项目可在 Linux、MacOS、windows系统下运行

### 1.3 软件依赖
* 可以通过Docker拉取所需软件
```shell
cd docker
docker-compose up
```
>需要使用Docker需自己安装Docker,也可以选择本地部署相关服务

### 1.4 客户端环境
客户端使用的所有代码均为使用python自带的库，确保节点机器上安装有python3.10以上的版本即可

## 2. 服务端
基于django实现的用于接收节点发送信息的Server，同时也提供了供前端数据交互的api
### 2.1 修改配置
1. 修改`/server/server/setting.py`配置文件
```shell
cd /server/server
vim setting.py
```
2. 修改MySQL配置
```shell
# 找到这一段
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tracer',
        'USER': 'root', # 若有自己设置需修改为自己的用户
        'PASSWORD': 'root', # 若有自己的设置修改为自己的密码
        'HOST': '127.0.0.1', # 若没有部署在本机上需要修改MySQL所在主机地址
        'PORT': '3308', # 修改为自己启动的MySQL端口号
    }
}
```
3. 修改redis缓存配置
```shell
# 找到这一段
#cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        # 同样是将redis的服务信息修改为自己所起主机的地址和端口号
        'LOCATION': 'redis://127.0.0.1:6380',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### 2.2 初始化项目并启动后端
1. 在项目的根目录下执行以下命令初始化数据库表结构
```shell
python manage.py migrate
```
2. 启动后端
```shell
python manage.py runserver
```

## 3. 前端
前端使用vue3实现
### 3.1 安装前端依赖
```shell
cd web
npm install
```
### 3.2 启动前端
```shell
npm run dev
```

## 3.节点客户端
### 3.1 获取密钥
```shell
cd node_client
python manager.py getkey
```

### 3.2 启动客户端
```shell
python manager.py runclient
```
