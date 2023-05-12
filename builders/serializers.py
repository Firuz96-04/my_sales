from rest_framework import serializers
from .models import *
from .validators import (builder_verify, resident_verify,
                         apartment_validate, floor_validate, apartment_put_validate, complex_verify)
from main_auth.serializers import CustomUserSerializer


class BuilderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Builder
        fields = '__all__'


class BuilderVerifySerializer(serializers.ModelSerializer):
    # user = serializers.IntegerField(source='user_id', required=False, read_only=True)

    class Meta:
        model = Builder
        fields = ('brand_name', 'legal_name', 'address', 'inn', 'bank_account',
                  'license_period', 'description', 'image_logo')

    def validate(self, data):
        error = builder_verify(data)
        if error:
            raise serializers.ValidationError({'errors': error})
        return data


class ManagerComplexConnectSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)

    class Meta:
        model = ResidentComplex
        fields = ('id', 'name', 'manager')

    def validate(self, data):
        builder = self.context['builder']
        # manager = Manager.objects.get()
        manager = data['manager'].builder_id
        # if manager != builder:
        #     raise serializers.ValidationError({'manager': 'builder and manager'})

        # print(self.context, 'eee')
        return data


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = ('user_id',)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = CustomUserSerializer(instance.user).data
        return response


class ResidentManagerSerializer(serializers.Serializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    sure_name = serializers.CharField(source="user.sure_name")
    phone = serializers.CharField(source="user.phone")

    # class Meta:
    #     model = Manager
    #     fields = ('id', 'first_name', 'last_name', 'sure_name', 'phone')


class ResidentComSerializer(serializers.ModelSerializer):
    total_apartment = serializers.IntegerField(default=1)
    image_banner = serializers.ImageField(required=False, max_length=None, allow_empty_file=True, use_url=True)

    # elevator = serializers.PrimaryKeyRelatedField(queryset=Elevator.objects.all(), many=True)

    class Meta:
        model = ResidentComplex
        fields = ('name', 'address', 'city', 'deadline', 'floor', 'total_apartment',
                  'ceiling_height_from', 'image_banner', 'status', 'building_class', 'building_type', 'elevator',
                  'parking',
                  'kitchen', 'decoration', 'facade', 'heating', 'description')
        image_banner = {'image_banner': {'required': False}}

    def validate(self, data):
        error = complex_verify(data)
        if error:
            raise serializers.ValidationError({'errors': error})
        return data

    def to_representation(self, instance):
        response = super().to_representation(instance)
        request = self.context.get('request')
        if instance.image_banner:
            response['image_banner'] = request.build_absolute_uri(instance.image_banner.url)
        # response['manager'] = ResidentManagerSerializer(instance.manager).data
        # response['building_type'] = BuildingTypeSerializer(instance.building_type).data
        # response['building_class'] = BuildingClassSerializer(instance.building_class).data
        return response


class ResidentManSerializerUpd(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)

    class Meta:
        model = ResidentComplex
        fields = ('name', 'building_class', 'address', 'city', 'deadline', 'floor',
                  'building_class', 'building_type', 'elevator', 'parking',
                  'kitchen', 'decoration', 'facade', 'heating', 'total_apartment',
                  'ceiling_height_from', 'image_banner', 'status', 'manager', 'description')


class BlockSerializer(serializers.ModelSerializer):
    resident_complex = serializers.IntegerField(source='resident_complex.id', read_only=True)

    class Meta:
        model = Block
        fields = ('id', 'name', 'status', 'deadline', 'resident_complex')

    def validate(self, data):
        errors = []
        manager_id = self.context['request']['user_id']
        block = Block.objects.filter(name__iexact=data['name'], resident_complex__manager_id=manager_id)
        if block:
            errors.append({'block': 'this block name has already exists'})
        if errors:
            raise serializers.ValidationError({'errors': errors})
        return data

    def create(self, validated_data):
        manager_id = self.context['request']['user_id']
        com_res_id = ResidentComplex.objects.get(manager_id=manager_id).id
        return Block.objects.create(**validated_data, resident_complex_id=com_res_id)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['entrances'] = list()
        return response


class FloorSerializer(serializers.ModelSerializer):
    block = serializers.IntegerField(source='entrance.block.id', read_only=True)

    class Meta:
        model = Floor
        fields = ('id', 'name', 'entrance', 'image_1', 'block', 'floor_type')

    def validate(self, data):
        errors = floor_validate(data)
        if errors:
            raise serializers.ValidationError({'errors': errors})
        return data

    def to_representation(self, instance):
        response = super().to_representation(instance)
        request = self.context.get('request')
        if instance.image_1:
            response['image_1'] = request.build_absolute_uri(instance.image_1.url)
        response['apartments'] = ()
        return response


class ApartmentSerializer(serializers.ModelSerializer):
    status = serializers.IntegerField(source='status_id', default=1)

    class Meta:
        model = Apartment
        fields = ('id', 'name', 'floor', 'status', 'image_1', 'image_2')

    def validate(self, data):
        errors = apartment_validate(data)
        if errors:
            raise serializers.ValidationError({'errors': errors})
        return data

    def to_representation(self, instance):
        response = super().to_representation(instance)

        response['block'] = instance.floor.entrance.block.id
        response['entrance'] = instance.floor.entrance.id
        response['images'] = (
            response['image_1'],
            response['image_2'],
        )
        del response['image_1']
        del response['image_2']
        return response


class ApartmentAddEditSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    cost = serializers.SerializerMethodField(method_name='cost_apartment')
    decoration = serializers.IntegerField(source='decoration_id', required=False)

    class Meta:
        model = Apartment
        fields = ('id', 'name', 'floor', 'status', 'square', 'cost',
                  'decoration', 'price', 'image_1', 'image_2', 'ceiling_height')

    def cost_apartment(self, obj):
        return obj.square * obj.price

    def validate(self, data):
        errors = apartment_put_validate(data)
        if errors:
            raise serializers.ValidationError({'errors': errors})
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        response = super().to_representation(instance)
        # response = dict()

        response['block'] = instance.floor.entrance.block.id
        response['entrance'] = instance.floor.entrance.id
        response['images'] = list()
        if instance.image_1:
            response['images'].append(request.build_absolute_uri(instance.image_1.url))
        if instance.image_2:
            response['images'].append(request.build_absolute_uri(instance.image_2.url))
        # if instance.image_2:
        #     response['image_2'] = request.build_absolute_uri(instance.image_2.url)
        del response['image_1']
        del response['image_2']
        return response


class EntranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrance
        fields = ('id', 'name', 'block')

    def validate(self, data):
        errors = []
        entrance = Entrance.objects.filter(name__iexact=data['name'], block_id=data['block'].id)
        if entrance:
            errors.append({'entrance': 'this entrance has already exists'})

        if errors:
            raise serializers.ValidationError({'errors': errors})
        return data

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['floors'] = list()
        return response


class ComplexManagerSerializer(serializers.ModelSerializer):
    # builder_id = serializers.IntegerField(required=False, read_only=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = ResidentComplex
        fields = ('id', 'name', 'manager')

    def validate(self, data):
        errors = []
        manager = data['manager']
        rs_complex = ResidentComplex.objects.get(id=self.context['id'])
        if rs_complex.builder_id != manager.builder_id:
            errors.append({'manager_error': 'this manager does not belong to this builder'})

        if errors:
            raise serializers.ValidationError({'errors': errors})
        return data


class FloorMainSerializer(serializers.ModelSerializer):
    block = serializers.IntegerField(source='entrance.block.id', read_only=True)
    apartments = ApartmentSerializer(many=True, read_only=True)
    image_1 = serializers.ImageField()

    class Meta:
        model = Floor
        fields = ('id', 'name', 'entrance', 'image_1', 'block', 'floor_type', 'apartments')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response


class EntranceMainSerializer(serializers.ModelSerializer):
    floors = FloorMainSerializer(many=True, read_only=True)

    class Meta:
        model = Entrance
        fields = ('id', 'name', 'block', 'floors')


class BlockMainSerializer(serializers.ModelSerializer):
    entrances = EntranceMainSerializer(many=True)

    class Meta:
        model = Block
        fields = ('id', 'name', 'entrances')


class SimpleApartment(serializers.Serializer):
    id = serializers.IntegerField()
    status = serializers.IntegerField(source='status.id')


class ClientNoticeApartmentSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    sale_manager = serializers.IntegerField(source='sale_manager.id', read_only=True)
    apartment_name = serializers.CharField(source='apartment.name', read_only=True)

    class Meta:
        model = Client
        fields = ('id', 'first_name', 'last_name', 'sure_name', 'phone', 'recall', 'info_apartment',
                  'social_media', 'apartment', 'action', 'sale_manager', 'apartment_name', 'comment', 'created_at')

    def get_created_at(self, obj):
        myDate = obj.created_at
        formatedDate = myDate.strftime("%Y-%m-%d %H:%M:%S")
        return formatedDate

    def validate(self, data):
        errors = []
        apartment = Apartment.objects.get(pk=data['apartment'].id)
        if apartment.status_id == 2:
            errors.append({'apartment': 'this room has already sold'})
        if errors:
            raise serializers.ValidationError({'errors': errors})
        return data

    def to_representation(self, instance):
        response = super().to_representation(instance)
        # print(instance.sale_manager_id)
        # response['apartment'] = SimpleApartment(instance.apartment).data
        response['sale_manager'] = instance.sale_manager_id
        return response

    # def create(self, validated_data):
    #     return super().create(validated_data)


class ApartmentBuySerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    sale_manager = serializers.IntegerField(source='sale_manager.id', read_only=True)

    class Meta:
        model = ApartmentBuy
        fields = ('id', 'client', 'apartment', 'sale_manager', 'created_at')

    def get_created_at(self, obj):
        myDate = obj.created_at
        formatedDate = myDate.strftime("%Y-%m-%d %H:%M:%S")
        return formatedDate
