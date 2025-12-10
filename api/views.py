import json

from django.http import JsonResponse
from rest_framework.views import csrf_exempt


def register_user_in_db(data):
    ...


@csrf_exempt
def register_user(request):
    data = request.body
    data = json.loads(data)

    return JsonResponse(data={})
