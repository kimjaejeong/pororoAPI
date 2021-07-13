from django.urls import path
from .views import *
# from . import views

urlpatterns = [
    path('qa_analysis', QaAnalysisView.as_view(), name='qa_analysis'),
    path('qa_analysis/', QaAnalysisView.as_view(), name='qa_analysis'),
]