from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .handlers import MAP


# Create your views here.
class CompileCode(APIView):
    """
    API View to Compile code
    """

    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema()
    def post(self, request: Request):
        """
        POST
        """
        data = request.POST
        timeout = int(data["timeout"])
        HandlerClass = MAP[data["language"].lower()]
        handler = HandlerClass(userid=data["userid"], timeout=timeout)
        output, err = handler.execute(data["source"])
        return Response(
            data={
                "status": "OK",
                "message": {
                    "output": output if len(output) else None,
                    "error": err if len(err) else None,
                },
            },
            status=status.HTTP_200_OK,
        )
