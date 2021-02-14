from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.views.decorators.http import require_http_methods
from utils.dataset_process import  DatasetProcess
import os
import traceback
import json
# Create your views here.


def get_datesets_list(request):
    return render(request, "../templates/dist/index.html")

@require_http_methods(['POST'])
def upload_dataset(request):
    '''
    上传数据集到mongodb
    '''

    username='admin'
    dp=DatasetProcess(username=username)
    data={
        "msg":None,
        "code":None,
        "data":None
    }
    try:
        upload_file=request.FILES.getlist('file')
        for f in upload_file:
            save_path = os.path.join("temp", f.name)
            with open(save_path,"wb") as des:
                for chunk in f.chunks():
                    des.write(chunk)
            res=dp.upload(save_path,username)
            if res[0]:
                data['msg']=res[1]
                data['code']=200
                #删除临时文件
                os.remove(save_path)
            else:
                data['msg']=res[1]
                os.remove(save_path)
                raise Exception("上传失败")
    except Exception as e:
        data['code']=500
        traceback.print_exc()
    return JsonResponse(data,safe=False,status=data['code'])
@require_http_methods(['GET'])
def get_data_list(request):
    '''
    获取用户上传的所有数据集名称
    '''
    data={
            "msg":None,
            "code":None,
            "data":None
        }
    username='admin'
    dp=DatasetProcess(username=username)
    try:
        lists=[list(i.keys())[0] for i in dp.user['dataset']]
        data['data']=lists
    except Exception as e:
        data['msg']=str(e)
        data['code']=500
    return JsonResponse(data,status=data['code'], safe=False)

@require_http_methods(['GET'])
def show_dataset(request):
    '''
    根据用户选择的数据集，展示所有数据
    '''
    data={
            "msg":None,
            "code":None,
            "data":None
        }
    username="admin"
    dp = DatasetProcess(username=username)
    try:
        dataset_name=request.GET.get("dataset_name")
        data_dict=dp.get_dataset(dataset_name)
        if data_dict is None:
            raise Exception("数据加载失败")
        data['data']=data_dict
        data['data']['cols']=list(data_dict.keys())
        data['code']=200
        data['msg']="Success"
    except Exception as e:
        data['code']=500
        data['msg']=str(e)
        traceback.print_exc()
    return JsonResponse(data,status=data['code'])

@require_http_methods(['POST'])
def del_dataset(request):
    data={
        "msg":None,
        "code":None
    }
    username = "admin"
    dp = DatasetProcess(username=username)
    try:
        concat = request.POST
        postBody = json.loads(request.body)
        dataset_name=postBody.get("dataset_name",None)
        if dataset_name and dp.delete(dataset_name):
            data['code']=200
            data['msg']=dataset_name + "  删除成功  ！"
        else:
            raise Exception("删除失败")

    except Exception as e:
        traceback.print_exc()
        data['msg']=str(e)
        data['code']=500
    return JsonResponse(data,status=data['code'])


@require_http_methods(['GET'])
def model_params(request):
    pass
