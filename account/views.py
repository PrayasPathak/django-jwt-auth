from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from .renderers import UserRenderer


# Generate tokens manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response(
            {"token": token, "msg": "Registration was successful"},
            status=status.HTTP_201_CREATED,
        )


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get("email")
        password = serializer.data.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response(
                {"token": token, "msg": "Login Successful"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"errors": {"non_field_errors": ["Email or password do not match"]}},
                status=status.HTTP_404_NOT_FOUND,
            )
