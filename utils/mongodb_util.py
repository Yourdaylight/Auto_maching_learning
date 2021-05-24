import time

from pymongo import MongoClient


class MongoUtil:
    def __init__(self, database="AML"):
        self.client = MongoClient(host="localhost", port=27017)
        self.mydb = self.client[database]

    def find_dataset(self, user_name, dataset_name):
        try:
            collection = self.mydb["dataset_model"]
            dataset = collection.find_one({"username": user_name, "dataset_name": dataset_name})
            return dataset.get("data", {})
        except Exception as e:
            raise e

    def insert_object(self, database_name, object):
        """
        插入新的对象到数据库
        :param user_name:
        :param database_name:
        :param object:dict:
        :return:
        """
        try:
            self.mydb[database_name].insert_one(object)
        except Exception as e:
            raise e

    def update_object(self, database_name, filter_object, update_object):
        """

        :param database_name:
        :param filter_object: 过滤条件
        :param update_object: 更新内容
        :return:
        """
        try:
            return self.mydb[database_name].update_one(
                filter_object, {"$set": update_object}
            )
        except Exception as e:
            raise e

    def find_object(self, database_name, object):
        """
        自定义查询
        :param database_name:
        :param object: dict:查询条件
        :return:
        """
        try:
            return list(self.mydb[database_name].find(object))
        except Exception as e:
            raise e

    def delete_object(self, database_name, object):
        """
        删除
        :param database_name:
        :param object:
        :return:
        """
        try:
            res = self.mydb[database_name].delete_one(object)
            print (res)
            return res
        except Exception as e:
            raise e

    def upload_dataset(self, user_name, dataset_name, new_data):
        """
        上传数据集
        :param user_name:
        :param dataset_name:
        :param new_data: DataFrame
        :return:
        """
        upload_time = time.time()
        columns = list(new_data.columns)
        data = new_data.to_dict(orient="list")
        # 插入到数据集集合
        self.mydb["dataset_model"].insert_one({
            "username": user_name,
            "dataset_name": dataset_name,
            "columns": columns,
            "data": data
        })
        # 更新用户集合
        self.mydb["user_model"].update_many({"username": user_name},
                                            {"$push": {"dataset": {"name": dataset_name, 'upload_time': upload_time}}})


if __name__ == '__main__':
    # import pandas as pd
    #
    # a = MongoUtil()
    # data = a.find_dataset("lzh3", "day_csv")
    # df = pd.DataFrame(data)
    # df.to_csv("../temp/clean.day.csv", index=None)
    pass
