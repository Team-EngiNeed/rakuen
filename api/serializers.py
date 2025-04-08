from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note


from rest_framework import serializers
from .models import CustomUser  # Replace with the actual path to your model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "password", "role", "section", "username"]
        extra_kwargs = {
            "password": {"write_only": True},
            "username": {"read_only": True},  # It's auto-generated
        }

    def create(self, validated_data):
        # This ensures the CustomUserManager's logic (username generation) is applied
        return CustomUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        # Allow password update if provided
        if "password" in validated_data:
            instance.set_password(validated_data.pop("password"))

        # Allow role/section updates, then regenerate the username
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.update_username()
        instance.save()
        return instance



from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = [
            'id',
            'author',
            'created_at',
            'fullName',
            'gradeSection',
            'completed',
            'dateSubmitted',
            'damagedProperty',
            'comment',
            'image',
            'priority',
        ]
        read_only_fields = ['id', 'created_at', 'priority', 'author']

    def create(self, validated_data):
        # Automatically assign the author from the request user
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['author'] = request.user
        return super().create(validated_data)

