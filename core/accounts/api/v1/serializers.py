from rest_framework import serializers
from accounts.models import  Profile
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions


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
        # since we are using a custom user manager for creating users
        # we must use that manager for creating users
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
    
    
class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = ["id", "email", "first_name", "last_name", "description", "image"]
        read_only_fields = ["email"]