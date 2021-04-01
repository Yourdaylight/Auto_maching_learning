from django.db import models

# Create your models here.
import mongoengine

class DatasetModel(mongoengine.Document):
    username = mongoengine.StringField(max_length=16)
    dataset_name=mongoengine.StringField()
    columns=mongoengine.ListField()
    data=mongoengine.DictField()


