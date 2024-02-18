from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from knox.auth import TokenAuthentication

from django.contrib.auth import login
from api.models import Artifact, User, Guide
from api.serializers import ArtifactSerializer, RegisterSerializer, GuideSerializer

from rest_framework import permissions, viewsets, generics
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ArtifactViewSet(viewsets.ModelViewSet):
    queryset = Artifact.objects.all()
    serializer_class = ArtifactSerializer


class GuideViewSet(viewsets.ModelViewSet):
    serializer_class = GuideSerializer

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            queryset = Guide.objects.all()
        else:
            queryset = Guide.objects.filter(visible=True)
        return queryset
