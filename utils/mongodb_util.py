from pymongo import MongoClient


class MongoUtil:
    def __init__(self, database="AML"):
        self.client = MongoClient(host="localhost", port=27017)
        self.mydb = self.client[database]

    def find_dataset(self, user_name,dataset_name):
        collection = self.mydb["dataset_model"]
        dataset = collection.find_one({"username": user_name, "dataset_name": dataset_name})
        return dataset.get("data",{})


if __name__ == '__main__':
    # a = MongoUtil()
    # print(a.find_dataset("lzh3","day_csv"))
    pass
