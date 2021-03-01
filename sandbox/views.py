from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CompilerSerializer
from .handlers import HandlerMapping


# Create your views here.
class CompileCode(APIView):
    """
    API View to Compile code
    """

    permission_classes = (permissions.AllowAny,)

    # TODO drf swagger
    @swagger_auto_schema()
    def post(self, request: Request):
        """
        POST
        """
        # data validation
        compiler_serializer = CompilerSerializer(data=request.POST)
        if not compiler_serializer.is_valid():
            # validation error
            return Response(
                data={
                    "status": "ERROR",
                    "message": compiler_serializer.errors,
                },
                status=status.HTTP_200_OK,
            )
        # fetching the validated data
        validated_data = compiler_serializer.validated_data
        userid, language, source, timeout = (
            validated_data["userid"],
            validated_data["language"],
            validated_data["source"],
            validated_data["timeout"],
        )
        # obtaining handler class from handler mapping
        HandlerClass = HandlerMapping.get(language)
        handler = HandlerClass(userid=userid, timeout=timeout)
        # TODO add it to task queue
        task_id = handler.execute(source)
        return Response(
            data={
                "status": "OK",
                "message": {
                    "task_id": task_id,
                },
            },
            status=status.HTTP_200_OK,
        )
