from rest_framework import serializers

from django.utils.translation import gettext_lazy as _

from .models import (City, Region, BuildingClass, BuildingType, Parking, Kitchen, Elevator,
                     Decoration, Facade, Heating, FloorType, ApartmentDecoration, SaleManagerAction, SocialMedia)
import uuid


class RegionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30)

    class Meta:
        model = Region
        fields = ('id', 'name')

    def validate(self, data):
        name = data['name']
        city = Region.objects.filter(name__iexact=name)
        if city.exists():
            raise serializers.ValidationError({'error': f'{name} is already exists'})
        return data


class CitySerializer(serializers.ModelSerializer):
    # title = serializers.CharField(max_length=30, source='name')

    class Meta:
        model = City
        fields = ('id', 'name', 'region')

    def validate(self, data):
        name = data['name']
        region = data['region']
        city = City.objects.filter(name__iexact=name, region=region)
        if city.exists():
            raise serializers.ValidationError({'error': 'this city is already exists'})

        return data

    def to_representation(self, instance):
        response = super().to_representation(instance)
        # response['city'] = instance.city.name
        response['region'] = RegionSerializer(instance.region).data
        return response


class CityChildRegionUpd(serializers.ModelSerializer):
    key = serializers.IntegerField(source='id')
    title = serializers.CharField(max_length='30', source='name')

    class Meta:
        model = Region
        fields = ('key', 'title')


class CityUpdSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name',)

    def to_representation(self, instance):
        answer = dict()
        answer['title'] = instance.name
        answer['key'] = instance.id
        answer['children'] = CityChildRegionUpd(instance.region).data
        return answer


class CityListSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='name')
    # kod = serializers.IntegerField(source='id')
    parent = serializers.IntegerField(source='region_id')
    key = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ('title', 'id', 'parent', 'key')

    def get_key(self, obj):
        key_name = uuid.uuid4().hex[:8]
        return key_name


class RegionListSerializer(serializers.ModelSerializer):
    children = CityListSerializer(many=True, source='city_set')
    title = serializers.CharField(source='name')
    # key = serializers.IntegerField(source='id')
    key = serializers.SerializerMethodField()

    class Meta:
        model = Region
        fields = ('id', 'title', 'key', 'children')

    def get_key(self, obj):
        key_name = uuid.uuid4().hex[:10]
        return key_name

    # def get_children(self, obj):
    #     children = City.objects.filter(region=obj)
    #     serializer = CityListSerializer(children, many=True)
    #
    #     return serializer.data


class BuildingClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingClass
        fields = ('id', 'name')


class BuildingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingType
        fields = ('id', 'name')


class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = ('id', 'name')


class KitchenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kitchen
        fields = ('id', 'name')


class DecorationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Decoration
        fields = ('id', 'name')


class ElevatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elevator
        fields = ('id', 'name')


class FacadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facade
        fields = ('id', 'name')


class HeatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Heating
        fields = ('id', 'name')


class FloorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloorType
        fields = ('id', 'name')


class ApartmentDecorationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartmentDecoration
        fields = ('id', 'name')


class SaleManagerActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleManagerAction
        fields = ('id', 'name')

    def validate(self, data):
        errors = []
        sale = SaleManagerAction.objects.filter(name__iexact=data['name'])
        if sale:
            errors.append({'action': 'this is action is already exists'})

        if errors:
            raise serializers.ValidationError({'errors': errors})
        return data


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = ('id', 'name', 'is_social')

    def validate(self, data):
        errors = []
        sale = SocialMedia.objects.filter(name__iexact=data['name'])
        if sale:
            errors.append({'social_media': 'this is social_media is already exists'})

        if errors:
            raise serializers.ValidationError({'errors': errors})
        return data
