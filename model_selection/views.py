from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.views.decorators.http import require_http_methods
from utils.dataset_process import  dataset_process
import os
import traceback
# Create your views here.
dp = dataset_process()

def get_datesets_list(request):
    return render(request, "../templates/dist/index.html")

@require_http_methods(['POST'])
def upload_dataset(request):
    '''
    上传数据集到mongodb
    '''
    username='admin'
    data={
        "msg":None,
        "code":None
    }
    try:
        upload_file=request.FILES.getlist('file')
        for f in upload_file:
            save_path = os.path.join("temp", f.name)
            with open(save_path,"wb") as des:
                for chunk in f.chunks():
                    des.write(chunk)

            if dp.upload(save_path,username):
                msg = "上传成功"
                data['msg']=msg
                data['code']=200
            else:
                raise Exception("上传失败")
    except Exception as e:
        data['msg']="上传失败"
        data['code']=500
        traceback.print_exc()
    return JsonResponse(data,safe=False,status=data['code'])
@require_http_methods(['GET'])
def get_data_list(request):
    '''
    获取用户上传的所有数据集名称
    '''
    lists=[list(i.keys())[0] for i in dp.user['dataset']]
    return JsonResponse({"data_list":lists}, safe=False)

@require_http_methods(['GET'])
def show_dataset(request):
    '''
    根据用户选择的数据集，展示所有数据
    '''
    print(request)
    dataset_name=request.GET.get("dataset_name")
    print(dataset_name)
    dp=dataset_process()
    df=dp.get_dataset('day')
    df_json=df.to_json()
    return HttpResponse(df_json)

@require_http_methods(['GET'])
def model_params(request):
    pass
