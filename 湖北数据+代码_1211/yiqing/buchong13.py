# -*- coding: utf-8 -*-
"""
@Author  : 343
@Project: BigData35
@Date  : 2020-11-19 10:00:24
@Desc : 养老院 整体用电变化率 名单
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

    # 建立 各养老院疫情前_后每日用电能力指数表
    ylyid_rq_ydnlzs1 = pd.DataFrame(columns=('养老院id', '日期', '用电能力指数'))

    # 建立 各养老院疫情前_后整体用电能力变化表
    ylyid_jd_ydnlzs_ztbhl = pd.DataFrame(columns=('养老院id', '疫情前平均用电能力指数', '疫情后平均用电能力指数', '整体变化率'))

    # 计算 各养老院平均用电能力指数
    for i in range(yly_data.shape[0]):
        # 获取养老院 第一次筛选
        yly = yly_data[i]

        for j in range(yyq_data.shape[0]):
            # 获取 时间 第二次筛选
            rq = yyq_data[j]

            if rq != datetime.date(2020, 2, 29):
                # 获取 去年日期
                datetool = lambda x: datetime.date(x.year - 1, x.month, x.day)
                rq2 = datetool(rq).strftime("%Y-%m-%d %H:%M:%S")
                # print(rq, rq2)

                # 获取此日正常养老机构数
                zcyly_data = (data[(data['data_date'] == rq) & (data['sfhy'] == 1)])

                if zcyly_data.empty == False:
                    zcyly = (data[(data['data_date'] == rq) & (data['sfhy'] == 1)]).shape[0]

                    # 获取 此日总养老院数
                    zyly = (data[data['data_date'] == rq])['ylyid'].unique().shape[0]

                    # 获取 此日总用电量1 (2020)
                    zydl_data = (data[(data['data_date'] == rq) & (data['ylyid'] == yly)])

                    # 获取 此日总用电量2 (2019)
                    zydl_data2 = (data[(data['data_date'] == rq2) & (data['ylyid'] == yly)])

                    if ((zydl_data.empty == False) & (zydl_data2.empty == False)):
                        zydl1 = zydl_data['xqdl'].sum()
                        zydl2 = zydl_data2['xqdl'].sum()

                        if zydl2 != 0:

                            # 计算 该地该日养老机构用电能力指数
                            ydnlzs = (zcyly / zyly) * 0.5 + (zydl1 / zydl2) * 0.5

                            # 将日期转换为 xx月xx日格式
                            month = datetime.datetime.strftime(rq, '%m')
                            day = datetime.datetime.strftime(rq, '%d')
                            rq3 = month + '月' + day + '日'

                            # 数据入表
                            ylyid_rq_ydnlzs1 = ylyid_rq_ydnlzs1.append(pd.DataFrame({'养老院id': [yly], '日期': [rq3], '用电能力指数': [ydnlzs]}),
                                                         ignore_index=True)

        for j in range(yyh_data.shape[0]):
            # 获取时间 第二次筛选
            rq = yyh_data[j]

            if rq != datetime.date(2020, 2, 29):
                # 获取 去年日期
                datetool = lambda x: datetime.date(x.year - 1, x.month, x.day)
                rq2 = datetool(rq).strftime("%Y-%m-%d %H:%M:%S")
                # print(rq, rq2)

                # 获取此日正常养老机构数
                zcyly_data = (data[(data['data_date'] == rq) & (data['sfhy'] == 1)])

                if zcyly_data.empty == False:
                    zcyly = (data[(data['data_date'] == rq) & (data['sfhy'] == 1)]).shape[0]

                    # 获取 此日总养老院数
                    zyly = (data[data['data_date'] == rq])['ylyid'].unique().shape[0]

                    # 获取 此日总用电量1 (2020)
                    zydl_data = (data[(data['data_date'] == rq) & (data['ylyid'] == yly)])

                    # 获取 此日总用电量2 (2019)
                    zydl_data2 = (data[(data['data_date'] == rq2) & (data['ylyid'] == yly)])

                    if ((zydl_data.empty == False) & (zydl_data2.empty == False)):
                        zydl1 = zydl_data['xqdl'].sum()
                        zydl2 = zydl_data2['xqdl'].sum()

                        if zydl2 != 0:
                            # 计算 该地该日养老机构用电能力指数
                            ydnlzs = (zcyly / zyly) * 0.5 + (zydl1 / zydl2) * 0.5

                            # 将日期转换为 xx月xx日格式
                            month = datetime.datetime.strftime(rq, '%m')
                            day = datetime.datetime.strftime(rq, '%d')
                            rq3 = month + '月' + day + '日'

                            # 数据入表
                            ylyid_rq_ydnlzs1 = ylyid_rq_ydnlzs1.append(
                                pd.DataFrame({'养老院id': [yly], '日期': [rq3], '用电能力指数': [ydnlzs]}),
                                ignore_index=True)
    ylyid_rq_ydnlzs1.to_excel(f'{listdata_addr}各地市疫情前_后每日用电能力指数表.xlsx')

    # 计算 各养老院用电能力指数整体变化率
    for i in range(yly_data.shape[0]):
        # 获取该地市 疫情前的平均用电能力指数
        yly = yly_data[i]

        # 获取该养老院 疫情前的用电能力指数
        ydnlzs1_data = ylyid_rq_ydnlzs1[
            (ylyid_rq_ydnlzs1['养老院id'] == yly) & (ylyid_rq_ydnlzs1['日期'] >= '01月01日') & (ylyid_rq_ydnlzs1['日期'] <= '01月22日')]

        # 获取该地市 疫情后的用电能力指数
        ydnlzs2_data = ylyid_rq_ydnlzs1[
            (ylyid_rq_ydnlzs1['养老院id'] == yly) & (ylyid_rq_ydnlzs1['日期'] >= '04月08日') & (ylyid_rq_ydnlzs1['日期'] <= '04月29日')]

        if (ydnlzs1_data.empty == False) & (ydnlzs2_data.empty == False):
            ydnlzs1 = ydnlzs1_data['用电能力指数'].mean()
            ydnlzs2 = ydnlzs2_data['用电能力指数'].mean()

            # 数据入表
            ylyid_jd_ydnlzs_ztbhl = ylyid_jd_ydnlzs_ztbhl.append(
                pd.DataFrame({'养老院id': [yly], '疫情前平均用电能力指数': [ydnlzs1], '疫情后平均用电能力指数': [ydnlzs2]}),
                ignore_index=True)

            ylyid_jd_ydnlzs_ztbhl.eval('''
                        整体变化率=100*(疫情后平均用电能力指数-疫情前平均用电能力指数)/疫情前平均用电能力指数
                        ''', inplace=True)
    ylyid_jd_ydnlzs_ztbhl.to_excel(f'{listdata_addr}各养老院整体用电能力指数变化表.xlsx')
