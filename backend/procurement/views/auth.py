from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()


class RegisterView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        user = User.objects.create_user(
            email=email, password=password, first_name=first_name, last_name=last_name
        )
        return Response(
            {"status": "success", "user_id": user.id}, status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            return Response({"status": "success", "user_id": user.id})
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )
