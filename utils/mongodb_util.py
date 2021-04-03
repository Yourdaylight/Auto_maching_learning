import time
from pymongo import MongoClient


class MongoUtil:
    def __init__(self, database="AML"):
        self.client = MongoClient(host="localhost", port=27017)
        self.mydb = self.client[database]

    def find_dataset(self, user_name, dataset_name):
        collection = self.mydb["dataset_model"]
        dataset = collection.find_one({"username": user_name, "dataset_name": dataset_name})
        return dataset.get("data", {})

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
            "username":user_name,
            "dataset_name":dataset_name,
            "columns":columns,
            "data":data
        })
        # 更新用户集合
        self.mydb["user_model"].update_many({"username":user_name},
                                            {"$push": {"dataset": {"name": dataset_name, 'upload_time': upload_time}}})



if __name__ == '__main__':
    # a = MongoUtil()
    # print(a.find_dataset("lzh3","day_csv"))
    pass
