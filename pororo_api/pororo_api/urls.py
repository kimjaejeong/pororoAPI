from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info
    (title="Kronos log_api",
     default_version='v1',
     description=
     '''이것은 크로노스 cpu, memory, storage, traffic 데이터
     1. 호출 후 적재
     2. db 검색
     3. 업데이트
     4. 삭제
     5. 분석 및 mattermost 연동
     이 가능한 api 문서입니다.''',
     terms_of_service="https://www.google.com/policies/terms/",),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('', include('search.urls')),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url('api/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-api'),
]

# A JSON view of your API specification at /swagger.json
# A YAML view of your API specification at /swagger.yaml
# A swagger-ui view of your API specification at /swagger/
# A ReDoc view of your API specification at /redoc/
