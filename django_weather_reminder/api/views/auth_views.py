from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from django_weather_reminder.api.serializers.auth_serializers import (
    RegistrationSerializer
)

from django_weather_reminder.api.permissions import IsNotAuthenticated


class RegistrationAV(APIView):
    """Register a new user. Returns a new user's data and credentials."""

    permission_classes = IsNotAuthenticated,

    @staticmethod
    def post(request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            new_user = serializer.save()

            refresh = RefreshToken.for_user(new_user)

            data_to_response = {
                'token': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
            }
            data_to_response.update(serializer.data)

            return Response(data_to_response, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
