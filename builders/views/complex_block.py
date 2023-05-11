from django.db.models import Prefetch
from rest_framework import generics, mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from builders.permissions import OnlyManagerPermission, OnlySaleManagerPermission
from builders.serializers import (
    BlockSerializer, EntranceSerializer,
    FloorSerializer, ApartmentSerializer, BlockMainSerializer, ApartmentAddEditSerializer)
from builders.models import Block, Entrance, Floor, Apartment, SaleManager
from django.db.models.deletion import ProtectedError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound


class BlockMainApiView(mixins.ListModelMixin,
                       generics.GenericAPIView):

    serializer_class = BlockMainSerializer
    permission_classes = (OnlyManagerPermission,)

    def get_permissions(self):
        if self.request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'] and self.request.user.role_id == 3:
            return [OnlyManagerPermission()]
        elif self.request.method == 'GET' and self.request.user.role_id == 4:
            return [OnlySaleManagerPermission()]
        return super().get_permissions()

    def get_queryset(self):
        # print(self.request.user.id)
        user_id = None
        if self.request.user.role_id == 3:
            user_id = self.request.user.id
        else:
            sale_man = SaleManager.objects.get(pk=self.request.user.id)
            user_id = sale_man.manager_id
        return Block.objects.filter(resident_complex__manager_id=user_id).\
            prefetch_related(
                Prefetch('entrances'),
                Prefetch('entrances__floors', queryset=Floor.objects.order_by('-id')),
                Prefetch('entrances__floors__apartments')
        )

    def get(self, request, *args, **kwargs):
        # print(self.request.META)
        block = BlockMainSerializer(self.get_queryset(), many=True, context={'request': request})
        return Response({'data': block.data})


class BlockApiView(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   generics.GenericAPIView):
    serializer_class = BlockSerializer
    permission_classes = (OnlyManagerPermission,)

    def get_queryset(self):
        manager_id = self.request.user.id
        return Block.objects.filter(resident_complex__manager_id=manager_id)

    def get(self, request, *args, **kwargs):
        block = BlockSerializer(self.get_queryset(), many=True)
        return Response({'data': block.data})

    def post(self, request, *args, **kwargs):
        block = BlockSerializer(data=request.data, context={'request': {'user_id': request.user.id}})
        block.is_valid(raise_exception=True)
        block.save()
        return Response({'data': block.data})

    def delete(self, request, *args, **kwargs):
        block_id = request.query_params.get('id')
        try:
            block = Block.objects.get(pk=block_id)
            block.delete()
            return Response({'data': block.name})
        except ProtectedError:
            return Response({'protect': 'This object is referenced by other objects and cannot be deleted.'},
                            status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'block_not_found': f'Block {block_id} not found'},
                            status=status.HTTP_400_BAD_REQUEST)


class EntranceApiView(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      generics.GenericAPIView):
    serializer_class = EntranceSerializer
    permission_classes = (OnlyManagerPermission,)

    def get_queryset(self):
        manager_id = self.request.user.id
        return Entrance.objects.filter(block__resident_complex__manager=manager_id)

    def get(self, request, *args, **kwargs):
        entrance = EntranceSerializer(self.get_queryset(), many=True)
        return Response({'data': entrance.data})

    def post(self, request, *args, **kwargs):
        entrance = EntranceSerializer(data=request.data)
        entrance.is_valid(raise_exception=True)
        entrance.save()
        return Response({'data': entrance.data})

    def delete(self, request, *args, **kwargs):
        entrance_id = request.query_params.get('id')
        try:
            entrance = Entrance.objects.get(pk=entrance_id)
            entrance.delete()
            return Response({'data': entrance.name}, status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return Response({'protect': 'This object is referenced by other objects and cannot be deleted.'},
                            status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'entrance_not_found': f'entrance {entrance_id} not found'},
                            status=status.HTTP_400_BAD_REQUEST)


class FloorApiView(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   generics.GenericAPIView):
    serializer_class = FloorSerializer
    permission_classes = (OnlyManagerPermission,)
    parser_classes = (MultiPartParser, JSONParser )

    def get_queryset(self):
        manager_id = self.request.user.id
        return Floor.objects.filter(entrance__block__resident_complex__manager_id=manager_id).\
            select_related('floor_type', 'entrance__block').order_by('-id')

    def get(self, request, *args, **kwargs):
        floor = FloorSerializer(self.get_queryset(), many=True, context={"request": request})
        return Response({'data': floor.data})

    def post(self, request, *args, **kwargs):
        floor = FloorSerializer(data=request.data,  context={"request": request})
        floor.is_valid(raise_exception=True)
        floor.save()
        return Response({'data': floor.data})

    def delete(self, request, *args, **kwargs):
        floor_id = request.query_params.get('id')
        try:
            floor = Floor.objects.get(pk=floor_id)
            floor.delete()
            return Response({'data': floor.name}, status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return Response({'protect': 'This object is referenced by other objects and cannot be deleted.'},
                            status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'floor_not_found': f'floor {floor_id} not found'}, status=status.HTTP_400_BAD_REQUEST)


class ApartmentApiView(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       generics.GenericAPIView):
    serializer_class = ApartmentSerializer
    parser_classes = (JSONParser, MultiPartParser)
    permission_classes = (OnlyManagerPermission,)

    def get_queryset(self):
        manager_id = self.request.user.id
        return Apartment.objects.filter(floor__entrance__block__resident_complex__manager_id=manager_id).\
            select_related('floor__entrance__block')

    def get(self, request, *args, **kwargs):
        floor = ApartmentSerializer(self.get_queryset(), many=True)
        return Response({'data': floor.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        apartment = ApartmentAddEditSerializer(data=request.data, context={"request": request})
        apartment.is_valid(raise_exception=True)
        apartment.save()
        return Response({'apartment': apartment.data}, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        apartment_id = request.query_params.get('id')
        apartment = Apartment.objects.get(id=apartment_id)
        serial = ApartmentAddEditSerializer(apartment, data=request.data, context={"request": request})
        serial.is_valid(raise_exception=True)
        serial.save()
        return Response({'data': serial.data}, status=status.HTTP_202_ACCEPTED)