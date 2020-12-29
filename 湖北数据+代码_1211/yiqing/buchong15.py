# -*- coding: utf-8 -*-
"""
@Author  : 343
@Project: bak1129_重庆
@Date  : 2020-11-30 18:03:24
@Desc : 各养老院  床均用电量变化率
"""
import pandas as pd
import datetime

ysdata_addr='../resource/data/ys/'
listdata_addr='../resource/data/list/'

if __name__ == '__main__':
    # 读取 源表
    # 需求字段为
    # 养老院id(ylyid)  数据日期(data_date)
    # 当日用电量(xqdl)  床位数(bed_num)
    data = pd.read_excel(f'{ysdata_addr}mxys_dlkms_rdl_hubei.xlsx')
    # print(data)
    data = data[['ylyid', 'data_date', 'xqdl', 'bed_num']]
    data['data_date'] = pd.to_datetime(data['data_date'])
    data = data[(data['data_date'] >= '2020-01-01 00:00:00')]

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

    # 建立 各养老院疫情前_后每日用电床均用电量表
    ylyid_rq_cjydl = pd.DataFrame(columns=('养老院id', '日期', '床均用电量'))
    #
    # 建立 各养老院疫情前_后床均用电量变化率表
    ylyid_cjydbhl = pd.DataFrame(columns=('养老院id', '床均用电变化率'))

    for i in range(yly_data.shape[0]):
        # 获取 养老院id
        yly = yly_data[i]

        for j in range(yyq_data.shape[0]):
            # 获取 日期
            rq = yyq_data[j]

            # 获取 该养老院该日数据
            temp1 = data[(data['ylyid'] == yly) & (data['data_date'] == rq)]
            if temp1.empty == False:
                # 获取 床位数 用电量
                bednum = temp1['bed_num'].sum()
                xqdl = temp1['xqdl'].sum()

                if bednum != 0:
                    cjydl = xqdl / bednum

                    # 将日期转换为 xx月xx日格式
                    month = datetime.datetime.strftime(rq, '%m')
                    day = datetime.datetime.strftime(rq, '%d')
                    rq3 = month + '月' + day + '日'

                    # 数据入表
                    ylyid_rq_cjydl = ylyid_rq_cjydl.append(
                        pd.DataFrame({'养老院id': [yly], '日期': [rq3], '床均用电量': [cjydl]}),
                        ignore_index=True)

        for j in range(yyh_data.shape[0]):
            # 获取 日期
            rq = yyh_data[j]

            # 获取 该养老院该日数据
            temp1 = data[(data['ylyid'] == yly) & (data['data_date'] == rq)]
            if temp1.empty == False:
                # 获取 床位数 用电量
                bednum = temp1['bed_num'].sum()
                xqdl = temp1['xqdl'].sum()

                if bednum != 0:
                    cjydl = xqdl / bednum

                    # 将日期转换为 xx月xx日格式
                    month = datetime.datetime.strftime(rq, '%m')
                    day = datetime.datetime.strftime(rq, '%d')
                    rq3 = month + '月' + day + '日'

                    # 数据入表
                    ylyid_rq_cjydl = ylyid_rq_cjydl.append(
                        pd.DataFrame({'养老院id': [yly], '日期': [rq3], '床均用电量': [cjydl]}),
                        ignore_index=True)
    # ylyid_rq_cjydl.to_excel('2.xlsx')

    # 计算 各养老院 疫情前_后床均用电量变化率
    for i in range(yly_data.shape[0]):
        # 获取养老院
        yly = yly_data[i]

        # 获取该养老院 疫情前的床均用电量
        cjydl1_data = ylyid_rq_cjydl[
            (ylyid_rq_cjydl['养老院id'] == yly) & (ylyid_rq_cjydl['日期'] >= '01月01日') & (ylyid_rq_cjydl['日期'] <= '01月22日')]

        # 获取该养老院 疫情后的床均用电量
        cjydl2_data = ylyid_rq_cjydl[(ylyid_rq_cjydl['养老院id'] == yly) & (ylyid_rq_cjydl['日期'] >= '04月08日') & (
                ylyid_rq_cjydl['日期'] <= '04月27日')]

        if (cjydl1_data.empty == False) & (cjydl2_data.empty == False):
            yyqcjydl = cjydl1_data['床均用电量'].mean()
            yyhcjydl = cjydl2_data['床均用电量'].mean()

            if yyqcjydl != 0:
                cjydbhl = 100 * (yyhcjydl - yyqcjydl) / yyqcjydl

                # 数据入表
                ylyid_cjydbhl = ylyid_cjydbhl.append(pd.DataFrame({'养老院id': [yly], '床均用电变化率': [cjydbhl]}),
                        ignore_index=True)
    ylyid_cjydbhl.to_excel(f'{listdata_addr}湖北_各养老院床均用电变化率表.xlsx')
