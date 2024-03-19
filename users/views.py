from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from users.models import UserType
from users.serializers import UserSerializer


class CreateUserView(APIView):
    def post(self, request):
        data = request.data
        data["user_type"] = UserType.USER
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.create()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
