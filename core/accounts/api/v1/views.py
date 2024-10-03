from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from .serializers import (
    RegistrationSerializer,
    CustomAuthTokenSerializer,
    ChangePasswordSerializer,
    CustomTokenObtainPairSerializer,
    ActivationResendSerializer,
    ResetPasswordSerializer,
    ResetPasswordConfirmSerializer,
    ProfileSerializer,
)

from accounts.models import  Profile
# from .utils import TokenHandler, EmailSender

User = get_user_model()
from ..utils import EmailThread
from mail_templated import EmailMessage

class UserRegistration(GenericAPIView):
    """Creates new user with the given info and credentials"""

    serializer_class = RegistrationSerializer

    # def post(self, request, *args, **kwargs):
    #     """
    #     Register class
    #     """

    #     serializer = RegistrationSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     email = serializer.validated_data["email"]
    #     data = {"email": email}
    #     user_obj = get_object_or_404(User, email=email)
    #     EmailSender.send_activation_email(request, user_obj)
    #     return Response(data, status=status.HTTP_201_CREATED)
    def post(self, request, *args, **kwargs):
            serializer = RegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                email = serializer.validated_data["email"]
                data = {
                    "detail": "We sent an email to you for verification.",
                    "email": email,
                }
                user_obj = get_object_or_404(User, email=email)
                token = self.get_tokens_for_user(user_obj)
                email_obj = EmailMessage(
                    "email/activation_email.tpl",
                    {"token": token},
                    "admin@admin.com",
                    to=[email],
                )
                # multi threading
                EmailThread(email_obj).start()
                return Response(data, status.HTTP_201_CREATED)
            
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

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
        
        
class CustomObtainAuthToken(ObtainAuthToken):
    """Generate an authentication token for user"""
    serializer_class = CustomAuthTokenSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request":request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "user_id": user.pk,
            "email": user.email
            }
        )
        
class CustomDiscardAuthToken(APIView):
    """Delete user's existing authentication token"""
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(
                {"detail": "Token does not exist. "},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        
class CustomTokenObtainPairView(TokenObtainPairView):
    """Obtaining JWT pairs for user"""
    serializer_class = CustomTokenObtainPairSerializer
        
        
class ActivationAPIView(APIView):
    """Decoding JWT authentication token and activating user account"""
    
    def get(self, request, token, *args, **kwargs):
        _, user_id = TokenHandler.Validate_jwt_access_token(token)
        user_obj = User.objects.get(id=user_id)
        if user_obj.is_verified:
            return Response(
                {"details": "Your account has already been verified and is active."}
            )
        user_obj.is_verified = True
        user_obj.save()
        return Response(
            {"details": "Your account has been verified and activated."}
            )

class ActivationResendAPIView(GenericAPIView):
    """Resending JWT authentication token for user activation"""
    
    serializer_class = ActivationResendSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        EmailSender.send_activation_email(request, user_obj)
        return Response(
            {"details": "Activation link resend was successful."},
            status=status.HTTP_200_OK,
        )
        
        
class ResetPasswordAPIView(GenericAPIView):
    """Sending a reset password link to the user by email"""
    serializer_class = ResetPasswordSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        if user_obj:
            EmailSender.send_resetpassword_email(request, user_obj)
        return Response(
            {
                "details": "reset password link was sent to you..."
            }
        )
        

class ResetPasswordConfirmAPIView(GenericAPIView):
    """Validating JWT token"""
    
    def get(self, request, token, *args, **kwargs):
        valid_token, _ = TokenHandler.Validate_jwt_access_token(token)
        data = {
            "token": token,
            "valid_token": valid_token,
        }
        # token can also be saved in the session to be used
        # then check the valid_token and redirect user to the the password reset form
        return Response(data, status=status.HTTP_200_OK)

class ResetPasswordValidateAPIView(GenericAPIView):
    """Resetting user's password"""
    
    serializer_class = ResetPasswordConfirmSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uid = serializer.validated_data.get("uid")
        user_obj = User.objects.get(pk=uid)
        # set_password also hashes the password that the user will get
        user_obj.set_password(serializer.validated_data.get("password"))
        user_obj.save()
        return Response(
            {"detals": "Reset password was successful"},
            status=status.HTTP_200_OK,
        )
        
        
class ProfileApiView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj
