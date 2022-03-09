from rest_framework import serializers

from django_weather_reminder.models import (
    City, Country, CurrentWeather, Subscription
)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = City
        fields = '__all__'


class NameRelatedField(serializers.RelatedField):
    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        return value.name


class CurrentWeatherSerializer(serializers.ModelSerializer):
    city = NameRelatedField(read_only=True)

    class Meta:
        model = CurrentWeather
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    def create(self, validated_data):
        try:
            city, frequency = (
                validated_data['city'], validated_data['frequency']
            )
        except KeyError:
            raise serializers.ValidationError(
                'You passed wrong fields!'
            )

        user = self.context['request'].user

        if user.city_subscriptions.filter(pk=city.pk).exists():
            raise serializers.ValidationError(
                'You can only subscribe to one city once!'
            )

        if not city.active:
            city.active = True
            city.save()

        return Subscription.subscriptions.create(
            user=user, city=city, frequency=frequency
        )

    class Meta:
        model = Subscription
        fields = '__all__'

        extra_kwargs = {
            'city': {'required': False}
        }
