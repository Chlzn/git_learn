
# -*- coding: utf-8 -*-
"""
@Author  : 343
@Project: BigData35
@Date  : 2020-11-03 11:40:38
@Desc :  数据筛简
        每日总用电量
        各地市每日总用电量
        各规模每日总用电量

"""

import pandas as pd
import datetime

ysdata_addr='../resource/data/ys/'
listdata_addr='../resource/data/list/'

if __name__ == '__main__':
    # 读取源数据
    # 需求字段为 所属地市(SSDS)  养老院id(YLYID)  数据日期(DATA_DATE)
    # 当日用电量(XQDL)   是否活跃(SFHY) 养老院规模(SCALE)

    data = pd.read_excel(f"{ysdata_addr}mxys_dlkms_rdl_hubei.xlsx")
    data = data[['ssds', 'ylyid', 'data_date', 'xqdl', 'sfhy', 'scale']]
    data['data_date'] = pd.to_datetime(data['data_date'])

    data.to_excel(f'{listdata_addr}源数据筛简表.xlsx')

    # print(data)

    # 地市数据
    ds_data = data['ssds'].unique()
    # print(ds_data)

    # 养老院数据 ylyid
    yly_data = data['ylyid'].unique()
    # print(yly_data)

    # 时间数据
    rq_data = data['data_date'].unique()
    # print(rq_data)

    # 按照需求设定 疫情日期以及 统计范围
    # 1.1-1.22为疫情前     1.23-4.07为疫情中  4.8-4.30为疫情后
    yyq_a = '2020-01-01'
    yyq_b = '2020-01-22'
    yyz_a = '2020-01-23'
    yyz_b = '2020-04-07'
    yyh_a = '2020-04-08'
    yyh_b = '2020-04-27'

    yyq_data = pd.to_datetime(
        (data[(data['data_date'] >= yyq_a) & (data['data_date'] <= yyq_b)])['data_date'].unique())
    yyz_data = pd.to_datetime(
        (data[(data['data_date'] >= yyz_a) & (data['data_date'] <= yyz_b)])['data_date'].unique())
    yyh_data = pd.to_datetime(
        (data[(data['data_date'] >= yyh_a) & (data['data_date'] <= yyh_b)])['data_date'].unique())
    # print(yyq_data)

    # 养老机构规模数据
    scale_data = data['scale'].unique()

    # 建立 重庆 每日总用电量数据
    rq_zydl = pd.DataFrame(columns=('日期', '总用电量'))

    # 建立 各地市每日总用电量数据表
    ds_rq_zydl = pd.DataFrame(columns=('地市', '日期', '总用电量'))

    # 建立 各规模养老院每日总用电量数据表
    scale_rq_zydl = pd.DataFrame(columns=('规模', '日期', '总用电量'))

    # 计算 每日总用电量数据
    for i in range(rq_data.shape[0]):
        # 获取 时间
        rq = rq_data[i]

        # 获取 此日总用电量
        zydl = (data[(data['data_date'] == rq)])['xqdl'].sum()
        # print(zydl)

        # 数据入表
        rq_zydl = rq_zydl.append(pd.DataFrame({'日期': [rq], '总用电量': [zydl], }),
                                 ignore_index=True)
    rq_zydl.to_excel(f'{listdata_addr}每日总用电量数据表.xlsx')

    # 计算 各地市每日总用电量
    for i in range(ds_data.shape[0]):
        # 获取地市
        ds1 = ds_data[i]

        for j in range(rq_data.shape[0]):
            # 获取时间
            rq = rq_data[j]

            # 获取此地市此日总电量
            zydl = (data[(data['ssds'] == ds1) & (data['data_date'] == rq)])['xqdl'].sum()

            # print(ds,rq,zydl)

            ds_rq_zydl = ds_rq_zydl.append(pd.DataFrame({'地市': [ds1],
                                                         '日期': [rq], '总用电量': [zydl], }),
                                           ignore_index=True)

    ds_rq_zydl.to_excel(f'{listdata_addr}各地市每日总用电量数据表.xlsx')

    # 计算 每个规模养老院每日总用电量数据
    for i in range(scale_data.shape[0]):
        # 获取 养老院规模
        scale = scale_data[i]

        for j in range(rq_data.shape[0]):
            # 获取 日期
            rq = rq_data[j]

            # 计算 该规模养老院该日总用电量
            zydl = data[(data['scale'] == scale) & (data['data_date'] == rq)]['xqdl'].sum()

            # 数据入表
            scale_rq_zydl = scale_rq_zydl.append(
                pd.DataFrame({'规模': [scale], '日期': [rq], '总用电量': [zydl]}), ignore_index=True)
    scale_rq_zydl.to_excel(f'{listdata_addr}各规模每日总用电量数据表.xlsx')
