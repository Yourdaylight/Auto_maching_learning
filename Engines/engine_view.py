import json
import os
import traceback

import pandas as pd

from django.http import JsonResponse, HttpResponse

from django.views.decorators.http import require_http_methods


@require_http_methods(['POST'])
def check_clean_condition(request):
    postBody = json.loads(request.body)
    return JsonResponse(postBody)