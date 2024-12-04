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

        user.generate_invite_code()
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
            return Response({"message": "Successfully authorized.", "invite_code": user.invite_code})

        else:
            return Response({"error": "Invalid authorization code."}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    def get(self, request):
        phone_number = request.query_params.get('phone_number')

        if not phone_number:
            return Response({"error": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone_number=phone_number)
            # Список пользователей, которые использовали его инвайт-код
            referrals = User.objects.filter(activated_invite_code=user.invite_code).values_list('phone_number',
                                                                                                flat=True)

            return Response({
                "phone_number": user.phone_number,
                "invite_code": user.invite_code,
                "activated_invite_code": user.activated_invite_code,
                "referrals": list(referrals)
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)


class ActivateInviteCodeView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        invite_code = request.data.get('invite_code')

        if not phone_number or not invite_code:
            return Response({"error": "Phone number and invite code are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Получаем текущего пользователя
            user = User.objects.get(phone_number=phone_number)

            # Проверяем, не активирован ли уже инвайт-код
            if user.activated_invite_code:
                return Response(
                    {"error": f"Invite code already activated: {user.activated_invite_code}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Проверяем, существует ли пользователь с таким инвайт-кодом
            inviter = User.objects.filter(invite_code=invite_code).first()
            if not inviter:
                return Response({"error": "Invalid invite code."}, status=status.HTTP_404_NOT_FOUND)

            # Проверяем, что пользователь не активирует свой собственный код
            if inviter.phone_number == user.phone_number:
                return Response({"error": "You cannot activate your own invite code."}, status=status.HTTP_400_BAD_REQUEST)

            # Сохраняем активированный инвайт-код
            user.activated_invite_code = invite_code
            user.save()

            return Response({"message": "Invite code successfully activated."}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
