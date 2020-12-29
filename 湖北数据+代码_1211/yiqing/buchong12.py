# -*- coding: utf-8 -*-
"""
@Author  : 343
@Project: BigData35
@Date  : 2020-11-19 10:00:24
@Desc : 计算养老院 用电变化率 名单
"""

import pandas as pd
import datetime

ysdata_addr='../resource/data/ys/'
listdata_addr='../resource/data/list/'

if __name__ == '__main__':
    # 读取 源数据筛简表
    # 需求字段为
    # 所属地市(ssds) 养老院id(ylyid)  数据日期(data_date)
    # 当日用电量(xqdl) 是否活跃(sfhy)  养老院规模(scale)
    data = pd.read_excel(f'{listdata_addr}源数据筛简表.xlsx')
    # print(data)

    # 读取 每日总用电量数据表
    rq_zydl = pd.read_excel(f'{listdata_addr}每日总用电量数据表.xlsx')

    # 读取 各地市每日总用电量数据表
    ds_rq_zydl = pd.read_excel(f'{listdata_addr}各地市每日总用电量数据表.xlsx')

    # 读取 各规模每日总用电量数据表
    scale_rq_zydl = pd.read_excel(f'{listdata_addr}各规模每日总用电量数据表.xlsx')

    # 地市数据
    ds_data = data['ssds'].unique()
    # print(ds_data)

    # 养老院数据 ylyid
    yly_data = data['ylyid'].unique()
    # print(yly_data)

    # 时间数据
    rq_data = pd.to_datetime(data['data_date'].unique())
    # print(rq_data)

    # 按照需求设定 疫情日期以及 统计范围
    # 1.1-1.22为疫情前     1.23-4.07为疫情中  4.8-4.30为疫情后
    yyq_a = '2020-01-01 00:00:00'
    yyq_b = '2020-01-22 00:00:00'
    yyz_a = '2020-01-23 00:00:00'
    yyz_b = '2020-04-07 00:00:00'
    yyh_a = '2020-04-08 00:00:00'
    yyh_b = '2020-04-27 00:00:00'

    yyq_data = pd.to_datetime(
        (data[(data['data_date'] >= yyq_a) & (data['data_date'] <= yyq_b)])['data_date'].unique())
    yyz_data = pd.to_datetime(
        (data[(data['data_date'] >= yyz_a) & (data['data_date'] <= yyz_b)])['data_date'].unique())
    yyh_data = pd.to_datetime(
        (data[(data['data_date'] >= yyh_a) & (data['data_date'] <= yyh_b)])['data_date'].unique())
    # print(yyq_data)

    # 养老机构规模数据
    scale_data = data['scale'].unique()

    # 建立 各养老院每日用电变化率
    ylyid_rq_ydbhl = pd.DataFrame(columns=('养老院id', '日期', '用电变化率(%)'))

    # 建立 各养老院平均用电变化率表
    ylyid_pjydbhl = pd.DataFrame(columns=('养老院id', '平均用电变化率(%)'))

    # 计算 各养老院平均用电变化率
    for i in range(yly_data.shape[0]):
        # 获取养老院 第一次筛选
        yly = yly_data[i]

        for j in range(rq_data.shape[0]):
            # 获取 时间 第二次筛选
            rq = rq_data[j]

            if rq != datetime.date(2020, 2, 29):
                # 获取 去年日期
                datetool = lambda x: datetime.date(x.year - 1, x.month, x.day)
                rq2 = datetool(rq).strftime("%Y-%m-%d %H:%M:%S")
                # print(rq, rq2)

                # 获取 此日总用电量1 (2020)
                zydl_data = (data[(data['data_date'] == rq) & (data['ylyid'] == yly)])

                # 获取 此日总用电量2 (2019)
                zydl_data2 = (data[(data['data_date'] == rq2) & (data['ylyid'] == yly)])

                if ((zydl_data.empty == False) & (zydl_data2.empty == False)):
                    zydl1 = zydl_data['xqdl'].sum()
                    zydl2 = zydl_data2['xqdl'].sum()

                    if zydl2 != 0:
                        # 计算 该日用电变化率
                        ydbhl = 100 * (zydl1 - zydl2) / zydl2

                        # 将日期转换为 xx月xx日格式
                        month = datetime.datetime.strftime(rq, '%m')
                        day = datetime.datetime.strftime(rq, '%d')
                        rq3 = month + '月' + day + '日'

                        # 数据入表
                        ylyid_rq_ydbhl = ylyid_rq_ydbhl.append(
                            pd.DataFrame({'养老院id': [yly], '日期': [rq3], '用电变化率(%)': [ydbhl]}),
                            ignore_index=True)
    ylyid_rq_ydbhl.to_excel(f'{listdata_addr}各养老院每日用电变化率表.xlsx')

    for i in range(yly_data.shape[0]):
        # 获取 养老院
        yly = yly_data[i]

        # 计算 此养老院疫情中平均用电变化率
        pjydyxl_data = (ylyid_rq_ydbhl[ylyid_rq_ydbhl['养老院id'] == yly])

        if pjydyxl_data.empty == False:
            pjydbhl = (ylyid_rq_ydbhl[ylyid_rq_ydbhl['养老院id'] == yly])['用电变化率(%)'].mean()

            # 数据入表
            ylyid_pjydbhl = ylyid_pjydbhl.append(pd.DataFrame({'养老院id': [yly], '平均用电变化率(%)': [pjydbhl]}),
                                                 ignore_index=True)
    ylyid_pjydbhl.to_excel(f'{listdata_addr}各养老院平均用电变化率表.xlsx')
