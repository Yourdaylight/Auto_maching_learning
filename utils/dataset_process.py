'''
数据集操作模块
上传数据文件
选择数据数据
删除数据文件
'''

import pymongo
import pandas as pd
from ModelSelection.models import UserModel
import traceback
import os
import time

# username='root'
# password='lzh.mongo.admin'
# url='47.97.197.244'
# port=27017
class DatasetProcess():
    def __init__(self,database="AML",collection="user_model",username="admin"):
        self.client =pymongo.MongoClient(host="localhost",port=27017)
        self.collection=self.client[database][collection]
        self.username=username
        self.user = self.collection.find_one({"username": self.username})
        self.columns=[]
        self.datasets= [i.get('name') for i in self.user['dataset']]

    def get_dataset_info(self):
        names=[i.get('name') for i in self.user['dataset']]
        upload_times=[i.get('upload_time') for i in self.user['dataset']]
        return names,upload_times


    def upload(self,file_path,username):
        '''
        :param file_path: 用户上传的文件路径
        :return :是否成功上传的bool值
        '''
        #文件后缀检查
        postfix=os.path.split(file_path)[-1].split(".")
        if postfix[0] in self.datasets:
            return False,"该数据集已存在"
        try:
            if postfix[1]=='xls' or postfix[1]=='xlsx':
                df=pd.read_excel(file_path)
            elif postfix[1]=="csv" or postfix[1]=='txt':
                df = pd.read_csv(file_path,encoding="utf-8")
        except UnicodeDecodeError as e:
            df = pd.read_csv(file_path, encoding="gbk")
        except Exception as e:
            traceback.print_exc()
            return False,str(e)
        #将dataframe转换为字典形式
        data = {i: df[i].tolist() for i in df.columns}
        filename=postfix[0]+"_"+postfix[1]
        upload_time=time.time()
        try:
            self.collection.update_many({'username':self.username},{"$push":{"dataset":{filename:data,"name":filename,'upload_time':upload_time}}})
        except Exception as e:
            traceback.print_exc()
            return False, str(e)
        return True,"上传成功"

    def get_dataset(self,dataset_name):
        '''
        从数据库取出数据，转换为DF进行分析
        :param dataset_name:数据集名称
        :return: 获取数据集转换为DataFrame
        '''
        my_dataset =None
        flag=False
        for name in self.user['dataset']:
            if name['name']==dataset_name:
                my_dataset=name[dataset_name]
                flag=True
                break
        if flag:
            self.columns=list(my_dataset.keys())
            return my_dataset
        else:
            return None

    def delete(self,dataset_name):
        '''
        根据数据集名称删除数据
        :param dataset_name:
        :return:
        '''

        self.collection.update({"username":self.username},{"$pull":{"dataset":{"name":dataset_name}}})
        return True

#
if __name__=="__main__":
    pass
    # path="../Datasets/day.csv"
    # dp=DatasetProcess()
    # res=dp.get_dataset('not')
    # for i in dp.user['dataset']:
    #     print(i['name'])
    # dp.delete("hour")#删除admin用户下的hour文件
    # dp.upload(path)#将day.csv上传
    # a=dp.get_dataset("hour")
    # print(pd.DataFrame(a))


