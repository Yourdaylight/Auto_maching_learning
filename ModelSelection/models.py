# Create your models here.
import mongoengine


class DatasetModel(mongoengine.Document):
    username = mongoengine.StringField(max_length=16)
    dataset_name = mongoengine.StringField()
    columns = mongoengine.ListField()
    data = mongoengine.DictField()


class HistoryModel(mongoengine.Document):
    name = mongoengine.StringField()  # 构建的任务名称
    username = mongoengine.StringField(max_length=16)
    dataset_name = mongoengine.StringField()  # 数据集名称
    target = mongoengine.StringField()  # 目标列
    features = mongoengine.ListField()  # 特征列
    model_type = mongoengine.StringField()  # 选择的模型类型
    model_name = mongoengine.ListField()  # 选择的具体机器学习模型
    evaluate_methods = mongoengine.ListField()  # 模型评价方法
