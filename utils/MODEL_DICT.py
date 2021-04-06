"""
模型字典：前端用户选择的模型与生成代码-函数对应关系
"""
MODEL_DICT = {
    '分类': {
        '朴素贝叶斯': 'from sklearn.naive_bayes import GaussianNB',
        '决策树': 'from sklearn.tree import DecisionTreeClassifier',
        '支持向量机': 'from sklearn.svm import SVC',
        '神经网络': 'from sklearn.neural_network import MLPClassifier',
        '逻辑回归': 'from sklearn.linear_model import LogisticRegression',
        'KNN': 'from sklearn.neighbors import KNeighborsClassifier',
        "Adaboost": 'from sklearn.ensemble import AdaBoostClassifier',
        "随机森林": 'from sklearn.ensemble import RandomForestClassifier'

    },
    '回归': {
        '线性回归': 'from sklearn.linear_model import LinearRegression',
        'KNN': 'from sklearn.neighbors import KNeighborsRegressor',
        '决策树': 'from sklearn.tree import DecisionTreeRegressor',
        '支持向量机': 'from sklearn.svm import SVR',
        '神经网络': 'from sklearn.neural_network import MLPRegressor',
        'Adaboost': 'from sklearn.ensemble import AdaBoostRegressor',
        '随机森林': 'from sklearn.ensemble import RandomForestRegressor'
    },
    '聚类': {
        'K_means': 'from sklearn.cluster import KMeans',
        'MiniBatchKMeans': 'from sklearn.cluster import MiniBatchKMeans',
        'BIRCH': 'from sklearn.cluster import Birch'
    },
    'ROC曲线': 'plot_ROC_curve.py',
    '混淆矩阵': 'plot_confusion_matrix.py'
}

METRICS_DICT = {
    "分类": {
        'ROC曲线': 'plot_ROC_curve.py',
        '混淆矩阵': 'plot_confusion_matrix.py'
    },
    "回归": {
        "误差平方和": "",
        "决定系数(R²)": ""
    },
    "聚类": {}
}

CLEAN_DICT = {
    "缺失值填充": {
        "按0填充": "df[cols]=df[cols].fillna(0)",
        "均值填充": "df[cols]=df[cols].fillna(df[cols].mean())",
        "众数填充": "df[cols]=df[cols].fillna(df[cols].mode())",
        "使用上一个数据填充": "df[cols]=df[cols].fillna(method='pad')",
        "使用下一个数据填充": "df[cols]=df[cols].fillna(method='bfill')",
        "插值法填充": "df[cols] = df[cols].interpolate()"
    },
    "重复项删除": "df[cols] = df[cols].dropna()",
    "排序": "df.sort_values(by=cols, inplace= True)",
    "筛选": {
        "大于": "",
        "等于": "",
        "小于": "",
        "包含": ""
    },
    "标准化": {
        "最大最小规范化": "",
        "均值规范化": ""
    }
}
if __name__ == '__main__':
    print(MODEL_DICT['分类']['KNN'])
