import json
import os

import pandas as pd
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from Auto_maching_learning.settings import LOG_DIR
from ModelSelection.dataset_process_model import DatasetProcess
from ModelSelection.model_process_model import SetModel
from utils.MODEL_DICT import CLEAN_DICT, MODEL_DICT, METRICS_DICT
from utils.logutil import set_log

logger = set_log(os.path.join(LOG_DIR, os.path.split(__file__)[1].split(".")[0]))


# Create your views here.

def get_datesets_list(request):
    return render(request, "../templates/dist/index.html")


@require_http_methods(['POST'])
def upload_dataset(request):
    '''
    上传数据集到mongodb
    '''

    username = request.POST.get("username").replace('"', '')
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
        logger.exception(e)
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
        data['msg'] = str(e)
        data['code'] = 500
        logger.exception(e)
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
        data_dict = pd.DataFrame(data_dict).fillna("")
        # 由于ui框架的原因，0无法加载，需要转换成字符串
        data_dict = data_dict.replace(0, "0").to_dict(orient='list')
        if data_dict is None:
            raise Exception("数据加载失败")
        data['data'] = data_dict
        data['data']['cols'] = list(data_dict.keys())
        data['code'] = 200
        data['msg'] = "Success"
    except Exception as e:
        data['code'] = 500
        data['msg'] = str(e)
        logger.exception(e)
    return JsonResponse(data, status=data['code'], json_dumps_params={'ensure_ascii': False})


@require_http_methods(['GET'])
def get_dataset_cols(request):
    '''
       根据用户选择的数据集，返回数据集的所有列
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
        dataset_cols = dp.get_dataset_cols(dataset_name)
        # 将上述字典转Dataframe将缺失值填充为 "" 否则前端无法展示
        data['data'] = dataset_cols
        data['code'] = 200
        data['msg'] = "Success"
    except Exception as e:
        data['code'] = 500
        data['msg'] = str(e)
        logger.exception(e)
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
        data['msg'] = str(e)
        data['code'] = 500
        logger.exception(e)
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
        logger.exception(e)
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
        logger.exception(e)
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
        logger.exception(e)
        return HttpResponse(str(e))


@require_http_methods(['GET'])
def get_methods(request):
    """
    获取预定义的数据清洗/数据建模/模型评估方法
    :param request:
    :return:
    """
    res = {}
    types = {
        "ml": MODEL_DICT,
        "clean": CLEAN_DICT,
        "metrics": METRICS_DICT
    }
    code_dict = types.get(request.GET.get("type"), {})
    for method, sub_method in code_dict.items():
        if isinstance(sub_method, dict):
            res[method] = list(sub_method.keys())
        else:
            res[method] = sub_method
    return JsonResponse({"data": res}, status=200)


@require_http_methods(['POST'])
def generate_clean_code(request):
    data, code, msg = None, 200, None
    try:
        post_body = json.loads(request.body)
        dataset_name = post_body.pop("dataset", "")
        user_name = post_body.pop("user_name", "")
        conditions = post_body.pop("conditions", {})
        dp = DatasetProcess(username=user_name)
        data = dp.generate_clean_code(user_name, dataset_name, conditions)
        msg = "生成成功！"
    except Exception as e:
        msg = str(e)
        code = 500
        logger.exception(e)

    return JsonResponse({"data": data, "msg": msg, "code": code})


@require_http_methods(['POST'])
def plot_graph(request):
    pass
