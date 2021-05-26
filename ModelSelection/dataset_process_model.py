'''
数据集操作模块
上传数据文件
选择数据数据
删除数据文件
'''

import os
import time
import traceback

import pandas as pd
import pandas_profiling
import pymongo

from Auto_maching_learning.settings import LOG_DIR
from ModelSelection.models import DatasetModel
from utils.MODEL_DICT import CLEAN_DICT
from utils.logutil import set_log
logger = set_log(os.path.join(LOG_DIR, os.path.split(__file__)[1].split(".")[0]))

template_path = os.path.join(os.path.abspath(''), 'code_templates')


def joint_code(code_path, encoding='utf-8'):
    """拼接代码文件"""
    text = ""
    try:
        try:
            f = open(os.path.join(template_path, code_path), 'r', encoding=encoding)
            text = f.read()
        except Exception as e:
            f = open(os.path.join(template_path, code_path), 'r', encoding='gbk')
            text = f.read()
    except Exception as e:
        logger.exception(e)
    return text


class DatasetProcess:
    def __init__(self, database="AML", collection="user_model", username="admin"):
        self.client = pymongo.MongoClient(host="localhost", port=27017)
        self.mydb = self.client[database]
        self.user_collection = self.mydb[collection]
        self.username = username
        self.user = self.user_collection.find_one({"username": self.username})
        self.isVip = self.user.get('isVip', False)
        self.datasets = [i.get('name') for i in self.user['dataset']]
        self.columns = []
        self.DM = DatasetModel.objects()

    def get_dataset_info(self):
        names = [i.get('name') for i in self.user['dataset']]
        upload_times = [i.get('upload_time') for i in self.user['dataset']]
        return names, upload_times

    def upload(self, file_path, username):
        '''
        :param file_path: 用户上传的文件路径
        :return :是否成功上传的bool值
        '''
        # 文件后缀检查
        postfix = os.path.split(file_path)[-1].split(".")
        filename = postfix[0] + "_" + postfix[1]
        if not self.isVip:
            if len(self.datasets) > 5:
                return False, "非会员最多存储五份数据集"
        if filename in self.datasets:
            return False, "该数据集已存在"
        try:
            if postfix[1] == 'xls' or postfix[1] == 'xlsx':
                df = pd.read_excel(file_path)
            elif postfix[1] == "csv" or postfix[1] == 'txt':
                df = pd.read_csv(file_path, encoding="utf-8")
        except UnicodeDecodeError as e:
            df = pd.read_csv(file_path, encoding="gbk")
        except Exception as e:
            traceback.print_exc()
            return False, str(e)
        # 将dataframe转换为字典形式
        cols = df.columns
        data = {i: df[i].tolist() for i in cols}
        upload_time = time.time()
        try:
            try:
                self.DM.create(
                    username=self.username,
                    dataset_name=filename,
                    columns=cols,
                    data=data
                )
            except:
                self.DM.create(
                    username=self.username,
                    dataset_name=filename,
                    columns=cols,
                    data={}
                )
                self.DM.filter(
                    username=self.username,
                    dataset_name=filename).update(data=data)
            self.user_collection.update_many({'username': self.username},
                                             {"$push": {"dataset": {"name": filename, 'upload_time': upload_time}}})

        except Exception as e:
            return False, str(e)
        return True, "上传成功"

    def get_dataset(self, dataset_name):
        '''
        从数据库取出数据
        :param dataset_name:数据集名称
        :return: 获取数据集转换为字典
        '''
        try:
            model = self.mydb['dataset_model']
            query = dict(dataset_name=dataset_name, username=self.username)
            print(query)
            res = model.find_one(query)
            return res['data']
        except Exception as e:
            print(str(e))
            raise e

    def get_dataset_cols(self, dataset_name):
        '''
        从数据库取出数据集的列名
        :param dataset_name:数据集名称
        :return: 获取数据集转换为字典
        '''
        try:
            model = self.mydb['dataset_model']
            query = dict(dataset_name=dataset_name, username=self.username)
            res = model.find_one(query)
            return res['columns']
        except Exception as e:
            raise e

    def generate_report(self, dataset_name):
        try:
            current_path = os.getcwd()
            parent_path, current_file_name = os.path.split(current_path)
            filename = os.path.join(parent_path, "AML-frontend-master/static/%s_%s.html" % (self.username, dataset_name))

            if not os.path.exists(filename):
                model = self.mydb['dataset_model']
                query = dict(dataset_name=dataset_name, username=self.username)
                res = model.find_one(query)
                df = pd.DataFrame(res["data"])
                report = pandas_profiling.ProfileReport(df)
                report.to_file(filename)
            return os.path.split(filename)[-1]
        except Exception as e:
            raise e


    def generate_clean_code(self, user_name, dataset_name, conditions):
        """
        传入数据集，清洗条件
        :param user_name:
        :param dataset_name:
        :param conditions:
        :return: str : 数据清洗代码
        """
        generate_code = joint_code("main_clean.py") % dataset_name
        try:
            for condition in conditions:
                try:
                    cols = condition.get("columns", [])
                    clean_method = condition.get("clean_method", "")
                    clean_expression = CLEAN_DICT.get(clean_method, "")

                    # 清洗方法为字典，说明含有子方法，从映射表中取出对应表达式后执行语句
                    if clean_expression and isinstance(clean_expression, dict):

                        sub_method = condition.get("sub_method", "")
                        clean_expression = CLEAN_DICT.get(clean_method, {}).get(sub_method)
                        # 如果是筛选，需单独处理
                        if clean_method == "筛选":
                            sub_condition = condition.get("sub_condition","")
                            filter_param = "'%s'"%sub_condition if not sub_condition.isdigit() else sub_condition
                            clean_expression = clean_expression % filter_param

                    generate_code += """\ncols = {}\n{}
                                        """.format(cols, clean_expression)
                except Exception as e:
                    raise Exception(e)
            generate_code += "\ndf.to_csv('clean_'+FILE_PATH+'.csv')"
            timestamp = time.time()
            return generate_code
        except Exception as e:
            raise e

    def delete(self, dataset_name):
        '''
        根据数据集名称删除数据
        :param dataset_name:
        :return:
        '''

        self.user_collection.update({"username": self.username}, {"$pull": {"dataset": {"name": dataset_name}}})
        self.DM.filter(username=self.username, dataset_name=dataset_name).delete()
        return True


if __name__ == "__main__":
    pass
