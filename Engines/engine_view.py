import json
import os

import pandas as pd
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from Auto_maching_learning.settings import LOG_DIR
from ModelSelection.model_process_model import SetModel
from utils.logutil import set_log
from .engine_model import DataCleaningEngine, DataMiningEngine

logger = set_log(os.path.join(LOG_DIR, os.path.split(__file__)[1].split(".")[0]))

clean_engine = DataCleaningEngine()
mining_engine = DataMiningEngine()


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
        msg, code = str(e), 500
        logger.exception(e)
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
        msg, code = str(e), 500
        logger.exception(e)
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
        msg, code = str(e), 500
        logger.exception(e)
    return JsonResponse({"code": code, "msg": msg, "data": data})


@require_http_methods(['POST'])
def run_mining_code(request):
    data, code, msg = None, 200, None
    try:
        post_body = json.loads(request.body)
        user_name = post_body.pop("username", "")
        conditions = post_body.pop("data", {})
        data = mining_engine.run_code(user_name, conditions)
        # 引擎运行代码成功，保存运行成功的该条记录到admin账户
        conditions['username'] = 'admin'
        if not SetModel(**conditions).save_params():
            logger.error("保存至admin账户失败")
    except Exception as e:
        msg, code = str(e), 500
        logger.exception(e)
    return JsonResponse({"code": code, "msg": msg, "data": data})
