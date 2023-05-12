import os
import uuid
from io import BytesIO
from PIL import Image
from imagekit.models import ProcessedImageField
from django.db import models
from main.models import City, Parking, BuildingClass, BuildingType, Elevator, Kitchen, Decoration, \
    Facade, Heating, ApartmentDecoration, FloorType, ApartmentType, ApartmentStatus, SaleManagerAction, SocialMedia
from .utils import *
from django.core.files import File
from main_auth.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image as Im


# Create your models here.


class ComplexPicture(models.Model):
    image = models.CharField(max_length=40, blank=True)
    resident_complex = models.ForeignKey('ResidentComplex', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "complex_picture"


class Builder(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    brand_name = models.CharField(max_length=30, blank=True)
    legal_name = models.CharField(max_length=40, blank=True)
    address = models.TextField(blank=True)
    inn = models.CharField(max_length=15, blank=True)
    bank_account = models.CharField(max_length=20, blank=True)
    image_logo = models.ImageField(upload_to=upload_builder_logo,
                                   # validators=[ImageValidator()],
                                   blank=True, null=True)
    license = models.FileField(upload_to=upload_builder_license, blank=True, null=True)
    license_period = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    # print(self.image_logo is None)
    # print(bool(self.image_logo), 'logo')
    # if self.image_logo is None:
    #     print('true')
    #     new_image = self.compress(self.image_logo)
    #     self.image_logo = new_image
    #     super().save(*args, **kwargs)
    # else:
    #     print('false')
    # self.image_logo = None
    # new_image = self.compress(self.image_logo)
    # self.image_logo = new_image
    # self.compress(self.image_logo)
    # super().save(*args, **kwargs)
    #
    def save(self, *args, **kwargs):
        try:
            new_image = self.reduce_image_size(self.image_logo)
            self.image_logo = new_image
        except Exception as e:
            pass
        super().save(*args, **kwargs)

    # def convert_resize_and_rename_image(self):
    #     img = Image.open(self.image_logo.path)
    #     # Resize the image
    #     img = img.resize((800, 600), resample=Image.LANCZOS)
    #
    #     # Convert the image to WebP format
    #     output = BytesIO()
    #     img.save(output, format='webp', quality=85)
    #
    #     # Rename the new WebP image with a UUID-based filename
    #     base_name, ext = os.path.splitext(self.image_logo.name)
    #     new_name = '{}.webp'.format(uuid.uuid4())
    #     self.image_logo.name = os.path.join(os.path.dirname(self.image_logo.name), new_name)
    #
    #     # Save the new WebP image to the updated filename
    #     self.image_logo.save(self.image_logo.name, content=BytesIO(output.getvalue()), save=False)

    # 1)
    # def save(self, *args, **kwargs):  # new
    #     super().save(*args, **kwargs)
    #     try:
    #         img = Im.open(self.image_logo.path)
    #         if img.height > 300 or img.width > 300:
    #             output_size = (1500, 1500)
    #             img.thumbnail(output_size)
    #             img.save(self.image_logo.path)
    #     except Exception as e:
    #         pass

    def reduce_image_size(self, profile_pic):
        img = Image.open(profile_pic)
        thumb_io = BytesIO()
        img.save(thumb_io, 'webp', quality=50)
        new_image = File(thumb_io, name=profile_pic.name)
        return new_image

    def __str__(self):
        return self.brand_name


# BuildingClass
# BuildingType


class ResidentComplex(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT, blank=True, null=True)
    address = models.CharField(blank=True, max_length=250)
    deadline = models.CharField(max_length=10, blank=True)
    ceiling_height_from = models.CharField(max_length=3, blank=True)
    ceiling_height_to = models.CharField(max_length=3, blank=True)
    status = models.BooleanField(default=False)
    floor = models.CharField(max_length=15, blank=True)
    total_apartment = models.SmallIntegerField(default=1)
    latitude = models.CharField(max_length=12, blank=True)
    longitude = models.CharField(max_length=12, blank=True)
    manager = models.OneToOneField('Manager', on_delete=models.CASCADE, blank=True, null=True)
    image_banner = models.ImageField(upload_to=upload_resident_banner, blank=True, null=True)
    builder = models.ForeignKey(Builder, on_delete=models.CASCADE)
    building_class = models.ForeignKey(BuildingClass, on_delete=models.CASCADE, blank=True, null=True)
    building_type = models.ManyToManyField(BuildingType, blank=True)
    elevator = models.ManyToManyField(Elevator, blank=True)
    parking = models.ManyToManyField(Parking, blank=True)
    kitchen = models.ManyToManyField(Kitchen, blank=True)
    decoration = models.ManyToManyField(Decoration, blank=True)
    facade = models.ManyToManyField(Facade, blank=True)
    heating = models.ManyToManyField(Heating, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'resident_complex'


class Manager(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    builder = models.ForeignKey(Builder, on_delete=models.PROTECT, blank=True, null=True)
    photo = ProcessedImageField(upload_to=upload_manager_photo, format='webp', options={'quality': 40},
                                blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class SaleManager(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    manager = models.ForeignKey(Manager, on_delete=models.PROTECT, blank=True, null=True)


class Block(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=20)
    block_type = models.ForeignKey(BuildingType, on_delete=models.CASCADE, blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    status = models.BooleanField(default=False)
    resident_complex = models.ForeignKey(ResidentComplex, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Entrance(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=20)
    block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='entrances')

    def __str__(self):
        return self.name


class Floor(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=20)
    entrance = models.ForeignKey(Entrance, on_delete=models.PROTECT, related_name='floors')
    floor_type = models.ForeignKey(FloorType, on_delete=models.CASCADE, blank=True, null=True)
    image_1 = ProcessedImageField(upload_to=upload_block_floor, format='webp', options={'quality': 40},
                                  blank=True, null=True)

    def __str__(self):
        return self.name


class Apartment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    floor = models.ForeignKey(Floor, on_delete=models.PROTECT, related_name='apartments')
    decoration = models.ForeignKey(ApartmentDecoration,
                                   on_delete=models.CASCADE, blank=True, null=True, verbose_name='отделка')
    type = models.ForeignKey(ApartmentType, on_delete=models.CASCADE, blank=True, null=True)
    square = models.DecimalField(max_digits=3, decimal_places=1, default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.ForeignKey(ApartmentStatus, on_delete=models.CASCADE, default=1)
    ceiling_height = models.CharField(max_length=3, blank=True)
    image_1 = ProcessedImageField(upload_to=upload_block_apartment, format='webp', options={'quality': 40},
                                  blank=True, null=True)
    image_2 = ProcessedImageField(upload_to=upload_block_apartment, format='webp', options={'quality': 40},
                                  blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, blank=True)
    sure_name = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=14, blank=True)
    info_apartment = models.CharField(max_length=100, blank=True)
    social_media = models.ForeignKey(SocialMedia, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.PROTECT)
    action = models.ForeignKey(SaleManagerAction, on_delete=models.CASCADE)
    sale_manager = models.ForeignKey(SaleManager, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    recall = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)


class ApartmentPrice(models.Model):
    price = models.DecimalField(max_digits=12, decimal_places=2)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    created_at = models.DateField(default=get_cur_date)

    class Meta:
        db_table = "apartment_price"


class ApartmentBuy(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    sale_manager = models.ForeignKey(SaleManager, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "apartment_buy"
