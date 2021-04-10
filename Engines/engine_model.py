import pandas as pd

from utils.MODEL_DICT import CLEAN_DICT
from utils.mongodb_util import MongoUtil


class DataCleaningEngine:
    def __init__(self):
        self.db = MongoUtil()

    def check_clean_condition(self, user_name, dataset_name, conditions):
        """
        传入数据集，清洗条件
        :param user_name:
        :param dataset_name:
        :param conditions:
        :return: dataframe 清洗完成后的数据
        """
        try:

            dataset = self.db.find_dataset(user_name, dataset_name)
            df = pd.DataFrame(dataset) if dataset else {}
            if isinstance(df, pd.core.frame.DataFrame):
                for condition in conditions:
                    # cols用于后续的表达式执行
                    try:
                        cols = condition.get("columns", [])
                        clean_method = condition.get("clean_method", "")
                        clean_expression = CLEAN_DICT.get(clean_method, "")

                        # 清洗方法为字符串，说明并没有子方法，可直接执行该方法
                        if clean_expression and isinstance(clean_expression, str):
                            exec(clean_expression)

                        # 清洗方法为字典，说明含有子方法，从映射表中取出对应表达式后执行语句
                        elif clean_expression and isinstance(clean_expression, dict):
                            sub_method = condition.get("sub_method", "")
                            clean_expression = CLEAN_DICT.get(clean_method, {}).get(sub_method)
                            exec(clean_expression)
                    except Exception as e:
                        message = "对{}列进行{}失败！失败原因:{}".format(",".join(cols), clean_method, str(e))
                        raise Exception(message)
            return df
        except Exception as e:
            raise e

    def save_clean_data(self, user_name, dataset_name, new_data):
        """
        将清洗完成的数据集入库
        :param user_name:
        :param dataset_name: 原始数据集名称
        :param new_data: DataFrame
        :return:
        """
        try:
            new_name = "clean_{}".format(dataset_name)
            self.db.upload_dataset(user_name, new_name, new_data)
            return True
        except Exception as e:
            raise e


class DataMiningEngine:
    def __init__(self):
        pass
