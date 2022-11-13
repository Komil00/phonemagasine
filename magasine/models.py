import json

from django.contrib.postgres.fields import ArrayField
from django.dispatch import receiver
from django.template.defaultfilters import slugify

from customuser.models import CustomUser
from django.db import models
from django.db.models.signals import pre_save, post_save


class Brand(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.name


COLOR_CHOICES = (
    ("Red", "Red"),
    ("Green", "Green"),
    ("Blue", "Blue"),
    ("Yellow", "Yellow"),
    ("White", "White"),
    ("Black", "Black"),

)


class Images(models.Model):
    image = models.ImageField(upload_to='')


class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    modelname = models.CharField(max_length=50)
    image = models.ManyToManyField(Images)

    memory = models.FloatField()
    ram = models.FloatField()
    price = models.FloatField()
    color = models.CharField(max_length=40, choices=COLOR_CHOICES, default="BLACK")
    productquantity = models.IntegerField()

    display_type = models.CharField(max_length=100)
    display_size = models.FloatField()
    display_resolution = models.CharField(max_length=100)
    main_camera = models.CharField(max_length=150)
    selfie_vamera = models.CharField(max_length=150)
    battery_type = models.CharField(max_length=150)

    objects = models.Manager()

    def __str__(self):
        return self.modelname


# @receiver(post_save, sender=Product)
# def product_post_save(sender, instance, created, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = slugify(instance.modelname)
#         instance.save()


class OrderProduct(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    data_order = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product.modelname


# @receiver(post_save, sender=OrderProduct)
# def create_order(instance, created, *args, **kwargs):
#     if created:
#         product = instance.product
#         product.productquantity -= instance.quantity
#         product.save()


class UserFavoriteProduct(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.last_name
