# -*- coding: utf-8 -*-
"""
@Author  : 343
@Project: BigData35
@Date  : 2020-11-19 14:27:14
@Desc :  根据需求画对应图片
        数据来源指标计算 2 3 4 对应的表数据
"""
# 导入第三方库
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import math
from matplotlib.ticker import FuncFormatter
from matplotlib.pyplot import MultipleLocator
from pandas import DataFrame
from matplotlib.ticker import MaxNLocator

import warnings

# 忽略警告
warnings.filterwarnings("ignore")

# 导入自定义库
from utils.style_util import StyleUtil
from utils.models_util import ModelUtil

listdata_addr = '../resource/data/list/'
ds_addr = '../resource/data/hb/'


class HuaTu:

    # 图18 湖北各地市养老机构用电变化率
    def img18_yljgydbhl(self):
        """
        # 图18 湖北各地市养老机构用电变化率
        :return:
        """
        style = StyleUtil()
        style.set_figure()
        ds = ['随州', '黄冈', '宜昌', '黄石', '恩施', '武汉', '咸宁', '荆门', '十堰', '孝感', '仙桃', '襄阳', '荆州', '鄂州', '天门', '潜江']
        # ds = ['黄石', '恩施', '武汉', '咸宁', '荆门', '仙桃', '襄阳', '荆州', '天门', '潜江']
        color = ['black', 'aqua', 'blue', 'fuchsia', 'gray', 'green', 'lime', 'maroon', 'navy', 'olive', 'purple',
                 'red', 'silver', 'teal', 'pink', 'yellow']
        for i in range(len(ds)):
            ds_str = ds[i]
            color_str = color[i]
            rq_ydyxl = pd.read_excel(f'{ds_addr}{ds_str}每日用电变化率表.xlsx').sort_values(by='日期', axis=0)
            x4 = rq_ydyxl['日期']
            y4 = rq_ydyxl['用电变化率(%)']
            plt.plot(x4, y4, 'o-', color=color_str, linewidth=0.5, markersize=1.5, label=ds_str)

        plt.ylabel("用电变化率")
        plt.gca().xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d'))
        plt.xticks(pd.date_range('2020-1-1', '2020-4-30', freq='20d'))
        plt.legend(ncol=6, loc=(0, 1))

        # plt.title(f'{ds}_养老机构用电变化率')

        # y轴添加百分号
        def to_percent(temp, position):
            return '%1.0f' % temp + '%'

        plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))

        mu = ModelUtil()
        mu.save_pic(plt, f'图18 湖北各地市养老机构用电变化率_16')


if __name__ == '__main__':
    ht = HuaTu()
    ht.img18_yljgydbhl()

