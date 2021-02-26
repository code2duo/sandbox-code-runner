from django.urls import path
from .views import CompileCode

urlpatterns = [
    path("compile", CompileCode.as_view(), name="compile_code"),
]
