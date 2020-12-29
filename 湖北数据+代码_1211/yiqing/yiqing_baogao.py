import os
from docxtpl import DocxTemplate, InlineImage
import math
import pandas as pd
import datetime
import arrow
from pandas import DataFrame

import warnings

# 忽略警告
warnings.filterwarnings("ignore")


ysdata_addr='../resource/data/ys/'
listdata_addr='../resource/data/list/'
doc_addr='../resource/doc/'
pic_addr='../resource/pic/'

def bg(city):
    ysh1 = pd.read_excel(f'{ysdata_addr}mxys_dlkms_rdl_hubei.xlsx')
    ysh1.rename(columns=lambda x: x.lower(), inplace=True)
    ysh1 = ysh1[['ylyid', 'org_name', 'ssds']]
    ysh = ysh1.drop_duplicates(['ylyid'])
    ysh.rename(columns={'ylyid': '养老院id'}, inplace=True)

    year_month = str(datetime.datetime.now())
    year_month = year_month[0:4] + "年" + year_month[5:7] + "月"

    ######################### 1、用电变化率分析  ##############################################################
    # 图18 养老机构用电变化率
    draw18_mrydbhl = pd.read_excel(f'{listdata_addr}湖北每日用电变化率表.xlsx')
    draw18_mrydbhl_mean = draw18_mrydbhl['用电变化率(%)'].mean()
    draw18_mrydbhl_mean = round(draw18_mrydbhl_mean)
    draw18_mrydbhl_mean = math.trunc(draw18_mrydbhl_mean)

    # 各规模养老机构用电变化率
    draw_gmpjydbhl = pd.read_excel(f'{listdata_addr}各规模平均用电变化率表.xlsx')
    draw_gmpjydbhl['平均用电变化率(%)'] = round(draw_gmpjydbhl['平均用电变化率(%)'])
    draw_gmpjydbhl['平均用电变化率(%)'] = draw_gmpjydbhl['平均用电变化率(%)'].map(lambda x: math.trunc(x))
    draw_gmpjydbhl = draw_gmpjydbhl.sort_values(by='规模', axis=0, ascending=False)
    draw_gmpjydbhl.reset_index(level=0, inplace=True)
    draw_gmpjydbhl = draw_gmpjydbhl[['规模', '平均用电变化率(%)']]
    print(draw_gmpjydbhl)

    # 图19 各区县养老机构用电变化率排名
    draw19_qxpjydbhl = pd.read_excel(f'{listdata_addr}各地市平均用电变化率表.xlsx')
    draw19_qxpjydbhl = draw19_qxpjydbhl.sort_values(by='平均用电变化率(%)', axis=0, ascending=False)
    draw19_qxpjydbhl = draw19_qxpjydbhl[draw19_qxpjydbhl['平均用电变化率(%)'] > 0]
    draw19_qxpjydbhl_city_list = draw19_qxpjydbhl['地市'].tolist()
    length = 1 if len(draw19_qxpjydbhl_city_list) == 1 else 2
    draw19_qxpjydbhl_city_str = '、'.join(draw19_qxpjydbhl_city_list[0:length])

    ######################### 2、用电能力指数分析  ##############################################################
    # 图20 养老机构用电能力指数变化趋势
    draw20_yljgmrydnlzs = pd.read_excel(f'{listdata_addr}湖北每日用电能力指数表.xlsx')
    draw20_ydnlzs_mean = draw20_yljgmrydnlzs['用电能力指数'].mean()
    draw20_ydnlzs_mean = round(draw20_ydnlzs_mean, 2)
    draw20_yljgmrydnlzs = draw20_yljgmrydnlzs.sort_values(by='用电能力指数', axis=0, ascending=True)
    draw20_yljgmrydnlzs.reset_index(level=0, inplace=True)
    month = datetime.datetime.strftime(draw20_yljgmrydnlzs.loc[0]['日期'], '%m')
    day = datetime.datetime.strftime(draw20_yljgmrydnlzs.loc[0]['日期'], '%d')
    ele_index_min_day = month + '月' + day + '日'

    # 各规模养老机构平均用电能力指数
    scale_pjydnlzs = pd.read_excel(f'{listdata_addr}各规模平均用电能力指数表.xlsx')
    scale_pjydnlzs['平均用电能力指数'] = round(scale_pjydnlzs['平均用电能力指数'], 2)
    scale_pjydnlzs = scale_pjydnlzs.sort_values(by='规模', axis=0, ascending=False)
    scale_pjydnlzs.reset_index(level=0, inplace=True)
    scale_pjydnlzs = scale_pjydnlzs[['规模', '平均用电能力指数']]

    # 图21 各区县用电能力指数排名
    draw21_qxydnlzs = pd.read_excel(f'{listdata_addr}各地市平均用电能力指数表.xlsx')
    draw21_qxydnlzs_mean = draw21_qxydnlzs['平均用电能力指数'].mean()
    draw21_qxydnlzs_mean = round(draw21_qxydnlzs_mean, 2)
    draw21_gao_mean = draw21_qxydnlzs[draw21_qxydnlzs['平均用电能力指数'] > draw21_qxydnlzs_mean]
    draw21_gao_mean = draw21_gao_mean.sort_values(by='平均用电能力指数', axis=0, ascending=False)
    draw21_gao_mean.reset_index(level=0, inplace=True)
    draw21_di_mean = draw21_qxydnlzs[draw21_qxydnlzs['平均用电能力指数'] < draw21_qxydnlzs_mean]
    draw21_di_mean = draw21_di_mean.sort_values(by='平均用电能力指数', axis=0, ascending=True)
    draw21_di_mean.reset_index(level=0, inplace=True)

    ######################### 3、疫情整体变化分析  ##############################################################
    # 图22 床均用电量变化较大养老机构区县分布
    ds_cjydbhl = pd.read_excel(f'{listdata_addr}湖北_各养老院床均用电变化率1.xlsx')
    ds_cjydbhl = ds_cjydbhl[ds_cjydbhl['床均用电变化率'] <= -90]
    cjydbhl_jd = ds_cjydbhl[['地市', '养老院名称']]
    cjydbhl_jd = cjydbhl_jd.groupby('地市').count()
    cjydbhl_jd = DataFrame(cjydbhl_jd)
    cjydbhl_jd = cjydbhl_jd.sort_values(by='养老院名称', axis=0, ascending=False)
    cjydbhl_jd.reset_index(inplace=True)

    # 图23 各区县用电量降幅较大养老机构分布
    ds_pjydbhl = pd.read_excel(f'{listdata_addr}各养老院平均用电变化率表1.xlsx')
    ds_pjydbhl = ds_pjydbhl[ds_pjydbhl['平均用电变化率(%)'] <= -90]
    pjydbhl_jd = ds_pjydbhl[['地市', '养老院名称']]
    pjydbhl_jd = pjydbhl_jd.groupby('地市').count()
    pjydbhl_jd = DataFrame(pjydbhl_jd)
    pjydbhl_jd = pjydbhl_jd.sort_values(by='养老院名称', axis=0, ascending=False)
    pjydbhl_jd.reset_index(inplace=True)



    # 图24 各养老机构规模用电能力指数变化情况
    draw24_gmydnlzsbhqk = pd.read_excel(f'{listdata_addr}各规模整体用电能力指数变化表.xlsx')
    draw24_gmydnlzsbhqk['整体变化率'] = round(draw24_gmydnlzsbhqk['整体变化率'])
    draw24_gmydnlzsbhqk['整体变化率'] = draw24_gmydnlzsbhqk['整体变化率'].map(lambda x: math.trunc(x))
    draw24_gmydnlzsbhqk = draw24_gmydnlzsbhqk.sort_values(by='规模', axis=0, ascending=False)
    draw24_gmydnlzsbhqk.reset_index(level=0, inplace=True)
    draw24_gmydnlzsbhqk = draw24_gmydnlzsbhqk[['规模', '整体变化率']]
    draw24_ztbhl_mean = draw24_gmydnlzsbhqk['整体变化率'].mean()
    draw24_ztbhl_mean = round(draw24_ztbhl_mean)
    draw24_ztbhl_mean = math.trunc(draw24_ztbhl_mean)

    # 图25 各区县养老机构用电能力指数变化情况
    draw25_qxydnlzsbhqk = pd.read_excel(f'{listdata_addr}各地市整体用电能力指数变化表.xlsx')
    draw25_qxydnlzsbhqk['整体变化率'] = round(draw25_qxydnlzsbhqk['整体变化率'])
    draw25_qxydnlzsbhqk['整体变化率'] = draw25_qxydnlzsbhqk['整体变化率'].map(lambda x: math.trunc(x))
    draw25_qxydnlzsbhqk['绝对值'] = abs(draw25_qxydnlzsbhqk['整体变化率'])
    draw25_qxydnlzsbhqk = draw25_qxydnlzsbhqk.sort_values(by='绝对值', axis=0, ascending=False)
    draw25_qxydnlzsbhqk.reset_index(level=0, inplace=True)
    flag = True if draw25_qxydnlzsbhqk.loc[0]['整体变化率'] < 0 else False
    fudu = '升幅' if flag == False else '降幅'
    draw25_qxydnlzsbhqk_new = draw25_qxydnlzsbhqk
    draw25_qxydnlzsbhqk_new = draw25_qxydnlzsbhqk_new.sort_values(by='整体变化率', axis=0, ascending=flag)
    draw25_qxydnlzsbhqk_new.reset_index(level=0, inplace=True)
    draw25_ztbhl_mean = draw25_qxydnlzsbhqk_new['整体变化率'].mean()
    draw25_gao_mean = draw25_qxydnlzsbhqk[draw25_qxydnlzsbhqk['整体变化率'] > draw25_ztbhl_mean]
    draw25_gao_mean = draw25_gao_mean.sort_values(by='整体变化率', axis=0, ascending=False)
    draw25_gao_mean.reset_index(level=0, inplace=True)
    draw25_di_mean = draw25_qxydnlzsbhqk[draw25_qxydnlzsbhqk['整体变化率'] < draw25_ztbhl_mean]

    # 用电能力指数变化率超过90%的情况
    ds_ydnlzs_jd = pd.read_excel(f'{listdata_addr}各养老院整体用电能力指数变化表1.xlsx')
    ds_ydnlzs_jd = ds_ydnlzs_jd[ds_ydnlzs_jd['整体变化率'] <= -90]
    ydnlzs_jd = ds_ydnlzs_jd[['地市', '养老院名称']]
    ydnlzs_jd = ydnlzs_jd.groupby('地市').count()
    ydnlzs_jd = DataFrame(ydnlzs_jd)
    ydnlzs_jd = ydnlzs_jd.sort_values(by='养老院名称', axis=0, ascending=False)
    ydnlzs_jd.reset_index(inplace=True)
    ydnlzs_jd['养老院名称1'] = ydnlzs_jd['养老院名称'].apply(str)
    ydnlzs_jd['各区县养老院数量'] = ydnlzs_jd['地市'] + ydnlzs_jd['养老院名称1'] + "家"
    ydnlzs_jd_city_list = ydnlzs_jd['各区县养老院数量'].tolist()
    ydnlzs_jd_city_str = '、'.join(ydnlzs_jd_city_list)



    # 调用模板
    doc = DocxTemplate(f"{doc_addr}base_hb2.docx")
    # 传入所有参数
    context = {'city': city,
               'year_month': year_month,

               ######################### 1、用电变化率分析  ##############################################################
               # 图18 养老机构用电变化率
               "ydbhl_mean": draw18_mrydbhl_mean,

               # 各规模养老机构用电变化率
               "ele_effect_1": draw_gmpjydbhl.loc[draw_gmpjydbhl['规模'] == '大型', '平均用电变化率(%)'].at[1],
               "ele_effect_2": draw_gmpjydbhl.loc[draw_gmpjydbhl['规模'] == '中型', '平均用电变化率(%)'].at[2],
               "ele_effect_3": draw_gmpjydbhl.loc[draw_gmpjydbhl['规模'] == '小型', '平均用电变化率(%)'].at[0],

               # 图21 各区县用电能力指数排名
               "ydbhl_city_zhengshu": draw19_qxpjydbhl_city_str,
               "ydbhl_city_zhengshu_num": len(draw19_qxpjydbhl_city_list),

               ######################### 2、用电能力指数分析  ##############################################################
               # 图20 养老机构用电能力指数变化趋势
               "ydnlzs_mean": draw20_ydnlzs_mean,
               "ele_index_min_day": ele_index_min_day,

               # 各规模养老机构平均用电能力指数
               "ele_index_mean_scale_1": scale_pjydnlzs.loc[scale_pjydnlzs['规模'] == '大型', '平均用电能力指数'].at[1],
               "ele_index_mean_scale_2": scale_pjydnlzs.loc[scale_pjydnlzs['规模'] == '中型', '平均用电能力指数'].at[2],
               "ele_index_mean_scale_3": scale_pjydnlzs.loc[scale_pjydnlzs['规模'] == '小型', '平均用电能力指数'].at[0],

               # 图21 各区县用电能力指数排名
               "ele_index_city_mean": draw21_qxydnlzs_mean,
               "ele_index_city_gao_1": draw21_gao_mean.loc[0]['地市'],
               "ele_index_city_gao_2": draw21_gao_mean.loc[1]['地市'],
               "ele_index_city_gaonum": len(draw21_gao_mean),
               "ele_index_city_di_1": draw21_di_mean.loc[0]['地市'],
               "ele_index_city_di_2": draw21_di_mean.loc[1]['地市'],
               "ele_index_city_dinum": len(draw21_di_mean),

               ######################### 3、疫情整体变化分析  ##############################################################
               # 图22 床均用电量变化较大养老机构区县分布
               "cjydlbh_jd_yljg_num":cjydbhl_jd['养老院名称'].sum(),
               "cjydlbh_jd_city":f"{cjydbhl_jd.loc[0]['地市']}、{cjydbhl_jd.loc[1]['地市']}、{cjydbhl_jd.loc[2]['地市']}",
               "cjydlbh_jd_city_num": len(cjydbhl_jd),

               # 图23 各区县用电量降幅较大养老机构分布
               "ydbhl_jd_yljg_num":pjydbhl_jd['养老院名称'].sum(),
               "ydbhl_jd_city": f"{pjydbhl_jd.loc[0]['地市']}、{pjydbhl_jd.loc[1]['地市']}、{pjydbhl_jd.loc[2]['地市']}",
               "ydbhl_jd_city_num": len(pjydbhl_jd),

               # 图24 各养老机构规模用电能力指数变化情况
               "ztbhl_scale_da": draw24_gmydnlzsbhqk.loc[draw24_gmydnlzsbhqk['规模'] == '大型', '整体变化率'].at[1],
               "ztbhl_scale_zhong": draw24_gmydnlzsbhqk.loc[draw24_gmydnlzsbhqk['规模'] == '中型', '整体变化率'].at[2],
               "ztbhl_scale_xiao": draw24_gmydnlzsbhqk.loc[draw24_gmydnlzsbhqk['规模'] == '小型', '整体变化率'].at[0],
               "ztbhl_scale_mean": draw24_ztbhl_mean,

               # 图25 各区县养老机构用电能力指数变化情况
               "ele_index_ztbh_city_gao1": draw25_gao_mean.loc[0]['地市'],
               "ele_index_ztbh_city_gao2": draw25_gao_mean.loc[1]['地市'],
               "ele_index_ztbh_city_gaonum": len(draw25_gao_mean),
               "ele_index_ztbh_city_dinum": len(draw25_di_mean),
               "ele_index_ztbh_city_1": draw25_qxydnlzsbhqk_new.loc[0]['地市'],
               "ele_index_ztbh_city_2": draw25_qxydnlzsbhqk_new.loc[1]['地市'],
               "ele_index_ztbh_city_lv1": draw25_qxydnlzsbhqk_new.loc[0]['绝对值'],
               "ele_index_ztbh_city_lv2": draw25_qxydnlzsbhqk_new.loc[1]['绝对值'],
               "fudu":fudu,

               # 用电能力指数变化率超过90%的情况
               "ydnlzs_jd_yljg_num": ydnlzs_jd['养老院名称'].sum(),
               "ydnlzs_jd_city": ydnlzs_jd_city_str,




               # 图片填充
               "img18_yljgydbhl": InlineImage(doc, f"{pic_addr}图18 养老机构用电变化率.png"),
               "img19_qxydbhl": InlineImage(doc, f"{pic_addr}图19 各区县养老机构用电变化率排名.png"),
               "img20_yljgydnlzs": InlineImage(doc, f"{pic_addr}图20 养老机构用电能力指数变化趋势.png"),
               "img21_qxydnlzs": InlineImage(doc, f"{pic_addr}图21 各区县用电能力指数排名.png"),
               "img22_cjydlbh_jd":InlineImage(doc, f"{pic_addr}图22 床均用电量变化较大养老机构区县分布.png"),
               "img23_ydbhl_jd": InlineImage(doc, f"{pic_addr}图23 各区县用电量降幅较大养老机构分布.png"),
               "img24_gmydnlzs": InlineImage(doc, f"{pic_addr}图24 各养老机构规模用电能力指数变化情况.png"),
               "img25_qxydnlzsbhqk": InlineImage(doc, f"{pic_addr}图25 各区县养老机构用电能力指数变化情况.png"),

               }
    # 渲染模板
    doc.render(context)
    # 保存文档
    try:
        doc.save(f"{doc_addr}疫情期间组织机构用电能力分析_{city}.docx")
    except:
        os.remove(f"{doc_addr}疫情期间组织机构用电能力分析_{city}.docx")
        doc.save(f"{doc_addr}疫情期间组织机构用电能力分析_{city}.docx")

    doc.save(f"{doc_addr}疫情期间组织机构用电能力分析_{city}.docx")


if __name__ == '__main__':
    bg(city="湖北")

