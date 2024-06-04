from rest_framework import serializers
from .models import Cars, UserInfo, Renting, Rating

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cars
        fields = ['id', 'car_model', 'cost']
    
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['id', 'username', 'email', 'date_of_birth', 'car_model']

class RentingSerializer(serializers.ModelSerializer):

    car_model_name = serializers.SerializerMethodField()

    class Meta:
        model = Renting
        fields = ['id', 'car_model', 'car_model_name', 'pick_up_date', 'return_date', 'user']
        read_only_fields = ['id', 'user']

    def get_car_model_name(self, obj):
        return obj.car_model.car_model

class RatingSerializer(serializers.ModelSerializer):

    car_model_name = serializers.SerializerMethodField()

    class Meta:
        model = Rating
        fields = ['id', 'score', 'car_model', 'car_model_name']

    def get_car_model_name(self, obj):
        return obj.car_model.car_model       