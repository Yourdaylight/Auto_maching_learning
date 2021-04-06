import json
import traceback

import pandas as pd
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .engine_model import DataCleaningEngine

clean_engine = DataCleaningEngine()


@require_http_methods(['POST'])
def check_clean_condition(request):
    """
    清洗条件校验, 校验失败时返回失败的清洗配置
    :param request:
    :return:
    """
    data, code, msg = None, 200, None
    try:
        post_body = json.loads(request.body)
        dataset_name = post_body.pop("dataset", "")
        user_name = post_body.pop("user_name", "")
        conditions = post_body.pop("conditions", {})
        clean_engine.check_clean_condition(user_name, dataset_name, conditions)
        msg = "校验通过！"
    except Exception as e:
        msg = str(e)
        code = 500
        traceback.print_exc()

    return JsonResponse({"code": code, "msg": msg, "data": data})


@require_http_methods(['POST'])
def save_clean_data(request):
    """
    保存清洗完的数据到数据集管理
    :param request:
    :return:
    """
    data, code, msg = None, 200, None
    try:
        post_body = json.loads(request.body)
        dataset_name = post_body.pop("dataset", "")
        user_name = post_body.pop("user_name", "")
        conditions = post_body.pop("conditions", {})
        new_data = clean_engine.check_clean_condition(user_name, dataset_name, conditions)
        if isinstance(new_data, pd.core.frame.DataFrame):
            res = clean_engine.save_clean_data(user_name, dataset_name, new_data)
            if res:
                msg = "保存成功"
    except Exception as e:
        msg = str(e)
        code = 500
        traceback.print_exc()

    return JsonResponse({"code": code, "msg": msg, "data": data})


@require_http_methods(['POST'])
def check_mining_condition(request):
    """
    检测建模条件， 对特征列类型的合理性进行校验
    :param request:
    :return:
    """
    data, code, msg = None, 200, None
    try:
        post_body = json.loads(request.body)
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
    except Exception as e:
        msg = str(e)
        coce = 500

    return JsonResponse({"code": code, "msg": msg, "data": data})


@require_http_methods(['POST'])
def run_mining_code(request):
    data, code, msg = None, 200, None
    try:
        post_body = json.loads(request.body)
        dataset_name = post_body.pop("dataset", "")
        user_name = post_body.pop("user_name", "")
        conditions = post_body.pop("conditions", {})
    except Exception as e:
        msg, code = str(e), 500
    return JsonResponse({"code": code, "msg": msg, "data": data})
