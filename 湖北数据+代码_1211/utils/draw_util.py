import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# from matplotlib.ticker import FuncFormatter
# 使用这个绘图时抛出'str' object is not callable
# https://stackoverflow.com/questions/24120023/strange-error-with-matplotlib-axes-labels
import matplotlib.ticker as mtick

class DrawUtil:
    # 画一条线的折线图
    def draw_one_line_chart(self,data, col_1, col_2, ylabel, title):
        """
        :param data: 二维数组
        :param col_1: x轴字段
        :param col_2: y轴字段
        :param ylabel: y轴标签
        :param title: 大标题
        :return: 返回一个图片 figure
        """
        figure = plt.figure(dpi=300)
        ax = plt.subplot()
        plt.plot(data[col_1], data[col_2], color='#002060')
        data["mean"] = data[col_2].mean()
        # 平均线 虚线
        plt.plot(data[col_1], data["mean"], color="#9D9D9D", linestyle="--")
        mean = int(data["mean"][0])
        plt.text(len(data) - 1, data["mean"][0] * 1.05, mean)
        # 取消边框
        ax.spines["top"].set_visible(False)
        ax.spines['right'].set_visible(False)
        # 设置Y轴 标签
        ax.set_ylabel(ylabel)

        # 设置X轴 ticks 文字竖着显示
        xticklabels = list(data[col_1])
        new_xticklabels = []
        for i in xticklabels:
            new_xticklabels.append("\n".join(i))
        ax.set_xticklabels(labels=new_xticklabels)
        # 设置标题
        plt.title(title)
        # 自动调整布局
        plt.tight_layout()
        return figure

    # 画二条线的折线图
    def draw_two_line_chart(self,data, col_1, col_2, col_3, label1, label2, ylabel, title):
        """
        :param data: 二维数组
        :param col_1: x轴字段
        :param col_2: 第一条线y轴字段
        :param col_3: 第二条线y轴字段
        :param label1: 第一条线标签
        :param label2: 第二条线标签
        :param ylabel: y轴标签
        :param title: 大标题
        :return: 返回一个图片 figure
        """
        figure = plt.figure(dpi=300)
        ax = plt.subplot()
        # 第一条线
        plt.plot(data[col_1], data[col_2], color='#002060', label=label1)
        # 第二条线
        plt.plot(data[col_1], data[col_3], color='#FFBB00', label=label2)
        # 取消边框
        ax.spines["top"].set_visible(False)
        ax.spines['right'].set_visible(False)
        # 设置Y轴 标签
        ax.set_ylabel(ylabel)

        # 设置X轴 ticks 文字竖着显示
        xticklabels = list(data[col_1])
        new_xticklabels = []
        for i in xticklabels:
            new_xticklabels.append("\n".join(i))
        ax.set_xticklabels(labels=new_xticklabels)
        # 开启图例
        leg = ax.legend(ncol=2)
        # 取消图例边框
        leg.get_frame().set_linewidth(0.0)
        # 设置标题
        plt.title(title)
        # 自动调整布局
        plt.tight_layout()
        return figure

    # 画三条线的折线图

    # 画三条线的折线图
    def draw_three_line_chart(self,data, col_1, col_2, col_3, col_4, label1, label2, label3, ylabel, title):
        """
        :param data: 二维数组
        :param col_1: x轴字段
        :param col_2: 第一条线y轴字段
        :param col_3: 第二条线y轴字段
        :param col_4: 第三条线y轴字段
        :param label1: 第一条线标签
        :param label2: 第二条线标签
        :param label3: 第三条线标签
        :param ylabel: y轴标签
        :param title: 大标题
        :return: 返回一个图片 figure

        """
        figure = plt.figure(dpi=300)
        ax = plt.subplot()
        # 第一条线
        plt.plot(data[col_1], data[col_2], color='#002060', label=label1)
        # 第二条线
        plt.plot(data[col_1], data[col_3], color='#FFBB00', label=label2)
        # 第三条线
        plt.plot(data[col_1], data[col_4], color='#A1A1A1', label=label3)
        # 取消边框
        ax.spines["top"].set_visible(False)
        ax.spines['right'].set_visible(False)
        # 设置Y轴 标签
        ax.set_ylabel(ylabel)

        # 设置X轴 ticks 文字竖着显示
        xticklabels = list(data[col_1])
        new_xticklabels = []
        for i in xticklabels:
            new_xticklabels.append("\n".join(i))
        ax.set_xticklabels(labels=new_xticklabels)
        # 开启图例
        leg = ax.legend(loc=(0.2, 0.9), ncol=3)
        # 取消图例边框
        leg.get_frame().set_linewidth(0.0)
        # 设置标题
        plt.title(title)
        # 自动调整布局
        plt.tight_layout()
        return figure

    # 双轴图（不带百分比）
    def draw_two_axis_chart_with_barandline(self,data, col_1, col_2, col_3, label1, label2, title):
        figure = plt.figure(dpi=300)
        ax1 = plt.subplot()
        ax1.bar(data[col_1], data[col_2], 0.5, color="#001055", label=label1)
        ax2 = ax1.twinx()
        ax2.plot(data[col_1], data[col_3], color="#ED7C30", label=label2, linewidth=1.5)
        # 设置X轴 ticks 文字竖着显示
        xticklabels = data[col_1]
        new_xticklabels = []
        for i in xticklabels:
            new_xticklabels.append("\n".join(i))
        ax1.set_xticklabels(labels=new_xticklabels)
        # 取消边框
        ax1.spines["top"].set_visible(False)
        ax2.spines["top"].set_visible(False)
        # 开启图例
        leg1 = ax1.legend(loc=(0.3, 0.9))
        leg2 = ax2.legend(loc=(0.5, 0.9))
        # 取消图例的边框
        leg1.get_frame().set_linewidth(0.0)
        leg2.get_frame().set_linewidth(0.0)
        # 设置标题
        ax1.set_title(title)
        # 自动调整布局
        plt.tight_layout()
        return figure

    #  画两个横向柱状图
    def draw_two_bar(self,data, col_1, col_2, col_3, sub_title_1, sub_title_2, title):
        figure = plt.figure(dpi=300)
        ax1 = plt.subplot(121)
        plt.barh(data[col_1], data[col_2], color="#001055")
        ax1.spines['top'].set_visible(False)
        ax1.spines['bottom'].set_visible(False)
        ax1.spines['left'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax2 = plt.subplot(122)
        plt.barh(data[col_1], data[col_3], color="#9D9D9D")
        ax2.spines['top'].set_visible(False)
        ax2.spines['bottom'].set_visible(False)
        ax2.spines['left'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        # 设置子标题
        ax1.set_title(sub_title_1)
        ax2.set_title(sub_title_2)
        figure.suptitle(title)

    # 画雷达图
    def draw_redar_chart1(self,data, col_1, col_2):
        labels = data[col_1]
        # 数据个数
        dataLenth = len(data)
        # 数据
        data1 = data[col_2]

        angles = np.linspace(0, 2 * np.pi, dataLenth, endpoint=False)  # 分割圆周长
        data1 = np.concatenate((data1, [data1[0]]))  # 闭合
        angles = np.concatenate((angles, [angles[0]]))  # 闭合

        fig = plt.figure(dpi=300)
        ax = plt.subplot(111, polar=True)  # polar参数！！
        ax.plot(angles, data1, 'bo-', linewidth=1, color="#001050")  # 画线，做极坐标系
        ax.fill(angles, data1, facecolor='#9D9D9D', alpha=0.25)  # 填充
        ax.set_thetagrids(angles * 180 / np.pi, labels)  # 做标签
        return fig

    def draw_plots_three(self,data, labels_pic, xy_name):
        """

        :param data:
        :param labels_pic: labels_pic = ['左侧y轴标签', '同期值', '右侧y轴标签']
        :param xy_name: xy_name = ['x轴列名', '折线1列名, '折线2列名'] 如，xy_name = ['org_name_sheng', 'ym_x', 'ym_y']
        :return:fig,ax
        调用函数例子：draw_plots_three(get_total, labels_pic, xy_name)
        """

        fig, ax1 = plt.subplots()
        data = data.fillna(0)
        if data.empty:
            return fig, ax1
        else:
            xticks_new = []
            for xl in data[xy_name[0]]:
                xticks_new.append('\n'.join(xl))
            xticks_new_pd = pd.Series(xticks_new)

            ax1.plot(data[xy_name[0]], round(data[xy_name[1]]), '.-', label=labels_pic[0], c='#001055')
            ax1.plot(data[xy_name[0]], round(data[xy_name[2]]), '.-', c='#FFBF00', label=labels_pic[1])
            for x, y in zip(data[xy_name[0]], data[xy_name[1]]):
                plt.text(x, y + max(data[xy_name[1]]) * 0.02, round(y), ha='center', va='bottom', fontsize=9)
            plt.xticks(data[xy_name[0]])
            ax1.set_ylabel(labels_pic[0])
            ax2 = ax1.twinx()

            # 设置纵轴格式
            fmt = '%.0f%%'
            # yticks = FuncFormatter(fmt)
            yticks = mtick.FormatStrFormatter(fmt)
            ax2.yaxis.set_major_formatter(yticks)
            if min(data['growth']) >= 0:
                ax2.set_ylim(0, int(max(data['growth']) * 1.1))
            elif max(data['growth']) < 0:
                ax2.set_ylim(int(min(data['growth'])) * 1.1, int(max(data['growth'])) * 0.5)
            else:
                ax2.set_ylim(int(min(data['growth'])) * 1.1, int(max(data['growth'])) * 1.2)
            ax2.set_ylabel(labels_pic[2])
            ax1.set_ylim(0, int(data[xy_name[1]].max() * 1.15))
            ax2.plot(data[xy_name[0]], data['growth'].values, c='#9D9D9D', label=labels_pic[2])
            ax2.set_xticklabels(labels=xticks_new_pd)
            handles1, labels1 = ax1.get_legend_handles_labels()
            handles2, labels2 = ax2.get_legend_handles_labels()
            plt.legend(handles1 + handles2, labels1 + labels2,
                       frameon=False, ncol=3, loc='upper center', handlelength=2)  # bbox_to_anchor=(0, 1)
            ax1.spines['right'].set_color('none')
            return fig, ax1

    def draw_twin_axial_3_plots(self,data, **pics):
        """

        :param data:
        :param pics: get_total, yl1label='业扩报装(个)', yl2lengent='同期值',
                                y2label='同比%', x='org_name_sheng', yl1='ym_x', yl2='ym_y', y2l='growth'
        :return:
        """
        fig, ax1 = plt.subplots()
        data = data.fillna(0)
        if data.empty:
            return fig, ax1
        else:
            xticks_new = []
            for xl in data[pics["x"]]:
                xticks_new.append('\n'.join(xl))
            xticks_new_pd = pd.Series(xticks_new)

            ax1.plot(data[pics["x"]], round(data[pics["yl1"]]), '.-', label=pics["yl1label"], c='#001055')
            ax1.plot(data[pics["x"]], round(data[pics["yl2"]]), '.-', c='#FFBF00', label=pics["yl2lengent"])
            for x, y in zip(data[pics["x"]], data[pics["yl1"]]):
                plt.text(x, y + max(data[pics["yl1"]]) * 0.02, round(y), ha='center', va='bottom', fontsize=9)
            plt.xticks(data[pics["x"]])
            ax1.set_ylabel(pics["yl1label"])
            ax2 = ax1.twinx()

            # 设置纵轴格式
            fmt = '%.0f%%'
            # yticks = FuncFormatter(fmt)
            yticks = mtick.FormatStrFormatter(fmt)
            ax2.yaxis.set_major_formatter(yticks)
            ax2.set_ylabel(pics["y2label"])
            ax1.set_ylim(0, int(data[pics["yl1"]].max() * 1.15))
            ax2.plot(data[pics["x"]], data[pics['y2l']].values, c='#9D9D9D', label=pics["y2label"])
            ax2.set_xticklabels(labels=xticks_new_pd)
            handles1, labels1 = ax1.get_legend_handles_labels()
            handles2, labels2 = ax2.get_legend_handles_labels()
            plt.legend(handles1 + handles2, labels1 + labels2,
                       frameon=False, ncol=3, loc='upper center', handlelength=2)  # bbox_to_anchor=(0, 1)
            ax1.spines['right'].set_color('none')
            return fig, ax1

    # 绘制带平均值的图plot
    def draw_2_plots_avg(self,data, **pics):
        """

        :param data: 如，get_duration
        :param pics: x='org_name_sheng', yl1='duration_x', yl2='duration_y', yl3='mean',
                        yl1lalel= '接电时长(天)', yl2label='同期值', yl3label='平均值'
        :return:
        """
        fig, ax1 = plt.subplots()
        if data.empty:
            return fig, ax1
        else:
            data = data.fillna(0)
            xticks_new = []
            for xl in data[pics["x"]]:
                xticks_new.append('\n'.join(xl))
            xticks_new_pd = pd.Series(xticks_new)

            ax1.plot(data[pics["x"]], round(data[pics["yl1"]]), label=pics["yl1lalel"], c='#001055')
            ax1.plot(data[pics["x"]], round(data[pics["yl2"]]), 'o-', c='#FFBF00', label=pics["yl2label"])
            for x, y in zip(data[pics["x"]], data[pics["yl1"]]):
                plt.text(x, y + max(data[pics["yl1"]]) * 0.02, round(y), ha='center', va='bottom', fontsize=9)
            ax1.plot(data[pics["x"]], data[pics["yl3"]], c='#9D9D9D', dashes=[6, 2], label=pics["yl3label"])  # 平均值线（直线）
            plt.xticks(data[pics["x"]])
            ax1.set_ylabel(pics["yl1lalel"])
            data_mean = round(max(data[pics["yl3"]]))
            ax1.text(data.iloc[-1, 0], data_mean * 1.02, round(data_mean), ha='center', va='bottom', fontsize=9)
            if max(data[pics["yl1"]]) > max(data[pics["yl2"]]):
                max_value = max(data[pics["yl1"]])
            else:
                max_value = max(data[pics["yl2"]])
            ax1.set_ylim(0, max_value * 1.2)
            ax1.set_xticklabels(labels=xticks_new_pd)
            handles1, labels1 = ax1.get_legend_handles_labels()
            plt.legend(handles1, labels1,
                       frameon=False, ncol=3, loc='upper center', handlelength=2)  # bbox_to_anchor=(0, 1)
            ax1.spines['right'].set_color('none')
            return fig, ax1

    # 绘制双轴带平均值的图
    def draw_three(self,data, yrformat='%.0f%%', **pics):
        """

        :param yrformat: 双轴右轴默认的格式为百分比
        :param data:
        :param pics:  例如：x='org_name_sheng', yl='duration_x', yr='growth',
                  hline='mean', yllabel='接电时长(天)', yrlabel='同比%', hllabel='平均值'
        :return:
        """
        if len(data) > 0:
            xticks_new = []
            for xl in data[pics["x"]]:
                xticks_new.append('\n'.join(xl))
            xticks_new_pd = pd.Series(xticks_new)

            data = data.fillna(0)
            fig, ax1 = plt.subplots()
            ax1.bar(data[pics["x"]], data[pics["yl"]], width=0.4, label=pics["yllabel"])
            ax1.set_ylabel(pics["yllabel"])

            # 柱状图标签
            max_gd = max(data[pics["yl"]])
            for x, y in zip(data[pics["x"]], round(data[pics["yl"]], 2)):
                ax1.text(x, y + max_gd * 0.02, y, ha='center', va='bottom', fontsize=9)
            # 平均值线
            ax1.plot(data[pics["x"]], data[pics["hline"]], c='grey', dashes=[6, 2], label=pics["hllabel"])
            max_mean = max(data[pics["hline"]])
            ax1.text(data.iloc[-1, 0], max_mean * 1.02, max_mean, ha='center', va='bottom', fontsize=9)
            ax1.set_ylim(0, int(max(data[pics["yl"]]) * 1.1))
            # 占(同比)比轴
            ax2 = ax1.twinx()
            # 设置纵轴格式
            # pics['yrformat']  = '%.0f%%'
            fmt = yrformat
            yticks = mtick.FormatStrFormatter(fmt)
            ax2.yaxis.set_major_formatter(yticks)
            if min(data[pics["yr"]]) > 0:
                ax2.set_ylim(0, int(max(data[pics["yr"]]) * 1.1))
            elif max(data[pics["yr"]]) < 0:
                ax2.set_ylim(int(min(data[pics["yr"]])) * 1.1, int(max(data[pics["yr"]])) * 0.5)
            else:
                ax2.set_ylim(int(min(data[pics["yr"]])) * 1.1, int(max(data[pics["yr"]])) * 1.2)
            ax2.set_ylabel(pics["yrlabel"])
            ax1.set_ylim(0, int(data[pics["yl"]].max() * 1.15))
            ax2.plot(data[pics["x"]], data[pics["yr"]].values, 'o-', c='orange', label=pics["yrlabel"])

            ax2.set_xticklabels(labels=xticks_new_pd)
            # 图例
            handles1, labels1 = ax1.get_legend_handles_labels()
            handles2, labels2 = ax2.get_legend_handles_labels()
            plt.legend(handles1 + handles2, labels1 + labels2,
                       frameon=False, ncol=3, loc='upper center', handlelength=2)  # bbox_to_anchor=(0, 1)
            return fig, ax1, ax2
        else:
            return plt.subplots()

    # 绘制单轴柱状图with平均值
    def draw_bar_avg(self,data, **pics):
        """

        :param data:
        :param pics: 如,x='org_name_sheng', yl='ym_x', hline='mean',
                    yllabel='工单数(个)', hllabel='平均值'
        :return:
        """
        if len(data) > 0:
            data = data.fillna(0)
            fig, ax1 = plt.subplots()
            ax1.bar(data[pics["x"]], data[pics["yl"]], width=0.4, label=pics["yllabel"])
            ax1.set_ylabel(pics["yllabel"])

            # 柱状图标签
            max_gd = max(data[pics["yl"]])
            for x, y in zip(data[pics["x"]], round(data[pics["yl"]], 2)):
                ax1.text(x, y + max_gd * 0.02, y, ha='center', va='bottom', fontsize=9)
            # 平均值线
            ax1.plot(data[pics["x"]], data[pics["hline"]], c='grey', dashes=[6, 2], label=pics["hllabel"])
            max_mean = max(data[pics["hline"]])
            ax1.text(data.iloc[-1, 0], max_mean * 1.02, max_mean, ha='center', va='bottom', fontsize=9)
            ax1.set_ylim(0, int(max(data[pics["yl"]]) * 1.1))
            ax1.set_ylim(0, int(data[pics["yl"]].max() * 1.15))

            ax1.spines["right"].set_visible(False)
            xticks_new = []
            for xl in data[pics["x"]]:
                if len(xl) <= 3:
                    xticks_new.append('\n'.join(xl))
                else:
                    xticks_new.append(xl)
            xticks_new_pd = pd.Series(xticks_new)
            ax1.set_xticklabels(labels=xticks_new_pd)
            # 图例
            handles1, labels1 = ax1.get_legend_handles_labels()
            plt.legend(handles1, labels1,
                       frameon=False, ncol=3, loc='upper center', handlelength=2)  # bbox_to_anchor=(0, 1)
            return fig, ax1
        else:
            return plt.subplots()

    # draw pie with circle：环形图
    def draw_pie(self,data):
        fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
        wedges, texts = ax.pie(data, wedgeprops=dict(width=0.5), startangle=-30)
        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72, alpha=0)
        # bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        kw = dict(arrowprops=dict(arrowstyle="-"),
                  bbox=bbox_props, zorder=0, va="center")

        for i, p in enumerate(wedges[:3]):
            ang = (p.theta2 - p.theta1) / 2. + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = "angle,angleA=0,angleB={}".format(ang)
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            ax.annotate(round(data[i], 2), xy=(x, y), xytext=(1.25 * np.sign(x), 1.3 * y),
                        horizontalalignment=horizontalalignment, fontsize=9, **kw)
        return fig, ax

    # 双轴双线图（不带百分比）
    def draw_two_line_two_axis(self,data, col_1, col_2, col_3, label1, label2, title):
        figure = plt.figure(dpi=300)
        ax1 = plt.subplot()
        ax1.plot(data[col_1], data[col_2], color="#001055", label=label1, linewidth=1.5)
        ax2 = ax1.twinx()
        ax2.plot(data[col_1], data[col_3], color="#ED7C30", label=label2, linewidth=1.5)
        # 设置X轴 ticks 文字竖着显示
        xticklabels = data[col_1]
        new_xticklabels = []
        for i in xticklabels:
            new_xticklabels.append("\n".join(i))
        ax1.set_xticklabels(labels=new_xticklabels)
        # 取消边框
        ax1.spines["top"].set_visible(False)
        ax2.spines["top"].set_visible(False)
        # 开启图例
        leg1 = ax1.legend(loc=(0.3, 0.9))
        leg2 = ax2.legend(loc=(0.5, 0.9))
        # 取消图例的边框
        leg1.get_frame().set_linewidth(0.0)
        leg2.get_frame().set_linewidth(0.0)
        # 设置标题
        ax1.set_title(title)
        # 自动调整布局
        plt.tight_layout()
        return figure, ax1, ax2

    # 词云图
    def draw_ciyuntu(self):
        pass