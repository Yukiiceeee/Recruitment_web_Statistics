import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# 设置显示中文字体
from pylab import mpl
mpl.rcParams["font.sans-serif"] = ["SimHei"]
# 设置显示正常符号
mpl.rcParams["axes.unicode_minus"] = False
pd.set_option('display.unicode.east_asian_width',True)

# 设置列对齐
pd.set_option('display.unicode.ambiguous_as_wide',True)
pd.set_option('display.unicode.east_asian_width',True)

file_path = 'D:\Pytorch_机器学习与深度学习\数据爬取、可视化、分析实战\【智联招聘】招聘信息数据分析项目\【原始数据】Python职业招聘数据-上海.csv'
test = pd.read_csv(file_path)

def convert_salary_to_number(salary):
    """
    将薪资范围从文本转换为数值平均值。
    """
    # 移除附加文本（如果存在）
    salary = salary.split(' · ')[0]
    salary = salary.split('/')[0]

    # 将中文字符转换为数值
    salary = salary.replace('万', '*10000').replace('千', '*1000').replace('k', '*1000')

    # 如果存在范围，则计算平均值
    if '-' in salary:
        lower, upper = salary.split('-')
        try:
            return (eval(lower) + eval(upper)) / 2
        except Exception:
            return None
    else:
        try:
            return eval(salary)
        except Exception:
            return None
        
def clean(test):
    # 将0替换成Nan
    test.replace(to_replace=0,value=np.nan,inplace=True)
    # 缺失值处理
    test = test.dropna(subset=[col for col in test.columns if col != '公司性质'])
    # 替换公司性质列空白值
    test = test.copy()
    test['公司性质'].fillna('未知', inplace=True)

    # 可视化看数据分布，这里是pandas模块里的画图
    test.plot(kind='box',subplots=True,layout=(1,2),sharex=False,figsize = (10,10))
    plt.savefig("【Python-上海】薪资分布箱线图")
    plt.show()

    # 异常值处理
    # 异常值检验函数 =========================
    def outlier_test(data, column):
        # 确保列是数值类型
        if not np.issubdtype(data[column].dtype, np.number):
            return pd.DataFrame(), None, None
        print(f'以 {column} 列为依据，使用 上下截断点法(iqr) 检测异常值...')
        print('=' * 70)
        # 四分位点；这里调用函数会存在异常
        column_iqr = np.quantile(data[column], 0.75) - np.quantile(data[column], 0.25)
        # 1，3 分位数
        (q1, q3) = np.quantile(data[column], 0.25), np.quantile(data[column], 0.75)
        # 计算上下截断点
        upper, lower = (q3 + 1.5 * column_iqr), (q1 - 1.5 * column_iqr)
        # 检测异常值
        outlier = data[(data[column] <= lower) | (data[column] >= upper)]
        print(f'第一分位数: {q1}, 第三分位数：{q3}, 四分位极差：{column_iqr}')
        print(f"上截断点：{upper}, 下截断点：{lower}")
        return outlier, upper, lower
    # 对薪资采取四分位法检测异常值
    outlier, _, _ = outlier_test(data=test, column="薪资")
    # 删除异常值之前确认索引存在
    if not outlier.empty:
        test = test.drop(index=outlier.index)

    return test

# 对薪资列应用转换函数
test['薪资'] = test['薪资'].apply(convert_salary_to_number)

# 删除薪资为 NaN 的行（包括薪资为“面议”的行）
test = test.dropna(subset=['薪资'])

test_cleaned = clean(test)

# 显示清洗后的数据前几行
print(test_cleaned.head())

# 保存清洗后的数据
test_cleaned.to_csv('【清洗后数据】Python职业招聘数据-上海.csv', index=False)





















