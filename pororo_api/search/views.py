from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
import sys
from drf_yasg.utils import swagger_auto_schema
from model.pororo_qa import func_qa

sys.path.append("../")  # vm에서 동작을 위함

from .serializers import QaAnalysisBodySerializer

class QaAnalysisView(APIView):
    operation_id = "데이터 호출 및 적재"
    operation_description = "데이터를 호출하고, 필요시 Elastic Search에 적재할 수 있는 API입니다."

    # 1. 크로노스 로그 데이터 검색
    # (+) 검색 후 적재
    @swagger_auto_schema(operation_id=operation_id, operation_description=operation_description, request_body=GetLogBodySerializer)
    def post(self, request, *args, **kwargs):
        # 데이터 적재
        question = request.POST.get("question", '')
        original_news_data = request.POST.get("original_news_data", '')

        summary_sentence = func_qa(question, original_news_data)

        return JsonResponse(summary_sentence, safe=False, json_dumps_params={'ensure_ascii': True},
                            status=status.HTTP_201_CREATED, charset='utf-8')