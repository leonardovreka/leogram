from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterSerializer, ConfirmEmailSerializer, ResendVerificationSerializer
from accounts.actions.register import register_user
from accounts.actions.confirm_email import confirm_email
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from accounts.actions.resend_verification import resend_verification_email

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = register_user(
                email=serializer.validated_data['email'],
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
            )
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {'id': user.id, 'email': user.email, 'username': user.username},
            status=status.HTTP_201_CREATED
        )

class ConfirmEmailView(APIView):
    def post(self, request):
        serializer = ConfirmEmailSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            confirm_email(token=serializer.validated_data['token'])
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)

@method_decorator(ratelimit(key='ip', rate='5/m', block=True), name='post')
class ResendVerificationView(APIView):
    def post(self, request):
        serializer = ResendVerificationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        resend_verification_email(email=serializer.validated_data['email'])

        return Response(
            {'message': 'If this email exists and is unverified, a new verification email has been sent.'},
            status=status.HTTP_200_OK
        )