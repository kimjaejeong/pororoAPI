from django.urls import path
from .views import *
# from . import views


urlpatterns = [
    path('01_get_log', GetLogView.as_view(), name='get_log'),
    #path('get_log/', GetLogView.as_view(), name='get_log'),
    path('02_search_date', SearchDateView.as_view(), name="search_date"),
    #path('search_db/', SearchDBView.as_view(), name="searchdb"),
    # path('03_search_all', SearchAllView.as_view(), name="search_all"),
    # path('03_update', UpdateView.as_view(), name='update'),
    # #path('update/', UpdateView.as_view(), name='update'),
    # path('04_delete', DeleteView.as_view(), name='delete'),
    # #path('delete/', DeleteView.as_view(), name='delete'),
    # path('05_build_model', BuildModelView.as_view(), name='build_model'),
    # #path('create/', CreateView.as_view(), name='create'),
    # path('06_analyze', AnalyzeView.as_view(), name="analyze"),
    # #path('analyze/', AnalyzeView.as_view(), name="analyze"),
]