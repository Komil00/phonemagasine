from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Product, OrderProduct, Brand, UserFavoriteProduct, Images
from customuser.serializers import CustomUserListSerializer


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']


class ImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['image']


class ProductListSerializers(serializers.ModelSerializer):
    brand = BrandSerializer()
    image = ImageSerializers(many=True)

    class Meta:
        model = Product
        fields = ['id', 'brand', 'modelname', 'image', 'memory', 'price', 'color']


class ProductListDetailSerializers(serializers.ModelSerializer):
    brand = BrandSerializer()
    image = ImageSerializers(many=True)

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.productquantity > 0:
            representation['isInStock'] = True
            return representation
        else:
            representation['isInStock'] = False
            return representation


class ChangePriceSerializer(serializers.Serializer):
    price = serializers.FloatField(required=True)


class OrderProductListSerializers(serializers.ModelSerializer):
    user = CustomUserListSerializer(read_only=True)
    product = ProductListSerializers(read_only=True)

    class Meta:
        model = OrderProduct
        fields = ['id', 'user', 'product', 'quantity', 'data_order']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['total_price'] = instance.product.price * instance.quantity
        return representation


class OrderProductPostSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['id', 'user', 'product', 'quantity']

    def validate_quantity(self, value):
        if value < 1:
            raise ValidationError("quantity 0 dan kop bolishi kerak")
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['total_price'] = instance.product.price * instance.quantity
        return representation


class OrderProductPutSerializers(serializers.ModelSerializer):
    user = CustomUserListSerializer(read_only=True)
    product = ProductListSerializers(read_only=True)

    def validate_quantity(self, value):
        if value < 1:
            raise ValidationError("quantity 0 dan kop bolishi kerak")
        return value

    class Meta:
        model = OrderProduct
        fields = '__all__'


class UserFavoriteProductListSerializers(serializers.ModelSerializer):
    user = CustomUserListSerializer(read_only=True)
    product = ProductListSerializers(read_only=True)

    class Meta:
        model = UserFavoriteProduct
        fields = ['id', 'user', 'product']


class UserFavoriteProductPostSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserFavoriteProduct
        fields = ['id', 'user', 'product']
