# -*- coding: utf-8 -*-
# @Time    : 2020/12/20 14:23
# @Author  : Creekyu
# @FileName: FinalExp2.py
# @Software: PyCharm
# @Github  : https://github.com/Creekyu

from com.xby.project import FinalExp1 as FE1
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""
二.  视频网站数据清洗整理和分析
1、数据清洗 - 去除空值
要求：创建函数
提示：fillna方法填充缺失数据，注意inplace参数
"""
data2 = pd.read_csv(FE1.path2 + "爱奇艺视频数据.csv",engine='python')
FE1.data_clean(data2)
data2

"""
2、数据清洗 - 时间标签转化
要求：
① 将时间字段改为时间标签
② 创建函数
提示：
需要将中文日期转化为非中文日期，例如 2016年5月24日 → 2016.5.24
"""

def trans(df):
    """将中文日期格式变更为英文格式
    其原理是借助列表，从每一个日期字符串转换得来的列表的尾部开始弹出
    将相应的英文格式字符插入新列表中，从尾部弹出可减小相当的时间复杂度
    传入的DataFrame自身将被修改

    :param df: 传入DataFrame类
    """
    temp = df["数据获取日期"]
    date_list = []

    for date in temp:
        # date字符串转为列表
        ch_list = list(date)
        leng = len(ch_list)
        # 计数
        count = 0
        alist = []
        # 转换过程
        while(count < leng):
            ch = ch_list.pop()
            if ch == "日":
                pass
            elif ch in ["月","年"]:
                alist.insert(0,".")
            else:
                alist.insert(0,ch)
            count += 1
        date_list.append("".join(alist))
    new_series = pd.Series(date_list)
    df.drop(["数据获取日期"],axis=1,inplace=True)
    df.insert(0,"数据获取日期",new_series)

trans(data2)
# data2


"""
3、问题1 分析出不同导演电影的好评率，并筛选出TOP20
要求：
① 计算统计出不同导演的好评率，不要求创建函数
②	通过多系列柱状图，做图表可视化
提示：
① 好评率 = 好评数 / 评分人数
② 可自己设定图表风格
"""
# 计算好评率
grouped_data2 = data2.groupby(["导演"])
rate_of_like = grouped_data2.sum().reset_index()[["导演","评分人数","好评数"]]
rate_of_like["好评率"] = rate_of_like["好评数"] / rate_of_like["评分人数"]
rate_of_like.sort_values("好评率",ascending=False,inplace=True)

# 做柱状图
top20_of_like = rate_of_like.iloc[0:20]
# top20_of_like

list_of_director = top20_of_like["导演"].tolist()
# list_of_director

x_values_2 = list(range(0,20,1))
y_values_2 = top20_of_like["好评率"].tolist()

plt.figure(figsize=(15,6),dpi=400)
plt.bar(x_values_2,y_values_2,
        alpha=0.8,color="lightskyblue",
        edgecolor="black",lw=1)
plt.grid(axis='y',ls=":",lw=1)
plt.title("导演好评率")
plt.xlabel("导演")
plt.ylabel("好评率")
plt.ylim([0.975,1])
plt.xticks(x_values_2,list_of_director,rotation=40) # 替换x轴标签，并旋转40度
plt.legend(["好评率"],fontsize=20)

# 加入数据标签
for i,j in zip(x_values_2,y_values_2):
    plt.text(i,0.976,"%.3f"%j,
             ha="center")
# 趋势线
import matplotlib.pylab as pl
def plt_trend(x, y, n):
    """拟合趋势线
       参考:https://blog.csdn.net/qq_34105362/article/details/89554156

    :param x: x坐标集
    :param y: y坐标集
    :param n: 函数次数
    """
    pl.plot(x, y, 'ko')
    parameter = np.polyfit(x, y, n) # n=1为一次函数，返回函数参数
    f = np.poly1d(parameter) # 拼接方程
    pl.plot(x, f(x),color="hotpink",ls="-")
plt_trend(x_values_2,y_values_2,1)

# 保存图片
plt.savefig(FE1.path2 + "Top20导演好评率.png",dpi=400)

"""
4、问题2 统计分析2001-2016年每年评影人数总量
要求：
① 计算统计出2001-2016年每年评影人数总量，不要求创建函数
② 通过面积图，做图表可视化，分析每年人数总量变化规律
"""
# 以上映年份作为每年影评统计人数总量
grouped_data3 = data2.groupby(["上映年份"])
total = grouped_data3.sum().reset_index()[["上映年份","评分人数"]]
total.sort_values(["上映年份"],ascending=False,inplace=True)
total = total[0:16]
total.sort_values(["上映年份"],inplace=True)
# total

# 做面积图
x_values_3 = total["上映年份"].tolist()
y_values_3 = total["评分人数"].tolist()

# 基本参数
plt.figure(figsize=(12,6),dpi=400)
plt.ylim([0,1.05*max(y_values_3)])
plt.xlim([2001,2016])
plt.plot(x_values_3,y_values_3,color="grey")
plt.xticks(x_values_3)
plt.xlabel("年份")
plt.ylabel("评分总人数")
plt.title("2001-2016影评人数总量")
plt.grid(True,ls=":",lw=1)

# 填充
plt.fill_between(x_values_3,y_values_3,0,color="turquoise")
plt.legend(["趋势线","总人数"])

# 保存图片
plt.savefig(FE1.path2 + "2001-2016影评人数总量",dpi=400)

