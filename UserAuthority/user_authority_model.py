import traceback

import pymongo

from utils.EmailClient import EmailService
from .models import UserModel

em = EmailService()


class UserProcess():
    def __init__(self, database="AML", collection="user_model"):
        self.client = pymongo.MongoClient(host="localhost", port=27017)
        self.mydb = self.client[database]
        self.user_collection = self.mydb[collection]

    def check_exist(self, query_dict):
        exist = self.user_collection.find_one(query_dict)
        if exist:
            return True
        return False

    def login(self, username, password):
        exist = self.user_collection.find_one({
            "username": username,
            "password": password
        })
        if exist is not None:
            return True
        else:
            return False

    def check_code(self):
        pass


def Regist(infos, **params):
    '''
    注册信息
    :param infos:dict
    :return:
    '''
    try:
        code = params.get("check_code")
        email = infos.get("email")
        if em.check_input(code, email):
            UserModel.objects().create(**infos)
            return True
        return False
    except:
        traceback.print_exc()
        return False


def sendCode(email):
    send = em.send_email(email)
    if send:
        print("发送成功:", send)
        return True
    return False


if __name__ == '__main__':
    up = UserProcess()
    a = up.check_exist({"username": "admin", "password": "admin"})
    # if sendCode("526494747@qq.com"):
    pass
