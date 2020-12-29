
import pandas as pd

ysdata_addr='../resource/data/ys/'
listdata_addr='../resource/data/list/'


def convert_data1(fileName):
    ysh1 = pd.read_excel(f'{ysdata_addr}mxys_dlkms_rdl_hubei.xlsx')
    ysh1.rename(columns=lambda x: x.lower(), inplace=True)
    ysh1 = ysh1[['ylyid', 'org_name', 'ssds']]
    ysh = ysh1.drop_duplicates(['ylyid'])
    print(len(ysh))
    ysh.rename(columns={'ylyid': '养老院id', 'ssds': '地市', 'org_name': '养老院名称'}, inplace=True)
    data = pd.read_excel(f'{listdata_addr}{fileName}.xlsx')
    print(len(data))
    resault = pd.merge(data, ysh, left_on=['养老院id'], how="inner",
                       right_on=['养老院id'])
    print(len(resault))
    resault.to_excel(f'{listdata_addr}{fileName}1.xlsx')






if __name__ == '__main__':
    # convert_data1('湖北_各养老院床均用电变化率表')
    # convert_data1('各养老院平均用电变化率表')
    convert_data1('各养老院整体用电能力指数变化表')







