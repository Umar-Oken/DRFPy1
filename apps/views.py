from django.contrib.auth import login, logout

from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.parsers import JSONParser, FileUploadParser, MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, AdminRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.models import Task
from apps.serializer import (
    LoginSerializer,
    RegisterSerializer,
    TaskSerializer,
)


# Create your views here.
class TaskModelViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = [AdminRenderer , JSONRenderer]

    parser_classes = [MultiPartParser]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        request=RegisterSerializer,
        responses={
            201: inline_serializer(
                name="RegisterResponse",
                fields={
                    "id": serializers.IntegerField(),
                    "username": serializers.CharField(),
                },
            )
        },
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"id": user.pk, "username": user.username},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        request=LoginSerializer,
        responses={
            200: inline_serializer(
                name="LoginResponse",
                fields={
                    "id": serializers.IntegerField(),
                    "username": serializers.CharField(),
                },
            )
        },
    )
    def post(self, request):
        serializer = LoginSerializer(
            data=request.data,
            context={"request": request._request},
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request._request, user)
        return Response({"id": user.pk, "username": user.username})


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=None,
        responses={
            200: inline_serializer(
                name="LogoutResponse",
                fields={"detail": serializers.CharField()},
            )
        },
    )
    def post(self, request):
        logout(request._request)
        return Response({"detail": "Successfully logged out."})
