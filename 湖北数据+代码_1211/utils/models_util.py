# -*- coding: utf-8 -*-
"""
@Author  : ctjc
@Project:
@Date  : 2020-09-01 10:20:01
@Desc : 模型工具类：模型训练过程可公用的方法
"""
import os
import joblib
import matplotlib.pyplot as plt
import simplejson
import logging


class ModelUtil:
    def save_pic(self, pic, pic_name):
        """
        2.保存模型图片:  png
        :param pic:  图片
        :param pic_name: 图片名称
        :return:
        """
        # ###①创建保存图片的路径
        pic_url = f'{os.path.dirname(os.path.dirname(__file__))}/resource/pic/'

        # ###②保存图片
        try:
            pic.savefig(f"{pic_url}{pic_name}.png", dpi=500, bbox_inches='tight')    # dpi  每英寸像素数
        except IOError as e:
            logging.error(f'保存{pic_name}图片错误：{e}')
        plt.close()


