from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = [
            "id",
            "created_at",
            "author",
            "fullName",
            "gradeSection",
            "completed",
            "dateSubmitted",
            "damagedProperty",
            "comment",
        ]
        extra_kwargs = {
            "author": {"read_only": True},  # Ensure 'author' is read-only
            "created_at": {"read_only": True},  # Read-only for automatically added timestamps
            "dateSubmitted": {"required": False},  # Optional field for submissions
        }
