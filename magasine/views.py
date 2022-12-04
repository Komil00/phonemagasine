from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from magasine.models import OrderProduct, UserFavoriteProduct, Product
from .serializers import (
    ProductListSerializers,
    OrderProductListSerializers,
    OrderProductPutSerializers, UserFavoriteProductListSerializers, UserFavoriteProductPostSerializers,
    OrderProductPostSerializers, ProductListDetailSerializers, ChangePriceSerializer
)
from rest_framework.viewsets import ModelViewSet


# Create your views here.

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ['price']
    search_fields = ['modelname', 'brand__name', 'price', 'memory', 'color']
    http_method_names = ['get']
    serializer_class = ProductListSerializers

    def get_serializer_class(self):
        if self.action in ['list']:
            return ProductListSerializers
        return ProductListDetailSerializers


class OrderProductViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = OrderProduct.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ['product__price', 'data_order']
    search_fields = ['product__modelname', 'product__brand__name', 'product__price', 'product__memory', 'product__color']
    authentication_classes = [SessionAuthentication]
    http_allowed_methods = ['get', 'post', 'put', 'delete']

    def create(self, request, *args, **kwargs):
        serializer = OrderProductPostSerializers(data=request.data)
        product = Product.objects.get(id=request.data['product'])
        try:
            orderproduct = int(request.data['quantity'])
            if product.productquantity < orderproduct:
                return Response("buncha mahsulot yo'q", status=status.HTTP_400_BAD_REQUEST)
            serializer.is_valid(raise_exception=True)
            product.productquantity -= orderproduct
            product.save()
            serializer.save(user=self.request.user) # user pole ni zapros berayotgan user bn tuldiradi
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError:
            return Response('Butun son kiriting', status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        serializer = OrderProductPutSerializers(data=request.data)
        serializer.is_valid()
        set_order = set()
        order = get_object_or_404(self.queryset, pk=pk)
        set_order.add(order)
        ord = set_order.pop()
        quantised = serializer.validated_data.get('quantity')
        product = ord.product
        if quantised:
            if quantised >= ord.quantity:
                if product.productquantity < quantised - ord.quantity:
                    return Response("do'konda buncha mahsulot yo'q", status=status.HTTP_400_BAD_REQUEST)
                product.productquantity -= quantised - ord.quantity
            else:
                product.productquantity += ord.quantity - quantised
            product.save()
            ord.quantity = quantised
            ord.save()
            return Response({"success": "mahsulotingiz soni muvafaqiyatli o'zgartirildi"})
        return Response("mahsulot sonini to'gri kiriting", status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return OrderProduct.objects.filter(user=self.request.user)

    #
    def get_serializer_class(self):
        if self.action in ['list']:
            return OrderProductListSerializers
        if self.action in ['create']:
            return OrderProductPostSerializers
        return OrderProductPutSerializers


class UserFavoriteProductViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserFavoriteProduct.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ['product__price']
    search_fields = ['product__modelname', 'product__category__name']
    authentication_classes = [SessionAuthentication]
    http_allowed_methods = ['get', 'post', 'put', 'delete']
    serializer_class = UserFavoriteProductPostSerializers

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['list']:
            return UserFavoriteProductListSerializers
        return UserFavoriteProductPostSerializers

    def create(self, request, *args, **kwargs):
        serializer = UserFavoriteProductPostSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user) # user pole ni zapros berayotgan user bn tuldiradi
        return Response(serializer.data, status=status.HTTP_201_CREATED)
