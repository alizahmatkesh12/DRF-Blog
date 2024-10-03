from django.conf import settings
from rest_framework import serializers
from accounts.models import  Profile
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
import jwt

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """Registration serializer with password checkup"""
    
    password1 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "password1"]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError(
                {"detail": "passswords doesnt match"}
            )

        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("password1", None)
        return User.objects.create_user(**validated_data)
    
    
class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True, label=_("Old Password"))
    new_password = serializers.CharField(required=True, label=_("New Password"))
    new_password1 = serializers.CharField(required=True, label=_("Confirm New Password"))
    
    def validate_old_password(self, value):
        """
        Check that the old password provided is correct.
        """
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                _('Your old password was entered incorrectly. Please enter it again.')
            )
        return value
        
    def validate(self, attrs):
        """
        Check if the new passwords match and validate the new password.
        """
        if attrs["new_password"] != attrs["new_password1"]:
            raise serializers.ValidationError(
                {"detail": _("Passwords do not match!")}
            )
        try:
            validate_password(attrs["new_password"])
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(
                {"new_password": list(e.messages)}
            )
        return super().validate(attrs)
    
    
class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        username = attrs.get("email")
        password = attrs.get("password")
        
        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password
            )
            
        # The authenticate call simply returns None for is_active=False
        # users. (Assuming the default ModelBackend authentication
        # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
            if not user.is_verified:
                raise serializers.ValidationError({"details": "User is not verified."})
        else:
            msg = _("Must include 'username' and 'password'. ")
            raise serializers.ValidationError(msg, code="autorization")
        
        attrs["user"] = user
        return attrs
    
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError({"details": "User is not verified. "})
        validated_data["email"] = self.user.email
        validated_data["user_id"] = self.user.pk
        return validated_data


class ActivationResendSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"details": "User does not exist"})
        if user_obj.is_verified:
            raise serializers.ValidationError(
                {"detail": "User is already verified and activated"}
            )
        attrs["user"] = user_obj
        return super().validate(attrs)
    
    
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
    def validate(self, attrs):
        email = attrs.get("email")
        user_obj = User.objects.filter(email__iexact=email).first()
        attrs["user"] = user_obj
        return super().validate(attrs)
    

class ResetPasswordConfirmSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    
    def validate(self, attrs):
        token = attrs.get("token")
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_token.get("user_id", None)
        except jwt.exceptions.ExpiredSignatureError:
            raise serializers.ValidationError(
                {'detail': "Token has been expired"}
            )
        except jwt.exceptions.InvalidSignatureError:
            raise serializers.ValidationError(
                {"detail": "Token is not vaild"}
            )
        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError(
                {"detail": "Passwords do not match!!!"}
            )
        
        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(
                {"new_password": list(e.messages)}
            )
        
        attrs["uid"] = user_id
        return super().validate(attrs)  
class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = ["id", "email", "first_name", "last_name", "description", "image"]
        read_only_fields = ["email"]