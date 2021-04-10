import json
import os

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from Auto_maching_learning.settings import LOG_DIR
# Create your views here.
from UserAuthority.user_authority_model import UserProcess, Regist, sendCode
from utils.logutil import set_log

logger = set_log(os.path.join(LOG_DIR, os.path.split(__file__)[1].split(".")[0]))
UP = UserProcess()


@require_http_methods(['POST'])
def login(request):
    '''
    用户登录
    :param request:
    :return:
    '''
    try:
        postBody = json.loads(request.body)
        username = postBody.get("username")
        password = postBody.get("password")
        res = UP.login(username, password)
        return JsonResponse({"msg": res})
    except Exception as e:
        logger.exception(e)
        return JsonResponse({'msg': res})


@require_http_methods(['POST'])
def check_exist(request):
    '''
    查询注册信息中的用户名/邮箱号是否存在
    :param request:
    :return:
    '''
    try:
        postBody = json.loads(request.body)
        query_dict = postBody.get("query_dict")
        res = UP.check_exist(query_dict)
        return JsonResponse({"msg": res})
    except Exception as e:
        logger.exception(e)
        return JsonResponse({'msg': res})


@require_http_methods(['POST'])
def regist(request):
    data = {
        "msg": None,
        "code": None,
    }
    try:
        postBody = json.loads(request.body)
        username = postBody.get('username')
        password = postBody.get('password')
        email = postBody.get("email")
        phone = postBody.get("phone")
        isVip = postBody.get("isVip", False)
        checkcode = postBody.get("checkcode")
        infos = dict(
            username=username,
            password=password,
            phone=phone,
            email=email,
            isVip=isVip,
            dataset=[]
        )
        if Regist(infos, check_code=checkcode):
            data['code'] = 200
            data['msg'] = '注册成功'
        else:
            raise Exception("验证码错误，注册失败")
    except Exception as e:
        logger.exception(e)
        data['code'] = 500
        data['msg'] = str(e)
    return JsonResponse(data, status=data['code'])


@require_http_methods(['POST'])
def send_code(request):
    '''
    注册发送验证码
    '''
    postBody = json.loads(request.body)
    email = postBody.get("email")
    flag = sendCode(email)
    return JsonResponse({"msg": flag}, status=200)
