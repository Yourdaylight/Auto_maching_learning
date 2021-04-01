from utils.mongodb_util import MongoUtil


class DataCleaningEngine:
    def __init__(self,conditions):
        self.conditions = conditions
        self.db = MongoUtil()

    # todo 数据清洗规则校验校验
    def check_clean_condition(self, conditions):
        dataset = self.db.find_dataset()


class DataMiningEngine:
    def __init__(self):
        pass
