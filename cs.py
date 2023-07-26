import requests  # 发送请求
from bs4 import BeautifulSoup  # 解析页面
import pandas as pd  # 存入csv数据
import os  # 判断文件存在
from time import sleep  # 等待间隔
import random  # 随机
import re  # 用正则表达式提取url
import requests

# 设置用户代理
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
}
# 构造请求参数
params = {
    'ie': 'UTF-8',
    'q': '你'
}
# 获取响应
r = requests.get('https://www.so.com/s?', headers=headers, params=params)
# 查看结果
get=r.content.decode()
with open("ls.txt","w",encoding="utf-8") as lss:
    lss.write(get)
with open("ls.txt","r",encoding="utf-8") as lsp:
    gets=lsp.readlines()
urls=[]
text=[]
for i in gets:
    if i[0:8]=="<a  href=":
        print(i)
        nrs=i.split("\"")
        urls.append(nrs[1])
        nrs=i.split("target=\"_blank\">")
        text.append(nrs[-1].replace("</a></h3>",""))
print(urls)
print(text)
