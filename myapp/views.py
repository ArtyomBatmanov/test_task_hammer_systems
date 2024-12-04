from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import User
from .serializers import UserProfileSerializer
import time


class SendAuthCodeView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')

        if not phone_number:
            return Response({"error": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Создание или получение пользователя
        user, created = User.objects.get_or_create(phone_number=phone_number)

        # Генерация 4-значного кода
        user.generate_auth_code()
        user.save()

        # Имитация отправки кода (задержка 2 секунды)
        time.sleep(2)
        print(f"Auth code sent: {user.auth_code}")  # В реальном проекте отправьте код через SMS.

        return Response({"message": "Authorization code sent."}, status=status.HTTP_200_OK)


class VerifyAuthCodeView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        auth_code = request.data.get('auth_code')

        if not phone_number or not auth_code:
            return Response({"error": "Phone number and auth code are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if user.auth_code == auth_code:
            user.auth_code = None  # Сбрасываем код после успешной авторизации
            user.save()
            return Response({"message": "Authorization successful."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid authorization code."}, status=status.HTTP_400_BAD_REQUEST)





class UserProfileView(APIView):
    def get(self, request):
        phone_number = request.query_params.get('phone_number')
        if not phone_number:
            return Response({"error": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Ищем пользователя без строгой зависимости от формата номера
            user = User.objects.get(
                Q(phone_number=phone_number) | Q(phone_number=phone_number.lstrip('+'))
            )
            serializer = UserProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
