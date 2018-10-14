
# docker容器环境搭建
	1) 下载ubuntu18.04: docker pull ubuntu:18.04
	2) docker run -d [镜像ID] (基于ubuntu18.04创建容器)
	3) docker attach [镜像ID] (进入容器)
	4) 安装python需要的各种库: pip3 install ...
	6) 安装mongodb: 
		apt-get install mongodb
	   配置mongodb: 
		vim /etc/mongodb.conf  注释bind_ip:127.0.0.1
	6) 安装redis: 
		apt-get install redis-server
	   配置redis: 
		vim /etc/redis/redis.conf  注释bind:127.0.0.1,并把protected-mode改为no

# 基于docker容器创建新镜像
	1) docker commit [容器ID] [新镜像名称:新镜像版本号] (创建新容器)
	2) 然后基于新镜像创建多个容器,这些容器都继承了之前已经搭建好的系统环境
	3) 重启redis: 
		/etc/init.d/redis-server restart  
	4) 测试远程连接: 
		redis-cli -h 192.168.xxx,xxx -p 6379 

# 爬虫任务的配置与执行
	1) 从宿主机拷贝爬虫项目到docker容器根目录下:
		sudo docker cp [宿主机路径] [容器ID或名称]:[容器路径]
	2) docker attach [容器ID或名称] (进入容器)
	3) 进入爬虫项目目录, 执行(PYTHONIOENCODING=utf8) python3 run.py
