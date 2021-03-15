'''
邮箱验证模块
'''

import smtplib
import pymongo
from email.mime.text import MIMEText
from email.header import Header
import random
import time
from temp import EmailTemp

# 用于构建邮件头

# 发信方的信息：发信邮箱，QQ 邮箱授权码
password = ''
# 收信方邮箱
to_addr = '526494747@qq.com'
class EmailService():
    def __init__(self):
        self.client = pymongo.MongoClient(host="localhost", port=27017)
        self.mydb = self.client["AML"]
        self.temp_collection = self.mydb["temp"]
        self.valid_time=60*5
    def send_email(self, to_addr,password='htvviggqfrwobbfc'):
        '''
        :param password: Email authorization code
        :param to_addr: recevier email address
        :return:{
            to_addr:收件人邮箱地址
            time:发送成功后的时间戳
        }
        '''
        from_addr = 'yikechengxushu@qq.com'
        smtp_server = 'smtp.qq.com'
        # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
        validate_num=random.randint(100000,999999)
        msg = MIMEText("你的验证码(注意，验证码仅{}分钟内有效)：{}".format(int(self.valid_time/60),validate_num), 'plain', 'utf-8')
        # 邮件头信息
        msg['From'] = Header(from_addr)
        msg['To'] = Header(to_addr)
        msg['Subject'] = Header('随机验证码')

        # 开启发信服务，这里使用的是加密传输
        server = smtplib.SMTP_SSL()
        server.connect(smtp_server, 465)
        # 登录发信邮箱
        server.login(from_addr, password)
        # 发送邮件
        server.sendmail(from_addr, to_addr, msg.as_string())
        # 关闭服务器
        server.quit()
        send_info={
            'address':to_addr,
            'check_code': validate_num,
            'send_time': time.time()
        }
        self.temp_collection.delete_many({"address":to_addr})
        self.temp_collection.insert_one(send_info)
        return send_info

    def check_input(self,text,address):
        '''
        输入验证码校验
        :param text:
        :param address:
        :return:
        '''
        query={"address":address}
        print("用户输入信息:",text,type(text))

        regist_info=self.temp_collection.find_one(query)
        print(regist_info)
        if regist_info:
            send_time=regist_info.get('send_time')
            if time.time()-send_time>self.valid_time:
                self.temp_collection.delete_one(query)
                return False
            if text==str(regist_info.get("check_code")):
                self.temp_collection.delete_one(query)
                print(address+'注册成功')
                return True
        return False

if __name__ == '__main__':
    pass
    # start=time.time()
    # em=EmailService()
    # mail="526494747@qq.com"
    # # em.send_email(mail)
    # a=em.check_input('156882',mail)
    # end=time.time()
    # print("发送校验耗时:",start-end)
    # print(a)

