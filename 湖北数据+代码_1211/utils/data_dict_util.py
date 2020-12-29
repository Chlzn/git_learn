



class DataDictUtil:
    # 获得占比
    def get_proportion(self,data, prop):
        data['prop'] = round(data[prop] * 100 / data[prop].sum(), 2)
        return data['prop']

    # 获得电压等级
    def get_volt_name(volt_code):
        if volt_code in ['交流10kV', '交流20kV', '交流6kV']:
            volt_name = "10(20)kV"
        elif volt_code in ['交流35kV']:
            volt_name = "35kV"
        elif volt_code in ['交流750kV', '交流500kV', '交流350kV', '交流220kV', '交流110kV', '交流66kV']:
            volt_name = "110(66)kV及以上"
        else:
            volt_name = "1kV及以下"
        return volt_name

    # 获得合同容量区间
    def get_contract_cap(self,contract_cap):
        if contract_cap > 50000:
            contract_name = '>5万'
        elif 50000 >= contract_cap > 10000:
            contract_name = '1万-5万'
        elif 10000 >= contract_cap > 5000:
            contract_name = '5千-1万'
        elif 5000 >= contract_cap > 2000:
            contract_name = '2千-5千'
        elif 2000 >= contract_cap > 1000:
            contract_name = '1千-2千'
        elif 1000 >= contract_cap > 500:
            contract_name = '5百-1千'
        elif 500 >= contract_cap > 200:
            contract_name = '2百-5百'
        else:
            contract_name = '0-2百'
        return contract_name

    # 接电时长时间区间
    def get_dur_range(self,duration):
        if duration > 500:
            duration_range = '>500'
        elif 500 >= duration > 260:
            duration_range = '260-500'
        elif 260 >= duration > 150:
            duration_range = '150-260'
        elif 150 >= duration > 80:
            duration_range = '80-150'
        elif 80 >= duration > 30:
            duration_range = '30-80'
        elif 30 >= duration > 1:
            duration_range = '1-30'
        else:
            duration_range = '<1'
        return duration_range

    def pct_group(self,pct):
        if 100 >= pct > 80:
            pct_range = '80-100%'
        elif 80 >= pct > 60:
            pct_range = '60-80%'
        elif 60 >= pct > 40:
            pct_range = '40-60%'
        elif 40 >= pct > 30:
            pct_range = '30-40%'
        elif 30 >= pct > 20:
            pct_range = '20-30%'
        else:
            pct_range = '10-20%'
        return pct_range

    def is_dg(self,city):
        dg_list = ['沈阳', '石家庄', '苏州', '太原', '唐山',
                   '通州', '乌鲁木齐', '武汉', '西安', '西宁',
                   '厦门', '银川', '郑州', '青岛', '浦东',
                   '宁波', '南京', '南昌', '兰州', '拉萨',
                   '济南', '合肥', '杭州', '哈尔滨', '福州',
                   '大连', '城区', '成都', '长沙', '长春',
                   '滨海']
        if city in dg_list:
            is_dg = True
        else:
            is_dg = False
        return is_dg

    # 设置12大行业类别
    # 工业，建筑业，交通运输、仓储和邮政业，信息传输、软件和信息技术服务业，
    # 住宿和餐饮业，金融业，房地产业，公共服务及管理组织，城乡居民生活
    # ，农、林、牧、渔业，租赁和商务服务业，批发和零售业
    def set_trade(self,data, div):
        data_tem = data
        # print(data[div])
        j = len(data[div])
        for x in data[div]:
            if '城乡居民' in x:
                data_tem.iloc[len(data[div]) - j, 0] = '城乡居民生活用电'
            elif '工业' in x:
                data_tem.iloc[len(data[div]) - j, 0] = '工业'
            elif '建筑业' in x:
                data_tem.iloc[len(data[div]) - j, 0] = '建筑业'
            elif '交通运输' in x:
                data_tem.iloc[len(data[div]) - j, 0] = '交通运输、仓储和邮政业'
            elif '信息传输' in x:
                data_tem.iloc[len(data[div]) - j, 0] = '信息传输、软件和信息技术服务业'
            elif '住宿' in x:
                data_tem.iloc[len(data[div]) - j, 0] = '住宿和餐饮业'
            elif '金融' in x:
                data_tem.iloc[len(data[div]) - j, 0] = '金融业'
            elif '房地产' in x:
                data_tem.iloc[len(data[div]) - j, 0] = '房地产业'
            elif '公共' in x:
                data_tem.iloc[len(data[div]) - j, 0] = '公共服务及管理组织'
            elif '农' in x:
                data_tem.iloc[len(data[div]) - j, 0] = '农、林、牧、渔业'
            elif '租赁' in x:
                data_tem.iloc[len(data[div]) - j, 0] = '租赁和商务服务业'
            elif '批发' in x:
                data_tem.iloc[len(data[div]) - j, 0] = '批发和零售业'
            elif '趸售' in x:
                data_tem.iloc[len(data[div]) - j, 0] = '趸售'
            else:
                data_tem.iloc[len(data[div]) - j, 0] = '其他'
            j = j - 1
        # print(f'set_trade\n{data_tem}')
        return data_tem

    # 设置用电类别
    # 大工业用电 # 一般工商业及其他用电 #   1、非、普工业用电#   2、非居民照明用电#   3、商业用电
    # 农业用电# 居民用电# 趸售用电# 打水用电# 其他用电
    def set_eleType(self,data, div):
        # print(data[div])
        data_tem = data
        j = len(data[div])
        for x in data[div]:
            if '居民生活' == x:
                data_tem.iloc[len(data[div]) - j, 0] = '居民用电'
            elif '居民生活' in x:
                data_tem.iloc[len(data[div]) - j, 0] = '居民用电'
            elif '大工业' in x:
                data_tem.iloc[len(data[div]) - j, 0] = '大工业用电'
            elif '商业' in x:
                data_tem.iloc[len(data[div]) - j, 0] = '一般工商业及其他用电'
            elif '非居民' in x:
                data_tem.iloc[len(data[div]) - j, 0] = '一般工商业及其他用电'
            elif '普通工业' in x:
                data_tem.iloc[len(data[div]) - j, 0] = '一般工商业及其他用电'
            elif '非工业' in x:
                data_tem.iloc[len(data[div]) - j, 0] = '一般工商业及其他用电'
            elif '生活' in x:
                data_tem.iloc[len(data[div]) - j, 0] = '一般工商业及其他用电'
            elif '农业' in x:
                data_tem.iloc[len(data[div]) - j, 0] = '农业用电'
            elif '打水' in x:
                data_tem.iloc[len(data[div]) - j, 0] = '打水用电'
            elif '趸售' in x:
                data_tem.iloc[len(data[div]) - j, 0] = '趸售用电'
            else:
                data_tem.iloc[len(data[div]) - j, 0] = '其他用电'
            j = j - 1
        # print(f'set_eleType\n{data_tem}')
        return data_tem

    # 获得电费类主题合同容量
    def get_contract_name(self,contract_cap):
        if contract_cap < 100:
            contract_name = "<100"
        elif 100 <= contract_cap < 315:
            contract_name = "100-315"
        elif 315 <= contract_cap < 1000:
            contract_name = "315-1000"
        elif 1000 <= contract_cap < 5000:
            contract_name = "1000-5000"
        elif 5000 <= contract_cap < 10000:
            contract_name = "5000-10000"
        else:
            contract_name = ">=10000"
        return contract_name

    # 转换用电类别
    def convert_elecType(self,data):
        value = data
        if '居民生活' == data:
            value = '居民用电'
        elif '大工业' == data:
            value = '大工业用电'
        elif '商业' == data:
            value = '一般工商业及其他用电'
        elif '非居民' == data:
            value = '一般工商业及其他用电'
        elif '普通工业' == data:
            value = '一般工商业及其他用电'
        elif '非工业' == data:
            value = '一般工商业及其他用电'
        elif '生活' == data:
            value = '一般工商业及其他用电'
        elif '农业' == data:
            value = '农业用电'
        elif '打水' == data:
            value = '打水用电'
        elif '趸售' == data:
            value = '趸售用电'
        else:
            value = '其他用电'
        return value

    # 固定资产报废：计算“输电线路”和“配电线路及设备”的资产净值 (资产净值=资产净值*报废比例)
    def get_NET_ASSET_VALUE(self,val1, val2, val3):
        '''
        :param val1: 资产大类名称
        :param val2: 资产净值
        :param val3: 报废比例
        :return:
        '''
        if val1 == '输电线路' or val1 == '配电线路及设备':
            val2 = val2 * val3
        return val2
