# import os
# from alipay import AliPay
#
#
# class Pay(object):
#     def __init__(self, appid=None, app_notify_url=None, app_private_key_string=None, alipay_public_key_string=None,
#                  debug=None, sign_type=None):
#         self.appid = appid
#         self.app_notify_url = app_notify_url  # 设置回调地址
#         self.app_private_key_string = app_private_key_string
#         self.alipay_public_key_string = alipay_public_key_string
#         self.debug = debug
#         self.sign_type = sign_type
#
#     def ini(self):
#         '''初始化'''
#         alipay = AliPay(
#             appid=self.appid,
#             app_notify_url=self.app_notify_url,  # 默认回调url
#             app_private_key_string=self.app_private_key_string,
#             alipay_public_key_string=self.alipay_public_key_string,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
#             sign_type=self.sign_type,  # RSA 或者 RSA2
#             debug=self.debug,  # 默认False
#         )
#         return alipay
#
#     def app_pay(self, out_trade_no, total_amount, subject, notify_url):
#         '''app 支付'''
#         order_string = self.ini().api_alipay_trade_app_pay(
#             out_trade_no=out_trade_no,
#             total_amount=total_amount,
#             subject=subject,
#             notify_url=notify_url  # 可选, 不填则使用默认notify url
#         )
#         return order_string
#
#     def wap_pay(self, out_trade_no, total_amount, subject, return_url, notify_url):
#         '''手机网站支付'''
#         # 手机网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
#         order_string = self.ini().api_alipay_trade_wap_pay(
#             out_trade_no=out_trade_no,
#             total_amount=total_amount,
#             subject=subject,
#             return_url=return_url,
#             notify_url=notify_url  # 可选, 不填则使用默认notify url
#         )
#         return order_string
#
#     def page_pay(self, out_trade_no, total_amount, subject, return_url, notify_url):
#         '''pc 支付'''
#         order_string = self.ini().api_alipay_trade_page_pay(
#             out_trade_no=out_trade_no,
#             total_amount=total_amount,
#             subject=subject,
#             return_url=return_url,
#             notify_url=notify_url  # 可选, 不填则使用默认notify url
#         )
#         return order_string
#
#
# if __name__ == '__main__':
#     pay = Pay(
#         appid="",  # 设置签约的appid
#         app_notify_url=None,  # 异步支付通知url
#         app_private_key_string=open(
#             os.path.join(settings.BASE_DIR, 'apps/order/testkey/alipay_private_key.pem')).read(),  # 设置应用私钥
#         alipay_public_key_string=open(
#             os.path.join(settings.BASE_DIR, 'apps/order/testkey/alipay_public_key.pem')).read(),
#         # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
#         sign_type="RSA2",
#         debug=True,  # 默认False 设置是否是沙箱环境，True是沙箱环境
#     )
#
#     url = pay.wap_pay(
#         subject="xmzl",  # # 订单名称
#         out_trade_no="201702021222",  # 订单号
#         total_amount=100,  # 支付金额
#         notify_url=None,
#         return_url=None
#     )
#
#     re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
#     print(re_url)