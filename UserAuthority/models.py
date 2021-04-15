import mongoengine


# Create your models here.
class UserModel(mongoengine.Document):
    username = mongoengine.StringField(max_length=16)
    password = mongoengine.StringField(max_length=16)
    phone = mongoengine.StringField(max_length=16)
    email = mongoengine.StringField(max_length=32)
    isVip = mongoengine.BooleanField(default=False)  # 会员权限
    dataset = mongoengine.ListField()
