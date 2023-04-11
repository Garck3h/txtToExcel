#Creation time：2023/3/29
#Author：garck
#用途：将基线结果整理到excel中
import os
import pandas as pd
import numpy as np
import re

src_path = '3/1/'
ip_address = [] #用于存储ip地址
file_name_src_list = []#用于存储文件路径
end_data_huizong = []#用于将所有的内容存在到里面，形成了一个二维数组，每个元素对应一个数组，即IP的内容，

def transformation(file_name_src_hanshu):#读取数据、转换格式，转成一维数组，然后在每个元素的中间都加上换行符
    try:
        #data = pd.read_table(file_name_src_hanshu, encoding='utf-8',header=None, delimiter="\t",on_bad_lines='skip')  # 读取txt的内容,跳过错误行
        data = pd.read_table(file_name_src_hanshu, encoding='utf-8', header=None, delimiter="\t")  # 读取txt的内容
        #data = pd.read_table(file_name_src_hanshu, encoding='utf-8',header=None, delimiter="\t",error_bad_lines = False, warn_bad_lines = True)  # 读取txt的内容,跳过错误行

        data1 = data.to_numpy()  # 将pd格式转成数组格式
        data2 = list(np.array(data1).flatten())  # 二维数组转成一维数组
        return data2
    except Exception as ex:
        print(ex)

def flag_bit(data2_hanshu):#获取标志位
    data2 = data2_hanshu
    flag_nu = []
    for x in range(len(data2)):
        target_str = re.match("检查项", data2[x])  # 定义个变量，使用正则去匹配有没有特定值的，如果有就返回一个匹配的对象，没有就返回None
        if target_str != None:  # if判断是否有
            flag_nu.append(x)
    flag_nu.append(len(data2))
    return flag_nu

def merge_hebing(flag_nu_hanshu,data2_hanshu):
    flag_nu = flag_nu_hanshu
    data2 = data2_hanshu
    end_data = []
    for x in range(len(flag_nu) - 1):
        end_data.append('\n'.join(data2[slice(flag_nu[x], flag_nu[x + 1], 1)]))  # 根据位置截取数组中的内容合并为一个元素，然后一一添加到end_dataq数组中
    return end_data

for root, dirs,files in os.walk(src_path):
    for i in files:
        file_name_src = src_path + i
        file_name_src_list.append(file_name_src)
        ip = file_name_src.replace('src/', '').replace('.txt', '')
        ip_address.append(ip)
        #print("第一个函数：",transformation(file_name_src))
        #print("第二个函数：",flag_bit(transformation(file_name_src)) )
        #print("第三个函数：",merge_hebing(flag_bit(transformation(file_name_src)),transformation(file_name_src)))
        print(ip+"  Success!")
        end_data_huizong.append(merge_hebing(flag_bit(transformation(file_name_src)),transformation(file_name_src)))

zidian = dict(zip(ip_address,end_data_huizong)) #将IP和全部数据的二维数组构造成一个字典
#df = pd.DataFrame(zidian)
df = pd.DataFrame(pd.DataFrame.from_dict(zidian, orient='index').values.T,columns=list(zidian.keys()))  # 防止输入的数值长度不一样的时候会崩掉


#print(df)
df.to_excel("piliang.xlsx", '操作系统安全',index=False,engine='xlsxwriter', encoding='utf-8')#engine清洗非法字符
print("\n"+"已完成全部内容的合并！！")
