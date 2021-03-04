from django.urls import path
from .views import CompileCode

urlpatterns = [
    path("compile", CompileCode.as_view(), name="compile_code"),
    path("status/<str:task_id>", CompileCode.as_view(), name="get_task_status"),
]
