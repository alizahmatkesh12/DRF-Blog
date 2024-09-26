from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .serializers import (
    RegistrationSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
)
from accounts.models import  Profile

User = get_user_model()


class RegisterApiView(GenericAPIView):
    """Creates new user with the given info and credentials"""

    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        """
        Register class
        """

        serializer = RegistrationSerializer(data=request.data, many=False)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(GenericAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    
    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            # if not self.object.check_password(serializer.data.get("old_password")):
            #     return Response(
            #         {"old_password": ["Wrong password."]},
            #         status = status.HTTP_400_BAD_REQUEST,
            #     )
            # set_password also hashes the password that the user will get
                    # "do it in serializer"
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"details": "password changed successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileApiView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj
