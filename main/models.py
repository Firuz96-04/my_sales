from django.db import models


# Create your models here.


#
class Region(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=30)

    # def children(self): # replies
    #     return City.objects.select_related('region').filter(region=self)


class City(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=30)
    region = models.ForeignKey(Region, on_delete=models.PROTECT)


class Parking(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=25)

    class Meta:
        db_table = 'parking'
        verbose_name = 'парковка'


class Kitchen(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=25)

    class Meta:
        db_table = 'kitchen'
        verbose_name = 'кухня'


class BuildingClass(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=25)

    class Meta:
        db_table = "building_class"
        verbose_name = 'Класс'


class Elevator(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=25)

    class Meta:
        db_table = 'elevator'
        verbose_name = 'Лифт'


class BuildingType(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=25)

    class Meta:
        db_table = "building_type"
        verbose_name = 'Тип дома'


class Decoration(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=25)

    class Meta:
        db_table = "decoration"
        verbose_name = 'Отделка'


class Facade(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=25)

    class Meta:
        db_table = "facade"
        verbose_name = 'Фасад'


class Heating(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=25)

    class Meta:
        db_table = "heating"
        verbose_name = 'отопление'


class ApartmentDecoration(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=25)

    class Meta:
        db_table = "apartment_decoration"
        verbose_name = 'отделка квартиры'


class ApartmentType(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=25)

    class Meta:
        db_table = "apartment_type"
        verbose_name = 'тип квартиры'
        # 1 комнатная, 2 комнатная, ....


class ApartmentStatus(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=20)

    class Meta:
        db_table = "apartment_status"
        verbose_name = "статус квартиры"

    def __str__(self):
        return self.name


class FloorType(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=20)

    class Meta:
        db_table = "floor_type"
        verbose_name = "тип этажа"


class SaleManagerAction(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=30)


class SocialMedia(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=20)
    is_social = models.BooleanField(default=False)

    class Meta:
        db_table = "social_media"
        verbose_name = "социальные сети"

    def __str__(self):
        return self.name
# class CCTV(models.Model):
#     id = models.SmallAutoField(primary_key=True)
#     name = models.CharField(max_length=25)
#
#     class Meta:
#         db_table = "cctv"
#         verbose_name = 'видеонаблюдение'
