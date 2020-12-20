# -*- coding: utf-8 -*-
# @Time    : 2020/12/19 20:35
# @Author  : Creekyu
# @FileName: FinalExp1.py
# @Software: PyCharm
# @Github  : https://github.com/Creekyu

"""
期末综合练习
"""
import pandas as pd
import numpy as np

# 导入数据
path1= "C:/Users/50309/Desktop/P1/"
path2 = "C:/Users/50309/Desktop/P2/"

data1 = pd.read_csv(path1 + "知乎数据_201701.csv",engine="python")


# 数据清洗
def data_clean(df):
    """如果是object数据类型则替换空值为“缺失数据”
    否则替换为0，inplace参数表示是否修改自身

    :param df:Dataframe类型
    :return: 返回修改后df
    """
    cols = df.columns
    for col in cols:
        if df[col].dtype is np.dtype('O'): # object类表示为np.dtype("O")
            df[col].fillna("缺失数据",inplace = True)
        else:
            df[col].fillna(0,inplace = True)

data_clean(data1)
# data1

"""
一、知友分布数据分析
① 按照学校（教育经历字段）统计粉丝数（‘关注者’）、
关注人数（‘关注’），并筛选出粉丝数TOP20的学校，
不要求创建函数
"""
grouped_data1 = data1.groupby(["教育经历"])
sum_of_fan = grouped_data1.sum()
sum_of_fan.reset_index(inplace=True)
# 粉丝数、关注人数
# sum_of_fan[["教育经历","关注者"]]
# sum_of_fan[["教育经历","关注"]]

# 筛选粉丝人数TOP20
sum_of_fan.sort_values("关注者",ascending=False,inplace=True)
# 第1、9、10、13、25是无用的教育经历，剔除
temp_data = sum_of_fan[["教育经历","关注者"]]
fans_top20 = pd.concat([temp_data.iloc[1:8],temp_data.iloc[10:12]])
fans_top20 = pd.concat([fans_top20,temp_data.iloc[14:24]])
fans_top20.append(temp_data.iloc[26])
# fans_top20

import sys
# max-min标准化
def max_min(serie):
    """max-min标准化，将密度值转换到0-100内

    :param serie: 传入Series类
    :return: 返回更改后的Series
    """
    max = -sys.maxsize
    min = sys.maxsize
    for i,v in serie.items():
    # 寻找最大最小值
        if v > max:
            max = v
        if v < min:
            min = v
    new_serie = (serie - min) / (max - min) * 100
    return new_serie


"""
② 通过散点图 → 横坐标为关注人数，纵坐标为粉丝数，做图表可视化
③ 散点图中，标记出平均关注人数（x参考线），平均粉丝数（y参考线）
"""
import matplotlib.pyplot as plt
import math

# 解决plt中文显示的问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 取交集得到top20关注总人数
top20 = pd.merge(fans_top20,sum_of_fan[["教育经历","关注"]],
                 on="教育经历",how="inner")
# top20

# 标准化值
stand_top20 = pd.DataFrame()
stand_top20["教育经历"] = top20["教育经历"]
stand_top20["关注"] = max_min(top20["关注"])
stand_top20["关注者"] = max_min(top20["关注者"])


x_values = top20["关注"].tolist()
y_values = top20["关注者"].tolist()

x_values_1 = stand_top20["关注"].tolist()
y_values_1 = stand_top20["关注者"].tolist()

# 计算到原点的距离作为相对距离来确定圆点大小和颜色
alist = []
for i in range(len(x_values)):
    alist.append(math.sqrt(x_values_1[i]**2 + y_values_1[i]**2)/2)

# 生成散点图
plt.figure(dpi=400)
plt.ylim([-100000,700000])
plt.scatter(x_values,y_values,
            alpha=0.8,c=alist,s=alist,
            edgecolors="gray",lw=0.7)
plt.xlabel("关注人数")
plt.ylabel("粉丝数")
plt.title("Top20知乎粉丝数高校排名")
plt.grid(ls=":",lw=0.5,c='black')

# 打印名称
name = top20["教育经历"].tolist()
count = 0
for i,j in zip(x_values,y_values):
    plt.text(i+1000,j-5000,name[count],fontsize=5)
    count += 1

# 均值参考线
mean_of_att = np.mean(x_values)
mean_of_fan = np.mean(y_values)
plt.axhline(mean_of_fan,
            lw=0.5,c="red",ls="--")
plt.axvline(mean_of_att,
            lw=0.5,c="green",ls="--")
plt.legend(["粉丝数均值：%.2f"%mean_of_fan,
            "关注人数均值:%.2f"%mean_of_att,
            "学校"],loc="upper left",
           fontsize=6)

# 保存图片，dip=400（调整清晰度）
plt.savefig(path2 + "Top20知乎粉丝数高校排名.png",dpi=400)


