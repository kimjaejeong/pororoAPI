from rest_framework import serializers
from .models import Collection


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'

class QaAnalysisBodySerializer(serializers.Serializer):
    question = serializers.CharField(help_text="질문 입력예시) 질문사항")
    original_news_data = serializers.CharField(help_text="기존 뉴스 데이터 입력예시) 뉴스데이터")