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


class HuaTu:

    # 图18 养老机构用电变化率
    def img18_yljgydbhl(self):
        """
        # 图18 养老机构疫情疫情影响率
        :return:
        """
        style = StyleUtil()
        style.set_figure()

        rq_ydyxl = pd.read_excel(f'{listdata_addr}每日用电变化率表.xlsx').sort_values(by='日期', axis=0)

        x4 = rq_ydyxl['日期']
        y4 = rq_ydyxl['用电变化率(%)']
        plt.plot(x4, y4, 'o-', color="#4e79a7", linewidth=0.5, markersize=1.5)
        plt.ylabel("用电变化率")
        plt.gca().xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d'))
        plt.xticks(pd.date_range('2020-1-1', '2020-4-30', freq='20d'))

        # 添加文字和竖线
        plt.text(x4[10], 14, '疫情前', fontsize=10, color='gray')
        plt.text(x4[50], 14, '疫情中', fontsize=10, color='gray')
        plt.text(x4[100], 14, '疫情后', fontsize=10, color='gray')
        plt.vlines(x4[23], -28, 15, colors='gray', linestyles='--', linewidth=0.5)
        plt.vlines(x4[97], -28, 15, colors='gray', linestyles='--', linewidth=0.5)

        # y轴添加百分号
        def to_percent(temp, position):
            return '%1.0f' % temp + '%'

        plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))

        mu = ModelUtil()
        mu.save_pic(plt, f'图18 养老机构用电变化率')

    # 各规模养老机构用电变化率：报告中只写数字不填图
    def draw_ggmydbhl(self):
        """
        # 各规模养老机构平均用电影响率
        :return:
        """
        style = StyleUtil()
        style.set_figure()

        scale_pjydyxl = pd.read_excel(f'{listdata_addr}各规模平均用电变化率表.xlsx').sort_values(by='平均用电变化率(%)', axis=0,
                                                                                      ascending=False)
        scale_pjydyxl['平均用电变化率(%)'] = round(scale_pjydyxl['平均用电变化率(%)'])
        scale_pjydyxl['平均用电变化率(%)'] = scale_pjydyxl['平均用电变化率(%)'].map(lambda x: math.trunc(x))
        # scale_pjydyxl = scale_pjydyxl.sort_values(by='平均用电影响率(%)', axis=0, ascending=False)
        x7 = scale_pjydyxl['规模']
        y7 = scale_pjydyxl['平均用电变化率(%)']
        for x, y in zip(x7, y7):
            y1 = str(y) + '%'
            plt.text(x, y, y1, ha='center', va='bottom', fontsize=10)
        plt.bar(x7, y7, 0.2, color="#4e79a7")
        plt.ylabel("平均用电变化率")

        # y轴添加百分号
        def to_percent(temp, position):
            return '%1.0f' % temp + '%'

        plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))

        mu = ModelUtil()
        mu.save_pic(plt, '各规模养老机构用电变化率')

    # 图19 各区县养老机构用电变化率排名
    def img19_qxydbhl(self):
        """
        # 图19 各地市养老机构平均用电影响率
        :return:
        """
        style = StyleUtil()
        style.set_figure()

        ds_pjydyxl = pd.read_excel(f'{listdata_addr}各地市平均用电变化率表.xlsx').sort_values(by='平均用电变化率(%)', axis=0,
                                                                                   ascending=False)

        ds_pjydyxl['均线'] = ds_pjydyxl['平均用电变化率(%)'].mean()

        plt.figure()
        ax = plt.subplot()
        x5 = ds_pjydyxl['地市']
        y5 = ds_pjydyxl['平均用电变化率(%)']
        plt.bar(x5, y5, 0.4, color="#4e79a7")
        plt.ylabel("平均用电变化率")
        ax.set_xticklabels(labels=style.wenziShu(x5))

        # x_major_locator = MultipleLocator(1.2)
        # ax.xaxis.set_major_locator(x_major_locator)

        # y轴添加百分号
        def to_percent(temp, position):
            return '%1.0f' % temp + '%'

        plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))

        mu = ModelUtil()
        mu.save_pic(plt, '图19 各区县养老机构用电变化率排名')

    # 图20 养老机构用电能力指数变化趋势
    def img20_yljgydnlzs(self):
        """
        图20 养老机构用电能力指数变化趋势
        :return:
        """
        style = StyleUtil()
        style.set_figure()

        rq_ydnlzs = pd.read_excel(f'{listdata_addr}湖北每日用电能力指数表.xlsx').sort_values(by='日期', axis=0)

        x1 = rq_ydnlzs['日期']
        y1 = rq_ydnlzs['用电能力指数']
        plt.plot(x1, y1, 'o-', color="#4e79a7", linewidth=0.5, markersize=1.8)
        plt.ylim(0, 1.2)  # y轴限制
        plt.ylabel("用电能力指数")
        plt.gca().xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d'))
        plt.xticks(pd.date_range('2020-1-1', '2020-4-30', freq='20d'))

        # 添加文字和竖线
        plt.text(x1[10], 1.1, '疫情前', fontsize=12)
        plt.text(x1[50], 1.1, '疫情中', fontsize=12)
        plt.text(x1[100], 1.1, '疫情后', fontsize=12)
        plt.vlines(x1[23], 0.0, 1.2, colors='gray', linestyles='--', linewidth=0.5)
        plt.vlines(x1[97], 0.0, 1.2, colors='gray', linestyles='--', linewidth=0.5)

        mu = ModelUtil()
        mu.save_pic(plt, '图20 养老机构用电能力指数变化趋势')

    # 图21 各区县用电能力指数排名
    def img21_qxydnlzs(self):
        """
        # 图21 各地市平均用电能力指数排名
        :return:
        """
        style = StyleUtil()
        style.set_figure()

        ds_pjydnlzs = pd.read_excel(f'{listdata_addr}各地市平均用电能力指数表.xlsx').sort_values(by='平均用电能力指数', axis=0,
                                                                                     ascending=False)

        ds_pjydnlzs['均线'] = ds_pjydnlzs['平均用电能力指数'].mean()

        plt.figure()
        ax = plt.subplot()

        ax.plot(ds_pjydnlzs['地市'], ds_pjydnlzs['均线'], c='grey', dashes=[6, 2], label='均线')

        x2 = ds_pjydnlzs['地市']
        y2 = ds_pjydnlzs['平均用电能力指数']
        plt.bar(x2, y2, 0.4, color="#4e79a7")
        plt.ylabel("用电能力指数")

        ax.set_xticklabels(labels=style.wenziShu(x2))

        mu = ModelUtil()
        mu.save_pic(plt, '图21 各区县用电能力指数排名')

    # 图22 床均用电量变化较大养老机构区县分布
    def img22_qx_cjydl_bhjd(self):
        """
        # 图22 各地市平均用电能力指数排名
        :return:
        """
        style = StyleUtil()
        style.set_figure()

        ds_cjydbhl = pd.read_excel(f'{listdata_addr}湖北_各养老院床均用电变化率1.xlsx')
        ds_cjydbhl = ds_cjydbhl[ds_cjydbhl['床均用电变化率'] <= -90]
        cjydbhl_jd = ds_cjydbhl[['地市', '养老院名称']]
        cjydbhl_jd = cjydbhl_jd.groupby('地市').count()
        cjydbhl_jd = DataFrame(cjydbhl_jd)
        cjydbhl_jd = cjydbhl_jd.sort_values(by='养老院名称', axis=0, ascending=False)
        cjydbhl_jd.reset_index(inplace=True)
        cjydbhl_jd['养老院名称'] = cjydbhl_jd['养老院名称'].map(lambda x: math.trunc(x))
        print(cjydbhl_jd)

        ax1 = plt.figure().gca()
        ax1.yaxis.set_major_locator(MaxNLocator(integer=True))

        x2 = cjydbhl_jd['地市']
        y2 = cjydbhl_jd['养老院名称']
        plt.bar(x2, y2, 0.25, color="#4e79a7")
        plt.ylabel("养老机构数（个）")
        for x, y in zip(cjydbhl_jd['地市'], cjydbhl_jd['养老院名称']):
            plt.text(x, y, y, ha='center', va='bottom', fontsize=10)
        # plt.ylim(0,3)

        mu = ModelUtil()
        mu.save_pic(plt, '图22 床均用电量变化较大养老机构区县分布')

    # 图23 各区县用电量降幅较大养老机构分布
    def img23_qxydnlzs(self):
        """
        # 图23 各区县用电量降幅较大养老机构分布
        :return:
        """
        style = StyleUtil()
        style.set_figure()

        ds_pjydbhl = pd.read_excel(f'{listdata_addr}各养老院平均用电变化率表1.xlsx')
        ds_pjydbhl = ds_pjydbhl[ds_pjydbhl['平均用电变化率(%)'] <= -90]
        pjydbhl_jd = ds_pjydbhl[['地市', '养老院名称']]
        pjydbhl_jd = pjydbhl_jd.groupby('地市').count()
        pjydbhl_jd = DataFrame(pjydbhl_jd)
        pjydbhl_jd = pjydbhl_jd.sort_values(by='养老院名称', axis=0, ascending=False)
        pjydbhl_jd.reset_index(inplace=True)
        print(pjydbhl_jd)

        pjydbhl_jd['养老院名称'] = pjydbhl_jd['养老院名称'].map(lambda x: math.trunc(x))
        ax1 = plt.figure().gca()
        ax1.yaxis.set_major_locator(MaxNLocator(integer=True))

        x2 = pjydbhl_jd['地市']
        y2 = pjydbhl_jd['养老院名称']
        plt.bar(x2, y2, 0.25, color="#4e79a7")
        plt.ylabel("养老机构数（个）")
        for x, y in zip(pjydbhl_jd['地市'], pjydbhl_jd['养老院名称']):
            plt.text(x, y, y, ha='center', va='bottom', fontsize=10)
        # plt.ylim(0,3)

        mu = ModelUtil()
        mu.save_pic(plt, '图23 各区县用电量降幅较大养老机构分布')

    # 图24 各养老机构规模用电能力指数变化情况
    def img24_gmydnlzs(self):
        """
        # 图24 各地市用电能力指数整体变化情况
        :return:   #96FED1    #2828FF
        """
        style = StyleUtil()
        style.set_figure(frame=True)

        ds_rq_ydnlzs_ztbhl = pd.read_excel(f'{listdata_addr}各规模整体用电能力指数变化表.xlsx')

        ds_rq_ydnlzs_ztbhl.rename(columns={'整体变化率': '变化率'}, inplace=True)
        ds_rq_ydnlzs_ztbhl = ds_rq_ydnlzs_ztbhl.sort_values(by='疫情前平均用电能力指数', axis=0, ascending=False)
        ds_rq_ydnlzs_ztbhl.reset_index(level=0,inplace=True)

        plt.figure()
        ax1 = plt.subplot()

        x3 = ds_rq_ydnlzs_ztbhl['规模']
        y3_1 = ds_rq_ydnlzs_ztbhl['疫情前平均用电能力指数']
        y3_2 = ds_rq_ydnlzs_ztbhl['疫情后平均用电能力指数']
        n = np.arange(x3.shape[0])
        bar_width = 0.25
        plt.bar(n, y3_1, bar_width, align="center", color="#4e79a7", label='疫情前')
        plt.bar(n + bar_width, y3_2, bar_width, color=(0.3, 0.7, 0.7, 0.91), align="center", label='疫情后')
        print(n + bar_width / 2)
        plt.xticks(n + bar_width / 2, x3)

        ax2 = ax1.twinx()
        ax2.plot(x3, ds_rq_ydnlzs_ztbhl['变化率'], color="#FBDA80", label="变化率", linewidth=1.5)

        def to_percent(temp, position):
            return '%1.0f' % temp + '%'

        plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))
        # 设置X轴ticks文字竖着显示
        # ax1.set_xticklabels(labels=style.wenziShu(x3))

        # 取消边框
        ax1.spines["top"].set_visible(False)
        ax2.spines["top"].set_visible(False)

        # Y轴标签
        ax1.set_ylabel('用电能力指数')
        ax2.set_ylabel('变化率')
        # 开启图例
        leg1 = ax1.legend(handleheight=0.05, ncol=2, columnspacing=0.4, loc=(0.38, 1))
        leg2 = ax2.legend(handleheight=0.45, columnspacing=0.4, loc=(0.7, 1))

        # 取消图例的边框
        leg1.get_frame().set_linewidth(0.0)
        leg2.get_frame().set_linewidth(0.0)

        # 自动调整布局
        plt.tight_layout()
        print(ds_rq_ydnlzs_ztbhl)

        for i in range(len(ds_rq_ydnlzs_ztbhl['变化率'])):
            print('----------------')
            print(ds_rq_ydnlzs_ztbhl.loc[i]['变化率'])
            ax2.text(i,ds_rq_ydnlzs_ztbhl.loc[i]['变化率'],ds_rq_ydnlzs_ztbhl.loc[i]['变化率'])

        mu = ModelUtil()
        mu.save_pic(plt, '图24 各养老机构规模用电能力指数变化情况')

    # 图25 各区县养老机构用电能力指数变化情况
    def img25_qxydnlzsbhqk(self):
        """
        # 图25 各地市用电能力指数整体变化情况
        :return:   #96FED1    #2828FF
        """
        style = StyleUtil()
        style.set_figure(frame=True)

        ds_rq_ydnlzs_ztbhl = pd.read_excel(f'{listdata_addr}各地市整体用电能力指数变化表.xlsx')

        ds_rq_ydnlzs_ztbhl.rename(columns={'整体变化率': '变化率'}, inplace=True)
        ds_rq_ydnlzs_ztbhl = ds_rq_ydnlzs_ztbhl.sort_values(by='疫情前平均用电能力指数', axis=0, ascending=False)

        plt.figure()
        ax1 = plt.subplot()

        x3 = ds_rq_ydnlzs_ztbhl['地市']
        y3_1 = ds_rq_ydnlzs_ztbhl['疫情前平均用电能力指数']
        y3_2 = ds_rq_ydnlzs_ztbhl['疫情后平均用电能力指数']
        n = np.arange(x3.shape[0])
        # bar_width = 0.25
        bar_width = 0.3
        plt.bar(n, y3_1, bar_width, align="center", color="#4e79a7", label='疫情前')
        plt.bar(n + bar_width, y3_2, bar_width, color=(0.3, 0.7, 0.7, 0.91), align="center", label='疫情后')
        print(n + bar_width / 2)
        plt.xticks(n + bar_width / 2, x3)

        ax2 = ax1.twinx()
        ax2.plot(x3, ds_rq_ydnlzs_ztbhl['变化率'], color="#FBDA80", label="变化率", linewidth=1.5)

        def to_percent(temp, position):
            return '%1.0f' % temp + '%'

        plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))

        # 设置X轴ticks文字竖着显示
        ax1.set_xticklabels(labels=style.wenziShu(x3))
        # ax2.set_xticklabels(labels=style.wenziShu(x3))

        # 取消边框
        ax1.spines["top"].set_visible(False)
        ax2.spines["top"].set_visible(False)

        # Y轴标签
        ax1.set_ylabel('用电能力指数')
        ax2.set_ylabel('变化率')
        # 开启图例
        leg1 = ax1.legend(handleheight=0.05, ncol=2, columnspacing=0.4, loc=(0.38, 1))
        leg2 = ax2.legend(handleheight=0.45, columnspacing=0.4, loc=(0.7, 1))

        # 取消图例的边框
        leg1.get_frame().set_linewidth(0.0)
        leg2.get_frame().set_linewidth(0.0)

        # 自动调整布局
        plt.tight_layout()

        mu = ModelUtil()
        mu.save_pic(plt, '图25 各区县养老机构用电能力指数变化情况')


if __name__ == '__main__':
    ht = HuaTu()
    # ht.img18_yljgydbhl()
    # ht.img19_qxydbhl()
    # ht.img20_yljgydnlzs()
    # ht.img21_qxydnlzs()
    ht.img24_gmydnlzs()
    # ht.img25_qxydnlzsbhqk()
    # ht.draw_ggmydbhl()
    # ht.img22_qx_cjydl_bhjd()
    # ht.img23_qxydnlzs()
