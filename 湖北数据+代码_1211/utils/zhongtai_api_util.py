# -*- coding: utf-8 -*-
"""
@Author  : ctjc
@Project:
@Date  : 2020-09-01 10:20:01
@Desc : 阿里中台API接口工具类：通过阿里中台API接口获取rds中的数据
"""

import requests
import json
import math
from pandas import Series, DataFrame
import os
import logging

class ZhongtaiApiUtil:

    def __init__(self):
        self.API_HOST = 'http://28461080ad454e80b8b5b5d17100bb77.apigateway.res.sgmc.sgcc.com.cn'  # 域名
        self.API_APPCODE = 'ab2b740822c642feac9ee01fd937fa65'  # appcode
        self.API_PAGESIZE = 2000  # 每页数据量默认值


    def get_apidata(self, method, param=""):
        """
        调用阿里中台api模板
        :param method: api接口方法名
        :param param:  api接口参数名
        :param filename: 文件名（如果想将从中台获取到的数据保存为Excel可以传此参数，如果不需要保存则传空串，如：""）
        :return:
        """

        try:
            # ###①获取数据总量：先以获取一页10条数据的方式模拟请求一次接口，来获取数据总量
            # 1.1拼接请求api接口的地址
            url_test = f"{self.API_HOST}/{method}?appCode={self.API_APPCODE}&pageNum=1&pageSize=10{param}"

            # 1.2使用requests请求api
            data_json_test = requests.get(url_test)
            data_json_test.raise_for_status()

            # 1.3将拿到的json数据转换为dict，然后获取数据总量：totalNum
            data_dict_test = json.loads(data_json_test.text)
            total_num = data_dict_test.get('data').get('totalNum')

            if total_num == 0:
                logging.info(f"ZhongtaiApiUtil get_apidata_no_param api方法-{method}接口:无数据")
            else:
                # ###②真正开始请求api接口获取“原始数据”
                datas_list = []
                # 2.1计算总页码数
                page_total_num = math.ceil(total_num / self.API_PAGESIZE)  # （向上取整）
                print(f"总页码数：{page_total_num}")
                print(f"总量数据：{total_num}")

                # ##2.2根据页码总数进行循环翻页取数：默认一页2000条，将每页的数据存到同一个数组中，数据格式： [{"id":1,"name":"a"},{"id":2,"name":"b"},{"id":3,"name":"c"}]
                for page_num in range(page_total_num):
                    url = f"{self.API_HOST}/{method}?appCode={self.API_APPCODE}&pageNum={page_num + 1}&pageSize={self.API_PAGESIZE}{param}"
                    data_json = requests.get(url)
                    data_dict = json.loads(data_json.text)
                    # 获取 rows 里的内容 结果是列表 里面包着字典
                    data_list = data_dict.get('data').get('rows')
                    datas_list += data_list

                # 2.3数组转字典，数据格式：{"id":[1,2,3],"name":["a","b","c"]}
                datas_dict = {}
                for _ in datas_list:
                    for k, v in _.items():
                        datas_dict.setdefault(k, []).append(v)

                # 2.4将字典转换为 DataFrame，并保存：此时的df和rds中的数据一样，可以理解为是未经过清洗的原始数据
                df = DataFrame(data=datas_dict)

                return df

        except Exception as e:
            logging.error(f'ApiDemo get_apidata api方法-{method}接口异常:{e}')
            raise

