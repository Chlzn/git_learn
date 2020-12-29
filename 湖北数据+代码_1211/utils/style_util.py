# -*- coding: utf-8 -*-
"""
@Author  : ctjc
@Project:
@Date  : 2020-09-01 10:20:01
@Desc : 画图工具类：画图过程中可公用的方法
"""

import matplotlib.pyplot as plt
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import RGBColor


class StyleUtil:

    def wenziShu(self,x):
        print('x:',x)

        xtickslabels = list(x)
        print('xtickslabels:',xtickslabels)
        new_xticklabels = []
        for i in xtickslabels:
            print(i,'------',new_xticklabels)
            new_xticklabels.append("\n".join(i))
        return new_xticklabels


    # 图像设置
    def set_figure(self, frame=False,legendFontsize=10,xtickLabelsize=10,ytickLabelsize=10,axesLabelsize=10,axesTitlesize=12,fontSize=12):
        plt_params = {"figure.figsize": (6.8, 3.06),
                      "font.size": fontSize,
                      "font.family": 'sans-serif',
                      "font.sans-serif": ['SimSun'],
                      "figure.subplot.wspace": 0.6,  #
                      "figure.subplot.hspace": 0.7,  #
                      "axes.spines.right": frame, # 坐标系-右侧线
                      "axes.spines.top": frame,
                      "axes.titlesize": axesTitlesize,
                      "axes.labelsize": axesLabelsize,
                      "axes.unicode_minus": False,
                      "legend.fontsize": legendFontsize,
                      "xtick.labelsize": xtickLabelsize,
                      "ytick.labelsize": ytickLabelsize,
                      "xtick.direction": 'out',
                      "ytick.direction": 'in'
                      }
        plt.rcParams.update(**plt_params)
        # plt.rcParams["font.sans-serif"] = ["SimHei"]  # 正常显示中文
        plt.rcParams["axes.unicode_minus"] = False  # 正常显示正负号

    def doc_styles(self,doc_tem):
        styles = doc_tem.styles
        styles['Normal'].font.name = 'Times New Roman'
        styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), u'方正仿宋_GBK')
        styles['Normal'].font.size = Pt(16)

        new_heading_style = styles.add_style('New Heading 1', WD_STYLE_TYPE.PARAGRAPH)
        new_heading_style.base_style = styles['Heading 1']
        font = new_heading_style.font
        font.name = 'Times New Roman'
        font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        styles['New Heading 1']._element.rPr.rFonts.set(qn('w:eastAsia'), u'方正仿宋_GBK')
        font.size = Pt(18)

        new_heading_style = styles.add_style('New Heading 2', WD_STYLE_TYPE.PARAGRAPH)
        new_heading_style.base_style = styles['Heading 2']
        font = new_heading_style.font
        font.name = 'Times New Roman'
        font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        styles['New Heading 2']._element.rPr.rFonts.set(qn('w:eastAsia'), u'方正仿宋_GBK')
        font.size = Pt(18)

        new_heading_style = styles.add_style('New Heading 0', WD_STYLE_TYPE.PARAGRAPH)
        new_heading_style.base_style = styles['Heading 1']
        font = new_heading_style.font
        font.name = 'Times New Roman'
        font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        styles['New Heading 0']._element.rPr.rFonts.set(qn('w:eastAsia'), u'方正仿宋_GBK')
        font.size = Pt(20)

        new_heading_style = styles.add_style('New Heading 3', WD_STYLE_TYPE.PARAGRAPH)
        new_heading_style.base_style = styles['Heading 3']
        font = new_heading_style.font
        font.name = 'Times New Roman'
        font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        styles['New Heading 3']._element.rPr.rFonts.set(qn('w:eastAsia'), u'方正仿宋_GBK')
        font.size = Pt(16)

        new_heading_style = styles.add_style('zbg title', WD_STYLE_TYPE.PARAGRAPH)
        new_heading_style.base_style = styles['Normal']
        font = new_heading_style.font
        font.name = 'Times New Roman'
        font.color.rgb = RGBColor(0xff, 0x00, 0x00)
        font.bold = True
        styles['zbg title']._element.rPr.rFonts.set(qn('w:eastAsia'), u'方正仿宋_GBK')
        font.size = Pt(26)
        return styles

