import json
import os

from bson import json_util

"""
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
"""
from utils.MODEL_DICT import MODEL_DICT
from ModelSelection.dataset_process_model import joint_code
from utils.mongodb_util import MongoUtil


class SetModel:
    """

    用于与前端界面交互，获取特征列，以及数据处理步骤。
    根据用户选择的步骤，读取预定义的代码。
    前端返回参数
    {
        target:[],
        features:[],

    }
    """

    def __init__(self, **params):
        """

        :param name(str,):任务名称
        :param dataset_name(str,):数据集名称
        :param features(str of list):特征列
        :param target(str):目标
        :param model_type(str):分类/回归/聚类
        :param model_name(str of list):模型
        :param evaluate_methods(str of list,非必填):模型评估方法
        :param username(str)
        :param model_scene(str):模型使用场景
        """
        self.name = params.get("name", "")
        self.dataset_name = params.get("dataset_name", "")
        self.target = params.get("target", "")
        self.features = params.get("features", [])
        self.model_type = params.get("model_type", "")
        self.model_name = params.get("model_name", [])
        self.evaluate_methods = params.get("evaluate_methods", [])
        self.username = params.get("username", "")
        self.model_scene = params.get("model_scene", "")
        self.generate = ''
        self.clean_code = ''

    def get_code(self):
        """
        根据模板，生成代码
        :return:
        """
        try:
            # 拼接模型需要的库
            for model in self.model_name:
                self.generate += MODEL_DICT[self.model_type][model] + "\n"
            # 拼接导入的库,并填充读取的文件名
            self.generate += joint_code('ImportPackages.py') % self.dataset_name.replace('_', '.')
            # 拼接变量
            self.generate += "\nFEATURES={}\nTARGET='{}'".format(self.features, self.target)
            # 拼接调用的模型
            sklearn_models = [MODEL_DICT[self.model_type].get(model, " ").split(' ')[-1] + '()' for model in self.model_name]
            self.generate += "\nMODEL = [{}]".format(", ".join(sklearn_models))

            # 拼接分类/回归/聚类的主函数与必要评估方法
            if self.model_type == "分类":
                self.generate += joint_code('main_supervisied.py')
                self.generate += joint_code("evaluation_classifier.py")
            elif self.model_type == "回归":
                self.generate += joint_code('main_supervisied.py')
                self.generate += joint_code("evaluation_regressor.py")
            elif self.model_type == "聚类":
                self.generate += joint_code("main_unsupervised.py")
                self.generate += joint_code("evaluation_cluster.py")

            # 拼接用户自选的可视化的评估方法
            if len(self.evaluate_methods) != 0:
                for method in self.evaluate_methods:
                    location = MODEL_DICT.get(method)
                    if location:
                        self.generate += joint_code(location)

            # 生成代码文件
            filename = "generate_{}_{}.py".format(self.username, self.name)
            filepath = os.path.join(os.path.abspath(''), 'temp', filename)
            print("存放路径:", filepath)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.generate)
        except Exception as e:
            self.generate = str(e)
        # 返回生成代码的文本
        return self.generate

    def save_params(self, hide_history=True):
        """
        保存当前参数(如果不重复的话)到数据库。
        hide_history:bool:是否向用户展示该条历史记录，
                            hide_history默认为True，当用户运行成功当前代码时自动保存，
                            该条历史记录保存在admin用户中，该记录用于后续推荐。
                            当用户在界面上选择保存当前参数时，hide_history为False，正常保存
        :return:
        """
        try:
            params = self.__dict__
            db_util = MongoUtil()
            del params["generate"], params["clean_code"]
            check_duplicate_query = {
                "username": self.username if not hide_history else "admin",
                "name": self.name
            }
            exists = db_util.find_object("history_model", check_duplicate_query)
            # 不存在这条记录且正常登陆，将这条记录加入历史记录集合
            if not exists and self.username:
                db_util.insert_object("history_model", params)
            # 存在则更新记录
            elif exists and self.username:
                db_util.update_object("history_model", check_duplicate_query, params)
            return True
        except Exception as e:
            raise e

    def get_history(self):
        """
        获取用户的所有历史记录,将所有列表项转换成,分割
        :return:
        """
        try:
            db_util = MongoUtil()
            search_query = {
                "username": self.username,
            }
            history_list = db_util.find_object("history_model", search_query)
            history_list = json.loads(json_util.dumps(history_list))
            for index, history in enumerate(history_list):
                for k, v in history.items():
                    if v is None:
                        history_list[index][k] = ""
                    if isinstance(v, list):
                        history_list[index][k] = ",".join(v)
            return history_list
        except Exception as e:
            raise e

    def delte_history(self):
        """
        删除历史记录
        :param object:dict 删除对象的查询条件
        :return:
        """
        try:
            db_util = MongoUtil()
            db_util.delete_object("history_model", {
                "username": self.username,
                "name": self.name
            })
            return True
        except Exception as e:
            raise e


if __name__ == '__main__':
    myModel = SetModel(username="lzh3")
    ll = myModel.get_history()
    print(ll)
    print("======================")
    for i in ll:
        print(i)
