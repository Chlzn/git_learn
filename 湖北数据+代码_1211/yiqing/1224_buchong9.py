# -*- coding: utf-8 -*-
"""
@Author  : 343
@Project: BigData35
@Date  : 2020-11-18 16:41:34
@Desc : 湖北各地市 用电变化率
"""
import pandas as pd
import datetime

ysdata_addr='../resource/data/ys/'
listdata_addr='../resource/data/list/'
save_addr='../resource/data/hb/'

def get_data(ds):
    data = pd.read_excel(f'{listdata_addr}源数据筛简表.xlsx')

    # 读取 每日总用电量数据表
    rq_zydl = pd.read_excel(f'{listdata_addr}各地市每日总用电量数据表.xlsx')
    rq_zydl = rq_zydl[rq_zydl['地市'] == ds]

    # 时间数据
    rq_data = pd.to_datetime(data['data_date'].unique())

    # 建立 重庆每日用电变化率表
    rq_ydbhl = pd.DataFrame(columns=('日期', '用电变化率(%)'))

    # 计算重庆电变化率
    for i in range(rq_data.shape[0]):
        # 获取日期
        rq = rq_data[i]

        if rq != datetime.date(2020, 2, 29):
            # 获取 去年日期
            datetool = lambda x: datetime.date(x.year - 1, x.month, x.day)
            rq2 = datetool(rq).strftime("%Y-%m-%d %H:%M:%S")

            # 获取 此日总用电量1 (2020）
            zydl1 = rq_zydl[(rq_zydl['日期'] == rq)]['总用电量'].sum()

            # 获取 此日总用电量2 (2019)
            zydl2 = rq_zydl[(rq_zydl['日期'] == rq2)]['总用电量'].sum()

            if zydl2 != 0:
                # 计算用电变化率
                ydbhl = 100 * (zydl1 - zydl2) / zydl2

                # 将日期转换为 xx月xx日格式
                month = datetime.datetime.strftime(rq, '%m')
                day = datetime.datetime.strftime(rq, '%d')
                rq3 = month + '月' + day + '日'

                # 数据入表
                rq_ydbhl = rq_ydbhl.append(pd.DataFrame({'日期': [rq], '用电变化率(%)': [ydbhl]}), ignore_index=True)

    rq_ydbhl.to_excel(f'{save_addr}{ds}每日用电变化率表.xlsx')


if __name__ == '__main__':
    ds = ['随州', '黄冈', '宜昌', '黄石', '恩施', '武汉', '咸宁', '荆门', '十堰', '孝感', '仙桃', '襄阳', '荆州', '鄂州', '天门', '潜江']
    for i in range(len(ds)):
        get_data(ds[i])




