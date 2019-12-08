#   Scrapy  入门

代码目录：mySpider

## 主要步骤

1. 创建一个scrapy项目 scrapy startproject <project_name>

   scrapy startproject mySpider

2. 生成一个爬虫 scrapy genspider <spider_name> <spider_domain>

   scrapy genspider itcast "itcast.cn”

3. 完善爬虫，提取数据 

   使用 xpath 等方法，解析响应

4. 保存数据

   在 pipeline 中完成 保存数据的代码



## 创建项目

文件说明

scrapy.cfg ：项目的配置文件

mySpider/ ：项目的Python模块，将会从这里引用代码

mySpider/items.py ：项目的目标文件 ，定义字段，用于记录爬取的内容，

mySpider/pipelines.py ：项目的管道文件	保存数据

mySpider/settings.py ：项目的设置文件，配置UA，启动管道

mySpider/spiders/ ：存储爬虫代码目录，定义爬虫的内容



## 完善爬虫

- 定义爬虫的名字
- 定义允许爬取的范围，以及起始URL
- 定义解析方法 parse ，接收下载中间件传来的response
- 使用 yield 使整个函数变成生成器，节约内存



**注意**：

1. 解析方法 parse名字不能变
2. 爬取的url 必须属于 allowed_domains 下的地址



## 使用 pipline

- process_item方法中实现存储的方法
- 需要在setting文件中开启pipline
- pipline可以有多个，多个pipline属于串联关系，即在前一个pipline中对items作的处理，经过下一个pipline时依旧有作用
- pipline的权重越小，优先级越高

## 断点调试
在工程路径下增加main文件，文件内容如下

```python
from scrapy.cmdline import execute
import os
import sys
if __name__ == '__main__':    
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(['scrapy','crawl','itcast'])
```
使用pycharm进行断点调试

## 请求详情 与 翻页

当获取url列表后还需请求详情或翻页时，构造 详情和翻页url，使用 `scrapy.Request` 请求详情url，并通过参数 `meta` 来传递解析的内容

```python
# 获取详情
post_id_url = "https://careers.tencent.com/tencentcareer/api/post/ByPostId?&postId={}&language=zh-cn". \    format(position_item["post_id"])
yield scrapy.Request(post_id_url, callback=HrSpider.parse_detail, meta={"item": position_item})
# 翻页请求
if len(title_list) == self.pageSize and self.pageSize <= self.max_page_Index:
    self.pageIndex += 1
    next_page_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?pageIndex={}&pageSize={}'.format(self.pageIndex, self.pageSize)
    yield scrapy.Request(next_page_url, callback=self.parse)
```

**注意**

- 获取详情前不用 `yield` 返回 item



## pipeline使用——开始与结束

`open_spider`和`close_spide`r方法在 在开启爬虫和结束爬虫的时候执行， 只执行一次，可以在两种方法中执行文件或者数据库的初始化

对于初始化配置，可以在`setting`文件中添加字段，在通过`spider.settings.get()`的方式来访问配置信息

```python
def open_spider(self, spider):   
    """ 在开启爬虫的时候执行， 只执行一次"""    
    # 将文件清空    
    with open(spider.settings.get("SAVE_FILE_NAME"), "w", encoding="utf-8") as f:
        f.write("")    
        self.start_time = datetime.datetime.now()

def close_spider(self, spider):    
    self.end_time = datetime.datetime.now()    
    print("程序运行时间：{}s".format((self.end_time - self.start_time).seconds))
```

