import json
import os
import traceback
import pandas as pd
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from utils.dataset_process import DatasetProcess
from utils.model_choose import SetModel
from utils.user_operate import UserProcess, Regist, sendCode

# Create your views here.

UP = UserProcess()


def get_datesets_list(request):
    return render(request, "../templates/dist/index.html")


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
    except:
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
    except:
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
        data['code'] = 500
        data['msg'] = str(e)
    return JsonResponse(data, status=data['code'])


@require_http_methods(['POST'])
def send_code(request):
    postBody = json.loads(request.body)
    email = postBody.get("email")
    flag = sendCode(email)
    return JsonResponse({"msg": flag}, status=200)


@require_http_methods(['POST'])
def upload_dataset(request):
    '''
    上传数据集到mongodb
    '''

    username = request.POST.get("username").replace('"', '')
    print("upload username:" + username)
    dp = DatasetProcess(username=username)
    data = {
        "msg": None,
        "code": None,
        "data": None
    }
    try:
        upload_file = request.FILES.getlist('file')
        for f in upload_file:
            save_path = os.path.join("temp", f.name)
            with open(save_path, "wb") as des:
                for chunk in f.chunks():
                    des.write(chunk)
            res = dp.upload(save_path, username)
            if res[0]:
                data['msg'] = res[1]
                data['code'] = 200
                # 删除临时文件
                os.remove(save_path)
            else:
                data['msg'] = res[1]
                os.remove(save_path)
                raise Exception("上传失败")
    except Exception as e:
        data['code'] = 500
        traceback.print_exc()
    return JsonResponse(data, safe=False, status=data['code'])


@require_http_methods(['GET'])
def get_data_list(request):
    '''
    获取用户上传的所有数据集名称
    '''
    data = {
        "msg": None,
        "code": None,
        "data": {}
    }
    username = request.GET.get('username').replace('"', '')
    dp = DatasetProcess(username=username)
    try:

        names, upload_times = dp.get_dataset_info()
        data['data']['name'] = names
        data['data']['upload_time'] = upload_times
    except Exception as e:
        traceback.print_exc()
        data['msg'] = str(e)
        data['code'] = 500
    return JsonResponse(data, status=data['code'], safe=False)


@require_http_methods(['GET'])
def show_dataset(request):
    '''
    根据用户选择的数据集，展示所有数据
    '''
    data = {
        "msg": None,
        "code": None,
        "data": None
    }

    username = request.GET.get('username').replace('"', '')
    dp = DatasetProcess(username=username)
    try:
        dataset_name = request.GET.get("dataset_name")
        data_dict = dp.get_dataset(dataset_name)
        # 将上述字典转Dataframe将缺失值填充为 "" 否则前端无法展示
        data_dict = pd.DataFrame(data_dict).fillna("").to_dict(orient='list')
        if data_dict is None:
            raise Exception("数据加载失败")
        data['data'] = data_dict
        data['data']['cols'] = list(data_dict.keys())
        data['code'] = 200
        data['msg'] = "Success"
    except Exception as e:
        data['code'] = 500
        data['msg'] = str(e)
        traceback.print_exc()
    return JsonResponse(data, status=data['code'], json_dumps_params={'ensure_ascii': False})


@require_http_methods(['GET'])
def show_dataset_report(request):
    data = {
        "msg": None,
        "code": None,
        "data": ""
    }
    username = request.GET.get('username').replace('"', '')
    dataset_name = request.GET.get('dataset_name').replace('"', '')
    dp = DatasetProcess(username=username)
    try:
        html_name = dp.generate_report(dataset_name)
        data["data"] = html_name
        data["code"] = 200
    except Exception as e:
        traceback.print_exc()
        data['msg'] = str(e)
        data['code'] = 500
    return JsonResponse(data, status=data['code'], safe=False)


@require_http_methods(['POST'])
def del_dataset(request):
    data = {
        "msg": None,
        "code": None
    }

    try:
        postBody = json.loads(request.body)
        username = postBody.get('username').replace('"', '')
        dp = DatasetProcess(username=username)
        dataset_name = postBody.get("dataset_name", None).replace('"', '')
        if dataset_name and dp.delete(dataset_name):
            data['code'] = 200
            data['msg'] = dataset_name + "  删除成功  ！"
        else:
            raise Exception("删除失败")

    except Exception as e:
        traceback.print_exc()
        data['msg'] = str(e)
        data['code'] = 500
    return JsonResponse(data, status=data['code'])


@require_http_methods(['POST'])
def generate_code(request):
    data = {
        "msg": None,
        "code": None
    }
    try:
        postBody = json.loads(request.body)
        username = postBody.pop('username')
        postBody = postBody.get('data')
        name = postBody.get('name')
        dataset_name = postBody.get('dataset_name')
        features = postBody.get('features')
        target = postBody.get('target')
        model_type = postBody.get('model_type')
        model_name = postBody.get('models')
        evaluate_methods = postBody.get("metrics")
        myModel = SetModel(name, dataset_name, features, target, model_type, model_name, username, evaluate_methods, )

        codes = myModel.get_code()
        if codes:
            data['data'] = codes
            data['msg'] = "上传成功"
            data['code'] = 200
        return JsonResponse(data, status=data['code'])
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'msg': str(e)})


@require_http_methods(['GET'])
def export_code(request):
    '''
    根据用户选择的数据集，展示所有数据
    '''
    data = {
        "msg": None,
        "code": None,
        "data": None
    }
    try:
        username = request.GET.get('username')
        name = request.GET.get('name')
        filename = "generate_{}_{}.py".format(username, name)
        filepath = os.path.join(os.path.abspath(''), 'temp', filename)
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                response = HttpResponse(f)
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = 'attachment;filename=' + filename
                # response['Set-Cookie'] = "fileDownload=true; path=/"  # 前端如果使用了插件就需要加上这一行
                return response
        else:
            raise Exception('文件不存在')
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(str(e))
