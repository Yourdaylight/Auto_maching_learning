import os
# from codes import MODEL_DICT

'''
流程：   
` 1、从monodb读取用户上传的数据集（已完成）`       
`2、传入需要处理的列(特征列)，以及处理过程函数。  
   * 内置填充缺失值、删除缺失值以及one-hot编码
    - 标准化数据（MinMax），可选参数 `    
` 3、模型构建，传入模型名称、目标列进行构建`
    - 允许用户进行参数搜索，前端用户输入的搜索参数格式为json格式

主函数生成：
- 自动生成代码的代码模块存放于同一个文件夹：
       仅包含功能函数
       
- 主函数预先定义一个代码文件，相关参数通过占位符填充，填充的参数来源于前段输入，包括：主要包括特征列、目标列，文件名
'''
MODEL_DICT={
    '分类':{
        '朴素贝叶斯':'from sklearn.naive_bayes import GaussianNB',
        '决策树':'from sklearn.tree import DecisionTreeClassifier',
        '支持向量机':'from sklearn.svm import SVC',
        '逻辑回归': 'from sklearn.linear_model import LogisticRegression',
        '神经网络':'from sklearn.neural_network import MLPClassifier'
    },
    '回归':{
        '线性回归':'from sklearn.linear_model import LinearRegression',
        '决策树':'from sklearn.tree import DecisionTreeRegressor',
        '支持向量机':'from sklearn.svm import SVR',
        '神经网络':'from sklearn.neural_network import MLPRegressor'
    },
    '聚类':{
        'K-means':'from sklearn.cluster import KMeans'
    },
    'ROC曲线':'plot_ROC_curve.py',
    '混淆矩阵':'plot_confusion_matrix.py'
}

class SetModel():
    '''

    用于与前端界面交互，获取特征列，以及数据处理步骤。
    根据用户选择的步骤，读取预定义的代码。
    前端返回参数
    {
        target:[],
        features:[],

    }
    '''

    def __init__(self, dataset_name,features,target,model_type,model_name,evaluate_methods=[]):
        '''

        :param dataset_name(str,):数据集名称
        :param features(str of list):特征列
        :param target(str):目标
        :param model_type(str):分类/回归/聚类
        :param model_name(str of list):模型
        :param evaluate_methods(str of list,非必填):模型评估方法
        '''
        self.code_files=os.path.join(os.path.abspath(''),'codes')
        self.dataset_name=dataset_name
        self.target=target
        self.features=features
        self.model_type=model_type
        self.model_name=model_name
        self.evaluate_methods=evaluate_methods
        self.generate=''

    def clean_data(self,df,cols,op,standard=''):
        '''
           自动数据清洗
           df:
           cols:
           op:数据清洗的操作
           '''
        if op == 'fillna':
            df.loc[:, cols].fillna()
        elif op == 'dropna':
            df.loc[:,cols].dropna()
        else:
            df.loc[:,cols].apply(op)
        return df

    def joint_code(self,code_path,encoding='utf-8'):
        '''拼接代码文件'''
        try:
            f = open(os.path.join(self.code_files,code_path), 'r',encoding=encoding)
            self.generate += f.read()+'\n'
        except:
            f = open(os.path.join(self.code_files,code_path), 'r', encoding='gbk')
            self.generate += f.read()+'\n'

    def get_code(self):
        #生成代码
        # 拼接导入的库
        self.joint_code('ImportPackages.py')
        for model in self.model_name:
            self.generate+='\n'+MODEL_DICT[self.model_type][model]+'\n'

        # 拼接函数评估方法
        if len(self.evaluate_methods)!=0:
            for method in self.evaluate_methods:
                self.joint_code(MODEL_DICT[method])

        # 拼接变量
        for model in self.model_name:
            sklearn_model = MODEL_DICT[self.model_type][model].split(' ')[-1] + '()'
            self.generate+='''
FILE_PATH='./{}'\n
FEATURES={}\n
TARGET='{}'\n
MODEL={}\n
        '''.format(self.dataset_name.replace('_','.'), self.features, self.target, sklearn_model)
        #拼接主函数
        self.joint_code('Main.py')

        #生成代码文件
        with open(os.path.join(os.path.abspath(''),'temp/generate.py'),'w',encoding='utf-8') as f:
            f.write(self.generate)
        f.close()
        return self.generate


if __name__=='__main__':
    myModel=SetModel('day',['cnt','yr','weekday'],'season','分类',['决策树'],['混淆矩阵','ROC曲线'])
    myModel.get_code()