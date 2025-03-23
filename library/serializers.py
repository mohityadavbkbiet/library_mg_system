from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Book

# ✅ AdminUser Serializer with enhanced validation and password hashing
class AdminUserSerializer(serializers.ModelSerializer):
    """
    Serializer for AdminUser model with password hashing.
    """
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        """
        Create and return a new admin user with hashed password.
        """
        password = validated_data.pop('password')
        user = get_user_model().objects.create_user(**validated_data)
        user.set_password(password)  # Hash the password before saving
        user.save()
        return user

    def validate_email(self, value):
        """
        Ensure the email is unique.
        """
        user_model = get_user_model()
        if user_model.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_password(self, value):
        """
        Validate password complexity.
        """
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value

# ✅ Book Serializer with additional validation
class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model.
    """
    class Meta:
        model = Book
        fields = '__all__'

    def validate_title(self, value):
        """
        Ensure the book title is not empty or too short.
        """
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long.")
        return value

    def validate_author(self, value):
        """
        Ensure the author's name is valid.
        """
        if len(value) < 3:
            raise serializers.ValidationError("Author name must be at least 3 characters long.")
        return value
