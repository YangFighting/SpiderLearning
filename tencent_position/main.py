#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/12/8 21:21
# @Author  : ZhangYang
# @File    : main.py

from scrapy.cmdline import execute
import os
import sys
if __name__ == '__main__':

    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(['scrapy','crawl','hr'])