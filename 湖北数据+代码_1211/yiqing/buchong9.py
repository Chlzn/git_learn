# -*- coding: utf-8 -*-
"""
@Author  : 343
@Project: BigData35
@Date  : 2020-11-18 16:41:34
@Desc : 湖北 用电变化率
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

    # 建立 重庆每日用电变化率表
    rq_ydbhl = pd.DataFrame(columns=('日期', '用电变化率(%)'))

    aaa = pd.DataFrame(columns=('日期', '用电变化率(%)','今年','去年'))

    # 建立 各地市每日用电变化率表
    ds_rq_ydbhl = pd.DataFrame(columns=('地市', '日期', '用电变化率(%)'))

    # 建立 各地市平均用电变化率表
    ds_pjydbhl = pd.DataFrame(columns=('地市', '平均用电变化率(%)'))

    # 建立 各规模养老院每日用电变化率表
    scale_rq_ydbhl = pd.DataFrame(columns=('规模', '日期', '用电变化率(%)'))

    # 建立 各规模养老院平均用电变化率表
    scale_pjydbhl = pd.DataFrame(columns=('规模', '平均用电变化率(%)'))

    # 计算重庆电变化率
    for i in range(rq_data.shape[0]):
        # 获取日期
        rq = rq_data[i]

        if rq != datetime.date(2020, 2, 29):
            # 获取 去年日期
            datetool = lambda x: datetime.date(x.year - 1, x.month, x.day)
            rq2 = datetool(rq).strftime("%Y-%m-%d %H:%M:%S")
            # print(rq, rq2)

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
                aaa = aaa.append(pd.DataFrame({'日期': [rq], '用电变化率(%)': [ydbhl],'去年':[zydl2],'今年':[zydl1]}), ignore_index=True)
    aaa.to_excel(f'{listdata_addr}湖北.xlsx')
    rq_ydbhl.to_excel(f'{listdata_addr}湖北每日用电变化率表.xlsx')

    # 计算 各地市平均用电变化率
    for i in range(ds_data.shape[0]):
        # 获取地市 第一次筛选
        ds = ds_data[i]

        for j in range(rq_data.shape[0]):
            # 获取 时间 第二次筛选
            rq = rq_data[j]

            if rq != datetime.date(2020, 2, 29):
                # 获取 去年日期
                datetool = lambda x: datetime.date(x.year - 1, x.month, x.day)
                rq2 = datetool(rq).strftime("%Y-%m-%d %H:%M:%S")
                # print(rq, rq2)

                # 获取 此日总用电量1 (2020)
                zydl_data = (ds_rq_zydl[(ds_rq_zydl['日期'] == rq) & (ds_rq_zydl['地市'] == ds)])
                zydl1 = zydl_data['总用电量'].sum()

                # 获取 此日总用电量2 (2019)
                zydl_data2 = (ds_rq_zydl[(ds_rq_zydl['日期'] == rq2) & (ds_rq_zydl['地市'] == ds)])
                zydl2 = zydl_data2['总用电量'].sum()

                if zydl2 != 0:
                    # 计算 该日用电影响率
                    ydbhl = 100 * (zydl1 - zydl2) / zydl2

                    # 将日期转换为 xx月xx日格式
                    month = datetime.datetime.strftime(rq, '%m')
                    day = datetime.datetime.strftime(rq, '%d')
                    rq3 = month + '月' + day + '日'

                    # 数据入表
                    ds_rq_ydbhl = ds_rq_ydbhl.append(pd.DataFrame({'地市': [ds], '日期': [rq3], '用电变化率(%)': [ydbhl]}),
                                                     ignore_index=True)
    # ds_rq_ydbhl.to_excel('各地市每日用电变化率表.xlsx')

    for i in range(ds_data.shape[0]):
        # 获取地市
        ds = ds_data[i]

        # 计算 此地市平均用电影响率
        pjydbhl = (ds_rq_ydbhl[ds_rq_ydbhl['地市'] == ds])['用电变化率(%)'].mean()

        # 数据入表
        ds_pjydbhl = ds_pjydbhl.append(pd.DataFrame({'地市': [ds], '平均用电变化率(%)': [pjydbhl]}),
                                       ignore_index=True)
    ds_pjydbhl.to_excel(f'{listdata_addr}各地市平均用电变化率表.xlsx')

    # 计算 各规模平均用电变化率
    for i in range(scale_data.shape[0]):
        # 获取规模 第一次筛选
        scale = scale_data[i]
        temp6 = data[data['scale'] == scale]

        for j in range(rq_data.shape[0]):
            # 获取时间 第二次筛选
            rq = rq_data[j]

            if rq != datetime.date(2020, 2, 29):
                # 获取 去年日期
                datetool = lambda x: datetime.date(x.year - 1, x.month, x.day)
                rq2 = datetool(rq).strftime("%Y-%m-%d %H:%M:%S")

                # 获取 此日总用电量(2020)
                zydl_data = (scale_rq_zydl[(scale_rq_zydl['日期'] == rq) & (scale_rq_zydl['规模'] == scale)])
                zydl1 = zydl_data['总用电量'].sum()

                # # 获取 此日总用电量(2019)
                zydl_data = (scale_rq_zydl[(scale_rq_zydl['日期'] == rq2) & (scale_rq_zydl['规模'] == scale)])
                zydl2 = zydl_data['总用电量'].sum()
                # print(scale, rq, zydl1,zydl2)

                # 计算 该规模该日养老机构该日用变化率
                if zydl2 != 0:
                    # 计算 该日用电影响率
                    ydbhl = 100 * (zydl1 - zydl2) / zydl2

                    # 将日期转换为 xx月xx日格式
                    month = datetime.datetime.strftime(rq, '%m')
                    day = datetime.datetime.strftime(rq, '%d')
                    rq3 = month + '月' + day + '日'

                    # 数据入表
                    scale_rq_ydbhl = scale_rq_ydbhl.append(
                        pd.DataFrame({'规模': [scale], '日期': [rq3], '用电变化率(%)': [ydbhl]}),
                        ignore_index=True)
    # scale_rq_ydbhl.to_excel('各规模每日用电变化率表.xlsx')

    for i in range(scale_data.shape[0]):
        # 获取规模
        scale = scale_data[i]

        # 计算此规模平均用电变化率
        pjydbhl = (scale_rq_ydbhl[scale_rq_ydbhl['规模'] == scale])['用电变化率(%)'].mean()

        # 数据入表
        scale_pjydbhl = scale_pjydbhl.append(pd.DataFrame({'规模': [scale], '平均用电变化率(%)': [pjydbhl]}),
                                             ignore_index=True)
    scale_pjydbhl.to_excel(f'{listdata_addr}各规模平均用电变化率表.xlsx')
