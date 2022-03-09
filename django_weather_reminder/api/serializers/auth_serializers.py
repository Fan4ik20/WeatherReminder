from rest_framework import serializers

from django_weather_reminder.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        write_only=True, style={'input-type': 'password'}
    )

    class Meta:
        model = User

        fields = ['username', 'email', 'password', 'password2']

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        username, email, password1, password2 = (
            self.validated_data['username'], self.validated_data['email'],
            self.validated_data['password'], self.validated_data['password2']
        )

        if password1 != password2:
            raise serializers.ValidationError('The passwords should match!')

        new_user = User.objects.create(username=username, email=email)
        new_user.set_password(password1)
        new_user.save()

        return new_user
