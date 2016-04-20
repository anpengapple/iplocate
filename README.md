# iplocate
A python tool for ip->location
写英文说明好别扭啊！还是直接写中文吧！

用法说明：

1、首先启动server：
python ipserver.py ip.txt
启动服务。这时候ip.txt会加载到内存中。ip.txt使用的是纯真IP数据库（http://www.cz88.net）。

2、使用client查询ip：
python client.py x.x.x.x
x.x.x.x是要查询的ip地址。输入后即可定位到地址。例如：

$ python ipclient.py 213.219.39.19
英国
