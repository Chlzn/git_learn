# -*- coding: utf-8 -*-
"""
@Author  : 343
@Project: BigData35
@Date  : 2020-11-19 10:00:24
@Desc : 湖北 整体变化率
"""

import pandas as pd
import datetime

ysdata_addr = '../resource/data/ys/'
listdata_addr = '../resource/data/list/'

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

    # 养老院数据 ylyid
    yly_data = data['ylyid'].unique()

    # 时间数据
    rq_data = pd.to_datetime(data['data_date'].unique())

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

    # 建立 各地市疫情前_后每日用电能力指数表
    ds_rq_ydnlzs1 = pd.DataFrame(columns=('地市', '日期', '用电能力指数'))

    # 建立 各地市疫情中整体用电能力变化表
    ds_jd_ydnlzs_ztbhl = pd.DataFrame(columns=('地市', '疫情前平均用电能力指数', '疫情后平均用电能力指数', '整体变化率'))

    # 计算 各地市疫情前中后平均用电能力指数
    for i in range(ds_data.shape[0]):
        # 获取地市 第一次筛选
        ds = ds_data[i]
        temp1 = data[data['ssds'] == ds]
        # 疫情前
        for j in range(yyq_data.shape[0]):
            # 获取时间 第二次筛选
            rq = yyq_data[j]

            if rq != datetime.date(2020, 2, 29):
                # 获取 去年日期
                datetool = lambda x: datetime.date(x.year - 1, x.month, x.day)
                rq2 = datetool(rq).strftime("%Y-%m-%d %H:%M:%S")

                # 获取该地市此日正常养老机构数
                zcyly_data = (temp1[(temp1['data_date'] == rq) & (temp1['sfhy'] == 1)])

                if zcyly_data.empty == False:
                    zcyly = (temp1[(temp1['data_date'] == rq) & (temp1['sfhy'] == 1)]).shape[0]

                    # 获取 此日总养老院数
                    zyly = (temp1[temp1['data_date'] == rq])['ylyid'].unique().shape[0]

                    # 获取 此日总用电量1(2020年)
                    zydl_data = (ds_rq_zydl[(ds_rq_zydl['日期'] == rq) & (ds_rq_zydl['地市'] == ds)])
                    zydl1 = zydl_data['总用电量'].sum()

                    # 获取 此日总用电量1(2019年)
                    zydl_data = (ds_rq_zydl[(ds_rq_zydl['日期'] == rq2) & (ds_rq_zydl['地市'] == ds)])
                    zydl2 = zydl_data['总用电量'].sum()
                    # print(ds, rq, zydl1, zydl2)

                    # 计算 该地该日养老机构用电能力指数
                    ydnlzs = (zcyly / zyly) * 0.5 + (zydl1 / zydl2) * 0.5

                    # 将日期转换为 xx月xx日格式
                    month = datetime.datetime.strftime(rq, '%m')
                    day = datetime.datetime.strftime(rq, '%d')
                    rq3 = month + '月' + day + '日'

                    # 数据入表
                    ds_rq_ydnlzs1 = ds_rq_ydnlzs1.append(pd.DataFrame({'地市': [ds], '日期': [rq3], '用电能力指数': [ydnlzs]}),
                                                         ignore_index=True)

        # 疫情后
        for j in range(yyh_data.shape[0]):
            # 获取时间 第二次筛选
            rq = yyh_data[j]

            if rq != datetime.date(2020, 2, 29):
                # 获取 去年日期
                datetool = lambda x: datetime.date(x.year - 1, x.month, x.day)
                rq2 = datetool(rq).strftime("%Y-%m-%d %H:%M:%S")

                # 获取该地市此日正常养老机构数
                zcyly_data = (temp1[(temp1['data_date'] == rq) & (temp1['sfhy'] == 1)])

                if zcyly_data.empty == False:
                    zcyly = (temp1[(temp1['data_date'] == rq) & (temp1['sfhy'] == 1)]).shape[0]

                    # 获取 此日总养老院数
                    zyly = (temp1[temp1['data_date'] == rq])['ylyid'].unique().shape[0]

                    # 获取 此日总用电量1(2020年)
                    zydl_data = (ds_rq_zydl[(ds_rq_zydl['日期'] == rq) & (ds_rq_zydl['地市'] == ds)])
                    zydl1 = zydl_data['总用电量'].sum()

                    # 获取 此日总用电量1(2019年)
                    zydl_data = (ds_rq_zydl[(ds_rq_zydl['日期'] == rq2) & (ds_rq_zydl['地市'] == ds)])
                    zydl2 = zydl_data['总用电量'].sum()
                    # print(ds, rq, zydl1, zydl2)

                    # 计算 该地该日养老机构用电能力指数
                    ydnlzs = (zcyly / zyly) * 0.5 + (zydl1 / zydl2) * 0.5

                    # 将日期转换为 xx月xx日格式
                    month = datetime.datetime.strftime(rq, '%m')
                    day = datetime.datetime.strftime(rq, '%d')
                    rq3 = month + '月' + day + '日'

                    # 数据入表
                    ds_rq_ydnlzs1 = ds_rq_ydnlzs1.append(pd.DataFrame({'地市': [ds], '日期': [rq3], '用电能力指数': [ydnlzs]}),
                                                         ignore_index=True)

        # 疫情中
        for j in range(yyz_data.shape[0]):
            # 获取时间 第二次筛选
            rq = yyz_data[j]

            if rq != datetime.date(2020, 2, 29):
                # 获取 去年日期
                datetool = lambda x: datetime.date(x.year - 1, x.month, x.day)
                rq2 = datetool(rq).strftime("%Y-%m-%d %H:%M:%S")

                # 获取该地市此日正常养老机构数
                zcyly_data = (temp1[(temp1['data_date'] == rq) & (temp1['sfhy'] == 1)])

                if zcyly_data.empty == False:
                    zcyly = (temp1[(temp1['data_date'] == rq) & (temp1['sfhy'] == 1)]).shape[0]

                    # 获取 此日总养老院数
                    zyly = (temp1[temp1['data_date'] == rq])['ylyid'].unique().shape[0]

                    # 获取 此日总用电量1(2020年)
                    zydl_data = (ds_rq_zydl[(ds_rq_zydl['日期'] == rq) & (ds_rq_zydl['地市'] == ds)])
                    zydl1 = zydl_data['总用电量'].sum()

                    # 获取 此日总用电量1(2019年)
                    zydl_data = (ds_rq_zydl[(ds_rq_zydl['日期'] == rq2) & (ds_rq_zydl['地市'] == ds)])
                    zydl2 = zydl_data['总用电量'].sum()
                    # print(ds, rq, zydl1, zydl2)

                    # 计算 该地该日养老机构用电能力指数
                    ydnlzs = (zcyly / zyly) * 0.5 + (zydl1 / zydl2) * 0.5

                    # 将日期转换为 xx月xx日格式
                    month = datetime.datetime.strftime(rq, '%m')
                    day = datetime.datetime.strftime(rq, '%d')
                    rq3 = month + '月' + day + '日'

                    # 数据入表
                    ds_rq_ydnlzs1 = ds_rq_ydnlzs1.append(pd.DataFrame({'地市': [ds], '日期': [rq3], '用电能力指数': [ydnlzs]}),
                                                         ignore_index=True)

    # 计算 各地市用电能力指数整体变化率
    for i in range(ds_data.shape[0]):
        # 获取该地市 疫情前的平均用电能力指数
        ds = ds_data[i]

        # 获取该地市 疫情前的用电能力指数
        ydnlzs1_data = ds_rq_ydnlzs1[
            (ds_rq_ydnlzs1['地市'] == ds) & (ds_rq_ydnlzs1['日期'] >= '01月01日') & (ds_rq_ydnlzs1['日期'] <= '01月22日')]

        # 获取该地市 疫情后的用电能力指数
        ydnlzs2_data = ds_rq_ydnlzs1[
            (ds_rq_ydnlzs1['地市'] == ds) & (ds_rq_ydnlzs1['日期'] >= '04月08日') & (ds_rq_ydnlzs1['日期'] <= '04月29日')]

        # 获取该地市 疫情中的用电能力指数
        ydnlzs3_data = ds_rq_ydnlzs1[
            (ds_rq_ydnlzs1['地市'] == ds) & (ds_rq_ydnlzs1['日期'] >= '01月23日') & (ds_rq_ydnlzs1['日期'] <= '04月07日')]

        if (ydnlzs1_data.empty == False) & (ydnlzs2_data.empty == False) & (ydnlzs3_data.empty == False):
            # 疫情前
            ydnlzs1 = ydnlzs1_data['用电能力指数'].mean()
            # 疫情后
            ydnlzs2 = ydnlzs2_data['用电能力指数'].mean()
            # 疫情中
            ydnlzs3 = ydnlzs3_data['用电能力指数'].mean()

            # 数据入表
            ds_jd_ydnlzs_ztbhl = ds_jd_ydnlzs_ztbhl.append(
                pd.DataFrame(
                    {'地市': [ds], '疫情前平均用电能力指数': [ydnlzs1], '疫情后平均用电能力指数': [ydnlzs2], '疫情中平均用电能力指数': [ydnlzs3]}),
                ignore_index=True)

            ds_jd_ydnlzs_ztbhl.eval('''
                        整体变化率=100*(疫情后平均用电能力指数-疫情前平均用电能力指数)/疫情前平均用电能力指数
                        ''', inplace=True)
    ds_jd_ydnlzs_ztbhl.to_excel(f'{listdata_addr}各地市整体用电能力指数变化表_1224.xlsx')
